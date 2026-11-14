import React from 'react';
import {AbsoluteFill, Audio, interpolate, Sequence, staticFile, useCurrentFrame} from 'remotion';
import {FilmLayer, Vertical} from './Documentary';
import type {ShortPlan, Timeline} from './types';
import {BODY, C, TITLE} from './theme';

const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;

const Header: React.FC<{title?: string; sub?: string}> = ({title, sub}) => {
  const f = useCurrentFrame();
  const o = interpolate(f, [0, 140, 160], [1, 1, 0], clamp);   // visible from frame 0: the first frame is the hook
  return (
    <div style={{position: 'absolute', top: 210, width: 1080, textAlign: 'center', opacity: o}}>
      <div style={{fontFamily: TITLE, fontWeight: 700, fontSize: 92, color: 'white', letterSpacing: 3, textShadow: '0 6px 30px rgba(0,0,0,0.8)'}}>{title}</div>
      <div style={{fontFamily: BODY, fontWeight: 600, fontSize: 40, color: C.ice, marginTop: 6, textShadow: '0 4px 20px rgba(0,0,0,0.8)'}}>
        {sub}
      </div>
    </div>
  );
};

// Vertical cut: each segment shows the film from its own start frame.
export const Short: React.FC<{tl: Timeline; short: ShortPlan; audio: string}> = ({tl, short, audio}) => (
  <Vertical.Provider value>
    <AbsoluteFill style={{backgroundColor: C.deep}}>
      {short.segments.map((s) => (
        <Sequence key={s.name} from={s.shortFrom} durationInFrames={s.dur} name={s.name}>
          <Sequence from={-s.filmFrom}>
            <FilmLayer tl={tl} />
          </Sequence>
        </Sequence>
      ))}
      {short.header?.title && <Header title={short.header.title} sub={short.header.sub} />}
      <Audio src={staticFile(audio)} />
    </AbsoluteFill>
  </Vertical.Provider>
);
