import React from "react";
import { useCurrentFrame, useVideoConfig, interpolate, Easing } from "remotion";
import {
  SCENES,
  ROUTE_WAYPOINTS,
  getSceneProgress,
  FPS,
} from "../telemetry";

// ─── Map projection bounds (padded slightly beyond all GPS points) ─────────────
const LAT_MIN = 51.3215;
const LAT_MAX = 51.3295;
const LNG_MIN = -0.5960;
const LNG_MAX = -0.5530;

// SVG canvas inside the card
const MAP_W = 272;
const MAP_H = 160;
const PAD = 10;

function project(lat: number, lng: number): [number, number] {
  // Apply cos-correction for longitude so distances look proportional
  const cosLat = Math.cos((51.327 * Math.PI) / 180); // ~0.626
  const x =
    PAD +
    ((lng - LNG_MIN) / (LNG_MAX - LNG_MIN)) *
      (MAP_W - PAD * 2);
  // Invert y because SVG y increases downward
  const y =
    PAD +
    (1 - (lat - LAT_MIN) / (LAT_MAX - LAT_MIN)) *
      (MAP_H - PAD * 2);
  return [x, y];
}

// Pre-project every waypoint once
const WAYPOINT_PX = ROUTE_WAYPOINTS.map(([lat, lng]) => project(lat, lng));

// Location pins: [label, lat, lng]
const PINS: Array<{ label: string; lat: number; lng: number; color: string }> = [
  { label: "Horsell Common", lat: 51.32777, lng: -0.56559, color: "#f59e0b" },
  { label: "Horsell Birch", lat: 51.32652, lng: -0.58590, color: "#f59e0b" },
  { label: "Hook Heath", lat: 51.32327, lng: -0.55917, color: "#f59e0b" },
];

// Build polyline points string from all waypoints
const polylinePoints = WAYPOINT_PX.map(([x, y]) => `${x},${y}`).join(" ");

