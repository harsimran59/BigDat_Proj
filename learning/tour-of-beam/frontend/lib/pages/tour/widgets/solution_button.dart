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

import 'package:easy_localization/easy_localization.dart';
import 'package:flutter/material.dart';
import 'package:flutter_svg/svg.dart';

import '../../../assets/assets.gen.dart';
import '../state.dart';

class SolutionButton extends StatelessWidget {
  final TourNotifier tourNotifier;

  const SolutionButton({
    required this.tourNotifier,
  });

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: tourNotifier,
      builder: (context, child) => TextButton.icon(
        style: ButtonStyle(
          backgroundColor: MaterialStateProperty.all(
            tourNotifier.isShowingSolution
                ? Theme.of(context).splashColor
                : null,
          ),
        ),
        onPressed: tourNotifier.toggleShowingSolution,
        icon: SvgPicture.asset(Assets.svg.solution),
        label: const Text('ui.solution').tr(),
      ),
    );
  }
}
