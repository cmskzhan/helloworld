/**
 * Scene 3 – Lemniscate of Bernoulli
 * Progressive drawing of the figure-8 curve with annotated lobes.
 */
import React from 'react';
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
  Easing,
} from 'remotion';
import { Starfield } from '../components/Starfield';
import { COLORS, interFamily, orbitronFamily } from '../styles';

// Generate full lemniscate path for a given number of sample points
const getLemniscatePoints = (
  cx: number,
  cy: number,
  scale: number,
  samples: number,
) => {
  const points: { x: number; y: number }[] = [];
  for (let i = 0; i <= samples; i++) {
    const t = (i / samples) * Math.PI * 2;
    const denom = 1 + Math.pow(Math.sin(t), 2);
    points.push({
      x: (scale * Math.cos(t)) / denom + cx,
      y: (scale * Math.sin(t) * Math.cos(t)) / denom + cy,
    });
  }
  return points;
};

export const LemniscateScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();

  const cx = width / 2;
  const cy = height / 2 + 30; // slightly below center to leave room for heading
  const scale = width * 0.25;

  // ── Heading ──
  const headingSpring = spring({ frame, fps, config: { damping: 200 } });

  // ── Progressive draw of the curve (0 → 1 over 3 seconds) ──
  const drawProgress = interpolate(frame, [15, 3 * fps], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.inOut(Easing.quad),
  });

  const totalSamples = 300;
  const visibleSamples = Math.floor(drawProgress * totalSamples);
  const allPoints = getLemniscatePoints(cx, cy, scale, totalSamples);
  const visiblePoints = allPoints.slice(0, visibleSamples + 1);

  const pathD =
    visiblePoints.length > 1
      ? `M ${visiblePoints.map((p) => `${p.x},${p.y}`).join(' L ')}`
      : '';

  // ── Ghost path (full outline, dim) ──
  const ghostPoints = allPoints;
  const ghostD = `M ${ghostPoints.map((p) => `${p.x},${p.y}`).join(' L ')} Z`;
  const ghostOpacity = interpolate(frame, [10, 40], [0, 0.12], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // ── Lobe labels ──
  const labelDelay = 2.5 * fps;
  const earthLabelSpring = spring({ frame, fps, delay: labelDelay, config: { damping: 200 } });
  const moonLabelSpring = spring({ frame, fps, delay: labelDelay + 15, config: { damping: 200 } });

  // Earth is at the right lobe, Moon at the left
  const earthLabelX = cx + scale + 60;
  const moonLabelX = cx - scale - 60;

  // ── Focus dots ──
  const dotOpacity = interpolate(frame, [30, 60], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill style={{ backgroundColor: COLORS.spaceDark }}>
      <Starfield count={120} />

      {/* Heading */}
      <div
        style={{
          position: 'absolute',
          top: 60,
          left: 0,
          right: 0,
          textAlign: 'center',
          fontFamily: orbitronFamily,
          fontWeight: 700,
          fontSize: 44,
          color: COLORS.cyanGlow,
          opacity: headingSpring,
          transform: `translateY(${interpolate(headingSpring, [0, 1], [-20, 0])}px)`,
        }}
      >
        The Lemniscate of Bernoulli
      </div>

      {/* Subtitle */}
      <div
        style={{
          position: 'absolute',
          top: 130,
          left: 0,
          right: 0,
          textAlign: 'center',
          fontFamily: interFamily,
          fontWeight: 300,
          fontSize: 24,
          color: COLORS.textSecondary,
          opacity: interpolate(headingSpring, [0, 1], [0, 0.8]),
        }}
      >
        A geometric approximation of the Figure-8 free-return orbit
      </div>

      {/* SVG drawing area */}
      <svg
        width={width}
        height={height}
        style={{ position: 'absolute', top: 0, left: 0 }}
      >
        {/* Ghost outline */}
        <path d={ghostD} fill="none" stroke={COLORS.cyanGlow} strokeWidth={1} opacity={ghostOpacity} />

        {/* Progressive drawn path */}
        <path
          d={pathD}
          fill="none"
          stroke={COLORS.cyanGlow}
          strokeWidth={3}
          strokeLinecap="round"
          opacity={0.9}
        />

        {/* Center point */}
        <circle cx={cx} cy={cy} r={4} fill={COLORS.textDim} opacity={dotOpacity} />

        {/* Earth focus dot (right) */}
        <circle
          cx={cx + scale * 0.6}
          cy={cy}
          r={18}
          fill={COLORS.earthBlue}
          opacity={dotOpacity}
          filter="url(#earthGlow)"
        />

        {/* Moon focus dot (left) */}
        <circle
          cx={cx - scale * 0.6}
          cy={cy}
          r={10}
          fill={COLORS.moonGray}
          opacity={dotOpacity}
          filter="url(#moonGlow)"
        />

        {/* Glow filters */}
        <defs>
          <filter id="earthGlow">
            <feGaussianBlur stdDeviation="6" result="blur" />
            <feMerge>
              <feMergeNode in="blur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
          <filter id="moonGlow">
            <feGaussianBlur stdDeviation="4" result="blur" />
            <feMerge>
              <feMergeNode in="blur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
        </defs>
      </svg>

      {/* Earth label */}
      <div
        style={{
          position: 'absolute',
          left: earthLabelX,
          top: cy - 50,
          opacity: earthLabelSpring,
          transform: `translateX(${interpolate(earthLabelSpring, [0, 1], [20, 0])}px)`,
        }}
      >
        <div
          style={{
            fontFamily: orbitronFamily,
            fontWeight: 700,
            fontSize: 22,
            color: COLORS.earthBlue,
          }}
        >
          Earth Lobe
        </div>
        <div
          style={{
            fontFamily: interFamily,
            fontSize: 16,
            color: COLORS.textSecondary,
            maxWidth: 200,
            marginTop: 6,
          }}
        >
          Departure &amp; arrival
        </div>
      </div>

      {/* Moon label */}
      <div
        style={{
          position: 'absolute',
          right: width - moonLabelX + 60,
          top: cy - 50,
          textAlign: 'right',
          opacity: moonLabelSpring,
          transform: `translateX(${interpolate(moonLabelSpring, [0, 1], [-20, 0])}px)`,
        }}
      >
        <div
          style={{
            fontFamily: orbitronFamily,
            fontWeight: 700,
            fontSize: 22,
            color: COLORS.moonGray,
          }}
        >
          Moon Lobe
        </div>
        <div
          style={{
            fontFamily: interFamily,
            fontSize: 16,
            color: COLORS.textSecondary,
            maxWidth: 200,
            marginTop: 6,
          }}
        >
          Gravity-assist swing-by
        </div>
      </div>
    </AbsoluteFill>
  );
};
