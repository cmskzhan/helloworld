import React from "react";
import { Composition } from "remotion";
import { SurreyExcursion } from "./Composition";
import { WIDTH, HEIGHT, FPS, TOTAL_FRAMES } from "./telemetry";

export const SurreyExcursionRoot: React.FC = () => {
  return (
    <>
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
