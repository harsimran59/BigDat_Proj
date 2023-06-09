/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import CommonJobProperties as commonJobProperties
import PostcommitJobBuilder

import static PythonTestProperties.VALIDATES_CONTAINER_DATAFLOW_PYTHON_VERSIONS

// This job runs the suite of Python ValidatesContainer tests against the
// Dataflow runner.
PostcommitJobBuilder.postCommitJob('beam_PostCommit_Py_ValCont',
    'Run Python Dataflow ValidatesContainer', 'Google Cloud Dataflow Runner Python ValidatesContainer Tests', this) {
      description('Runs Python ValidatesContainer suite on the Dataflow runner.')

      // Set common parameters.
      commonJobProperties.setTopLevelMainJobProperties(delegate)

      publishers {
        archiveJunit('**/pytest*.xml')
      }

      // Execute shell command to test Python SDK.
      steps {
        gradle {
          rootBuildScriptDir(commonJobProperties.checkoutDir)
          tasks(':sdks:python:test-suites:dataflow:validatesContainerTests')
          commonJobProperties.setGradleSwitches(delegate)
        }
      }
    }

PostcommitJobBuilder.postCommitJob('beam_PostCommit_Py_ValCont_with_RC',
    'Run Python RC Dataflow ValidatesContainer', 'Google Cloud Dataflow Runner Python ValidatesContainer Tests with RC Dependencies', this) {
      description('Runs Python ValidatesContainer suite on the Dataflow runner by installing Release Candidates.')

      // Set common parameters.
      commonJobProperties.setTopLevelMainJobProperties(delegate)

      publishers {
        archiveJunit('**/pytest*.xml')
      }

      // Execute shell command to test Python SDK.
      steps {
        gradle {
          rootBuildScriptDir(commonJobProperties.checkoutDir)
          tasks(':sdks:python:test-suites:dataflow:validatesContainerTests')
          switches('-PtestRCDependencies=true')
          commonJobProperties.setGradleSwitches(delegate)
        }
      }
    }
