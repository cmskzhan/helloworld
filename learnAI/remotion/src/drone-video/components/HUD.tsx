import React from "react";
import { useCurrentFrame, useVideoConfig, interpolate, Easing } from "remotion";
import { SCENES, getSceneProgress, FPS } from "../telemetry";

// ── Letterbox bars: cinematic 2.39:1 crop ────────────────────────────────────
export const Letterbox: React.FC = () => {
  const { width, height } = useVideoConfig();
  const frame = useCurrentFrame();

  // Bars slide in from top/bottom over first 45 frames
  const barH = Math.round(height - (width / 2.39)) / 2; // ≈ 34px at 1920x1080
  const progress = interpolate(frame, [0, 45], [0, 1], {
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.cubic),
  });
  const topY   = interpolate(progress, [0, 1], [-barH, 0]);
  const bottomY = interpolate(progress, [0, 1], [height + barH, height - barH]);

  return (
    <>
      {/* Top bar */}
      <div
        style={{
          position: "absolute",
          top: topY,
          left: 0,
          width,
          height: barH,
          background: "#000",
          zIndex: 10,
        }}
      />
      {/* Bottom bar */}
      <div
        style={{
          position: "absolute",
          top: bottomY,
          left: 0,
          width,
          height: barH,
          background: "#000",
          zIndex: 10,
        }}
      />
    </>
  );
};

// ── Scene title card ──────────────────────────────────────────────────────────
// Fades in ~2s after scene starts, holds 3s, fades out
export const TitleCard: React.FC<{ sceneIdx: number }> = ({ sceneIdx }) => {
  const frame = useCurrentFrame(); // local frame within this sequence
  const scene = SCENES[sceneIdx];

  const opacity = interpolate(
    frame,
    [0, 60, 120, 180, 240, 300],
    [0,  0,   1,   1,  1,   0],
    { extrapolateRight: "clamp", easing: Easing.inOut(Easing.quad) }
  );

  if (opacity <= 0) return null;

  return (
    <div
      style={{
        position: "absolute",
        bottom: 120,
        left: 0,
        right: 0,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        opacity,
        fontFamily: "'Space Mono', 'Courier New', monospace",
        pointerEvents: "none",
        zIndex: 8,
      }}
    >
      {/* Decorative line above */}
      <div
        style={{
          width: interpolate(opacity, [0, 1], [0, 160]),
          height: 1,
          background: "rgba(245,158,11,0.6)",
          marginBottom: 10,
        }}
      />
      <span
        style={{
          fontSize: 18,
          letterSpacing: "0.45em",
          color: "#ffffff",
          textTransform: "uppercase",
          textShadow: "0 2px 24px rgba(0,0,0,0.8)",
        }}
      >
        {scene.sublocation}
      </span>
      {/* Decorative line below */}
      <div
        style={{
          width: interpolate(opacity, [0, 1], [0, 80]),
          height: 1,
          background: "rgba(245,158,11,0.4)",
          marginTop: 10,
        }}
      />
    </div>
  );
};

