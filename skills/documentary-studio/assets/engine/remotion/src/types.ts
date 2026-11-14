// Shapes of the JSON files the Python pipeline writes (timeline*.json, short*.json).
export type Item = {
  id: string;
  kind: string;
  ch: string;
  desc: string;
  from: number;
  dur: number;
  overlay?: string | null;
  hard?: boolean;
  hold?: boolean;
  opener?: boolean; // inside the hook: text eases in
  punch?: boolean; // the hook's turn: one soft impact
  tone?: string;
  mg?: string | null;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  props?: Record<string, any>;
  lines?: string[][] | null;
  src?: string;
  srcType?: string;
  credit?: string;
};
export type Timeline = {
  fps: number;
  durationInFrames: number;
  vo: {from: number; voStart: number; voEnd: number}[];
  items: Item[];
  captions: {from: number; dur: number; text: string}[];
  opener_end?: number | null;
};
export type ShortPlan = {
  durationInFrames: number;
  segments: {name: string; filmFrom: number; shortFrom: number; dur: number}[];
  header?: {title?: string; sub?: string};
};
