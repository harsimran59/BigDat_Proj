#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""Performance tests for file based io connectors."""

import logging
import sys
import uuid
from typing import Tuple

import apache_beam as beam
from apache_beam import typehints
from apache_beam.io.filesystems import FileSystems
from apache_beam.io.iobase import Read
from apache_beam.io.textio import ReadFromText
from apache_beam.io.textio import WriteToText
from apache_beam.testing.load_tests.load_test import LoadTest
from apache_beam.testing.load_tests.load_test import LoadTestOptions
from apache_beam.testing.load_tests.load_test_metrics_utils import CountMessages
from apache_beam.testing.load_tests.load_test_metrics_utils import MeasureTime
from apache_beam.testing.synthetic_pipeline import SyntheticSource
from apache_beam.testing.test_pipeline import TestPipeline
from apache_beam.testing.util import assert_that
from apache_beam.testing.util import equal_to
from apache_beam.transforms.util import Reshuffle

WRITE_NAMESPACE = 'write'
READ_NAMESPACE = 'read'

_LOGGER = logging.getLogger(__name__)


class FileBasedIOTestOptions(LoadTestOptions):
  @classmethod
  def _add_argparse_args(cls, parser):
    parser.add_argument(
        '--test_class', required=True, help='Test class to run.')
    parser.add_argument(
        '--filename_prefix',
        required=True,
        help='Destination prefix for files generated by the test.')
    parser.add_argument(
        '--compression_type',
        default='auto',
        help='File compression type for writing and reading test files.')
    parser.add_argument(
        '--number_of_shards',
        type=int,
        default=0,
        help='Number of files this test will create during the write phase.')
    parser.add_argument(
        '--dataset_size',
        type=int,
        help='Size of data saved on the target filesystem (bytes).')


@typehints.with_output_types(bytes)
@typehints.with_input_types(Tuple[bytes, bytes])
class SyntheticRecordToStrFn(beam.DoFn):
  """
  A DoFn that convert key-value bytes from synthetic source to string record.

  It uses base64 to convert random bytes emitted from the synthetic source.
  Therefore, every 3 bytes give 4 bytes long ascii characters.

  Output length = 4(ceil[len(key)/3] + ceil[len(value)/3]) + 1
  """
  def process(self, element):
    import base64
    yield base64.b64encode(element[0]) + b' ' + base64.b64encode(element[1])


class CreateFolderFn(beam.DoFn):
  """Create folder at pipeline runtime."""
  def __init__(self, folder):
    self.folder = folder

  def process(self, element):
    from apache_beam.io.filesystems import FileSystems  # pylint: disable=reimported
    filesystem = FileSystems.get_filesystem(self.folder)
    if filesystem.has_dirs() and not filesystem.exists(self.folder):
      filesystem.mkdirs(self.folder)


class TextIOPerfTest:
  def run(self):
    write_test = _TextIOWritePerfTest(need_cleanup=False)
    read_test = _TextIOReadPerfTest(input_folder=write_test.output_folder)
    write_test.run()
    read_test.run()


class _TextIOWritePerfTest(LoadTest):
  def __init__(self, need_cleanup=True):
    super().__init__(WRITE_NAMESPACE)
    self.need_cleanup = need_cleanup
    self.test_options = self.pipeline.get_pipeline_options().view_as(
        FileBasedIOTestOptions)
    self.output_folder = FileSystems.join(
        self.test_options.filename_prefix, str(uuid.uuid4()))

  def test(self):
    # first makedir if needed
    _ = (
        self.pipeline
        | beam.Impulse()
        | beam.ParDo(CreateFolderFn(self.output_folder)))

    # write to text
    _ = (
        self.pipeline
        | 'Produce rows' >> Read(
            SyntheticSource(self.parse_synthetic_source_options()))
        | 'Count records' >> beam.ParDo(CountMessages(self.metrics_namespace))
        | 'Format' >> beam.ParDo(SyntheticRecordToStrFn())
        | 'Avoid Fusion' >> Reshuffle()
        | 'Measure time' >> beam.ParDo(MeasureTime(self.metrics_namespace))
        | 'Write Text' >> WriteToText(
            file_path_prefix=FileSystems.join(self.output_folder, 'test'),
            compression_type=self.test_options.compression_type,
            num_shards=self.test_options.number_of_shards))

  def cleanup(self):
    if not self.need_cleanup:
      return
    try:
      FileSystems.delete([self.output_folder])
    except IOError:
      # may not have delete permission, just raise a warning
      _LOGGER.warning(
          'Unable to delete file %s during cleanup.', self.output_folder)


class _TextIOReadPerfTest(LoadTest):
  def __init__(self, input_folder):
    super().__init__(READ_NAMESPACE)
    self.test_options = self.pipeline.get_pipeline_options().view_as(
        FileBasedIOTestOptions)
    self.input_folder = input_folder

  def test(self):
    output = (
        self.pipeline
        | 'Read from text' >>
        ReadFromText(file_pattern=FileSystems.join(self.input_folder, '*'))
        | 'Count records' >> beam.ParDo(CountMessages(self.metrics_namespace))
        | 'Measure time' >> beam.ParDo(MeasureTime(self.metrics_namespace))
        | 'Count' >> beam.combiners.Count.Globally())
    assert_that(output, equal_to([self.input_options['num_records']]))

  def cleanup(self):
    try:
      #FileSystems.delete([self.input_folder])
      pass
    except IOError:
      # may not have delete permission, just raise a warning
      _LOGGER.warning(
          'Unable to delete file %s during cleanup.', self.input_folder)


if __name__ == '__main__':
  logging.basicConfig(level=logging.INFO)

  test_options = TestPipeline().get_pipeline_options().view_as(
      FileBasedIOTestOptions)
  supported_test_classes = list(
      filter(
          lambda s: s.endswith('PerfTest') and not s.startswith('_'),
          dir(sys.modules[__name__])))

  if test_options.test_class not in supported_test_classes:
    raise RuntimeError(
        f'Test {test_options.test_class} not found. '
        'Supported tests are {supported_test_classes}')

  getattr(sys.modules[__name__], test_options.test_class)().run()