// ── Bottom-left telemetry HUD ─────────────────────────────────────────────────
export const TelemetryHUD: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const { sceneIdx, progress } = getSceneProgress(frame);
  const scene = SCENES[sceneIdx];

  // Entrance: slide up from bottom
  const slideY = interpolate(frame, [0, 45], [40, 0], {
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.cubic),
  });
  const opacity = interpolate(frame, [0, 45], [0, 1], {
    extrapolateRight: "clamp",
  });

  // Animate time within each scene (seconds tick)
  const [hStr, mStr, sStr] = scene.timeFull.split(":");
  const baseSec = parseInt(sStr, 10) + Math.floor((frame - (
    [0, 450, 1020, 1080, 1650, 2160, 3150][sceneIdx] ?? 0
  )) / fps);
  const dispS = String(baseSec % 60).padStart(2, "0");
  const timeStr = `${hStr}:${mStr}:${dispS}`;

  // Blinking cursor on coordinate line (every 45 frames)
  const blink = Math.floor(frame / 30) % 2 === 0;

  const coordLat = scene.lat.toFixed(4);
  const coordLng = Math.abs(scene.lng).toFixed(4);
  const latDir = scene.lat >= 0 ? "N" : "S";
  const lngDir = scene.lng >= 0 ? "E" : "W";
  const altStr = scene.altM.toFixed(1);

  const labelStyle: React.CSSProperties = {
    color: "rgba(0,229,255,0.65)",
    fontSize: 11,
    letterSpacing: "0.18em",
    fontFamily: "'Space Mono', 'Courier New', monospace",
    marginRight: 8,
  };
  const valueStyle: React.CSSProperties = {
    color: "rgba(255,255,255,0.9)",
    fontSize: 11,
    letterSpacing: "0.12em",
    fontFamily: "'Space Mono', 'Courier New', monospace",
  };

  return (
    <div
      style={{
        position: "absolute",
        bottom: 52,
        left: 40,
        opacity,
        transform: `translateY(${slideY}px)`,
        zIndex: 9,
        display: "flex",
        flexDirection: "column",
        gap: 5,
        pointerEvents: "none",
      }}
    >
      {/* Thin amber top rule */}
      <div style={{ width: 180, height: 1, background: "rgba(245,158,11,0.5)", marginBottom: 4 }} />

      <div style={{ display: "flex", alignItems: "center" }}>
        <span style={labelStyle}>COORD</span>
        <span style={valueStyle}>
          {coordLat}° {latDir},  {coordLng}° {lngDir}
          {blink ? " _" : "  "}
        </span>
      </div>

      <div style={{ display: "flex", alignItems: "center" }}>
        <span style={labelStyle}>ELEV </span>
        <span style={valueStyle}>{altStr} M  ABS</span>
      </div>

      <div style={{ display: "flex", alignItems: "center" }}>
        <span style={labelStyle}>TIME </span>
        <span style={valueStyle}>{timeStr}  GMT</span>
      </div>

      {/* Thin amber bottom rule */}
      <div style={{ width: 180, height: 1, background: "rgba(245,158,11,0.3)", marginTop: 4 }} />
    </div>
  );
};

// ── Opening quote card (Sci-Fi flavour, fades in/out in first 5s) ─────────────
export const OpeningQuote: React.FC = () => {
  const frame = useCurrentFrame();

  const opacity = interpolate(
    frame,
    [30, 90, 200, 270],
    [0,   1,   1,   0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.inOut(Easing.quad) }
  );

  if (opacity <= 0) return null;

  return (
    <div
      style={{
        position: "absolute",
        top: 0, left: 0, right: 0, bottom: 0,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        opacity,
        pointerEvents: "none",
        zIndex: 7,
      }}
    >
      <div
        style={{
          maxWidth: 760,
          textAlign: "center",
          padding: "0 60px",
        }}
      >
        <p
          style={{
            fontFamily: "'Space Mono', 'Courier New', monospace",
            fontSize: 16,
            lineHeight: 1.7,
            color: "rgba(255,255,255,0.72)",
            fontStyle: "italic",
            letterSpacing: "0.04em",
            textShadow: "0 2px 30px rgba(0,0,0,0.9)",
            margin: 0,
          }}
        >
          "No one would have believed, in the last years of the nineteenth century,<br />
          that this world was being watched…"
        </p>
        <p
          style={{
            fontFamily: "'Space Mono', 'Courier New', monospace",
            fontSize: 11,
            color: "rgba(245,158,11,0.7)",
            letterSpacing: "0.22em",
            marginTop: 18,
            textTransform: "uppercase",
            textShadow: "0 2px 16px rgba(0,0,0,0.9)",
          }}
        >
          — H.G. Wells · The War of the Worlds · Horsell Common, Surrey
        </p>
      </div>
    </div>
  );
};

// ── Fade-to-black outro overlay ───────────────────────────────────────────────
export const OutroFade: React.FC<{ totalFrames: number }> = ({ totalFrames }) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(
    frame,
    [totalFrames - 120, totalFrames - 1],
    [0, 1],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.in(Easing.cubic) }
  );

  return (
    <div
      style={{
        position: "absolute",
        inset: 0,
        background: "#000",
        opacity,
        pointerEvents: "none",
        zIndex: 20,
      }}
    />
  );
};
