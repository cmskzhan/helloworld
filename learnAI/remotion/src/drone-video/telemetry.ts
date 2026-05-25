// Telemetry data extracted from .SRT files
// GPS coordinates, elevations, timestamps for all 7 scenes

export const FPS = 60;
export const WIDTH = 1920;
export const HEIGHT = 1080;
export const TOTAL_FRAMES = 3450; // ~57.5s at 60fps
export const TRANSITION_FRAMES = 30; // 0.5s crossfade

// ─── Scene definitions ────────────────────────────────────────────────────────
export type SceneData = {
  id: string;
  file: string;
  location: string;
  sublocation: string;
  /** HH:MM telemetry timestamp shown in HUD */
  time: string;
  /** Full HMS for display clock */
  timeFull: string;
  lat: number;
  lng: number;
  altM: number;
  /** Seconds to skip from start of source file */
  trimBeforeS: number;
  /** How many seconds of the source to play */
  durationS: number;
  playbackRate: number;
};

export const SCENES: SceneData[] = [
  {
    id: "0004_s1",
    file: "DJI_20260124104255_0004_D.MP4",
    location: "HORSELL COMMON",
    sublocation: "H O R S E L L   C O M M O N",
    time: "10:42",
    timeFull: "10:42:55",
    lat: 51.32777,
    lng: -0.56559,
    altM: 212.9,
    trimBeforeS: 0,
    durationS: 8,
    playbackRate: 1,
  },
  {
    id: "0005",
    file: "DJI_20260124110814_0005_D.MP4",
    location: "HORSELL COMMON",
    sublocation: "P I N E   W O O D L A N D S",
    time: "11:08",
    timeFull: "11:08:14",
    lat: 51.32738,
    lng: -0.56615,
    altM: 212.5,
    trimBeforeS: 0,
    durationS: 10,
    playbackRate: 1,
  },
  {
    id: "0006",
    file: "DJI_20260124112727_0006_D.MP4",
    location: "HORSELL BIRCH",
    sublocation: "H O R S E L L   B I R C H",
    time: "11:27",
    timeFull: "11:27:28",
    lat: 51.3265, // estimated – no GPS lock in this clip
    lng: -0.583,
    altM: 198.1,
    trimBeforeS: 0,
    durationS: 1,
    playbackRate: 3, // speed-ramp 3s clip to 1s
  },
  {
    id: "0007",
    file: "DJI_20260124112826_0007_D.MP4",
    location: "HORSELL BIRCH",
    sublocation: "H O R S E L L   B I R C H",
    time: "11:28",
    timeFull: "11:28:26",
    lat: 51.32652,
    lng: -0.58590,
    altM: 198.8,
    trimBeforeS: 0,
    durationS: 10,
    playbackRate: 1,
  },
  {
    id: "0008",
    file: "DJI_20260124113216_0008_D.MP4",
    location: "HORSELL BIRCH",
    sublocation: "B I R C H   W O O D S   P O N D",
    time: "11:32",
    timeFull: "11:32:16",
    lat: 51.32683,
    lng: -0.58933,
    altM: 198.6,
    trimBeforeS: 0,
    durationS: 9,
    playbackRate: 1,
  },
  {
    id: "0009",
    file: "DJI_20260124131820_0009_D.MP4",
    location: "HOOK HEATH",
    sublocation: "H O O K   H E A T H",
    time: "13:18",
    timeFull: "13:18:20",
    lat: 51.32327,
    lng: -0.55917,
    altM: 202.3,
    trimBeforeS: 30, // start 30s in for best scenic section
    durationS: 17,
    playbackRate: 1,
  },
  {
    id: "0004_s2",
    file: "DJI_20260124104255_0004_D.MP4",
    location: "HORSELL COMMON",
    sublocation: "H O R S E L L   C O M M O N",
    time: "11:06",
    timeFull: "11:06:00",
    lat: 51.32754,
    lng: -0.56587,
    altM: 212.9,
    trimBeforeS: 35, // outro segment from later in the clip
    durationS: 5,
    playbackRate: 1,
  },
];

// ─── Frame boundaries (global) ────────────────────────────────────────────────
// TransitionSeries overlaps adjacent scenes by TRANSITION_FRAMES.
// Between scene 2 (0006) and scene 3 (0007) there is a DIRECT CUT (no transition).
// Global start frame for each scene:
//   S0: 0
//   S1: 480 - 30 = 450
//   S2: 450 + 600 - 30 = 1020
//   S3: 1020 + 60 = 1080  (direct cut, no overlap)
//   S4: 1080 + 600 - 30 = 1650
//   S5: 1650 + 540 - 30 = 2160
//   S6: 2160 + 1020 - 30 = 3150
//   Total: 3150 + 300 = 3450

export const SCENE_DURATIONS = [480, 600, 60, 600, 540, 1020, 300]; // frames

/** Global frame at which each scene STARTS (after subtracting transition overlaps) */
export const SCENE_STARTS: number[] = (() => {
  const starts: number[] = [0];
  for (let i = 0; i < SCENE_DURATIONS.length - 1; i++) {
    const overlap = i === 1 ? 0 : TRANSITION_FRAMES; // no transition between S2 and S3
    starts.push(starts[i] + SCENE_DURATIONS[i] - overlap);
  }
  return starts;
})();

/** Given a global frame, return the dominant scene index (0-6) and local progress 0–1 */
export function getSceneProgress(frame: number): { sceneIdx: number; progress: number } {
  for (let i = SCENES.length - 1; i >= 0; i--) {
    if (frame >= SCENE_STARTS[i]) {
      const local = frame - SCENE_STARTS[i];
      const progress = Math.min(local / SCENE_DURATIONS[i], 1);
      return { sceneIdx: i, progress };
    }
  }
  return { sceneIdx: 0, progress: 0 };
}

// ─── GPS route waypoints for the minimap ─────────────────────────────────────
// Each scene has a [startLat, startLng] and [endLat, endLng].
export const ROUTE_WAYPOINTS: Array<[number, number]> = [
  [51.32777, -0.56559], // S0 start (0004)
  [51.32738, -0.56615], // S1 start (0005)
  [51.32709, -0.56692], // S1 end
  [51.3265, -0.583],    // S2 (0006 – estimated)
  [51.32652, -0.58590], // S3 start (0007)
  [51.32676, -0.58840], // S3 end
  [51.32683, -0.58933], // S4 start (0008)
  [51.32707, -0.59013], // S4 end
  [51.32327, -0.55917], // S5 start (0009) – Hook Heath
  [51.32570, -0.55630], // S5 end
  [51.32754, -0.56587], // S6 outro (back near Horsell)
];

// Whoosh SFX fire at transition midpoints (global frames)
export const WHOOSH_FRAMES = [465, 1035, 1665, 2175, 3165];
