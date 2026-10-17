import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig} from 'remotion';
import {COLORS, FONT_STACK} from '../theme';

const INSET = 64;
const TICK = 28;

const pad = (n: number, len = 2) => String(n).padStart(len, '0');

// Shared overlay drawn on top of every section: section label,
// timecode and corner registration marks.
export const Hud: React.FC<{section: string; color?: string}> = ({
  section,
  color = COLORS.ink,
}) => {
  const frame = useCurrentFrame();
  const {fps, durationInFrames} = useVideoConfig();
  const seconds = Math.floor(frame / fps);
  const subFrame = frame % fps;

  const label: React.CSSProperties = {
    position: 'absolute',
    fontFamily: FONT_STACK,
    fontSize: 22,
    fontWeight: 600,
    letterSpacing: '0.18em',
    color,
  };

  const corner = (style: React.CSSProperties) => (
    <div
      style={{
        position: 'absolute',
        width: TICK,
        height: TICK,
        borderColor: color,
        borderStyle: 'solid',
        borderWidth: 0,
        ...style,
      }}
    />
  );

  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      {corner({top: INSET - 24, left: INSET - 24, borderTopWidth: 2, borderLeftWidth: 2})}
      {corner({top: INSET - 24, right: INSET - 24, borderTopWidth: 2, borderRightWidth: 2})}
      {corner({bottom: INSET - 24, left: INSET - 24, borderBottomWidth: 2, borderLeftWidth: 2})}
      {corner({bottom: INSET - 24, right: INSET - 24, borderBottomWidth: 2, borderRightWidth: 2})}
      <div style={{...label, top: INSET, left: INSET}}>{section}</div>
      <div
        style={{
          ...label,
          top: INSET,
          right: INSET,
          fontVariantNumeric: 'tabular-nums',
        }}
      >
        {`${pad(seconds)}:${pad(subFrame)} / ${pad(durationInFrames, 3)}F`}
      </div>
    </AbsoluteFill>
  );
};
