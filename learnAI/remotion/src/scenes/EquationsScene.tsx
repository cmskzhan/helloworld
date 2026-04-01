/**
 * Scene 4 – Parametric Equations
 * Animated reveal of x(t) and y(t) formulas with variable definitions.
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
import { COLORS, interFamily, orbitronFamily, monoFamily } from '../styles';

type EquationDef = {
  label: string;
  formula: string;
  color: string;
};

const EQUATIONS: EquationDef[] = [
  {
    label: 'x(t)',
    formula: 'x(t)  =  a · cos(t)  /  ( 1 + sin²(t) )',
    color: COLORS.cyanGlow,
  },
  {
    label: 'y(t)',
    formula: 'y(t)  =  a · sin(t) · cos(t)  /  ( 1 + sin²(t) )',
    color: COLORS.gold,
  },
];

type VariableDef = {
  symbol: string;
  description: string;
};

const VARIABLES: VariableDef[] = [
  { symbol: 'a', description: 'Focal distance — 35-40% of screen width' },
  { symbol: 't', description: 'Mission progress — mapped from 0 (Launch) to 2π (Splashdown)' },
  { symbol: 'sin²(t)', description: 'Creates the "pinch" at the center of the Figure-8' },
];

export const EquationsScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const headingSpring = spring({ frame, fps, config: { damping: 200 } });

  return (
    <AbsoluteFill style={{ backgroundColor: COLORS.spaceDark }}>
      <Starfield count={80} />

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
          padding: '0 180px',
        }}
      >
        {/* Heading */}
        <div
          style={{
            fontFamily: orbitronFamily,
            fontWeight: 700,
            fontSize: 44,
            color: COLORS.cyanGlow,
            marginBottom: 50,
            opacity: headingSpring,
            transform: `translateY(${interpolate(headingSpring, [0, 1], [-20, 0])}px)`,
          }}
        >
          Parametric Equations
        </div>

        {/* Equation cards */}
        {EQUATIONS.map((eq, i) => {
          const delay = 15 + i * 25;
          const eqSpring = spring({ frame, fps, delay, config: { damping: 200 } });

          return (
            <div
              key={i}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: 30,
                marginBottom: 30,
                opacity: eqSpring,
                transform: `translateX(${interpolate(eqSpring, [0, 1], [-30, 0])}px)`,
              }}
            >
              {/* Label badge */}
              <div
                style={{
                  fontFamily: monoFamily,
                  fontWeight: 500,
                  fontSize: 20,
                  color: COLORS.spaceDark,
                  backgroundColor: eq.color,
                  padding: '6px 16px',
                  borderRadius: 6,
                  minWidth: 60,
                  textAlign: 'center',
                }}
              >
                {eq.label}
              </div>

              {/* Formula */}
              <div
                style={{
                  fontFamily: monoFamily,
                  fontSize: 28,
                  color: COLORS.textPrimary,
                  backgroundColor: COLORS.equationBg,
                  border: `1px solid ${COLORS.equationBorder}`,
                  borderRadius: 12,
                  padding: '16px 28px',
                  flex: 1,
                  letterSpacing: 1,
                }}
              >
                {eq.formula}
              </div>
            </div>
          );
        })}

        {/* Divider */}
        <div
          style={{
            width: interpolate(
              spring({ frame, fps, delay: 60, config: { damping: 200 } }),
              [0, 1],
              [0, 500],
            ),
            height: 1,
            background: `linear-gradient(90deg, ${COLORS.cyanGlow}, transparent)`,
            margin: '30px 0',
          }}
        />

        {/* Variable definitions */}
        <div
          style={{
            fontFamily: orbitronFamily,
            fontWeight: 700,
            fontSize: 24,
            color: COLORS.textSecondary,
            marginBottom: 20,
            opacity: spring({ frame, fps, delay: 65, config: { damping: 200 } }),
          }}
        >
          Variable Definitions
        </div>
        {VARIABLES.map((v, i) => {
          const delay = 75 + i * 15;
          const vSpring = spring({ frame, fps, delay, config: { damping: 200 } });

          return (
            <div
              key={i}
              style={{
                display: 'flex',
                alignItems: 'baseline',
                gap: 16,
                marginBottom: 14,
                opacity: vSpring,
                transform: `translateY(${interpolate(vSpring, [0, 1], [15, 0])}px)`,
              }}
            >
              <div
                style={{
                  fontFamily: monoFamily,
                  fontSize: 22,
                  color: COLORS.cyanGlow,
                  minWidth: 80,
                }}
              >
                {v.symbol}
              </div>
              <div
                style={{
                  fontFamily: interFamily,
                  fontSize: 20,
                  color: COLORS.textSecondary,
                }}
              >
                {v.description}
              </div>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
