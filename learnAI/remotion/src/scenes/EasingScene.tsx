/**
 * Scene 5 – Easing & Orbital Velocity
 * Shows how sinusoidal easing simulates variable orbital speed.
 * Two-column layout: explanation left, easing curve visualization right.
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
import { COLORS, interFamily, orbitronFamily, monoFamily } from '../styles';

const BULLET_POINTS = [
  { label: 'Perigee (Earth)', desc: 'Highest velocity — spacecraft accelerates under Earth\'s gravity', color: COLORS.earthBlue },
  { label: 'Apogee (Moon)', desc: 'Lowest velocity — spacecraft "hangs" before lunar gravity slingshot', color: COLORS.moonGray },
  { label: 'Easing Function', desc: 'Easing.inOut(Easing.sin) mimics gravity-driven acceleration', color: COLORS.cyanGlow },
];

export const EasingScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();

  const headingSpring = spring({ frame, fps, config: { damping: 200 } });

  // ── Easing curve visualization ──
  const curveWidth = 400;
  const curveHeight = 300;
  const curveX = width - 300 - curveWidth / 2;
  const curveY = height / 2;

  // Progress dot on curve
  const animProgress = interpolate(frame, [30, 4 * fps], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // Generate easing curve points
  const curveSamples = 100;
  const curvePoints = Array.from({ length: curveSamples + 1 }).map((_, i) => {
    const t = i / curveSamples;
    const easedT = Easing.inOut(Easing.sin)(t);
    const px = curveX - curveWidth / 2 + t * curveWidth;
    const py = curveY + curveHeight / 2 - easedT * curveHeight;
    return { x: px, y: py };
  });
  const curvePath = `M ${curvePoints.map((p) => `${p.x},${p.y}`).join(' L ')}`;

  // Draw progress along the curve
  const drawnSamples = Math.floor(animProgress * curveSamples);
  const drawnPoints = curvePoints.slice(0, drawnSamples + 1);
  const drawnPath =
    drawnPoints.length > 1
      ? `M ${drawnPoints.map((p) => `${p.x},${p.y}`).join(' L ')}`
      : '';

  // Current position dot
  const currentIdx = Math.min(drawnSamples, curveSamples);
  const dotPos = curvePoints[currentIdx];

  // Linear reference line
  const linearPath = `M ${curvePoints[0].x},${curveY + curveHeight / 2} L ${curvePoints[curveSamples].x},${curveY - curveHeight / 2}`;

  const curveOpacity = interpolate(frame, [10, 30], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill style={{ backgroundColor: COLORS.spaceDark }}>
      <Starfield count={80} />

      {/* Left column: Text */}
      <div
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          bottom: 0,
          width: '50%',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          padding: '0 100px 0 160px',
        }}
      >
        <div
          style={{
            fontFamily: orbitronFamily,
            fontWeight: 700,
            fontSize: 40,
            color: COLORS.cyanGlow,
            marginBottom: 40,
            opacity: headingSpring,
            transform: `translateY(${interpolate(headingSpring, [0, 1], [-20, 0])}px)`,
          }}
        >
          Orbital Velocity &amp; Easing
        </div>

        {BULLET_POINTS.map((bp, i) => {
          const delay = 20 + i * 20;
          const bpSpring = spring({ frame, fps, delay, config: { damping: 200 } });

          return (
            <div
              key={i}
              style={{
                marginBottom: 28,
                opacity: bpSpring,
                transform: `translateY(${interpolate(bpSpring, [0, 1], [20, 0])}px)`,
              }}
            >
              <div
                style={{
                  fontFamily: orbitronFamily,
                  fontWeight: 700,
                  fontSize: 22,
                  color: bp.color,
                  marginBottom: 6,
                }}
              >
                ● {bp.label}
              </div>
              <div
                style={{
                  fontFamily: interFamily,
                  fontSize: 20,
                  color: COLORS.textSecondary,
                  paddingLeft: 24,
                }}
              >
                {bp.desc}
              </div>
            </div>
          );
        })}

        {/* Code snippet */}
        <div
          style={{
            fontFamily: monoFamily,
            fontSize: 16,
            color: COLORS.cyanGlow,
            backgroundColor: COLORS.equationBg,
            border: `1px solid ${COLORS.equationBorder}`,
            borderRadius: 10,
            padding: '14px 20px',
            marginTop: 20,
            opacity: spring({ frame, fps, delay: 80, config: { damping: 200 } }),
          }}
        >
          easing: Easing.inOut(Easing.sin)
        </div>
      </div>

      {/* Right column: Easing curve */}
      <svg
        width={width}
        height={height}
        style={{ position: 'absolute', top: 0, left: 0 }}
      >
        <g opacity={curveOpacity}>
          {/* Axis lines */}
          <line
            x1={curveX - curveWidth / 2}
            y1={curveY + curveHeight / 2}
            x2={curveX + curveWidth / 2}
            y2={curveY + curveHeight / 2}
            stroke={COLORS.textDim}
            strokeWidth={1}
          />
          <line
            x1={curveX - curveWidth / 2}
            y1={curveY + curveHeight / 2}
            x2={curveX - curveWidth / 2}
            y2={curveY - curveHeight / 2}
            stroke={COLORS.textDim}
            strokeWidth={1}
          />

          {/* Axis labels */}
          <text
            x={curveX}
            y={curveY + curveHeight / 2 + 30}
            fill={COLORS.textSecondary}
            fontSize={16}
            fontFamily={interFamily}
            textAnchor="middle"
          >
            Frame (time) →
          </text>
          <text
            x={curveX - curveWidth / 2 - 20}
            y={curveY}
            fill={COLORS.textSecondary}
            fontSize={16}
            fontFamily={interFamily}
            textAnchor="middle"
            transform={`rotate(-90, ${curveX - curveWidth / 2 - 20}, ${curveY})`}
          >
            Progress →
          </text>

          {/* Linear reference */}
          <path
            d={linearPath}
            fill="none"
            stroke={COLORS.textDim}
            strokeWidth={1}
            strokeDasharray="6 4"
          />
          <text
            x={curveX + curveWidth / 2 + 10}
            y={curveY - curveHeight / 2 + 5}
            fill={COLORS.textDim}
            fontSize={14}
            fontFamily={interFamily}
          >
            linear
          </text>

          {/* Ghost full curve */}
          <path d={curvePath} fill="none" stroke={COLORS.cyanGlow} strokeWidth={1} opacity={0.15} />

          {/* Drawn curve */}
          <path d={drawnPath} fill="none" stroke={COLORS.cyanGlow} strokeWidth={3} strokeLinecap="round" />

          {/* Moving dot */}
          {dotPos && (
            <>
              <circle cx={dotPos.x} cy={dotPos.y} r={8} fill={COLORS.magenta} />
              <circle cx={dotPos.x} cy={dotPos.y} r={16} fill={COLORS.magenta} opacity={0.2} />
            </>
          )}

          {/* Labels: Slow / Fast */}
          <text
            x={curveX - curveWidth / 2 + 10}
            y={curveY + curveHeight / 2 - 10}
            fill={COLORS.earthBlue}
            fontSize={14}
            fontFamily={orbitronFamily}
          >
            SLOW
          </text>
          <text
            x={curveX - 20}
            y={curveY - 10}
            fill={COLORS.magenta}
            fontSize={14}
            fontFamily={orbitronFamily}
          >
            FAST
          </text>
          <text
            x={curveX + curveWidth / 2 - 50}
            y={curveY - curveHeight / 2 + 20}
            fill={COLORS.moonGray}
            fontSize={14}
            fontFamily={orbitronFamily}
          >
            SLOW
          </text>
        </g>
      </svg>
    </AbsoluteFill>
  );
};
