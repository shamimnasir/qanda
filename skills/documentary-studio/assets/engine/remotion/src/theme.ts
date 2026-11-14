import {continueRender, delayRender, staticFile} from 'remotion';

import look from './look.json';

// Film looks, picked with "look" in project.json ("cold" is the default, "warm" was made for the Japan film, "dusk" is a grey-blue look with no snow, for inner stories that turn warm in the "Close" chapter).
const LOOKS = {
  cold: {
    C: {deep: '#06121f', navy: '#12304d', ice: '#d6ecff', accent: '#7fd3ff', warm: '#ffb36b', danger: '#ff5a4f', land: '#1a3350', landHi: '#24496d', muted: '#3a6a93'},
    grade: 'rgba(30,80,140,0.34)',
    filter: 'saturate(0.68) contrast(1.1) brightness(0.88)',
    captionBg: 'rgba(4,12,22,0.42)',
    motes: 'snow',
  },
  dusk: {
    C: {deep: '#0a0e15', navy: '#1b2533', ice: '#e4e9f0', accent: '#8fb9d9', warm: '#f6b26b', danger: '#ff5a4f', land: '#1f2a38', landHi: '#33475c', muted: '#5a7186'},
    grade: 'rgba(40,62,92,0.28)',
    filter: 'saturate(0.6) contrast(1.1) brightness(0.86)',
    captionBg: 'rgba(6,9,14,0.45)',
    motes: 'dust',
  },
  warm: {
    C: {deep: '#100d12', navy: '#2b2028', ice: '#f3ebe1', accent: '#ff6f61', warm: '#f6c177', danger: '#ff4f45', land: '#2d2a33', landHi: '#6b3a3f', muted: '#8a5a5f'},
    grade: 'rgba(255,170,120,0.10)',
    filter: 'saturate(0.9) contrast(1.06) brightness(0.92)',
    captionBg: 'rgba(12,8,10,0.45)',
    motes: 'dust',
  },
};
export const LOOK = LOOKS[(look as {look: string}).look as keyof typeof LOOKS] ?? LOOKS.cold;
export const C = LOOK.C;
export const TITLE = 'Oswald, "Noto Sans Bengali", sans-serif';
export const BODY = 'Inter, "Noto Sans Bengali", sans-serif';
export const MG_BG = `radial-gradient(ellipse at 50% 40%, ${C.navy} 0%, ${C.deep} 72%)`;

// Load the two OFL fonts before any frame renders.
const handle = delayRender('Loading fonts');
Promise.all(
  [
    new FontFace('Oswald', `url(${staticFile('Oswald.ttf')})`, {weight: '200 700'}),
    new FontFace('Inter', `url(${staticFile('Inter.ttf')})`, {weight: '100 900'}),
    new FontFace('Noto Sans Bengali', `url(${staticFile('NotoSansBengali.ttf')})`, {weight: '100 900'}),
  ].map((f) => f.load().then((loaded) => document.fonts.add(loaded))),
).then(() => continueRender(handle));
