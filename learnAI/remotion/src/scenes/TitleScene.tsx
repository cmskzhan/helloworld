/**
 * Scene 1 – Title Card
 * "ARTEMIS II" with cinematic reveal, subtitle, and tagline.
 */
import React from 'react';
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import { Starfield } from '../components/Starfield';
import { COLORS, orbitronFamily, interFamily } from '../styles';

export const TitleScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // ── Title spring entrance ──
  const titleSpring = spring({ frame, fps, config: { damping: 200 } });
  const titleY = interpolate(titleSpring, [0, 1], [60, 0]);
  const titleOpacity = titleSpring;

  // ── Subtitle (delayed) ──
  const subtitleSpring = spring({ frame, fps, delay: 15, config: { damping: 200 } });
  const subtitleY = interpolate(subtitleSpring, [0, 1], [40, 0]);

  // ── Tagline (further delayed) ──
  const taglineSpring = spring({ frame, fps, delay: 30, config: { damping: 200 } });

  // ── Glowing line ──
  const lineWidth = interpolate(
    spring({ frame, fps, delay: 10, config: { damping: 200 } }),
    [0, 1],
    [0, 400],
  );

  return (
    <AbsoluteFill style={{ backgroundColor: COLORS.spaceDark }}>
      <Starfield count={300} />

      {/* Radial glow behind title */}
      <div
        style={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          width: 800,
          height: 800,
          borderRadius: '50%',
          background: `radial-gradient(circle, ${COLORS.cyanDim} 0%, transparent 70%)`,
          opacity: interpolate(frame, [0, 60], [0, 0.3], {
            extrapolateRight: 'clamp',
          }),
        }}
      />

      <div
        style={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          gap: 20,
        }}
      >
        {/* Main Title */}
        <div
          style={{
            fontFamily: orbitronFamily,
            fontWeight: 900,
            fontSize: 120,
            color: COLORS.textPrimary,
            letterSpacing: 16,
            opacity: titleOpacity,
            transform: `translateY(${titleY}px)`,
            textShadow: `0 0 40px ${COLORS.cyanGlow}, 0 0 80px ${COLORS.cyanDim}`,
          }}
        >
          ARTEMIS II
        </div>

        {/* Decorative line */}
        <div
          style={{
            width: lineWidth,
            height: 2,
            background: `linear-gradient(90deg, transparent, ${COLORS.cyanGlow}, transparent)`,
          }}
        />

        {/* Subtitle */}
        <div
          style={{
            fontFamily: interFamily,
            fontWeight: 300,
            fontSize: 40,
            color: COLORS.cyanGlow,
            letterSpacing: 8,
            opacity: subtitleSpring,
            transform: `translateY(${subtitleY}px)`,
          }}
        >
          FREE-RETURN TRAJECTORY
        </div>

        {/* Tagline */}
        <div
          style={{
            fontFamily: interFamily,
            fontWeight: 400,
            fontSize: 24,
            color: COLORS.textSecondary,
            marginTop: 20,
            opacity: taglineSpring,
          }}
        >
          NASA's First Crewed Lunar Mission Since Apollo
        </div>
      </div>
    </AbsoluteFill>
  );
};
