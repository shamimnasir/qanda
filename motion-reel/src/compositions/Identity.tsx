import React from 'react';
import {AbsoluteFill, Easing, interpolate, useCurrentFrame} from 'remotion';
import {Hud} from '../components/Hud';
import {COLORS, FONT_STACK} from '../theme';

export const IDENTITY_DURATION = 120;

// The wipe ends fully on signal, so the next section should open on this.
export const IDENTITY_END_BACKGROUND = COLORS.signal;

// Beat boundaries (frames).
const DIAL_START = 0;
const DIAL_END = 40;
const BURST_START = 40;
const BURST_END = 80;
const DIAL_FADE_END = 54;
const WIPE_START = 80;
const WIPE_END = IDENTITY_DURATION - 1;
const WORD_START = 84;

const SVG_SIZE = 720;
const C = SVG_SIZE / 2;

const DIAL_RADIUS = 180;
const NEEDLE_LENGTH = 130;

const RAY_COUNT = 12;
const RAY_LONG = 270;
const RAY_SHORT = 170;
const RAY_INNER = 46;
const RAY_WIDTH = 38;

const clamp = {
  extrapolateLeft: 'clamp',
  extrapolateRight: 'clamp',
} as const;

const Dial: React.FC<{frame: number}> = ({frame}) => {
  const angle = interpolate(frame, [DIAL_START, DIAL_END], [0, 270], {
    ...clamp,
    easing: Easing.out(Easing.back(1.7)),
  });
  const opacity = interpolate(frame, [BURST_START, DIAL_FADE_END], [1, 0], clamp);
  const scale = interpolate(frame, [BURST_START, DIAL_FADE_END], [1, 0.9], {
    ...clamp,
    easing: Easing.in(Easing.cubic),
  });

  if (opacity === 0) {
    return null;
  }

  return (
    <svg
      width={SVG_SIZE}
      height={SVG_SIZE}
      viewBox={`0 0 ${SVG_SIZE} ${SVG_SIZE}`}
      style={{position: 'absolute', opacity, transform: `scale(${scale})`}}
    >
      <circle cx={C} cy={C} r={DIAL_RADIUS} fill="none" stroke={COLORS.ink} strokeWidth={3} />
      <g transform={`rotate(${angle} ${C} ${C})`}>
        <line
          x1={C}
          y1={C}
          x2={C}
          y2={C - NEEDLE_LENGTH}
          stroke={COLORS.signal}
          strokeWidth={10}
          strokeLinecap="round"
        />
      </g>
      <circle cx={C} cy={C} r={10} fill={COLORS.signal} />
    </svg>
  );
};

const Starburst: React.FC<{frame: number}> = ({frame}) => {
  const scale = interpolate(frame, [BURST_START, BURST_END], [0, 1], {
    ...clamp,
    // Remotion's elastic already settles at 1 after overshooting (peak ~1.13).
    easing: Easing.elastic(1.2),
  });
  const rotation = interpolate(frame, [BURST_START, BURST_END], [0, 90], {
    ...clamp,
    easing: Easing.out(Easing.cubic),
  });

  if (frame < BURST_START) {
    return null;
  }

  return (
    <svg
      width={SVG_SIZE}
      height={SVG_SIZE}
      viewBox={`0 0 ${SVG_SIZE} ${SVG_SIZE}`}
      style={{
        position: 'absolute',
        transform: `rotate(${rotation}deg) scale(${Math.max(scale, 0)})`,
      }}
    >
      {Array.from({length: RAY_COUNT}, (_, i) => {
        const length = i % 2 === 0 ? RAY_LONG : RAY_SHORT;
        return (
          <line
            key={i}
            x1={C}
            y1={C - RAY_INNER}
            x2={C}
            y2={C - length}
            transform={`rotate(${(360 / RAY_COUNT) * i} ${C} ${C})`}
            stroke={COLORS.signal}
            strokeWidth={RAY_WIDTH}
            strokeLinecap="round"
          />
        );
      })}
    </svg>
  );
};

const Wipe: React.FC<{frame: number}> = ({frame}) => {
  // Right inset shrinks from 100% to 0%, revealing left to right.
  const remaining = interpolate(frame, [WIPE_START, WIPE_END], [100, 0], {
    ...clamp,
    easing: Easing.inOut(Easing.cubic),
  });
  const wordX = interpolate(frame, [WORD_START, WIPE_END], [-420, 0], {
    ...clamp,
    easing: Easing.out(Easing.cubic),
  });

  if (frame < WIPE_START) {
    return null;
  }

  return (
    <AbsoluteFill
      style={{
        backgroundColor: COLORS.signal,
        clipPath: `inset(0 ${remaining}% 0 0)`,
        alignItems: 'center',
        justifyContent: 'center',
      }}
    >
      <div
        style={{
          fontFamily: FONT_STACK,
          fontWeight: 900,
          fontSize: 400,
          lineHeight: 1,
          letterSpacing: '-0.04em',
          color: COLORS.ink,
          transform: `translateX(${wordX}px)`,
          whiteSpace: 'nowrap',
        }}
      >
        CLAUDE
      </div>
    </AbsoluteFill>
  );
};

export const Identity: React.FC = () => {
  const frame = useCurrentFrame();

  return (
    <AbsoluteFill style={{backgroundColor: COLORS.paper}}>
      <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center'}}>
        <Dial frame={frame} />
        <Starburst frame={frame} />
      </AbsoluteFill>
      <Wipe frame={frame} />
      <Hud section="01 IDENTITY" />
    </AbsoluteFill>
  );
};
