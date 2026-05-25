import React from "react";
import { AbsoluteFill, Composition } from "remotion";
import { Minimap } from "./components/Minimap";
import { FPS, TOTAL_FRAMES, WIDTH, HEIGHT } from "./telemetry";

/**
 * Standalone Minimap Preview Composition
 * Shows just the minimap component on a black background with all animations
 * Select this from the Remotion preview UI to focus on minimap development
 */
export const MinimapPreviewComposition: React.FC = () => {
  return (
    <AbsoluteFill style={{ background: "#000" }}>
      <Minimap />
    </AbsoluteFill>
  );
};
