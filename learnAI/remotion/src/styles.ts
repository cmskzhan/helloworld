/**
 * Shared design tokens and styles for the Artemis II Educational Video.
 */

// ── Color Palette ──────────────────────────────────────────────
export const COLORS = {
  // Backgrounds
  spaceDark: '#06080F',
  spaceDeep: '#0B0D17',
  panelBg: 'rgba(12, 17, 35, 0.85)',

  // Accent colors
  cyanGlow: '#00D4FF',
  cyanDim: 'rgba(0, 212, 255, 0.5)',
  magenta: '#FF3366',
  gold: '#FFD700',
  nasaBlue: '#0B3D91',

  // Celestial
  earthBlue: '#4B9CD3',
  moonGray: '#E0E0E0',

  // Text
  textPrimary: '#FFFFFF',
  textSecondary: 'rgba(255, 255, 255, 0.7)',
  textDim: 'rgba(255, 255, 255, 0.4)',

  // Equation highlight
  equationBg: 'rgba(0, 212, 255, 0.08)',
  equationBorder: 'rgba(0, 212, 255, 0.3)',
} as const;

// ── Typography ─────────────────────────────────────────────────
import { loadFont as loadInter } from '@remotion/google-fonts/Inter';
import { loadFont as loadJetBrains } from '@remotion/google-fonts/JetBrainsMono';
import { loadFont as loadOrbitron } from '@remotion/google-fonts/Orbitron';

export const { fontFamily: interFamily } = loadInter('normal', {
  weights: ['300', '400', '600', '700'],
  subsets: ['latin'],
});

export const { fontFamily: monoFamily } = loadJetBrains('normal', {
  weights: ['400', '500'],
  subsets: ['latin'],
});

export const { fontFamily: orbitronFamily } = loadOrbitron('normal', {
  weights: ['400', '700', '900'],
  subsets: ['latin'],
});

// ── Layout Constants ───────────────────────────────────────────
export const COMP_WIDTH = 1920;
export const COMP_HEIGHT = 1080;
export const FPS = 30;

// ── Scene Durations (in frames) ────────────────────────────────
export const SCENE_DURATIONS = {
  title: 4 * FPS,       // 120 frames (4s)
  overview: 6 * FPS,    // 180 frames (6s)
  lemniscate: 6 * FPS,  // 180 frames (6s)
  equations: 5 * FPS,   // 150 frames (5s)
  easing: 5 * FPS,      // 150 frames (5s)
  trajectory: 8 * FPS,  // 240 frames (8s)
  outro: 3 * FPS,       // 90 frames (3s)
} as const;

export const TRANSITION_DURATION = 20; // frames overlap per transition (6 transitions)

// Total: sum(durations) - 6 * TRANSITION_DURATION
export const TOTAL_DURATION =
  Object.values(SCENE_DURATIONS).reduce((a, b) => a + b, 0) -
  6 * TRANSITION_DURATION;
