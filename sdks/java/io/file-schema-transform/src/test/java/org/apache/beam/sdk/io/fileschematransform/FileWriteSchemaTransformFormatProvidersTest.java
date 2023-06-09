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
package org.apache.beam.sdk.io.fileschematransform;

import static org.apache.beam.sdk.io.fileschematransform.FileWriteSchemaTransformFormatProviders.AVRO;
import static org.apache.beam.sdk.io.fileschematransform.FileWriteSchemaTransformFormatProviders.CSV;
import static org.apache.beam.sdk.io.fileschematransform.FileWriteSchemaTransformFormatProviders.JSON;
import static org.apache.beam.sdk.io.fileschematransform.FileWriteSchemaTransformFormatProviders.PARQUET;
import static org.apache.beam.sdk.io.fileschematransform.FileWriteSchemaTransformFormatProviders.XML;
import static org.junit.Assert.assertEquals;

import java.util.Map;
import java.util.Set;
import org.apache.beam.vendor.guava.v26_0_jre.com.google.common.collect.ImmutableSet;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.junit.runners.JUnit4;

/** Tests for {@link FileWriteSchemaTransformFormatProviders}. */
@RunWith(JUnit4.class)
public class FileWriteSchemaTransformFormatProvidersTest {
  @Test
  public void loadProviders() {
    Map<String, FileWriteSchemaTransformFormatProvider> formatProviderMap =
        FileWriteSchemaTransformFormatProviders.loadProviders();
    Set<String> keys = formatProviderMap.keySet();
    assertEquals(ImmutableSet.of(AVRO, CSV, JSON, PARQUET, XML), keys);
  }
}
