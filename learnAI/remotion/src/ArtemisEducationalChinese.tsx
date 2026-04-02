/**
 * ArtemisEducationalChinese – Main composition for the Chinese version.
 * Uses TransitionSeries to stitch scenes with fade transitions.
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

// Chinese Translations
const CHINESE_PROPS = {
  title: {
    title: "阿耳忒弥斯 2 号",
    subtitle: "自由返回轨道",
    tagline: "自阿波罗计划后首次载人绕月任务"
  },
  overview: {
    heading: "什么是自由返回轨道？",
    paragraphs: [
      "阿耳忒弥斯 2 号将载 4 名宇航员绕月飞行，这是自阿波罗计划以来首次载人绕月。",
      "轨道利用月球引力实现自动返回，无需消耗大量燃料即可安全飞回地球。",
      "这一路径在太空中划出一个独特的“数字 8”形状。"
    ]
  },
  lemniscate: {
    heading: "伯努利双纽线",
    subtitle: "自由返回轨道在几何学上的完美近似",
    earthLobe: "地球叶 (离去与返回)",
    moonLobe: "月球叶 (引力弹弓)"
  },
  equations: {
    heading: "参数方程",
    variableTitle: "变量定义",
    variables: [
      { symbol: 'a', description: '焦距 — 屏幕宽度的 35-40%' },
      { symbol: 't', description: '任务进度 — 从 0 (发射) 到 2π (落海)' },
      { symbol: 'sin²(t)', description: '形成“数字 8”中心的交叉点' }
    ]
  },
  easing: {
    heading: "轨道速度与引力加速",
    bullets: [
      { label: '近地点 (地球)', desc: '速度最快 — 受地心引力加速' },
      { label: '远地点 (月球)', desc: '速度最慢 — 在月球引力弹射前产生“悬停”感' },
      { label: '缓动函数', desc: 'Sinusoidal Easing 模拟了真实的重力加速度动态' }
    ]
  },
  trajectory: {
    title: "阿耳忒弥斯 2 号",
    subtitle: "自由返回轨道实时模拟",
    earth: "地球",
    moon: "月球",
    orion: "猎户座飞船",
    telemetry: "任务遥测",
    progress: "任务进度",
    phase: "当前阶段",
    phases: {
      launch: "发射 (Launch)",
      transLunar: "地月转移 (Trans-Lunar)",
      flyby: "月球飞越 (Lunar Flyby)",
      transEarth: "月地转移 (Trans-Earth)",
      reentry: "重返大气层 (Re-Entry)"
    }
  },
  outro: {
    note: "本可视化是基于伯努利双纽线的几何表示。在真实任务中，由于地球引力井大得多，地球侧的轨道环会比月球侧显著增大。"
  }
};

// Note: To properly support localized scenes, we'd ideally pass these as props.
// For now, I will modify the scenes themselves to accept these props or create a localized wrapper.
// Given the current structure, adding the Chinese version as a separate root composition.

export const ArtemisEducationalChinese: React.FC = () => {
  return (
    <AbsoluteFill className="font-sans">
      <Watermark />
      <TransitionSeries>
        <TransitionSeries.Sequence durationInFrames={SCENE_DURATIONS.title}>
          <TitleScene {...CHINESE_PROPS.title} />
        </TransitionSeries.Sequence>
        
        <TransitionSeries.Transition presentation={fade()} timing={FADE_TIMING} />
        
        <TransitionSeries.Sequence durationInFrames={SCENE_DURATIONS.overview}>
          <OverviewScene {...CHINESE_PROPS.overview} />
        </TransitionSeries.Sequence>

        <TransitionSeries.Transition presentation={fade()} timing={FADE_TIMING} />

        <TransitionSeries.Sequence durationInFrames={SCENE_DURATIONS.lemniscate}>
          <LemniscateScene {...CHINESE_PROPS.lemniscate} />
        </TransitionSeries.Sequence>

        <TransitionSeries.Transition presentation={fade()} timing={FADE_TIMING} />

        <TransitionSeries.Sequence durationInFrames={SCENE_DURATIONS.equations}>
          <EquationsScene {...CHINESE_PROPS.equations} />
        </TransitionSeries.Sequence>

        <TransitionSeries.Transition presentation={fade()} timing={FADE_TIMING} />

        <TransitionSeries.Sequence durationInFrames={SCENE_DURATIONS.easing}>
          <EasingScene {...CHINESE_PROPS.easing} />
        </TransitionSeries.Sequence>

        <TransitionSeries.Transition presentation={fade()} timing={FADE_TIMING} />

        <TransitionSeries.Sequence durationInFrames={SCENE_DURATIONS.trajectory}>
          <TrajectoryScene {...CHINESE_PROPS.trajectory} />
        </TransitionSeries.Sequence>

        <TransitionSeries.Transition presentation={fade()} timing={FADE_TIMING} />

        <TransitionSeries.Sequence durationInFrames={SCENE_DURATIONS.outro}>
          <OutroScene {...CHINESE_PROPS.outro} />
        </TransitionSeries.Sequence>
      </TransitionSeries>
    </AbsoluteFill>
  );
};
