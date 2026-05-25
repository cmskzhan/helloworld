import React from 'react';
import { Composition, Folder } from 'remotion';
import { ArtemisTrajectory } from '../ArtemisTrajectory';
import { ArtemisEducational } from './ArtemisEducational';
import { ArtemisEducationalChinese } from './ArtemisEducationalChinese';
import { COMP_WIDTH, COMP_HEIGHT, FPS, TOTAL_DURATION } from './styles';

import { SurreyExcursion } from './drone-video/Composition';
import { MinimapPreviewComposition } from './drone-video/MinimapPreview';
import {
  WIDTH as DRONE_WIDTH,
  HEIGHT as DRONE_HEIGHT,
  FPS as DRONE_FPS,
  TOTAL_FRAMES as DRONE_TOTAL_FRAMES,
} from './drone-video/telemetry';

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Folder name="Educational">
        <Composition
          id="ArtemisII-Educational"
          component={ArtemisEducational}
          durationInFrames={TOTAL_DURATION}
          fps={FPS}
          width={COMP_WIDTH}
          height={COMP_HEIGHT}
        />
        <Composition
          id="ArtemisII-Educational-CN"
          component={ArtemisEducationalChinese}
          durationInFrames={TOTAL_DURATION}
          fps={FPS}
          width={COMP_WIDTH}
          height={COMP_HEIGHT}
        />
      </Folder>
      <Folder name="Components">
        <Composition
          id="ArtemisII-Trajectory"
          component={ArtemisTrajectory}
          durationInFrames={300}
          fps={30}
          width={1920}
          height={1080}
        />
      </Folder>
      <Folder name="Surrey-Excursion">
        <Composition
          id="MinimapPreview"
          component={MinimapPreviewComposition}
          durationInFrames={DRONE_TOTAL_FRAMES}
          fps={DRONE_FPS}
          width={DRONE_WIDTH}
          height={DRONE_HEIGHT}
        />
        <Composition
          id="SurreyExcursion"
          component={SurreyExcursion}
          durationInFrames={DRONE_TOTAL_FRAMES}
          fps={DRONE_FPS}
          width={DRONE_WIDTH}
          height={DRONE_HEIGHT}
        />
      </Folder>
    </>
  );
};