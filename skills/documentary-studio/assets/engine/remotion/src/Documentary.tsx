import React from 'react';
import {
  AbsoluteFill,
  Audio,
  Easing,
  Img,
  interpolate,
  OffthreadVideo,
  Sequence,
  staticFile,
  useCurrentFrame,
} from 'remotion';
import {BODY, C, LOOK, MG_BG, TITLE} from './theme';
import {Graphic} from './graphics';

import type {Item, Timeline} from './types';
export type {Item, Timeline};

const OVERLAP = 8; // frames each shot runs past its cut, so the next one can cross-fade over it
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;

// True inside the vertical Short: footage is center-cropped, 16:9 graphics are scaled into a band, captions move up.
export const Vertical = React.createContext(false);

const Grade: React.FC<{warm: boolean}> = ({warm}) => (
  <>
    <AbsoluteFill
      style={{
        background: warm ? 'rgba(255,150,60,0.22)' : LOOK.grade,
        mixBlendMode: 'soft-light',
      }}
    />
    <AbsoluteFill
      style={{background: 'radial-gradient(ellipse at center, transparent 52%, rgba(0,0,0,0.6) 100%)'}}
    />
  </>
);

export const Footage: React.FC<{it: Item; index: number; dim?: number}> = ({it, index, dim = 0}) => {
  const f = useCurrentFrame();
  const total = it.dur + OVERLAP;
  const isImage = it.srcType === 'image';
  const [s0, s1] = isImage ? [1.04, 1.13] : [1.0, 1.06];
  const scale = interpolate(f, [0, total], [s0, s1], clamp);
  const dir = index % 2 === 0 ? 1 : -1;
  const tx = interpolate(f, [0, total], [0, isImage ? 34 * dir : 14 * dir], clamp);
  const warm = it.ch === 'Close';
  const filter = warm
    ? 'saturate(0.95) contrast(1.06) brightness(0.95)'
    : LOOK.filter;
  const media = {width: '100%', height: '100%', objectFit: 'cover' as const};
  // Not downloaded yet: show a labelled placeholder so stills still work before the media step.
  if (!it.src) {
    return (
      <AbsoluteFill style={{backgroundColor: '#111', justifyContent: 'center', alignItems: 'center', color: '#666', fontSize: 40}}>
        {`missing media: ${it.id}`}
      </AbsoluteFill>
    );
  }
  return (
    <AbsoluteFill style={{backgroundColor: 'black', overflow: 'hidden'}}>
      <AbsoluteFill style={{transform: `scale(${scale}) translateX(${tx}px)`, filter}}>
        {isImage ? (
          <Img src={staticFile(it.src as string)} style={media} />
        ) : (
          <OffthreadVideo src={staticFile(it.src as string)} muted style={media} />
        )}
      </AbsoluteFill>
      <Grade warm={warm} />
      {dim > 0 && <AbsoluteFill style={{backgroundColor: `rgba(0,0,0,${dim})`}} />}
    </AbsoluteFill>
  );
};

// The hook's turn: one soft impact on the shot marked "hit". The other hook shots keep their slow push.
const Punch: React.FC<{it: Item; children: React.ReactNode}> = ({it, children}) => {
  const f = useCurrentFrame();
  const enter = interpolate(f, [0, 8], [0, 1], {...clamp, easing: Easing.out(Easing.cubic)});
  const a = f > 7 ? 0 : 6 * (1 - f / 8) ** 2;
  const scale = 1.02 + 0.05 * enter + interpolate(f, [0, it.dur], [0, 0.03], clamp);
  const blur = 5 * (1 - enter);
  return (
    <AbsoluteFill style={{overflow: 'hidden'}}>
      <AbsoluteFill
        style={{
          transform: `translate(${a * Math.sin(f * 2.4)}px, ${a * Math.cos(f * 3.1)}px) scale(${scale})`,
          filter: blur < 0.2 ? undefined : `blur(${blur.toFixed(1)}px)`,
        }}
      >
        {children}
      </AbsoluteFill>
      <AbsoluteFill style={{background: '#fff4e1', opacity: interpolate(f, [0, 5], [0.2, 0], clamp), mixBlendMode: 'screen'}} />
    </AbsoluteFill>
  );
};

const OverlayText: React.FC<{text: string; it: Item}> = ({text, it}) => {
  const f = useCurrentFrame();
  const vertical = React.useContext(Vertical);
  const hard = it.hard;
  const o = hard ? 1 : interpolate(f, [6, 16], [0, 1], clamp);
  const y = hard ? 0 : interpolate(f, [6, 18], [24, 0], clamp);
  const punch = !!it.punch;
  const eased = !!it.opener && !punch;
  const slam = punch ? interpolate(f, [0, 4, 8], [1.2, 0.985, 1], clamp) : 1;
  const bar = interpolate(f, [2, 10], [0, 100], {...clamp, easing: Easing.out(Easing.cubic)});
  return (
    <div
      style={{
        position: 'absolute',
        left: vertical ? 60 : 110,
        bottom: vertical ? 760 : 220,
        opacity: punch ? interpolate(f, [0, 2], [0, 1], clamp) : eased ? interpolate(f, [0, 5], [0, 1], clamp) : o,
        transform: punch ? `scale(${slam})` : eased ? `translateY(${interpolate(f, [0, 8], [12, 0], clamp)}px)` : `translateY(${y}px)`,
        transformOrigin: 'left bottom',
        filter: punch ? `blur(${interpolate(f, [0, 3], [4, 0], clamp)}px)` : undefined,
        fontFamily: TITLE,
        fontWeight: 600,
        whiteSpace: 'pre-line',
        fontSize: vertical ? 84 : 104,
        letterSpacing: 4,
        color: 'white',
        textShadow: '0 6px 30px rgba(0,0,0,0.75)',
      }}
    >
      {text}
      {punch && <div style={{width: `${bar}%`, height: vertical ? 9 : 11, marginTop: 10, background: '#f6b26b', boxShadow: '0 3px 14px rgba(0,0,0,0.6)'}} />}
    </div>
  );
};

