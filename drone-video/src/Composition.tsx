import React from "react";
import {
  AbsoluteFill,
  Audio,
  Sequence,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  Easing,
} from "remotion";
import { Video } from "@remotion/media";
import {
  TransitionSeries,
  linearTiming,
  springTiming,
} from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";
import { wipe } from "@remotion/transitions/wipe";
import { whoosh } from "@remotion/sfx";

import { SCENES, TOTAL_FRAMES, SceneData } from "./telemetry";
import { Letterbox, TitleCard, TelemetryHUD, OpeningQuote, OutroFade } from "./components/HUD";
import { Minimap } from "./components/Minimap";

// ── Individual scene clip ─────────────────────────────────────────────────────
const ClipScene: React.FC<{ scene: SceneData; showTitle?: boolean }> = ({
  scene,
  showTitle = true,
}) => {
  const { fps } = useVideoConfig();

  return (
    <AbsoluteFill style={{ background: "#000" }}>
      <Video
        src={staticFile(`videos/${scene.file}`)}
        style={{ width: "100%", height: "100%" }}
        objectFit="cover"
        muted
        trimBefore={scene.trimBeforeS * fps}
        trimAfter={(scene.trimBeforeS + scene.durationS) * fps}
        playbackRate={scene.playbackRate}
        premountFor={fps * 2}
      />
      {showTitle && <TitleCard sceneIdx={SCENES.indexOf(scene)} />}
    </AbsoluteFill>
  );
};

// ── Speed-ramp scene (clip 0006): scale brightness + blur at speed peak) ──────
const SpeedRampScene: React.FC<{ scene: SceneData }> = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const totalF = scene.durationS * fps; // 60 frames for 1s at 60fps

  // Brightness flare in the middle of the speed ramp
  const brightness = interpolate(
    frame,
    [0, totalF * 0.4, totalF * 0.6, totalF],
    [1, 1.4, 1.4, 1],
    { extrapolateRight: "clamp", easing: Easing.inOut(Easing.quad) }
  );

  return (
    <AbsoluteFill
      style={{
        background: "#000",
        filter: `brightness(${brightness})`,
      }}
    >
      <Video
        src={staticFile(`videos/${scene.file}`)}
        style={{ width: "100%", height: "100%" }}
        objectFit="cover"
        muted
        trimBefore={scene.trimBeforeS * fps}
        trimAfter={(scene.trimBeforeS + scene.durationS) * fps}
        playbackRate={scene.playbackRate}
      />
    </AbsoluteFill>
  );
};

// ── Hook Heath scene: speed-ramp mid-flight ────────────────────────────────────
const HookHeathScene: React.FC<{ scene: SceneData }> = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Speed ramp: normal (1x) → fast (3x) at midpoint → slow (0.5x) at 70% → normal
  const playbackRate = interpolate(
    frame,
    [0, fps * 5, fps * 8, fps * 12, fps * 17],
    [1, 1, 3, 0.6, 0.6],
    { extrapolateRight: "clamp", easing: Easing.inOut(Easing.sin) }
  );

  return (
    <AbsoluteFill style={{ background: "#000" }}>
      <Video
        src={staticFile(`videos/${scene.file}`)}
        style={{ width: "100%", height: "100%" }}
        objectFit="cover"
        muted
        trimBefore={scene.trimBeforeS * fps}
        trimAfter={(scene.trimBeforeS + scene.durationS) * fps}
        playbackRate={playbackRate}
      />
      <TitleCard sceneIdx={SCENES.indexOf(scene)} />
    </AbsoluteFill>
  );
};

