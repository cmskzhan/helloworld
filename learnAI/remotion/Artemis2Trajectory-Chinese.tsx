import React, { useState, useEffect, useMemo } from 'react';

// Constants for the 30-second version
const TOTAL_DURATION_SECONDS = 30;
const FPS = 30;
const TOTAL_FRAMES = TOTAL_DURATION_SECONDS * FPS;

const getOrbitalPosition = (progress, width, height) => {
    const t = progress * Math.PI * 2;
    const scale = Math.min(width, height) * 0.35;
    const x = (scale * Math.cos(t)) / (1 + Math.pow(Math.sin(t), 2)) + width / 2;
    const y = (scale * Math.sin(t) * Math.cos(t)) / (1 + Math.pow(Math.sin(t), 2)) + height / 2;
    return { x, y };
};

// Easing function: Sine InOut
const easeInOutSin = (t) => {
    return (1 - Math.cos(Math.PI * t)) / 2;
};

const TitleSlide = ({ title, subtitle }) => (
    <div className="absolute inset-0 flex flex-col items-center justify-center text-white bg-slate-950 animate-in fade-in duration-1000">
        <h1 className="text-6xl md:text-8xl font-bold tracking-tighter mb-4 text-center px-4" style={{ textShadow: '0 0 20px rgba(255,255,255,0.5)' }}>
            {title}
        </h1>
        {subtitle && <p className="text-xl md:text-3xl tracking-widest opacity-80 uppercase text-center px-4">{subtitle}</p>}
    </div>
);

const InfoSlide = ({ title, description }) => (
    <div className="absolute inset-0 p-8 md:p-20 text-white bg-slate-950 animate-in fade-in slide-in-from-bottom-4 duration-700">
        <div className="h-full bg-black/40 backdrop-blur-md rounded-3xl p-8 md:p-12 border border-white/10">
            <h2 className="text-4xl md:text-5xl font-bold text-cyan-400 mb-6 md:mb-10 border-l-8 border-cyan-400 pl-6">
                {title}
            </h2>
            <div className="space-y-6 md:space-y-8">
                {description.map((text, i) => (
                    <p key={i} className="text-xl md:text-3xl leading-relaxed max-w-4xl opacity-90">
                        {text}
                    </p>
                ))}
            </div>
        </div>
    </div>
);

