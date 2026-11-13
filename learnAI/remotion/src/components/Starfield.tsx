/**
 * Shared utility: Starfield background component.
 * Generates deterministic "stars" using a seeded PRNG so every frame is identical.
 */
import React, { useMemo } from 'react';
import { interpolate, useCurrentFrame, useVideoConfig } from 'remotion';

// Simple seeded random for deterministic stars
const seededRandom = (seed: number) => {
  const x = Math.sin(seed * 9301 + 49297) * 49297;
  return x - Math.floor(x);
};

type Star = {
  x: number;
  y: number;
  r: number;
  brightness: number;
  twinkleSpeed: number;
};

export const Starfield: React.FC<{ count?: number }> = ({ count = 200 }) => {
  const frame = useCurrentFrame();
  const { width, height } = useVideoConfig();

  const stars: Star[] = useMemo(() => {
    return Array.from({ length: count }).map((_, i) => ({
      x: seededRandom(i * 2) * width,
      y: seededRandom(i * 2 + 1) * height,
      r: seededRandom(i * 3) * 2 + 0.5,
      brightness: seededRandom(i * 4) * 0.6 + 0.4,
      twinkleSpeed: seededRandom(i * 5) * 0.04 + 0.02,
    }));
  }, [count, width, height]);

  return (
    <svg
      width={width}
      height={height}
      style={{ position: 'absolute', top: 0, left: 0 }}
    >
      {stars.map((star, i) => {
        const twinkle = interpolate(
          Math.sin(frame * star.twinkleSpeed + i),
          [-1, 1],
          [star.brightness * 0.5, star.brightness],
        );
        return (
          <circle
            key={i}
            cx={star.x}
            cy={star.y}
            r={star.r}
            fill={`rgba(255, 255, 255, ${twinkle})`}
          />
        );
      })}
    </svg>
  );
};
