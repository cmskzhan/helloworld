# Project: Artemis II Free-Return Trajectory Visualization

## Overview
This project is a high-fidelity data visualization of the Artemis II mission, the first crewed flight of NASA's Orion spacecraft. Unlike later lunar landing missions, Artemis II follows a "free-return" trajectory.

This specific orbital path is a "Lunar Free-Return" profile where the spacecraft uses the Moon’s gravity to "whip" around and head back to Earth without requiring a major engine burn for the return trip. Visually, this creates a distinct "Figure-8" pattern in space relative to the Earth-Moon system.

## The Lemniscate of Bernoulli
To simulate this trajectory in a 2D environment (like Remotion or Canvas), we utilize the Lemniscate of Bernoulli. While real orbital mechanics involve complex $N$-body simulations, the Lemniscate provides an elegant geometric approximation of the Figure-8 motion.

The curve is defined as the locus of points where the product of the distances from two fixed points (foci) is constant. In this visualization, the two lobes of the curve represent:
- **The Earth Lobe**: The larger, departure and arrival end of the mission.
- **The Moon Lobe**: The smaller, gravity-assist "swing-by" end of the mission.

## Mathematical Implementation
The position of the Orion spacecraft is calculated parametrically. By varying a single parameter $t$ (representing the mission timeline), we can derive precise $(x, y)$ coordinates at any given frame.

### 1. Parametric Equations
Given a scale factor $a$ (which defines the "width" of the orbit) and a parameter $t$ (ranging from $0$ to $2\pi$), the coordinates are calculated as follows:

**For the X-coordinate:**
$$x(t) = \frac{a \cos(t)}{1 + \sin^2(t)}$$

**For the Y-coordinate:**
$$y(t) = \frac{a \sin(t) \cos(t)}{1 + \sin^2(t)}$$

### 2. Variable Definitions
- **$a$**: The focal distance. In the visualization code, this is typically set to roughly 35-40% of the screen width to ensure the orbit remains visible on all devices.
- **$t$**: The mission progress. In a 30fps video, $t$ is mapped from the currentFrame to a value between $0$ (Launch) and $2\pi$ (Splashdown).
- **$\sin^2(t)$**: This term in the denominator is what creates the "pinched" center of the Figure-8, forcing the spacecraft to cross the center point of the Earth-Moon line.

## Animation Strategy
To create a realistic sense of "orbital velocity," the value of $t$ is not increased linearly. We apply an Easing Function to the $t$ parameter:
- **Perigee (Earth)**: The spacecraft moves at its highest velocity.
- **Apogee (Moon)**: The spacecraft slows down as it fights Earth's gravity, before being accelerated by the Moon's gravity.

In the code, this is achieved by interpolating the frame count through a sinusoidal easing function to mimic the "hang-time" experienced in deep space.

> **Note**: This visualization is a geometric representation. In a real-world mission, the Earth lobe is significantly larger than the Lunar lobe due to the Earth's much larger gravitational well.