export const Credit: React.FC<{text: string}> = ({text}) => (
  <div
    style={{
      position: 'absolute',
      left: 48,
      top: 40,
      fontFamily: BODY,
      fontSize: 22,
      fontWeight: 500,
      color: 'rgba(255,255,255,0.82)',
      textShadow: '0 2px 8px rgba(0,0,0,0.9)',
    }}
  >
    {text}
  </div>
);

// Color arc: a shot's "tone" in the shotlist. Applied to the picture, not to the text or credits on top.
const TONES: Record<string, string> = {
  gray: 'saturate(0.25) contrast(1.05)',
  cool: 'saturate(0.75) hue-rotate(8deg) brightness(0.95)',
  night: 'saturate(0.6) brightness(0.72) contrast(1.08)',
  warm: 'saturate(1.1) sepia(0.14) brightness(1.03)',
  vivid: 'saturate(1.3) brightness(1.06)',
};

const Shot: React.FC<{it: Item; index: number; last: boolean}> = ({it, index, last}) => {
  const f = useCurrentFrame();
  const fade = it.kind === 'quote' ? 10 : it.kind === 'mg' ? 5 : 7;
  const opacity = index === 0 || it.hard ? 1 : interpolate(f, [0, fade], [0, 1], clamp);
  const vertical = React.useContext(Vertical);
  const outro = last ? interpolate(f, [it.dur - 30, it.dur], [1, 0], clamp) : 1;
  let body = it.kind === 'mg' || it.kind === 'quote' ? <Graphic it={it} index={index} /> : <Footage it={it} index={index} />;
  if (vertical && it.kind === 'mg') {
    // 16:9 graphic scaled to 75% and centered; its outer edges (mostly empty background) fall off the sides.
    const s = 0.75;
    body = (
      <AbsoluteFill style={{background: MG_BG}}>
        <div style={{position: 'absolute', left: (1080 - 1920 * s) / 2, top: (1920 - 1080 * s) / 2, width: 1920, height: 1080, overflow: 'hidden', transform: `scale(${s})`, transformOrigin: 'top left'}}>
          {body}
        </div>
      </AbsoluteFill>
    );
  }
  const toned = it.tone && TONES[it.tone] ? <AbsoluteFill style={{filter: TONES[it.tone]}}>{body}</AbsoluteFill> : body;
  return (
    <AbsoluteFill style={{opacity: opacity * outro}}>
      {it.punch ? <Punch it={it}>{toned}</Punch> : toned}
      {it.overlay && <OverlayText text={it.overlay} it={it} />}
      {it.credit && it.kind !== 'mg' && <Credit text={it.credit} />}
    </AbsoluteFill>
  );
};

const Caption: React.FC<{text: string; dur: number}> = ({text, dur}) => {
  const f = useCurrentFrame();
  const vertical = React.useContext(Vertical);
  const o = interpolate(f, [0, 3, dur - 2, dur], [0, 1, 1, 0], clamp);
  return (
    <AbsoluteFill style={{justifyContent: 'flex-end', alignItems: 'center', paddingBottom: vertical ? 520 : 70}}>
      <div
        style={{
          opacity: o,
          maxWidth: vertical ? 940 : 1500,
          textAlign: 'center',
          fontFamily: BODY,
          fontWeight: 650,
          fontSize: vertical ? 66 : 50,
          lineHeight: 1.25,
          color: 'white',
          padding: '8px 22px',
          borderRadius: 12,
          background: LOOK.captionBg,
          textShadow: '0 2px 10px rgba(0,0,0,0.85)',
        }}
      >
        {text}
      </div>
    </AbsoluteFill>
  );
};

// Every shot and caption of the film, without audio. The Short reuses it through offset sequences.
export const FilmLayer: React.FC<{tl: Timeline}> = ({tl}) => {
  const items = tl.items;
  return (
    <AbsoluteFill style={{backgroundColor: C.deep}}>
      {items.map((it, i) => {
        const last = i === items.length - 1;
        return (
          <Sequence key={it.id} from={it.from} durationInFrames={it.dur + (last ? 0 : OVERLAP)} name={`${it.id} ${it.desc}`}>
            <Shot it={it} index={i} last={last} />
          </Sequence>
        );
      })}
      {tl.captions.map((c, i) => (
        <Sequence key={`cap${i}`} from={c.from} durationInFrames={c.dur} name={`cap ${c.text}`} layout="none">
          <Caption text={c.text} dur={c.dur} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};

export const Documentary: React.FC<{tl: Timeline; audio: string}> = ({tl, audio}) => (
  <AbsoluteFill>
    <FilmLayer tl={tl} />
    <Audio src={staticFile(audio)} />
  </AbsoluteFill>
);