// ── Main composition ──────────────────────────────────────────────────────────
export const SurreyExcursion: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Scene durations in frames at 60fps
  const S = [480, 600, 60, 600, 540, 1020, 300];
  const T = 30; // transition frames

  // Whoosh SFX fired at each transition midpoint
  // S0→S1 midpoint: 480-T/2 = 465
  // S1→S2 midpoint: (450+600)-T/2 = 1035
  // S3→S4 midpoint: (1080+600)-T/2 = 1665
  // S4→S5 midpoint: (1650+540)-T/2 = 2175
  // S5→S6 midpoint: (2160+1020)-T/2 = 3165
  const whooshFrames = [465, 1035, 1665, 2175, 3165];

  return (
    <AbsoluteFill style={{ background: "#000" }}>

      {/* ── VIDEO LAYER ─────────────────────────────────────────────────── */}
      <TransitionSeries>

        {/* Scene 0: Horsell Common morning – the intro reveal */}
        <TransitionSeries.Sequence durationInFrames={S[0]} premountFor={fps}>
          <ClipScene scene={SCENES[0]} />
        </TransitionSeries.Sequence>

        <TransitionSeries.Transition
          presentation={fade()}
          timing={linearTiming({ durationInFrames: T })}
        />

        {/* Scene 1: Pine Woodlands drift */}
        <TransitionSeries.Sequence durationInFrames={S[1]} premountFor={fps}>
          <ClipScene scene={SCENES[1]} />
        </TransitionSeries.Sequence>

        <TransitionSeries.Transition
          presentation={wipe({ direction: "from-left" })}
          timing={springTiming({ config: { damping: 200 }, durationInFrames: T })}
        />

        {/* Scene 2: 0006 speed-ramp glitch cut */}
        <TransitionSeries.Sequence durationInFrames={S[2]} premountFor={fps}>
          <SpeedRampScene scene={SCENES[2]} />
        </TransitionSeries.Sequence>

        {/* Direct cut into Horsell Birch */}
        <TransitionSeries.Sequence durationInFrames={S[3]} premountFor={fps}>
          <ClipScene scene={SCENES[3]} />
        </TransitionSeries.Sequence>

        <TransitionSeries.Transition
          presentation={fade()}
          timing={linearTiming({ durationInFrames: T })}
        />

        {/* Scene 4: Birch Woods Pond reflection */}
        <TransitionSeries.Sequence durationInFrames={S[4]} premountFor={fps}>
          <ClipScene scene={SCENES[4]} />
        </TransitionSeries.Sequence>

        <TransitionSeries.Transition
          presentation={fade()}
          timing={linearTiming({ durationInFrames: T })}
        />

        {/* Scene 5: Hook Heath – climax with speed ramp */}
        <TransitionSeries.Sequence durationInFrames={S[5]} premountFor={fps}>
          <HookHeathScene scene={SCENES[5]} />
        </TransitionSeries.Sequence>

        <TransitionSeries.Transition
          presentation={fade()}
          timing={linearTiming({ durationInFrames: T })}
        />

        {/* Scene 6: Horsell Common outro – slow fade to canopy */}
        <TransitionSeries.Sequence durationInFrames={S[6]} premountFor={fps}>
          <ClipScene scene={SCENES[6]} showTitle={false} />
        </TransitionSeries.Sequence>

      </TransitionSeries>

      {/* ── HUD OVERLAYS ─────────────────────────────────────────────────── */}
      <Letterbox />
      <TelemetryHUD />
      <Minimap />

      {/* Opening H.G. Wells quote on first scene */}
      <Sequence from={0} durationInFrames={300} premountFor={0}>
        <OpeningQuote />
      </Sequence>

      {/* Final fade to black */}
      <OutroFade totalFrames={TOTAL_FRAMES} />

      {/* ── AUDIO LAYER ──────────────────────────────────────────────────── */}

      {/* Background ambient wind (loops throughout) */}
      <Audio
        src={staticFile("wind.ogg")}
        volume={0.28}
        loop
      />

      {/* Forest birdsong fades in at scene 2 and runs through scene 5 */}
      <Sequence from={450} durationInFrames={2700} premountFor={fps}>
        <Audio
          src={staticFile("birds.ogg")}
          volume={(f) =>
            interpolate(f, [0, fps * 2], [0, 0.15], {
              extrapolateRight: "clamp",
            })
          }
          loop
        />
      </Sequence>

      {/* Background music — user can replace public/music.mp3 with their track */}
      <Audio
        src={staticFile("music.mp3")}
        volume={(f) => {
          // Fade in over 2s, fade out over 2s at the end
          const fadeIn  = interpolate(f, [0, fps * 2], [0, 0.65], { extrapolateRight: "clamp" });
          const fadeOut = interpolate(f, [TOTAL_FRAMES - fps * 2, TOTAL_FRAMES], [0.65, 0], { extrapolateLeft: "clamp" });
          return Math.min(fadeIn, fadeOut);
        }}
        loop
      />

      {/* Transition whoosh SFX — timed to each scene cut */}
      {whooshFrames.map((startFrame) => (
        <Sequence key={startFrame} from={startFrame - 8} durationInFrames={48} premountFor={0}>
          <Audio src={whoosh} volume={0.45} />
        </Sequence>
      ))}

    </AbsoluteFill>
  );
};