export const Minimap: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // ── Which scene & progress? ──────────────────────────────────────────────
  const { sceneIdx, progress } = getSceneProgress(frame);

  // Determine dot position: interpolate along waypoints proportional to overall
  // video progress (0→1 across all 3450 frames)
  const totalFrames = 3450;
  const overallProgress = Math.min(frame / (totalFrames - 1), 1);

  // Map overall progress to waypoint index (fractional)
  const waypointProgress = overallProgress * (WAYPOINT_PX.length - 1);
  const wpIdx = Math.floor(waypointProgress);
  const wpFrac = waypointProgress - wpIdx;
  const wpA = WAYPOINT_PX[Math.min(wpIdx, WAYPOINT_PX.length - 1)];
  const wpB = WAYPOINT_PX[Math.min(wpIdx + 1, WAYPOINT_PX.length - 1)];
  const dotX = wpA[0] + (wpB[0] - wpA[0]) * wpFrac;
  const dotY = wpA[1] + (wpB[1] - wpA[1]) * wpFrac;

  // ── Pulsing radar ring (frame-driven, not CSS) ──────────────────────────
  const pulseProgress = ((frame % fps) / fps); // 0→1 every second
  const pulseR = 6 + pulseProgress * 14;
  const pulseOpacity = (1 - pulseProgress) * 0.7;

  // ── Card entrance animation (fade+slide from right) ─────────────────────
  const cardOpacity = interpolate(frame, [0, 45], [0, 1], {
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.quad),
  });
  const cardX = interpolate(frame, [0, 45], [30, 0], {
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.quad),
  });

  // ── Time label from the active scene ───────────────────────────────────
  const scene = SCENES[sceneIdx];
  // Animate the seconds ticking within the scene
  const localFrame = frame - (
    sceneIdx === 0 ? 0 :
    sceneIdx === 1 ? 450 :
    sceneIdx === 2 ? 1020 :
    sceneIdx === 3 ? 1080 :
    sceneIdx === 4 ? 1650 :
    sceneIdx === 5 ? 2160 : 3150
  );
  const [hStr, mStr, sStr] = scene.timeFull.split(":");
  const baseSec = parseInt(sStr, 10) + Math.floor(localFrame / fps);
  const dispH = hStr;
  const dispM = mStr;
  const dispS = String(baseSec % 60).padStart(2, "0");
  const timeDisplay = `${dispH}:${dispM}:${dispS}`;

  return (
    <div
      style={{
        position: "absolute",
        top: 32,
        right: 32,
        width: 296,
        opacity: cardOpacity,
        transform: `translateX(${cardX}px)`,
        fontFamily: "'Space Mono', 'Courier New', monospace",
      }}
    >
      {/* Glass card */}
      <div
        style={{
          background: "rgba(0, 0, 0, 0.55)",
          backdropFilter: "blur(12px)",
          WebkitBackdropFilter: "blur(12px)",
          border: "1px solid rgba(250, 200, 80, 0.35)",
          borderRadius: 8,
          overflow: "hidden",
          boxShadow: "0 4px 32px rgba(0,0,0,0.6), inset 0 0 0 1px rgba(255,255,255,0.04)",
        }}
      >
        {/* Header bar */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            padding: "6px 10px",
            borderBottom: "1px solid rgba(250, 200, 80, 0.2)",
            background: "rgba(250, 200, 80, 0.06)",
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
            {/* Animated radar blip */}
            <div
              style={{
                width: 7,
                height: 7,
                borderRadius: "50%",
                background: "#f59e0b",
                boxShadow: "0 0 6px #f59e0b",
                animation: "none",
                opacity: 0.5 + pulseProgress * 0.5,
              }}
            />
            <span
              style={{
                color: "#fac840",
                fontSize: 9,
                letterSpacing: "0.18em",
                textTransform: "uppercase",
              }}
            >
              EXCURSION ROUTE
            </span>
          </div>
          <span style={{ color: "rgba(255,255,255,0.5)", fontSize: 9, letterSpacing: "0.1em" }}>
            WOKING · SURREY
          </span>
        </div>

        {/* SVG map */}
        <div style={{ position: "relative" }}>
          <svg
            width={MAP_W}
            height={MAP_H}
            viewBox={`0 0 ${MAP_W} ${MAP_H}`}
            style={{ display: "block" }}
          >
            {/* Dark terrain background */}
            <rect width={MAP_W} height={MAP_H} fill="#0c1a10" />

            {/* Subtle grid lines */}
            {[0.25, 0.5, 0.75].map((t) => (
              <React.Fragment key={t}>
                <line
                  x1={PAD + t * (MAP_W - PAD * 2)} y1={PAD}
                  x2={PAD + t * (MAP_W - PAD * 2)} y2={MAP_H - PAD}
                  stroke="rgba(255,255,255,0.04)" strokeWidth={0.5}
                />
                <line
                  x1={PAD} y1={PAD + t * (MAP_H - PAD * 2)}
                  x2={MAP_W - PAD} y2={PAD + t * (MAP_H - PAD * 2)}
                  stroke="rgba(255,255,255,0.04)" strokeWidth={0.5}
                />
              </React.Fragment>
            ))}

            {/* Route trail — glowing cyan polyline */}
            {/* Glow layer */}
            <polyline
              points={polylinePoints}
              fill="none"
              stroke="#00e5ff"
              strokeWidth={4}
              strokeOpacity={0.18}
              strokeLinecap="round"
              strokeLinejoin="round"
            />
            {/* Main line */}
            <polyline
              points={polylinePoints}
              fill="none"
              stroke="#00e5ff"
              strokeWidth={1.5}
              strokeOpacity={0.75}
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeDasharray="3 2"
            />

            {/* Location pin dots */}
            {PINS.map((pin) => {
              const [px, py] = project(pin.lat, pin.lng);
              return (
                <g key={pin.label}>
                  <circle cx={px} cy={py} r={4} fill="#f59e0b" opacity={0.9} />
                  <circle cx={px} cy={py} r={7} fill="none" stroke="#f59e0b" strokeWidth={0.8} opacity={0.4} />
                </g>
              );
            })}

            {/* Pulsing radar ring around current dot */}
            <circle
              cx={dotX}
              cy={dotY}
              r={pulseR}
              fill="none"
              stroke="#f59e0b"
              strokeWidth={1}
              opacity={pulseOpacity}
            />

            {/* Current position dot */}
            <circle cx={dotX} cy={dotY} r={4.5} fill="#f59e0b" />
            <circle cx={dotX} cy={dotY} r={3} fill="#fff" opacity={0.9} />

            {/* Compact location labels */}
            {[
              { label: "Horsell", lat: 51.32777, lng: -0.56559, anchor: "start" as const, dy: -7 },
              { label: "Birch", lat: 51.32683, lng: -0.58933, anchor: "start" as const, dy: -7 },
              { label: "Hook Heath", lat: 51.32327, lng: -0.55917, anchor: "middle" as const, dy: 14 },
            ].map(({ label, lat, lng, anchor, dy }) => {
              const [lx, ly] = project(lat, lng);
              return (
                <text
                  key={label}
                  x={lx}
                  y={ly + dy}
                  textAnchor={anchor}
                  fill="#f59e0b"
                  fontSize={7}
                  fontFamily="'Space Mono', monospace"
                  opacity={0.85}
                  letterSpacing={0.5}
                >
                  {label.toUpperCase()}
                </text>
              );
            })}

            {/* North indicator */}
            <text x={MAP_W - PAD - 2} y={PAD + 8} fill="rgba(255,255,255,0.3)" fontSize={7} textAnchor="end" fontFamily="monospace">N↑</text>
          </svg>
        </div>

        {/* Footer: live clock + active location */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            padding: "5px 10px",
            borderTop: "1px solid rgba(250, 200, 80, 0.12)",
          }}
        >
          <span
            style={{
              color: "#00e5ff",
              fontSize: 11,
              letterSpacing: "0.12em",
              fontVariantNumeric: "tabular-nums",
            }}
          >
            {timeDisplay} GMT
          </span>
          <span
            style={{
              color: "rgba(255,255,255,0.45)",
              fontSize: 8,
              letterSpacing: "0.14em",
              textTransform: "uppercase",
              maxWidth: 110,
              textAlign: "right",
            }}
          >
            {scene.location}
          </span>
        </div>
      </div>
    </div>
  );
};
