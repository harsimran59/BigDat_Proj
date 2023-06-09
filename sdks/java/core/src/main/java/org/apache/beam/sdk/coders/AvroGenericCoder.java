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
package org.apache.beam.sdk.coders;

import org.apache.avro.Schema;
import org.apache.avro.generic.GenericRecord;

/**
 * AvroCoder specialisation for GenericRecord.
 *
 * @deprecated Avro related classes are deprecated in module <code>beam-sdks-java-core</code> and
 *     will be eventually removed. Please, migrate to a new module <code>
 *     beam-sdks-java-extensions-avro</code> by importing <code>
 *     org.apache.beam.sdk.extensions.avro.coders.AvroGenericCoder</code> instead of this one.
 */
@Deprecated
public class AvroGenericCoder extends AvroCoder<GenericRecord> {
  AvroGenericCoder(Schema schema) {
    super(GenericRecord.class, schema);
  }

  public static AvroGenericCoder of(Schema schema) {
    return new AvroGenericCoder(schema);
  }
}
