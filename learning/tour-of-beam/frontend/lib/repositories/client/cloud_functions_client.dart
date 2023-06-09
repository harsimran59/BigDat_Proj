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

import 'dart:convert';
import 'dart:io';

import 'package:get_it/get_it.dart';
import 'package:http/http.dart' as http;

import '../../auth/notifier.dart';
import '../../config.dart';
import '../../models/content_tree.dart';
import '../../models/unit_content.dart';
import '../models/get_content_tree_response.dart';
import '../models/get_sdks_response.dart';
import '../models/get_user_progress_response.dart';
import 'client.dart';

// TODO(nausharipov): add repository and handle exceptions
class CloudFunctionsTobClient extends TobClient {
  @override
  Future<GetSdksResponse> getSdks() async {
    final json = await http.get(
      Uri.parse(
        '$cloudFunctionsBaseUrl/getSdkList',
      ),
    );

    final map = jsonDecode(utf8.decode(json.bodyBytes)) as Map<String, dynamic>;
    return GetSdksResponse.fromJson(map);
  }

  @override
  Future<ContentTreeModel> getContentTree(String sdkId) async {
    final json = await http.get(
      Uri.parse(
        '$cloudFunctionsBaseUrl/getContentTree?sdk=$sdkId',
      ),
    );

    final map = jsonDecode(utf8.decode(json.bodyBytes)) as Map<String, dynamic>;
    final response = GetContentTreeResponse.fromJson(map);
    return ContentTreeModel.fromResponse(response);
  }

  @override
  Future<UnitContentModel> getUnitContent(String sdkId, String unitId) async {
    final json = await http.get(
      Uri.parse(
        '$cloudFunctionsBaseUrl/getUnitContent?sdk=$sdkId&id=$unitId',
      ),
    );

    final map = jsonDecode(utf8.decode(json.bodyBytes)) as Map<String, dynamic>;
    return UnitContentModel.fromJson(map);
  }

  @override
  Future<GetUserProgressResponse?> getUserProgress(String sdkId) async {
    final token = await GetIt.instance.get<AuthNotifier>().getToken();
    if (token == null) {
      return null;
    }
    final json = await http.get(
      Uri.parse(
        '$cloudFunctionsBaseUrl/getUserProgress?sdk=$sdkId',
      ),
      headers: {
        HttpHeaders.authorizationHeader: 'Bearer $token',
      },
    );
    final map = jsonDecode(utf8.decode(json.bodyBytes)) as Map<String, dynamic>;
    final response = GetUserProgressResponse.fromJson(map);
    return response;
  }

  @override
  Future<void> postUnitComplete(String sdkId, String id) async {
    final token = await GetIt.instance.get<AuthNotifier>().getToken();
    await http.post(
      Uri.parse(
        '$cloudFunctionsBaseUrl/postUnitComplete?sdk=$sdkId&id=$id',
      ),
      headers: {
        HttpHeaders.authorizationHeader: 'Bearer $token',
      },
    );
  }
}
