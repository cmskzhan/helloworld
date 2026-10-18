/**
 * ArtemisEducational – Main composition.
 * Uses TransitionSeries to stitch 7 scenes with fade transitions.
 */
import React from 'react';
import { AbsoluteFill } from 'remotion';
import { TransitionSeries, linearTiming } from '@remotion/transitions';
import { fade } from '@remotion/transitions/fade';

import { TitleScene } from './scenes/TitleScene';
import { OverviewScene } from './scenes/OverviewScene';
import { LemniscateScene } from './scenes/LemniscateScene';
import { EquationsScene } from './scenes/EquationsScene';
import { EasingScene } from './scenes/EasingScene';
import { TrajectoryScene } from './scenes/TrajectoryScene';
import { OutroScene } from './scenes/OutroScene';
import { SCENE_DURATIONS, TRANSITION_DURATION } from './styles';
import { Watermark } from './components/Watermark';

const FADE_TIMING = linearTiming({ durationInFrames: TRANSITION_DURATION });

export const ArtemisEducational: React.FC = () => {
  return (
    <AbsoluteFill>
      <Watermark />
      <TransitionSeries>
        {/* Scene 1 – Title Card */}
        <TransitionSeries.Sequence durationInFrames={SCENE_DURATIONS.title} premountFor={30}>
          <TitleScene />
        </TransitionSeries.Sequence>

        <TransitionSeries.Transition
          presentation={fade()}
          timing={FADE_TIMING}
        />

        {/* Scene 2 – Overview */}
        <TransitionSeries.Sequence durationInFrames={SCENE_DURATIONS.overview} premountFor={30}>
          <OverviewScene />
        </TransitionSeries.Sequence>

        <TransitionSeries.Transition
          presentation={fade()}
          timing={FADE_TIMING}
        />

        {/* Scene 3 – Lemniscate of Bernoulli */}
        <TransitionSeries.Sequence durationInFrames={SCENE_DURATIONS.lemniscate} premountFor={30}>
          <LemniscateScene />
        </TransitionSeries.Sequence>

        <TransitionSeries.Transition
          presentation={fade()}
          timing={FADE_TIMING}
        />

        {/* Scene 4 – Parametric Equations */}
        <TransitionSeries.Sequence durationInFrames={SCENE_DURATIONS.equations} premountFor={30}>
          <EquationsScene />
        </TransitionSeries.Sequence>

        <TransitionSeries.Transition
          presentation={fade()}
          timing={FADE_TIMING}
        />

        {/* Scene 5 – Orbital Velocity & Easing */}
        <TransitionSeries.Sequence durationInFrames={SCENE_DURATIONS.easing} premountFor={30}>
          <EasingScene />
        </TransitionSeries.Sequence>

        <TransitionSeries.Transition
          presentation={fade()}
          timing={FADE_TIMING}
        />

        {/* Scene 6 – Full Trajectory Animation */}
        <TransitionSeries.Sequence durationInFrames={SCENE_DURATIONS.trajectory} premountFor={30}>
          <TrajectoryScene />
        </TransitionSeries.Sequence>

        <TransitionSeries.Transition
          presentation={fade()}
          timing={FADE_TIMING}
        />

        {/* Scene 7 – Outro */}
        <TransitionSeries.Sequence durationInFrames={SCENE_DURATIONS.outro} premountFor={30}>
          <OutroScene />
        </TransitionSeries.Sequence>
      </TransitionSeries>
    </AbsoluteFill>
  );
};
