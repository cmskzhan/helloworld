import React from "react";
import { Composition } from "remotion";
import { SurreyExcursion } from "./Composition";
import { MinimapPreviewComposition } from "./MinimapPreview";
import { WIDTH, HEIGHT, FPS, TOTAL_FRAMES } from "./telemetry";

export const SurreyExcursionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="MinimapPreview"
        component={MinimapPreviewComposition}
        durationInFrames={TOTAL_FRAMES}
        fps={FPS}
        width={WIDTH}
        height={HEIGHT}
      />
      <Composition
        id="SurreyExcursion"
        component={SurreyExcursion}
        durationInFrames={TOTAL_FRAMES}
        fps={FPS}
        width={WIDTH}
        height={HEIGHT}
      />
    </>
  );
};
