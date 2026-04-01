/**
 * Scene 7 – Outro
 * Summary note and credits with elegant fade-out.
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
import { COLORS, interFamily, orbitronFamily } from '../styles';

export const OutroScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  const entranceSpring = spring({ frame, fps, config: { damping: 200 } });

  // Fade everything out for last 1 second
  const exitOpacity = interpolate(
    frame,
    [durationInFrames - fps, durationInFrames],
    [1, 0],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' },
  );

  return (
    <AbsoluteFill style={{ backgroundColor: COLORS.spaceDark, opacity: exitOpacity }}>
      <Starfield count={100} />

      <div
        style={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          gap: 30,
          opacity: entranceSpring,
        }}
      >
        {/* Title reprise */}
        <div
          style={{
            fontFamily: orbitronFamily,
            fontWeight: 900,
            fontSize: 72,
            color: COLORS.textPrimary,
            letterSpacing: 10,
            textShadow: `0 0 30px ${COLORS.cyanDim}`,
          }}
        >
          ARTEMIS II
        </div>

        {/* Decorative line */}
        <div
          style={{
            width: interpolate(entranceSpring, [0, 1], [0, 300]),
            height: 2,
            background: `linear-gradient(90deg, transparent, ${COLORS.cyanGlow}, transparent)`,
          }}
        />

        {/* Note */}
        <div
          style={{
            fontFamily: interFamily,
            fontWeight: 400,
            fontSize: 20,
            color: COLORS.textSecondary,
            textAlign: 'center',
            maxWidth: 700,
            lineHeight: 1.8,
          }}
        >
          This visualization is a geometric representation using the Lemniscate of Bernoulli.
          In a real mission, the Earth lobe is significantly larger than the Lunar lobe
          due to Earth's much larger gravitational well.
        </div>

        {/* Credits */}
        <div
          style={{
            fontFamily: interFamily,
            fontSize: 14,
            color: COLORS.textDim,
            marginTop: 20,
            letterSpacing: 3,
            textTransform: 'uppercase',
          }}
        >
          Data Visualization • Educational Content
        </div>
      </div>
    </AbsoluteFill>
  );
};
