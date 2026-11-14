import React from 'react';
import {Composition} from 'remotion';
import {Documentary} from './Documentary';
import {Short} from './Short';
import type {ShortPlan, Timeline} from './types';
import tlEn from './timeline.json';
import tlBn from './timeline_bn.json';
import shortEn from './short.json';
import shortBn from './short_bn.json';

// One film and one Short per language. The pipeline overwrites these JSON files; placeholders keep unused languages valid.
const versions: {id: string; tl: Timeline; short: ShortPlan; suffix: string}[] = [
  {id: 'EN', tl: tlEn as unknown as Timeline, short: shortEn as unknown as ShortPlan, suffix: ''},
  {id: 'BN', tl: tlBn as unknown as Timeline, short: shortBn as unknown as ShortPlan, suffix: '_bn'},
];

export const RemotionRoot: React.FC = () => (
  <>
    {versions.map((v) => (
      <React.Fragment key={v.id}>
        <Composition id={`Film${v.id}`} component={Documentary} durationInFrames={Math.max(1, v.tl.durationInFrames)} fps={v.tl.fps}
          width={1920} height={1080} defaultProps={{tl: v.tl, audio: `final_mix${v.suffix}.wav`}} />
        <Composition id={`Short${v.id}`} component={Short} durationInFrames={Math.max(1, v.short.durationInFrames)} fps={v.tl.fps}
          width={1080} height={1920} defaultProps={{tl: v.tl, short: v.short, audio: `short_mix${v.suffix}.wav`}} />
      </React.Fragment>
    ))}
  </>
);
