/**
 * Scene 6 – Full Trajectory Animation
 * Enhanced version of ArtemisTrajectory with labels, HUD, and star background.
 */
import React from 'react';
import {
  AbsoluteFill,
  interpolate,
  useCurrentFrame,
  useVideoConfig,
  Easing,
  spring,
} from 'remotion';
import { Starfield } from '../components/Starfield';
import { COLORS, interFamily, orbitronFamily, monoFamily } from '../styles';

// Lemniscate of Bernoulli
const getOrbitalPosition = (progress: number, cx: number, cy: number, scale: number) => {
  const t = progress * Math.PI * 2;
  const denom = 1 + Math.pow(Math.sin(t), 2);
  const x = (scale * Math.cos(t)) / denom + cx;
  const y = (scale * Math.sin(t) * Math.cos(t)) / denom + cy;
  return { x, y };
};

export const TrajectoryScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames, width, height } = useVideoConfig();

  const cx = width / 2;
  const cy = height / 2;
  const scale = width * 0.3;

  // ── HUD entrance ──
  const hudSpring = spring({ frame, fps, config: { damping: 200 } });

  // ── Mission progress (eased) ──
  const progress = interpolate(frame, [0, durationInFrames], [0, 1], {
    extrapolateRight: 'clamp',
    easing: Easing.inOut(Easing.sin),
  });

  const orionPos = getOrbitalPosition(progress, cx, cy, scale);

  // ── Trail ──
  const trailPoints = Array.from({ length: Math.floor(frame) + 1 }).map((_, i) => {
    const hp = interpolate(i, [0, durationInFrames], [0, 1], {
      easing: Easing.inOut(Easing.sin),
    });
    const pos = getOrbitalPosition(hp, cx, cy, scale);
    return `${pos.x},${pos.y}`;
  });
  const trailD = trailPoints.length > 1 ? `M ${trailPoints.join(' L ')}` : '';

  // ── Full ghost orbit ──
  const ghostSamples = 200;
  const ghostPoints = Array.from({ length: ghostSamples + 1 }).map((_, i) => {
    const p = i / ghostSamples;
    const pos = getOrbitalPosition(p, cx, cy, scale);
    return `${pos.x},${pos.y}`;
  });
  const ghostD = `M ${ghostPoints.join(' L ')} Z`;

  // Celestial body positions
  const earthX = cx + scale * 0.6;
  const moonX = cx - scale * 0.6;

  // Mission percentage
  const missionPct = Math.round(progress * 100);
  const missionPhase =
    progress < 0.15
      ? 'LAUNCH'
      : progress < 0.4
        ? 'TRANS-LUNAR COAST'
        : progress < 0.6
          ? 'LUNAR FLYBY'
          : progress < 0.85
            ? 'TRANS-EARTH COAST'
            : 'RE-ENTRY';

  return (
    <AbsoluteFill style={{ backgroundColor: COLORS.spaceDark }}>
      <Starfield count={250} />

      {/* SVG layer */}
      <svg width={width} height={height} style={{ position: 'absolute' }}>
        {/* Glow filters */}
        <defs>
          <filter id="trailGlow">
            <feGaussianBlur stdDeviation="3" result="blur" />
            <feMerge>
              <feMergeNode in="blur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
          <filter id="bodyGlow">
            <feGaussianBlur stdDeviation="8" result="blur" />
            <feMerge>
              <feMergeNode in="blur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
          <radialGradient id="earthGrad">
            <stop offset="0%" stopColor="#6BC5E8" />
            <stop offset="60%" stopColor={COLORS.earthBlue} />
            <stop offset="100%" stopColor="#2A6DA8" />
          </radialGradient>
          <radialGradient id="moonGrad">
            <stop offset="0%" stopColor="#F5F5F5" />
            <stop offset="70%" stopColor={COLORS.moonGray} />
            <stop offset="100%" stopColor="#A0A0A0" />
          </radialGradient>
        </defs>

        {/* Ghost orbit outline */}
        <path d={ghostD} fill="none" stroke={COLORS.cyanGlow} strokeWidth={1} opacity={0.1} />

        {/* Trail */}
        <path
          d={trailD}
          fill="none"
          stroke={COLORS.cyanGlow}
          strokeWidth={3}
          opacity={0.7}
          filter="url(#trailGlow)"
        />

        {/* Earth */}
        <circle cx={earthX} cy={cy} r={36} fill="url(#earthGrad)" filter="url(#bodyGlow)" />

        {/* Moon */}
        <circle cx={moonX} cy={cy} r={16} fill="url(#moonGrad)" filter="url(#bodyGlow)" />

        {/* Orion spacecraft */}
        <circle cx={orionPos.x} cy={orionPos.y} r={7} fill={COLORS.magenta} />
        <circle cx={orionPos.x} cy={orionPos.y} r={14} fill={COLORS.magenta} opacity={0.25} />
        <circle cx={orionPos.x} cy={orionPos.y} r={22} fill={COLORS.magenta} opacity={0.08} />
      </svg>

      {/* Earth label */}
      <div
        style={{
          position: 'absolute',
          left: earthX - 30,
          top: cy + 50,
          fontFamily: orbitronFamily,
          fontWeight: 700,
          fontSize: 16,
          color: COLORS.earthBlue,
          textAlign: 'center',
          opacity: hudSpring,
        }}
      >
        EARTH
      </div>

      {/* Moon label */}
      <div
        style={{
          position: 'absolute',
          left: moonX - 22,
          top: cy + 30,
          fontFamily: orbitronFamily,
          fontWeight: 700,
          fontSize: 14,
          color: COLORS.moonGray,
          textAlign: 'center',
          opacity: hudSpring,
        }}
      >
        MOON
      </div>

      {/* Orion label (follows spacecraft) */}
      <div
        style={{
          position: 'absolute',
          left: orionPos.x + 18,
          top: orionPos.y - 10,
          fontFamily: orbitronFamily,
          fontWeight: 400,
          fontSize: 13,
          color: COLORS.magenta,
          whiteSpace: 'nowrap',
        }}
      >
        ORION
      </div>

      {/* ── HUD: Top-left title ── */}
      <div
        style={{
          position: 'absolute',
          top: 40,
          left: 60,
          opacity: hudSpring,
        }}
      >
        <div
          style={{
            fontFamily: orbitronFamily,
            fontWeight: 700,
            fontSize: 28,
            color: COLORS.textPrimary,
            letterSpacing: 4,
          }}
        >
          ARTEMIS II
        </div>
        <div
          style={{
            fontFamily: interFamily,
            fontSize: 16,
            color: COLORS.cyanGlow,
            marginTop: 4,
          }}
        >
          Free-Return Trajectory Simulation
        </div>
      </div>

      {/* ── HUD: Bottom-left telemetry ── */}
      <div
        style={{
          position: 'absolute',
          bottom: 50,
          left: 60,
          opacity: hudSpring,
          display: 'flex',
          gap: 40,
        }}
      >
        {/* Mission Progress */}
        <div>
          <div
            style={{
              fontFamily: interFamily,
              fontSize: 12,
              color: COLORS.textDim,
              textTransform: 'uppercase',
              letterSpacing: 2,
            }}
          >
            Mission Progress
          </div>
          <div
            style={{
              fontFamily: monoFamily,
              fontSize: 36,
              color: COLORS.cyanGlow,
              marginTop: 4,
            }}
          >
            {missionPct}%
          </div>
        </div>

        {/* Phase */}
        <div>
          <div
            style={{
              fontFamily: interFamily,
              fontSize: 12,
              color: COLORS.textDim,
              textTransform: 'uppercase',
              letterSpacing: 2,
            }}
          >
            Phase
          </div>
          <div
            style={{
              fontFamily: orbitronFamily,
              fontSize: 22,
              color: COLORS.gold,
              marginTop: 8,
            }}
          >
            {missionPhase}
          </div>
        </div>
      </div>

      {/* ── HUD: Bottom-right coordinates ── */}
      <div
        style={{
          position: 'absolute',
          bottom: 50,
          right: 60,
          textAlign: 'right',
          opacity: hudSpring,
        }}
      >
        <div
          style={{
            fontFamily: interFamily,
            fontSize: 12,
            color: COLORS.textDim,
            textTransform: 'uppercase',
            letterSpacing: 2,
          }}
        >
          Orion Coordinates
        </div>
        <div
          style={{
            fontFamily: monoFamily,
            fontSize: 18,
            color: COLORS.textSecondary,
            marginTop: 6,
          }}
        >
          x: {Math.round(orionPos.x)} &nbsp; y: {Math.round(orionPos.y)}
        </div>
      </div>

      {/* ── HUD: Progress bar ── */}
      <div
        style={{
          position: 'absolute',
          bottom: 20,
          left: 60,
          right: 60,
          height: 3,
          backgroundColor: COLORS.textDim,
          borderRadius: 2,
          opacity: hudSpring * 0.5,
        }}
      >
        <div
          style={{
            width: `${missionPct}%`,
            height: '100%',
            backgroundColor: COLORS.cyanGlow,
            borderRadius: 2,
          }}
        />
      </div>
    </AbsoluteFill>
  );
};
