# Remotion video

<p align="center">
  <a href="https://github.com/remotion-dev/logo">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://github.com/remotion-dev/logo/raw/main/animated-logo-banner-dark.apng">
      <img alt="Animated Remotion Logo" src="https://github.com/remotion-dev/logo/raw/main/animated-logo-banner-light.gif">
    </picture>
  </a>
</p>

Welcome to your Remotion project! This repository contains multiple merged video compositions in a single workspace.

## Project Structure

### 1. Educational Compositions
- **ArtemisII-Educational**: An educational video detailing the Artemis II mission and trajectory.
- **ArtemisII-Educational-CN**: A Chinese-localized version of the Artemis II educational video.
- **ArtemisII-Trajectory**: A component composition visualizing the orbital trajectory of the Artemis II spacecraft.

### 2. Surrey Heathlands Excursion (`SurreyExcursion`)
A cinematic compilation showing a drone flight excursion across Surrey Heathlands (including Horsell Common, Horsell Birch, and Hook Heath). Features:
- **Telemetry HUD**: Displays real-time GPS coordinates, elevation, speed, flight mode, and standard flight instrumentation (pitch/roll/yaw guides) overlaid on the video.
- **Dynamic Audio Layering**: Synchronized ambient wind, fading birdsong, custom background music, and whoosh transition SFX timed precisely to cut points.
- **Speed Ramping & Glitch Effects**: Custom playbacks (such as high-speed transitions and flare animations) synchronized with telemetry states.

#### Custom SVG Minimap Component
The project includes a fully responsive SVG **Minimap** overlay (`Minimap.tsx` & `MinimapPreview.tsx`) that:
- Draws the complete flight path as a smooth, styled SVG vector path over a terrain/map background.
- Dynamically interpolates the drone's position marker along the coordinates in sync with the video timeline.
- Features a radar sweeps/telemetry indicator showing real-time heading and coordinates.
- Displays dynamic numeric text updates for current latitude, longitude, and elevation.

## Commands

**Install Dependencies**

```console
npm i
```

**Start Preview**

```console
npm run dev
npm run start
npx remotion preview
```

**Render video**

```console
npx remotion render
npm run render <CompositionName> [output]
npx remotion render SurreyExcursion out/SurreyExcursion.mp4
```

**Upgrade Remotion**

```console
npx remotion upgrade
```

## Docs

Get started with Remotion by reading the [fundamentals page](https://www.remotion.dev/docs/the-fundamentals).

## Help

We provide help on our [Discord server](https://discord.gg/6VzzNDwUwV).

## Issues

Found an issue with Remotion? [File an issue here](https://github.com/remotion-dev/remotion/issues/new).

## License

Note that for some entities a company license is needed. [Read the terms here](https://github.com/remotion-dev/remotion/blob/main/LICENSE.md).