export default function App() {
    const [frame, setFrame] = useState(0);
    const [dimensions, setDimensions] = useState({ width: 1200, height: 800 });

    // Update dimensions for responsive preview
    useEffect(() => {
        const update = () => setDimensions({ width: window.innerWidth, height: window.innerHeight });
        update();
        window.addEventListener('resize', update);
        return () => window.removeEventListener('resize', update);
    }, []);

    // Animation loop to simulate Remotion's frame engine
    useEffect(() => {
        let interval = setInterval(() => {
            setFrame((f) => (f + 1) % TOTAL_FRAMES);
        }, 1000 / FPS);
        return () => clearInterval(interval);
    }, []);

    const { width, height } = dimensions;

    // Logic to determine which "Slide" to show based on frame
    const currentSlide = useMemo(() => {
        if (frame < 90) return 'intro'; // 0-3s
        if (frame < 240) return 'concept'; // 3-8s
        if (frame < 390) return 'math'; // 8-13s
        if (frame < 600) return 'physics'; // 13-20s
        return 'sim'; // 20-30s
    }, [frame]);

    // Simulation calculations
    const simStart = 600;
    const simFrame = Math.max(0, frame - simStart);
    const rawProgress = simFrame / 300;
    const simProgress = easeInOutSin(rawProgress);

    const orionPos = getOrbitalPosition(simProgress, width, height);

    let phase = "发射 (Launch)";
    if (simProgress > 0.15) phase = "地月转移 (Trans-Lunar Coast)";
    if (simProgress > 0.45) phase = "绕月飞行 (Lunar Flyby)";
    if (simProgress > 0.65) phase = "月地转移 (Trans-Earth Coast)";
    if (simProgress > 0.90) phase = "重返大气层 (Re-Entry)";

    return (
        <div className="w-full h-full bg-slate-950 overflow-hidden relative font-sans">
            {/* Starfield Background */}
            <div className="absolute inset-0 opacity-40">
                {Array.from({ length: 100 }).map((_, i) => (
                    <div
                        key={i}
                        className="absolute bg-white rounded-full"
                        style={{
                            width: Math.random() * 2 + 1,
                            height: Math.random() * 2 + 1,
                            left: `${Math.random() * 100}%`,
                            top: `${Math.random() * 100}%`,
                        }}
                    />
                ))}
            </div>

            {currentSlide === 'intro' && (
                <TitleSlide title="阿耳忒弥斯 2 号" subtitle="自由返回轨道模拟" />
            )}

            {currentSlide === 'concept' && (
                <InfoSlide
                    title="什么是自由返回轨道？"
                    description={[
                        "阿耳忒弥斯 2 号将载 4 名宇航员绕月飞行，这是自阿波罗计划以来首次载人绕月。",
                        "轨道利用月球引力实现自动返回，无需消耗大量燃料即可安全飞回地球。",
                        "这一路径在太空中划出一个独特的“数字 8”形状。"
                    ]}
                />
            )}

            {currentSlide === 'math' && (
                <InfoSlide
                    title="伯努利双纽线"
                    description={[
                        "数学上，这种轨迹可以用伯努利双纽线 (Lemniscate) 来模拟。",
                        "x(t) = a cos(t) / (1 + sin²(t))",
                        "y(t) = a sin(t) cos(t) / (1 + sin²(t))",
                        "这种几何近似能够完美展示出地月系统间的引力平衡点。"
                    ]}
                />
            )}

            {currentSlide === 'physics' && (
                <InfoSlide
                    title="轨道速度与引力"
                    description={[
                        "在近地点（地球附近）速度最快，受地心引力加速。",
                        "在远地点（月球附近）速度最慢，形成“悬停”效果，随后被月球引力弹回。",
                        "模拟使用了 Sinusoidal Easing 来还原真实的引力加速动态。"
                    ]}
                />
            )}

            {currentSlide === 'sim' && (
                <div className="absolute inset-0 animate-in fade-in duration-1000">
                    {/* Header */}
                    <div className="absolute top-8 left-8 text-white z-10">
                        <h1 className="text-3xl font-bold tracking-widest text-cyan-400">阿耳忒弥斯 2 号</h1>
                        <p className="text-lg opacity-60">自由返回轨道实时模拟</p>
                    </div>

                    {/* Orbit SVG */}
                    <svg width={width} height={height} className="absolute inset-0">
                        <path
                            d={`M ${Array.from({ length: 101 }).map((_, i) => {
                                const p = getOrbitalPosition(i / 100, width, height);
                                return `${p.x},${p.y}`;
                            }).join(' L ')} Z`}
                            fill="none"
                            stroke="rgba(255, 255, 255, 0.1)"
                            strokeWidth={2}
                        />
                        {/* Dynamic Trail */}
                        <path
                            d={`M ${Array.from({ length: Math.floor(simProgress * 100) + 1 }).map((_, i) => {
                                const p = getOrbitalPosition(i / 100, width, height);
                                return `${p.x},${p.y}`;
                            }).join(' L ')}`}
                            fill="none"
                            stroke="cyan"
                            strokeWidth={4}
                            strokeLinecap="round"
                            className="drop-shadow-[0_0_10px_cyan]"
                        />
                    </svg>

                    {/* Earth */}
                    <div
                        style={{ left: width / 2 + width * 0.35 - 40, top: height / 2 - 40 }}
                        className="absolute w-20 h-20 bg-blue-500 rounded-full shadow-[0_0_50px_rgba(59,130,246,0.6)] flex items-center justify-center border-2 border-blue-300"
                    >
                        <span className="text-xs text-white font-bold">地球</span>
                    </div>

                    {/* Moon */}
                    <div
                        style={{ left: width / 2 - width * 0.35 - 20, top: height / 2 - 20 }}
                        className="absolute w-10 h-10 bg-slate-300 rounded-full shadow-[0_0_30px_rgba(255,255,255,0.4)] flex items-center justify-center"
                    >
                        <span className="text-[10px] text-black font-bold">月球</span>
                    </div>

                    {/* Orion */}
                    <div
                        style={{ left: orionPos.x - 10, top: orionPos.y - 10 }}
                        className="absolute w-5 h-5 bg-red-500 rounded-full shadow-[0_0_20px_red]"
                    >
                        <div className="absolute top-6 left-1/2 -translate-x-1/2 text-red-400 font-bold whitespace-nowrap text-xs">猎户座飞船</div>
                    </div>

                    {/* Dashboard */}
                    <div className="absolute bottom-8 left-8 right-8 flex flex-wrap gap-4 justify-between items-end border-t border-white/20 pt-6 text-white uppercase">
                        <div>
                            <p className="text-xs opacity-50 mb-1">任务进度 (Progress)</p>
                            <p className="text-3xl font-mono">{(simProgress * 100).toFixed(1)}%</p>
                        </div>
                        <div className="text-center">
                            <p className="text-xs opacity-50 mb-1">当前阶段 (Phase)</p>
                            <p className="text-xl font-bold text-cyan-400">{phase}</p>
                        </div>
                        <div className="text-right hidden md:block">
                            <p className="text-xs opacity-50 mb-1">坐标 (Coordinates)</p>
                            <p className="text-lg font-mono text-slate-400">X: {Math.round(orionPos.x)} | Y: {Math.round(orionPos.y)}</p>
                        </div>
                    </div>
                </div>
            )}

            {/* Progress Bar for the whole 30s video */}
            <div className="absolute bottom-0 left-0 h-1 bg-cyan-500 transition-all duration-100" style={{ width: `${(frame / TOTAL_FRAMES) * 100}%` }} />
        </div>
    );
}