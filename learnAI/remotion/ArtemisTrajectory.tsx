import React from 'react';
import {
    AbsoluteFill,
    interpolate,
    useCurrentFrame,
    useVideoConfig,
    Easing,
} from 'remotion';

// The mathematical formula for our Figure-8 orbit
const getOrbitalPosition = (progress: number, width: number, height: number) => {
    // Map progress (0 to 1) to a full circle (0 to 2π)
    const t = progress * Math.PI * 2;

    // Scale the orbit to take up 70% of the screen width
    const scale = width * 0.35;

    // Lemniscate of Bernoulli equations
    const x = (scale * Math.cos(t)) / (1 + Math.pow(Math.sin(t), 2)) + width / 2;
    const y = (scale * Math.sin(t) * Math.cos(t)) / (1 + Math.pow(Math.sin(t), 2)) + height / 2;

    return { x, y };
};

export const ArtemisTrajectory: React.FC = () => {
    const frame = useCurrentFrame();
    const { durationInFrames, width, height } = useVideoConfig();

    // 1. Calculate the progress of the mission (0 to 1)
    // We use an InOut easing to simulate gravity (slower at the edges, faster in the middle)
    const progress = interpolate(frame, [0, durationInFrames], [0, 1], {
        extrapolateRight: 'clamp',
        easing: Easing.inOut(Easing.sin),
    });

    // 2. Get the current coordinates for the Orion spacecraft
    const orionPos = getOrbitalPosition(progress, width, height);

    // 3. Generate the dynamic SVG path for the orbital trail
    // We calculate the path from frame 0 up to the *current* frame to create a drawing effect
    const trailPoints = Array.from({ length: Math.floor(frame) + 1 }).map((_, i) => {
        // Interpolate the specific progress for this historical frame
        const historyProgress = interpolate(i, [0, durationInFrames], [0, 1], {
            easing: Easing.inOut(Easing.sin),
        });
        const pos = getOrbitalPosition(historyProgress, width, height);
        return `${pos.x},${pos.y}`;
    });
    const pathD = trailPoints.length > 0 ? `M ${trailPoints.join(' L ')}` : '';

    // 4. Calculate fixed positions for Earth (Right Lobe) and Moon (Left Lobe)
    const scale = width * 0.35;
    const earthX = width / 2 + scale;
    const moonX = width / 2 - scale;
    const centerY = height / 2;

    return (
        <AbsoluteFill style={{ backgroundColor: '#0B0D17' }}>

            {/* Dynamic Orbital Trail */}
            <svg width={width} height={height} style={{ position: 'absolute' }}>
                <path
                    d={pathD}
                    fill="none"
                    stroke="rgba(0, 212, 255, 0.5)"
                    strokeWidth={4}
                    strokeDasharray="10 5" // Gives it a dashed "trajectory" look
                />
            </svg>

            {/* Earth */}
            <div
                style={{
                    position: 'absolute',
                    left: earthX - 40,
                    top: centerY - 40,
                    width: 80,
                    height: 80,
                    backgroundColor: '#4B9CD3', // Earth Blue
                    borderRadius: '50%',
                    boxShadow: '0 0 40px rgba(75, 156, 211, 0.4)',
                }}
            />

            {/* Moon */}
            <div
                style={{
                    position: 'absolute',
                    left: moonX - 20,
                    top: centerY - 20,
                    width: 40,
                    height: 40,
                    backgroundColor: '#E0E0E0', // Moon Gray
                    borderRadius: '50%',
                    boxShadow: '0 0 20px rgba(224, 224, 224, 0.2)',
                }}
            />

            {/* Orion Spacecraft */}
            <div
                style={{
                    position: 'absolute',
                    left: orionPos.x - 8,
                    top: orionPos.y - 8,
                    width: 16,
                    height: 16,
                    backgroundColor: '#FF3366', // High visibility color
                    borderRadius: '50%',
                    boxShadow: '0 0 15px #FF3366',
                }}
            />
        </AbsoluteFill>
    );
};