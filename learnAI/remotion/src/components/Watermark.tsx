import React from 'react';
import { COLORS, interFamily } from '../styles';

export const Watermark: React.FC = () => {
  return (
    <div
      style={{
        position: 'absolute',
        top: 40,
        right: 40,
        fontFamily: interFamily,
        fontSize: 18,
        color: COLORS.textDim,
        zIndex: 1000,
        pointerEvents: 'none',
        letterSpacing: 1,
        textShadow: '0 0 10px rgba(0,0,0,0.5)',
      }}
    >
      张侃制作 © made by Kai
    </div>
  );
};
