import React from 'react';
import { Composition, Folder } from 'remotion';
import { ArtemisTrajectory } from '../ArtemisTrajectory';
import { ArtemisEducational } from './ArtemisEducational';
import { COMP_WIDTH, COMP_HEIGHT, FPS, TOTAL_DURATION } from './styles';

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
    </>
  );
};