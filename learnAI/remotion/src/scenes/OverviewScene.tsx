/**
 * Scene 2 – Mission Overview
 * Explains what a free-return trajectory is with animated text blocks.
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

const PARAGRAPHS = [
  'The Artemis II mission will send four astronauts on a journey around the Moon — the first crewed flight of NASA\'s Orion spacecraft.',
  'Unlike later landing missions, Artemis II follows a "free-return" trajectory: Orion uses the Moon\'s gravity to swing around and return to Earth without a major engine burn.',
  'This orbital path creates a distinctive Figure-8 pattern in space, tracing a loop around both the Earth and the Moon.',
];

export const OverviewScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // ── Heading entrance ──
  const headingSpring = spring({ frame, fps, config: { damping: 200 } });

  return (
    <AbsoluteFill style={{ backgroundColor: COLORS.spaceDark }}>
      <Starfield count={150} />

      <div
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          padding: '0 160px',
        }}
      >
        {/* Section heading */}
        <div
          style={{
            fontFamily: orbitronFamily,
            fontWeight: 700,
            fontSize: 48,
            color: COLORS.cyanGlow,
            marginBottom: 50,
            opacity: headingSpring,
            transform: `translateX(${interpolate(headingSpring, [0, 1], [-40, 0])}px)`,
          }}
        >
          What is a Free-Return Trajectory?
        </div>

        {/* Animated paragraphs */}
        {PARAGRAPHS.map((text, i) => {
          const delay = 20 + i * 30; // stagger by ~1 second
          const paraSpring = spring({
            frame,
            fps,
            delay,
            config: { damping: 200 },
          });
          const paraY = interpolate(paraSpring, [0, 1], [30, 0]);

          return (
            <div
              key={i}
              style={{
                fontFamily: interFamily,
                fontWeight: 400,
                fontSize: 30,
                lineHeight: 1.7,
                color: COLORS.textPrimary,
                marginBottom: 30,
                opacity: paraSpring,
                transform: `translateY(${paraY}px)`,
                borderLeft: `3px solid ${i === 1 ? COLORS.cyanGlow : 'transparent'}`,
                paddingLeft: i === 1 ? 20 : 0,
              }}
            >
              {text}
            </div>
          );
        })}

        {/* Decorative accent */}
        <div
          style={{
            position: 'absolute',
            right: 100,
            top: '50%',
            transform: 'translateY(-50%)',
            width: 300,
            height: 300,
            borderRadius: '50%',
            border: `1px solid ${COLORS.cyanDim}`,
            opacity: interpolate(frame, [40, 80], [0, 0.3], {
              extrapolateLeft: 'clamp',
              extrapolateRight: 'clamp',
            }),
          }}
        />
      </div>
    </AbsoluteFill>
  );
};
