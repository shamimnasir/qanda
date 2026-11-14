import React from 'react';
import {AbsoluteFill, Easing, Img, interpolate, random, staticFile, useCurrentFrame} from 'remotion';
import type {Item} from './types';
import {Credit, Footage} from './Documentary';
import mapdata from './mapdata.json';
import {BODY, C, LOOK, MG_BG, TITLE} from './theme';

const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const ease = Easing.out(Easing.cubic);
type P = {it: Item; index: number};
// eslint-disable-next-line @typescript-eslint/no-explicit-any
const pr = (it: Item) => (it.props ?? {}) as Record<string, any>;

const BANGLA = /[\u0980-\u09FF]/;

const Snow: React.FC<{count?: number; seed?: string}> = ({count = 70, seed = 'snow'}) => {
  const f = useCurrentFrame();
  if (LOOK.motes === 'dust') {
    // Warm look: fewer, slower motes drifting upward.
    return (
      <AbsoluteFill>
        {Array.from({length: Math.round(count * 0.4)}).map((_, i) => {
          const x = random(`${seed}x${i}`) * 1920 + Math.sin((f + i * 40) / 90) * 30;
          const y = random(`${seed}y${i}`) * 1080 - ((f * (0.15 + random(`${seed}s${i}`) * 0.35)) % 1080);
          const r = 1.5 + random(`${seed}r${i}`) * 3;
          return (
            <div
              key={i}
              style={{position: 'absolute', left: x, top: (y + 1080) % 1080, width: r * 2, height: r * 2, borderRadius: r, background: 'rgba(255,214,170,0.22)'}}
            />
          );
        })}
      </AbsoluteFill>
    );
  }
  return (
    <AbsoluteFill>
      {Array.from({length: count}).map((_, i) => {
        const x0 = random(`${seed}x${i}`) * 1920;
        const y0 = random(`${seed}y${i}`) * 1150;
        const sp = 0.6 + random(`${seed}s${i}`) * 1.6;
        const r = 1.2 + random(`${seed}r${i}`) * 2.6;
        const y = ((y0 + f * sp) % 1150) - 40;
        const x = x0 + Math.sin((f + i * 30) / 40) * 18;
        return (
          <div
            key={i}
            style={{position: 'absolute', left: x, top: y, width: r * 2, height: r * 2, borderRadius: r, background: 'rgba(230,244,255,0.55)'}}
          />
        );
      })}
    </AbsoluteFill>
  );
};

const Label: React.FC<{text: string; at: number; x: number; y: number; size?: number; color?: string; align?: 'left' | 'center' | 'right'; weight?: number; font?: string}> = ({
  text, at, x, y, size = 56, color = 'white', align = 'left', weight = 600, font = TITLE,
}) => {
  const f = useCurrentFrame();
  const o = interpolate(f, [at, at + 10], [0, 1], clamp);
  const dy = interpolate(f, [at, at + 12], [18, 0], {...clamp, easing: ease});
  const tx = align === 'center' ? '-50%' : align === 'right' ? '-100%' : '0';
  return (
    <div
      style={{
        position: 'absolute', left: x, top: y, opacity: o, transform: `translate(${tx}, ${dy}px)`,
        fontFamily: font, fontWeight: weight, fontSize: size, letterSpacing: font === TITLE && !BANGLA.test(text) ? 3 : 0,
        color, textAlign: align, whiteSpace: 'pre', textShadow: '0 4px 24px rgba(0,0,0,0.6)',
      }}
    >
      {text}
    </div>
  );
};

const Footnote: React.FC<{text: string}> = ({text}) => (
  <div style={{position: 'absolute', right: 48, top: 40, fontFamily: BODY, fontSize: 22, color: 'rgba(214,236,255,0.6)'}}>{text}</div>
);

/* Thermometer falling to the target temperature. */
const Thermo: React.FC<P> = ({it}) => {
  const f = useCurrentFrame();
  const props = pr(it) as {to: number; from?: number; unit?: string; clock?: string};
  const p = interpolate(f, [4, it.dur * 0.55], [0, 1], {...clamp, easing: ease});
  const from = props.from ?? 20;
  const temp = from + (props.to - from) * p;
  const yOf = (t: number) => interpolate(t, [-70, 20], [800, 190]);
  const decimals = Number.isInteger(props.to) ? 0 : 1;
  const frost = interpolate(f, [it.dur * 0.3, it.dur], [0, 0.5], clamp);
  return (
    <AbsoluteFill style={{background: MG_BG}}>
      <Snow seed="thermo" />
      <svg width={1920} height={1080} style={{position: 'absolute'}}>
        <rect x={580} y={160} width={64} height={680} rx={32} fill="rgba(214,236,255,0.10)" stroke={C.ice} strokeWidth={4} />
        <circle cx={612} cy={880} r={62} fill={C.accent} stroke={C.ice} strokeWidth={4} />
        <rect x={596} y={yOf(temp)} width={32} height={880 - yOf(temp)} rx={16} fill={C.accent} />
        {[20, 0, -20, -40, -60].map((t) => (
          <g key={t}>
            <line x1={656} x2={690} y1={yOf(t)} y2={yOf(t)} stroke={C.ice} strokeWidth={3} />
            <text x={704} y={yOf(t) + 12} fill={C.ice} fontFamily={BODY} fontSize={32} opacity={0.75}>{t}</text>
          </g>
        ))}
      </svg>
      <div style={{position: 'absolute', left: 860, top: 330, fontFamily: TITLE, fontWeight: 700, fontSize: 250, color: 'white', letterSpacing: 2}}>
        {temp.toFixed(decimals)}
        <span style={{fontSize: 120, marginLeft: 16, color: C.accent}}>{props.unit ?? '°C'}</span>
      </div>
      {props.clock && <Label text={props.clock} at={2} x={872} y={250} size={64} color={C.accent} />}
      <AbsoluteFill style={{boxShadow: `inset 0 0 240px rgba(200,235,255,${frost})`}} />
    </AbsoluteFill>
  );
};

/* Title card over a photo or clip. props: {title, subtitle} */
const Title: React.FC<P> = ({it, index}) => {
  const f = useCurrentFrame();
  const spacing = BANGLA.test(pr(it).title ?? '') ? 0 : interpolate(f, [0, it.dur], [46, 20], {...clamp, easing: ease});
  const blur = interpolate(f, [0, 16], [14, 0], clamp);
  const o = interpolate(f, [0, 14], [0, 1], clamp);
  return (
    <AbsoluteFill>
      <Footage it={it} index={index} dim={0.45} />
      <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', flexDirection: 'column'}}>
        <div style={{fontFamily: TITLE, fontWeight: 700, fontSize: 210, color: 'white', letterSpacing: spacing, opacity: o, filter: `blur(${blur}px)`, textShadow: '0 10px 50px rgba(0,0,0,0.7)'}}>
          {pr(it).title}
        </div>
        <div style={{fontFamily: BODY, fontWeight: 500, fontSize: 44, color: C.ice, opacity: interpolate(f, [14, 30], [0, 1], clamp), marginTop: 6}}>
          {pr(it).subtitle}
        </div>
      </AbsoluteFill>
      {it.credit && <Credit text={it.credit} />}
    </AbsoluteFill>
  );
};

/* Route map from mapdata.json (built by build_map.py). props: {leg: 0}. Air legs draw an arc with a plane, road legs a line. */
const RouteMap: React.FC<P> = ({it}) => {
  const f = useCurrentFrame();
  const leg = mapdata.legs[pr(it).leg ?? 0] as {from: string; to: string; mode: string; label?: string; sub?: string; route: number[][];
    viewStart: number[]; viewEnd: number[]; fromXY: number[]; toXY: number[]};
  const z = interpolate(f, [0, it.dur], [0, 1], {...clamp, easing: Easing.inOut(Easing.quad)});
  const vb = leg.viewStart.map((v, i) => v + (leg.viewEnd[i] - v) * z);
  const k = vb[2] / 1920; // map units per screen pixel
  const prog = interpolate(f, [8, it.dur * 0.75], [0, 1], {...clamp, easing: Easing.inOut(Easing.cubic)});
  const [ax, ay] = leg.fromXY;
  const [bx, by] = leg.toXY;
  const air = leg.mode === 'air';
  const cx = (ax + bx) / 2;
  const cy = Math.min(ay, by) - Math.hypot(bx - ax, by - ay) * 0.28;
  const q = (tt: number) => [(1 - tt) ** 2 * ax + 2 * (1 - tt) * tt * cx + tt ** 2 * bx, (1 - tt) ** 2 * ay + 2 * (1 - tt) * tt * cy + tt ** 2 * by];
  const route = leg.route;
  const segs = route.length - 1;
  const iSeg = Math.min(segs - 1, Math.floor(prog * segs));
  const rem = prog * segs - iSeg;
  const head = prog >= 1 ? route[segs] : [route[iSeg][0] + (route[iSeg + 1][0] - route[iSeg][0]) * rem, route[iSeg][1] + (route[iSeg + 1][1] - route[iSeg][1]) * rem];
  const pts = air ? Array.from({length: 61}, (_, i) => q((i / 60) * prog)) : [...route.slice(0, iSeg + 1), head];
  const city = (name: string, x: number, y: number, show: number) => (
    <g opacity={interpolate(f, [show, show + 8], [0, 1], clamp)}>
      <circle cx={x} cy={y} r={9 * k} fill={C.warm} />
      <circle cx={x} cy={y} r={18 * k} fill="none" stroke={C.warm} strokeWidth={2.5 * k} />
      <text x={x + 24 * k} y={y - 18 * k} fill="white" fontFamily={TITLE} fontSize={44 * k} letterSpacing={2 * k}>{name.toUpperCase()}</text>
    </g>
  );
  const plane = q(prog);
  return (
    <AbsoluteFill style={{background: C.deep}}>
      <svg width={1920} height={1080} viewBox={vb.join(' ')} style={{position: 'absolute'}}>
        {mapdata.paths.map((p) => (
          <path key={p.name} d={p.d} fill={p.name === mapdata.highlight ? C.landHi : C.land} stroke="#4d7ea8" strokeWidth={1.2 * k} />
        ))}
        <polyline points={pts.map((p) => p.join(',')).join(' ')} fill="none" stroke={air ? C.accent : C.warm} strokeWidth={(air ? 5 : 6) * k}
          strokeDasharray={air ? `${14 * k} ${10 * k}` : undefined} strokeLinejoin="round" />
        {air && <circle cx={plane[0]} cy={plane[1]} r={12 * k} fill="white" />}
        {city(leg.from, ax, ay, 0)}
        {city(leg.to, bx, by, it.dur * 0.7)}
      </svg>
      {leg.label && <Label text={leg.label} at={air ? it.dur * 0.45 : 6} x={110} y={leg.sub ? 700 : 820} size={leg.sub ? 110 : 96} />}
      {leg.sub && <Label text={leg.sub} at={it.dur * 0.35} x={110} y={835} size={72} color={C.warm} />}
      <Footnote text={air ? 'Map: Natural Earth' : 'Route shown is approximate. Map: Natural Earth'} />
    </AbsoluteFill>
  );
};

/* Stopwatch running to N minutes. props: {minutes, label, alert} */
const Timer: React.FC<P> = ({it}) => {
  const f = useCurrentFrame();
  const p = interpolate(f, [4, it.dur * 0.7], [0, 1], {...clamp, easing: Easing.inOut(Easing.quad)});
  const secs = Math.round(p * (pr(it).minutes ?? 15) * 60);
  const mm = String(Math.floor(secs / 60)).padStart(2, '0');
  const ss = String(secs % 60).padStart(2, '0');
  const r = 300;
  const circ = 2 * Math.PI * r;
  const done = f > it.dur * 0.7;
  return (
    <AbsoluteFill style={{background: MG_BG}}>
      <Snow seed="timer" count={40} />
      <svg width={1920} height={1080} style={{position: 'absolute'}}>
        <circle cx={960} cy={500} r={r} fill="none" stroke="rgba(214,236,255,0.15)" strokeWidth={22} />
        <circle cx={960} cy={500} r={r} fill="none" stroke={done ? C.danger : C.accent} strokeWidth={22} strokeLinecap="round"
          strokeDasharray={`${circ * p} ${circ}`} transform="rotate(-90 960 500)" />
      </svg>
      <div style={{position: 'absolute', width: 1920, top: 395, textAlign: 'center', fontFamily: TITLE, fontWeight: 600, fontSize: 190, color: 'white'}}>
        {mm}:{ss}
      </div>
      <Label text={pr(it).label ?? 'MINUTES'} at={4} x={960} y={880} size={52} align="center" color={C.ice} />
      {done && pr(it).alert && <Label text={pr(it).alert} at={it.dur * 0.7} x={960} y={600} size={64} align="center" color={C.danger} />}
    </AbsoluteFill>
  );
};

/* Simplified biology: vessels narrow, cells freeze, tissue darkens. */
const Vessels: React.FC<P> = ({it}) => {
  const f = useCurrentFrame();
  const phase = (it.props as {phase: number}).phase;
  const p = interpolate(f, [0, it.dur], [0, 1], clamp);
  let body: React.ReactNode = null;
  if (phase === 1) {
    const gap = interpolate(p, [0.15, 0.85], [250, 70], {...clamp, easing: Easing.inOut(Easing.cubic)});
    const top = 540 - gap / 2;
    const speed = interpolate(p, [0, 1], [9, 2.5]);
    body = (
      <svg width={1920} height={1080} style={{position: 'absolute'}}>
        <defs>
          <linearGradient id="cold" x1="0" x2="1">
            <stop offset="0" stopColor={C.accent} stopOpacity={0.55 * p} />
            <stop offset="1" stopColor={C.accent} stopOpacity={0} />
          </linearGradient>
        </defs>
        <rect x={0} y={0} width={1920} height={1080} fill="url(#cold)" />
        <rect x={0} y={top - 40} width={1920} height={40} fill="#c25a5a" />
        <rect x={0} y={top + gap} width={1920} height={40} fill="#c25a5a" />
        <rect x={0} y={top} width={1920} height={gap} fill="rgba(120,20,30,0.35)" />
        {Array.from({length: 18}).map((_, i) => {
          const x = ((i * 130 + f * speed) % 2200) - 140;
          const y = 540 + Math.sin(i * 1.7) * (gap / 2 - 30);
          return <ellipse key={i} cx={x} cy={y} rx={Math.min(46, gap / 2.8)} ry={Math.min(26, gap / 4.5)} fill="#e0393f" />;
        })}
      </svg>
    );
  } else if (phase === 2) {
    body = (
      <svg width={1920} height={1080} style={{position: 'absolute'}}>
        {Array.from({length: 18}).map((_, i) => {
          const col = i % 6;
          const row = Math.floor(i / 6);
          const cx = 360 + col * 240;
          const cy = 380 + row * 210;
          const g = interpolate(p, [0.05 + (i % 7) * 0.04, 0.55 + (i % 5) * 0.05], [0, 1], clamp);
          const tear = interpolate(p, [0.55, 0.9], [0, 1], clamp);
          return (
            <g key={i}>
              <rect x={cx - 100} y={cy - 90} width={200} height={180} rx={56} fill="rgba(240,170,170,0.22)" stroke={tear > 0.3 && i % 3 === 0 ? C.danger : '#e3a0a0'} strokeWidth={4} />
              {Array.from({length: 6}).map((__, a) => {
                const ang = (a * Math.PI) / 3 + i;
                const len = 80 * g;
                return (
                  <g key={a}>
                    <line x1={cx} y1={cy} x2={cx + Math.cos(ang) * len} y2={cy + Math.sin(ang) * len} stroke={C.ice} strokeWidth={5} strokeLinecap="round" />
                    <line x1={cx + Math.cos(ang) * len * 0.55} y1={cy + Math.sin(ang) * len * 0.55}
                      x2={cx + Math.cos(ang + 0.6) * len * 0.8} y2={cy + Math.sin(ang + 0.6) * len * 0.8} stroke={C.ice} strokeWidth={3} />
                  </g>
                );
              })}
            </g>
          );
        })}
      </svg>
    );
  } else {
    const dark = interpolate(p, [0.1, 1], [0, 0.85], clamp);
    const mix = (a: number[], b: number[]) => `rgb(${a.map((v, i) => Math.round(v + (b[i] - v) * dark)).join(',')})`;
    body = (
      <svg width={1920} height={1080} style={{position: 'absolute'}}>
        <defs>
          <linearGradient id="spread" x1="0" x2="1">
            <stop offset="0" stopColor="#1b1b1f" stopOpacity={dark} />
            <stop offset={Math.max(0.01, dark)} stopColor="#1b1b1f" stopOpacity={dark * 0.8} />
            <stop offset={Math.min(1, dark + 0.2)} stopColor="#1b1b1f" stopOpacity={0} />
          </linearGradient>
        </defs>
        <rect x={160} y={330} width={1600} height={90} fill={mix([235, 170, 150], [70, 60, 66])} />
        <rect x={160} y={420} width={1600} height={200} fill={mix([215, 120, 115], [55, 40, 46])} />
        <rect x={160} y={620} width={1600} height={170} fill={mix([240, 210, 150], [90, 80, 70])} />
        <rect x={160} y={330} width={1600} height={460} fill="url(#spread)" />
        <text x={180} y={316} fill={C.ice} fontFamily={BODY} fontSize={28}>Skin</text>
        <text x={180} y={850} fill={C.ice} fontFamily={BODY} fontSize={28} opacity={0.7}>Simplified illustration</text>
      </svg>
    );
  }
  const labels: Record<number, [string, string?]> = {
    1: ['BLOOD VESSELS SQUEEZE SHUT'],
    2: ['WATER IN CELLS FREEZES', 'ICE CRYSTALS TEAR TISSUE'],
    3: ['SKIN TURNS BLACK', 'TISSUE MAY BE DYING'],
  };
  const [l1, l2] = pr(it).label ? [pr(it).label as string, pr(it).label2 as string | undefined] : labels[phase];
  return (
    <AbsoluteFill style={{background: MG_BG}}>
      {body}
      <Label text={l1} at={4} x={110} y={60} size={72} />
      {l2 && <Label text={l2} at={it.dur * 0.5} x={110} y={155} size={56} color={phase === 2 ? C.danger : C.ice} />}
      {phase !== 3 && <Footnote text="Simplified illustration" />}
    </AbsoluteFill>
  );
};

/* A count stacking up. props: {count, unit, value, note} */
const Layers: React.FC<P> = ({it}) => {
  const f = useCurrentFrame();
  const n = Math.round(interpolate(f, [4, it.dur * 0.55], [0, pr(it).count ?? 20], {...clamp, easing: ease}));
  const colors = ['#8b6a4f', '#a7a9ad', '#5d4a3c', '#c9b79c', '#6f7a86'];
  return (
    <AbsoluteFill style={{background: MG_BG}}>
      <svg width={1920} height={1080} style={{position: 'absolute'}}>
        {Array.from({length: n}).map((_, i) => (
          <rect key={i} x={1060 + (i % 2) * 8} y={900 - i * 34} width={560 - i * 6} height={28} rx={10} fill={colors[i % colors.length]} />
        ))}
      </svg>
      <div style={{position: 'absolute', left: 110, top: 300, fontFamily: TITLE, fontWeight: 700, fontSize: 240, color: 'white'}}>{n}</div>
      <Label text={pr(it).unit ?? ''} at={2} x={120} y={560} size={80} color={C.ice} />
      {pr(it).value && <Label text={pr(it).value} at={it.dur * 0.45} x={120} y={680} size={96} color={C.warm} />}
      {pr(it).note && <Label text={pr(it).note} at={it.dur * 0.6} x={122} y={810} size={36} font={BODY} weight={500} color={C.ice} />}
    </AbsoluteFill>
  );
};

/* Two values side by side; the right one counts. props: {left: {value, label}, right: {from, to, unit, label}} */
const Delta: React.FC<P> = ({it}) => {
  const f = useCurrentFrame();
  const split = interpolate(f, [0, 18], [1920, 960], {...clamp, easing: ease});
  const L = pr(it).left ?? {value: '', label: ''};
  const Rt = pr(it).right ?? {from: 0, to: 0, unit: '', label: ''};
  const out = interpolate(f, [12, it.dur * 0.6], [Rt.from, Rt.to], {...clamp, easing: ease});
  return (
    <AbsoluteFill style={{background: C.deep}}>
      <div style={{position: 'absolute', left: 0, top: 0, width: split, height: 1080, background: 'linear-gradient(135deg, #5a2a12, #2a140b)'}} />
      <div style={{position: 'absolute', left: split, top: 0, right: 0, height: 1080, background: `linear-gradient(135deg, ${C.navy}, ${C.deep})`}} />
      <div style={{position: 'absolute', left: split - 4, top: 0, width: 8, height: 1080, background: C.ice, opacity: 0.6}} />
      <Label text={L.value} at={0} x={480} y={360} size={190} align="center" color={C.warm} />
      <Label text={L.label} at={4} x={480} y={600} size={60} align="center" color="#ffd9b3" />
      <div style={{position: 'absolute', left: 1440, top: 360, transform: 'translateX(-50%)', fontFamily: TITLE, fontWeight: 600, fontSize: 190, color: C.accent, whiteSpace: 'nowrap', opacity: interpolate(f, [12, 20], [0, 1], clamp)}}>
        {Math.round(out)} {Rt.unit}
      </div>
      <Label text={Rt.label} at={16} x={1440} y={600} size={60} align="center" color={C.ice} />
    </AbsoluteFill>
  );
};

/* Ground cross-section showing deep permafrost. */
const Permafrost: React.FC<P> = ({it}) => {
  const f = useCurrentFrame();
  const pan = interpolate(f, [8, it.dur], [0, -170], {...clamp, easing: Easing.inOut(Easing.quad)});
  return (
    <AbsoluteFill style={{background: C.deep, overflow: 'hidden'}}>
      <svg width={1920} height={1500} style={{position: 'absolute', top: pan}}>
        <rect x={0} y={0} width={1920} height={380} fill="#0d2238" />
        <rect x={0} y={380} width={1920} height={24} fill="#e9f4ff" />
        <rect x={0} y={404} width={1920} height={60} fill="#5b4636" />
        <rect x={0} y={464} width={1920} height={1040} fill="#2f5876" />
        {Array.from({length: 26}).map((_, i) => (
          <line key={i} x1={0} x2={1920} y1={500 + i * 40} y2={500 + i * 40 + (i % 2 ? 14 : -10)} stroke="#4d7ea8" strokeWidth={2} opacity={0.5} />
        ))}
        <rect x={860} y={250} width={200} height={110} fill="#6b4b33" />
        <polygon points="840,250 960,180 1080,250" fill="#8a6446" />
        {[880, 950, 1020].map((x) => <rect key={x} x={x} y={360} width={18} height={60} fill="#6b4b33" />)}
        <line x1={1500} x2={1500} y1={480} y2={1440} stroke={C.ice} strokeWidth={5} />
        <polygon points="1484,1420 1516,1420 1500,1460" fill={C.ice} />
      </svg>
      <Label text={pr(it).title ?? 'PERMAFROST'} at={6} x={110} y={640} size={110} color="white" />
      <Label text={pr(it).sub ?? ''} at={16} x={114} y={790} size={44} font={BODY} weight={500} color={C.ice} />
    </AbsoluteFill>
  );
};

/* Cross-section of a town: hollow mines below, waste piles above. props: {show: below|above|both|water|collapse, title, sub, labels: [{text, at, x, y}]} */
const Strata: React.FC<P> = ({it}) => {
  const f = useCurrentFrame();
  const s = pr(it) as {show?: string; title?: string; sub?: string; labels?: {text: string; at?: number; x?: number; y?: number; color?: string}[]};
  const show = s.show ?? 'both';
  const G = 470;
  const tunnels: [number, number, number, number][] = [[140, 610, 420, 56], [620, 600, 360, 64], [1040, 620, 500, 58], [300, 730, 520, 62], [880, 750, 560, 56], [90, 860, 430, 54], [590, 880, 460, 60], [1120, 870, 620, 58], [260, 680, 44, 60], [760, 660, 40, 100], [1240, 680, 46, 80], [430, 790, 40, 90], [1010, 806, 44, 80], [760, 940, 400, 44]];
  const below = show !== 'above';
  const above = show !== 'below';
  const dig = (i: number) => (show === 'below' ? interpolate(f, [4 + i * 3, 14 + i * 3], [0, 1], clamp) : 1);
  const grow = show === 'above' ? interpolate(f, [4, 44], [0.05, 1], {...clamp, easing: ease}) : 1;
  const water = show === 'water' ? interpolate(f, [8, Math.max(30, it.dur - 8)], [1000, 590], clamp) : 2000;
  const fall = show === 'collapse' ? interpolate(f, [10, 34], [0, 1], {...clamp, easing: Easing.in(Easing.quad)}) : 0;
  const house = (x: number, k: number) => (
    <g key={k} transform={`translate(${x},${G - 54})`}>
      <rect x={0} y={16} width={70} height={38} fill={C.landHi} />
      <polygon points="-6,16 35,-10 76,16" fill={C.muted} />
    </g>
  );
  const pile = (cx: number, w: number, h: number, k: number) => (
    <polygon key={k} points={`${cx - w},${G} ${cx - w * 0.28},${G - h * grow} ${cx + w * 0.22},${G - h * 0.92 * grow} ${cx + w},${G}`} fill="#9a9c98" />
  );
  return (
    <AbsoluteFill style={{background: MG_BG, overflow: 'hidden'}}>
      <svg width={1920} height={1080} style={{position: 'absolute'}}>
        <defs>
          <clipPath id={`tun${it.id}`}>{tunnels.map(([x, y, w, h], i) => <rect key={i} x={x} y={y} width={w} height={h} rx={14} />)}</clipPath>
        </defs>
        <rect x={0} y={G} width={1920} height={610} fill="#3a3027" />
        <rect x={0} y={G} width={1920} height={18} fill="#5b4a39" />
        {Array.from({length: 11}).map((_, i) => <line key={i} x1={0} x2={1920} y1={G + 60 + i * 52} y2={G + 60 + i * 52 + (i % 2 ? 12 : -8)} stroke="#4b3e32" strokeWidth={2} opacity={0.7} />)}
        {above && pile(1500, 300, 260, 0)}
        {above && pile(1120, 170, 150, 1)}
        {[150, 260, 370, 500, 610].map((x, i) => (show === 'collapse' && i > 1 && i < 5 ? null : house(x, i)))}
        <g transform={`translate(780,${G - 190})`}>
          <rect x={12} y={40} width={6} height={150} fill={C.muted} /><rect x={62} y={40} width={6} height={150} fill={C.muted} />
          <ellipse cx={40} cy={30} rx={42} ry={30} fill={C.landHi} />
        </g>
        {below && tunnels.map(([x, y, w, h], i) => <rect key={i} x={x} y={y} width={w} height={h} rx={14} fill="#0b0d10" opacity={dig(i)} />)}
        {show === 'water' && <g clipPath={`url(#tun${it.id})`}><rect x={0} y={water} width={1920} height={1000} fill="#a8552f" opacity={0.9} /></g>}
        {show === 'collapse' && (
          <g>
            <polygon points={`350,${G} 720,${G} 660,${G + 150 + fall * 90} 410,${G + 150 + fall * 90}`} fill="#0b0d10" opacity={fall} />
            {[370, 500, 610].map((x, i) => <g key={i} transform={`translate(${(i - 1) * 18 * fall},${fall * 150}) rotate(${(i - 1) * 14 * fall} ${x + 35} ${G - 20})`} opacity={1 - fall * 0.85}>{house(x, 10 + i)}</g>)}
          </g>
        )}
      </svg>
      {s.title && <Label text={s.title} at={6} x={110} y={70} size={84} color="white" />}
      {s.sub && <Label text={s.sub} at={14} x={114} y={176} size={40} font={BODY} weight={500} color={C.ice} />}
      {(s.labels ?? []).map((l, i) => <Label key={i} text={l.text} at={l.at ?? 16 + i * 12} x={l.x ?? 110} y={l.y ?? 900} size={56} color={l.color ?? C.warm} />)}
    </AbsoluteFill>
  );
};

/* Cutaway of a house wall and its layers. */
const Wall: React.FC<P> = ({it}) => {
  const phase = (it.props as {phase: number}).phase;
  const f = useCurrentFrame();
  const glow = interpolate(f, [0, it.dur], [0.4, 0.8], clamp);
  const layer = (x: number, w: number, color: string, show: number) => (
    <rect x={x} y={180} width={w} height={600} fill={color} opacity={interpolate(f, [show, show + 10], [0, 1], clamp)} />
  );
  const labels1: [string, number][] = [['THICK WOODEN BEAMS', 4], ['LAYERS OF INSULATION', 0.45]];
  const labels2: [string, number][] = [['TRIPLE-GLAZED WINDOWS', 2], ['BASALT WOOL', 0.35], ['FOAM', 0.65]];
  const labels = (pr(it).labels as [string, number][]) ?? (phase === 1 ? labels1 : labels2);
  return (
    <AbsoluteFill style={{background: MG_BG}}>
      <svg width={1920} height={1080} style={{position: 'absolute'}}>
        <rect x={120} y={180} width={360} height={600} fill={`rgba(255,170,90,${glow * 0.35})`} />
        {layer(480, 90, '#7a5636', 0)}
        {layer(570, 90, '#d9c27a', phase === 1 ? it.dur * 0.45 : 0)}
        {layer(660, 60, '#bcd3e3', phase === 1 ? it.dur * 0.55 : 0)}
        {layer(720, 30, '#8f6a48', 0)}
        <rect x={750} y={180} width={260} height={600} fill="rgba(127,211,255,0.10)" />
        {phase === 2 && [0, 1, 2].map((i) => (
          <rect key={i} x={500 + i * 80} y={330} width={14} height={180} fill="rgba(214,236,255,0.9)" opacity={interpolate(f, [2 + i * 4, 12 + i * 4], [0, 1], clamp)} />
        ))}
        <rect x={120} y={780} width={890} height={40} fill="#5b4636" />
        {[180, 400, 620, 860].map((x) => <rect key={x} x={x} y={820} width={46} height={150} fill="#7a5636" />)}
        <rect x={0} y={950} width={1920} height={130} fill="#e9f4ff" opacity={0.85} />
        <text x={150} y={230} fill="#ffd9b3" fontFamily={BODY} fontSize={30}>{pr(it).inside ?? 'Warm inside'}</text>
        <text x={780} y={230} fill={C.ice} fontFamily={BODY} fontSize={30}>{pr(it).outside ?? 'Cold outside'}</text>
      </svg>
      {labels.map(([t, at], i) => (
        <Label key={t} text={t} at={at < 1 ? at * it.dur : at} x={1120} y={300 + i * 130} size={64} />
      ))}
    </AbsoluteFill>
  );
};

/* One boiler feeding the village; then the pipes freeze. */
const Boiler: React.FC<P> = ({it}) => {
  const f = useCurrentFrame();
  const freeze = interpolate(f, [it.dur * 0.18, it.dur * 0.45], [0, 1], clamp);
  const houses = [[300, 260], [300, 760], [1620, 260], [1620, 760]];
  const hot = [255, 150, 60];
  const cold = [127, 211, 255];
  const col = `rgb(${hot.map((v, i) => Math.round(v + (cold[i] - v) * freeze)).join(',')})`;
  const flow = f * 6 * (1 - freeze);
  return (
    <AbsoluteFill style={{background: MG_BG}}>
      <svg width={1920} height={1080} style={{position: 'absolute'}}>
        {houses.map(([x, y], i) => (
          <g key={i}>
            <polyline points={`960,520 ${x < 960 ? 700 : 1220},520 ${x < 960 ? 700 : 1220},${y} ${x},${y}`} fill="none" stroke={col} strokeWidth={16}
              strokeDasharray="40 22" strokeDashoffset={x < 960 ? flow : -flow} strokeLinejoin="round" />
            <rect x={x - 90} y={y - 70} width={180} height={140} fill="#3a2a20" />
            <polygon points={`${x - 110},${y - 70} ${x},${y - 150} ${x + 110},${y - 70}`} fill="#57402f" />
            <rect x={x - 30} y={y - 30} width={60} height={50} fill={`rgba(255,200,110,${1 - freeze * 0.9})`} />
          </g>
        ))}
        <rect x={860} y={420} width={200} height={220} rx={24} fill="#2b3a48" stroke={col} strokeWidth={6} />
        <circle cx={960} cy={560} r={40} fill={`rgba(255,120,40,${1 - freeze})`} />
        <rect x={930} y={300} width={60} height={120} fill="#2b3a48" />
      </svg>
      <Label text={pr(it).title ?? 'ONE BOILER'} at={0} x={960} y={60} size={60} align="center" color={C.warm} />
      <Label text={pr(it).line1 ?? 'PIPES FREEZE'} at={it.dur * 0.25} x={960} y={150} size={60} align="center" color={C.accent} />
      <Label text={pr(it).line2 ?? 'HOMES GO COLD'} at={it.dur * 0.45} x={960} y={240} size={52} align="center" color={C.ice} />
      <AbsoluteFill style={{boxShadow: `inset 0 0 260px rgba(200,235,255,${freeze * 0.35})`}} />
    </AbsoluteFill>
  );
};

/* Fact card. props: {kicker, title, value} */
const Rules: React.FC<P> = ({it}) => (
  <AbsoluteFill style={{background: MG_BG}}>
    <Snow seed="rules" count={40} />
    <Label text={pr(it).kicker ?? ''} at={0} x={960} y={250} size={64} align="center" color={C.accent} />
    <Label text={pr(it).title ?? ''} at={it.dur * 0.3} x={960} y={400} size={120} align="center" />
    <Label text={pr(it).value ?? ''} at={it.dur * 0.45} x={960} y={560} size={150} align="center" color={C.warm} />
  </AbsoluteFill>
);

/* A scale with a danger threshold and a pointer. props: {min, max, threshold, thresholdLabel, value, valueLabel, unit} */
const School: React.FC<P> = ({it}) => {
  const f = useCurrentFrame();
  const s = pr(it) as {min: number; max: number; threshold: number; thresholdLabel: string; value: number; valueLabel: string; unit: string};
  const xOf = (t: number) => interpolate(t, [s.min, s.max], [1660, 260]);
  const today = interpolate(f, [it.dur * 0.35, it.dur * 0.7], [s.max, s.value], {...clamp, easing: ease});
  return (
    <AbsoluteFill style={{background: MG_BG}}>
      <svg width={1920} height={1080} style={{position: 'absolute'}}>
        <rect x={260} y={520} width={1400} height={36} rx={18} fill="rgba(214,236,255,0.18)" />
        <rect x={xOf(s.threshold)} y={520} width={1660 - xOf(s.threshold)} height={36} fill="rgba(255,90,79,0.55)" />
        {Array.from({length: 5}, (_, i) => s.max + ((s.min - s.max) * i) / 4).map((t) => (
          <text key={t} x={xOf(t)} y={620} fill={C.ice} fontFamily={BODY} fontSize={34} textAnchor="middle">{t}</text>
        ))}
        <line x1={xOf(s.threshold)} x2={xOf(s.threshold)} y1={470} y2={580} stroke={C.danger} strokeWidth={6} />
        <polygon points={`${xOf(today) - 22},470 ${xOf(today) + 22},470 ${xOf(today)},510`} fill="white" />
      </svg>
      <Label text={s.thresholdLabel} at={2} x={960} y={250} size={72} align="center" color={C.danger} />
      <Label text={`${s.valueLabel} ${Math.round(today)} ${s.unit}`} at={it.dur * 0.35} x={xOf(today)} y={360} size={72} align="center" />
    </AbsoluteFill>
  );
};

/* Quoted line on its own card. */
const Quote: React.FC<P> = ({it}) => {
  const lines = (it.lines ?? []) as [string, string][];
  return (
    <AbsoluteFill style={{background: MG_BG, justifyContent: 'center', alignItems: 'center'}}>
      <Snow seed={it.id} count={60} />
      <div style={{display: 'flex', flexDirection: 'column', gap: 50, alignItems: 'center', maxWidth: 1500}}>
        {lines.map(([who, what], i) => (
          <QuoteLine key={i} who={who} what={what} at={i * Math.round(it.dur / (lines.length + 0.6))} />
        ))}
      </div>
    </AbsoluteFill>
  );
};
const QuoteLine: React.FC<{who: string; what: string; at: number}> = ({who, what, at}) => {
  const f = useCurrentFrame();
  const o = interpolate(f, [at + 4, at + 14], [0, 1], clamp);
  return (
    <div style={{opacity: o, textAlign: 'center'}}>
      <div style={{fontFamily: TITLE, fontSize: 40, letterSpacing: /[\u0980-\u09FF]/.test(who) ? 0 : 8, color: C.accent}}>{who}</div>
      <div style={{fontFamily: BODY, fontWeight: 500, fontStyle: 'italic', fontSize: 76, color: 'white', marginTop: 12}}>“{what}”</div>
    </div>
  );
};

/* Closing card over a photo or clip. props: {title, lines: [..]} */
const EndCard: React.FC<P> = ({it, index}) => (
  <AbsoluteFill>
    <Footage it={it} index={index} dim={0.5} />
    <Label text={pr(it).title ?? ''} at={6} x={960} y={330} size={170} align="center" />
    {((pr(it).lines ?? []) as string[]).map((l, i) => (
      <Label key={i} text={l} at={20 + i * 20} x={960} y={560 + i * 100} size={i === 0 ? 56 : 48} align="center" font={BODY} weight={500} color={i === 0 ? C.ice : 'white'} />
    ))}
    {it.credit && <Credit text={it.credit} />}
  </AbsoluteFill>
);

const Credits: React.FC<P> = ({it}) => {
  const f = useCurrentFrame();
  const lines = (pr(it).lines ?? []) as string[];
  const out = interpolate(f, [it.dur - 25, it.dur], [1, 0], clamp);
  return (
    <AbsoluteFill style={{background: 'black', justifyContent: 'center', alignItems: 'center', opacity: out}}>
      <div style={{display: 'flex', flexDirection: 'column', gap: 26, maxWidth: 1500}}>
        {lines.map((c, i) => (
          <div key={i} style={{fontFamily: BODY, fontSize: 34, color: i === lines.length - 1 ? C.accent : C.ice, textAlign: 'center',
            opacity: interpolate(f, [4 + i * 5, 14 + i * 5], [0, 1], clamp)}}>
            {c}
          </div>
        ))}
      </div>
    </AbsoluteFill>
  );
};

/* One big number over a photo, clip or plain background. props: {value, label, sub} */
const Stat: React.FC<P> = ({it, index}) => (
  <AbsoluteFill style={{background: MG_BG}}>
    {it.src && <Footage it={it} index={index} dim={0.55} />}
    <Label text={pr(it).value ?? ''} at={2} x={960} y={300} size={230} align="center" />
    <Label text={pr(it).label ?? ''} at={10} x={960} y={600} size={72} align="center" color={C.accent} />
    {pr(it).sub && <Label text={pr(it).sub} at={22} x={960} y={720} size={44} align="center" font={BODY} weight={500} color={C.ice} />}
  </AbsoluteFill>
);

const fmt = (n: number) => Math.round(n).toLocaleString('en-US');

/* A number counting from one value to another. props: {from, to, label, sub, fromLabel} */
const Count: React.FC<P> = ({it, index}) => {
  const f = useCurrentFrame();
  const s = pr(it) as {from: number; to: number; label?: string; sub?: string; fromLabel?: string};
  const n = interpolate(f, [8, it.dur * 0.7], [s.from, s.to], {...clamp, easing: Easing.inOut(Easing.cubic)});
  return (
    <AbsoluteFill style={{background: MG_BG}}>
      {it.src && <Footage it={it} index={index} dim={0.6} />}
      <Snow seed={it.id} count={50} />
      {s.fromLabel && <Label text={s.fromLabel} at={0} x={960} y={230} size={52} align="center" font={BODY} weight={500} color={C.ice} />}
      <div style={{position: 'absolute', width: 1920, top: 330, textAlign: 'center', fontFamily: TITLE, fontWeight: 700, fontSize: 230, color: 'white',
        textShadow: '0 10px 40px rgba(0,0,0,0.6)'}}>{fmt(n)}</div>
      {s.label && <Label text={s.label} at={10} x={960} y={640} size={72} align="center" color={C.accent} />}
      {s.sub && <Label text={s.sub} at={it.dur * 0.7} x={960} y={760} size={44} align="center" font={BODY} weight={500} color={C.ice} />}
    </AbsoluteFill>
  );
};

/* Two bars, before and after. props: {left: {label, value, text}, right: {label, value, text}, title, note} (values 0 to 100) */
const Bars: React.FC<P> = ({it}) => {
  const f = useCurrentFrame();
  const s = pr(it) as {title?: string; note?: string; left: {label: string; value: number; text: string}; right: {label: string; value: number; text: string}};
  const grow = (at: number) => interpolate(f, [at, at + 22], [0, 1], {...clamp, easing: ease});
  const bar = (x: number, b: {label: string; value: number; text: string}, at: number, color: string) => {
    const h = 460 * (b.value / 100) * grow(at);
    return (
      <>
        <div style={{position: 'absolute', left: x, top: 770 - h, width: 300, height: h, background: color, borderRadius: '14px 14px 0 0'}} />
        <Label text={b.text} at={at + 12} x={x + 150} y={770 - 460 * (b.value / 100) - 100} size={72} align="center" />
        <Label text={b.label} at={at} x={x + 150} y={790} size={56} align="center" color={C.ice} />
      </>
    );
  };
  return (
    <AbsoluteFill style={{background: MG_BG}}>
      {s.title && <Label text={s.title} at={0} x={960} y={90} size={60} align="center" color={C.accent} />}
      {bar(520, s.left, 6, C.muted)}
      {bar(1100, s.right, it.dur * 0.35, C.warm)}
      {s.note && <Footnote text={s.note} />}
    </AbsoluteFill>
  );
};

/* A rank falling down a ladder of places. props: {steps: [{year, rank}], of, title} */
const Rank: React.FC<P> = ({it}) => {
  const f = useCurrentFrame();
  const s = pr(it) as {steps: {year: string; rank: number; at?: number}[]; of: number; title?: string};
  const yOf = (r: number) => interpolate(r, [1, s.of], [230, 900]);
  const per = (it.dur * 0.75) / s.steps.length;
  // Each step appears at its own "at" (seconds into the shot, to match the narration), else evenly spaced.
  const starts = s.steps.map((st, i) => (st.at !== undefined ? st.at * 30 : i * per));
  const k = Math.max(0, starts.filter((x) => x <= f).length - 1);
  const t = interpolate(f - starts[k], [0, 18], [0, 1], {...clamp, easing: Easing.inOut(Easing.cubic)});
  const prev = s.steps[Math.max(0, k - 1)].rank;
  const cur = k === 0 ? s.steps[0].rank : prev + (s.steps[k].rank - prev) * t;
  return (
    <AbsoluteFill style={{background: MG_BG}}>
      {s.title && <Label text={s.title} at={0} x={960} y={90} size={60} align="center" color={C.accent} />}
      <svg width={1920} height={1080} style={{position: 'absolute'}}>
        <line x1={1180} x2={1180} y1={yOf(1)} y2={yOf(s.of)} stroke={C.ice} strokeOpacity={0.25} strokeWidth={6} />
        {[1, Math.round(s.of / 2), s.of].map((r) => (
          <text key={r} x={1220} y={yOf(r) + 14} fill={C.ice} fontFamily={BODY} fontSize={34}>{r === 1 ? '1st' : r === s.of ? `${r}th (last)` : `${r}th`}</text>
        ))}
        <circle cx={1180} cy={yOf(cur)} r={26} fill={C.accent} />
      </svg>
      {s.steps.slice(0, k + 1).map((st, i) => (
        <Label key={i} text={`${st.year}:  ${ordinal(st.rank)}`} at={starts[i] + 4} x={330} y={300 + i * 150} size={84} color={i === k ? 'white' : `${C.ice}8c`} />
      ))}
    </AbsoluteFill>
  );
};
const ordinal = (n: number) => `${n}${n % 100 >= 11 && n % 100 <= 13 ? 'th' : ['th', 'st', 'nd', 'rd'][n % 10] ?? 'th'}`;

/* A bowl filling up and stopping at a percent. props: {percent, label, sub} */
const Bowl: React.FC<P> = ({it}) => {
  const f = useCurrentFrame();
  const s = pr(it) as {percent: number; label?: string; sub?: string};
  const p = interpolate(f, [6, it.dur * 0.6], [0, s.percent / 100], {...clamp, easing: Easing.out(Easing.quad)});
  const top = 300, bottom = 680, h = (bottom - top) * p;
  return (
    <AbsoluteFill style={{background: MG_BG}}>
      <Snow seed={it.id} count={40} />
      <svg width={1920} height={1080} style={{position: 'absolute'}}>
        <defs>
          <clipPath id={`bowl${it.id}`}><path d={`M640 ${top} Q960 ${bottom + 250} 1280 ${top} Z`} /></clipPath>
        </defs>
        <rect x={600} y={bottom + 60 - h * 1.15} width={720} height={h * 1.15 + 40} fill={C.warm} opacity={0.85} clipPath={`url(#bowl${it.id})`} />
        <path d={`M640 ${top} Q960 ${bottom + 250} 1280 ${top}`} fill="none" stroke={C.ice} strokeWidth={10} strokeLinecap="round" />
        <line x1={600} x2={1320} y1={top} y2={top} stroke={C.ice} strokeWidth={10} strokeLinecap="round" />
      </svg>
      <div style={{position: 'absolute', width: 1920, top: 70, textAlign: 'center', fontFamily: TITLE, fontWeight: 700, fontSize: 170, color: 'white'}}>
        {Math.round(p * 100)}%
      </div>
      {s.label && <Label text={s.label} at={it.dur * 0.55} x={960} y={740} size={64} align="center" color={C.accent} />}
      {s.sub && <Label text={s.sub} at={it.dur * 0.65} x={960} y={830} size={40} align="center" font={BODY} weight={500} color={C.ice} />}
    </AbsoluteFill>
  );
};

/* A viewfinder over footage: corners, blinking REC, a running timecode. props: {label} */
const Rec: React.FC<P> = ({it, index}) => {
  const f = useCurrentFrame();
  const secs = Math.floor(f / 30);
  const tc = `01:58:${String(10 + secs).padStart(2, '0')}`;
  const corner = (x: number, y: number, dx: number, dy: number) => (
    <polyline key={`${x}${y}`} points={`${x + dx * 90},${y} ${x},${y} ${x},${y + dy * 90}`} fill="none" stroke="white" strokeWidth={6} opacity={0.85} />
  );
  return (
    <AbsoluteFill>
      <Footage it={it} index={index} />
      <svg width={1920} height={1080} style={{position: 'absolute'}}>
        {corner(70, 70, 1, 1)}{corner(1850, 70, -1, 1)}{corner(70, 1010, 1, -1)}{corner(1850, 1010, -1, -1)}
        <circle cx={150} cy={130} r={17} fill={C.danger} opacity={Math.floor(f / 15) % 2 ? 0.25 : 1} />
      </svg>
      <div style={{position: 'absolute', left: 185, top: 100, fontFamily: BODY, fontWeight: 700, fontSize: 44, color: 'white'}}>REC</div>
      <div style={{position: 'absolute', right: 130, top: 100, fontFamily: BODY, fontWeight: 600, fontSize: 44, color: 'white'}}>{tc}</div>
      {pr(it).label && <Label text={pr(it).label} at={6} x={960} y={110} size={48} align="center" color={C.warm} />}
    </AbsoluteFill>
  );
};

/* One word struck through, then the word that replaces it. props: {from, to, sub} */
const Flip: React.FC<P> = ({it}) => {
  const f = useCurrentFrame();
  const s = pr(it) as {from: string; to: string; sub?: string};
  const strikeAt = it.dur * 0.2;
  const toAt = it.dur * 0.32;
  const strike = interpolate(f, [strikeAt, strikeAt + 8], [0, 1], {...clamp, easing: ease});
  const fromO = interpolate(f, [toAt - 4, toAt + 6], [1, 0.28], clamp);
  return (
    <AbsoluteFill style={{background: MG_BG}}>
      <Snow seed={it.id} count={40} />
      <div style={{position: 'absolute', width: 1920, top: 170, textAlign: 'center', opacity: fromO}}>
        <span style={{position: 'relative', display: 'inline-block', fontFamily: TITLE, fontWeight: 700, fontSize: 170, color: C.ice}}>
          {s.from}
          <span style={{position: 'absolute', left: -20, top: '54%', height: 14, width: `calc((100% + 40px) * ${strike})`, background: C.danger}} />
        </span>
      </div>
      <Label text={s.to} at={toAt} x={960} y={380} size={240} align="center" color={C.warm} />
      {s.sub && <Label text={s.sub} at={it.dur * 0.5} x={960} y={700} size={68} align="center" color="white" />}
    </AbsoluteFill>
  );
};

/* A ship drifting off a straight course and correcting back, again and again. props: {target, wind, note} */
const Course: React.FC<P> = ({it}) => {
  const f = useCurrentFrame();
  const s = pr(it) as {target?: string; wind?: string; note?: string};
  const p = interpolate(f, [6, it.dur - 8], [0, 1], clamp);
  const yAt = (u: number) => 540 + Math.sin(u * Math.PI * 6) * 120 * (1 - u * 0.55);
  const xAt = (u: number) => 170 + u * 1480;
  const pts = Array.from({length: 121}, (_, i) => (i / 120) * p).map((u) => `${xAt(u)},${yAt(u)}`).join(' ');
  const angle = (Math.atan2(yAt(p + 0.004) - yAt(p), xAt(p + 0.004) - xAt(p)) * 180) / Math.PI;
  return (
    <AbsoluteFill style={{background: MG_BG}}>
      <Snow seed={it.id} count={30} />
      <svg width={1920} height={1080} style={{position: 'absolute'}}>
        <line x1={170} y1={540} x2={1650} y2={540} stroke={C.ice} strokeWidth={4} strokeDasharray="14 18" opacity={0.55} />
        <polyline points={pts} fill="none" stroke={C.warm} strokeWidth={8} strokeLinecap="round" strokeLinejoin="round" />
        <g transform={`translate(${xAt(p)},${yAt(p)}) rotate(${angle})`}>
          <polygon points="34,0 -24,-20 -14,0 -24,20" fill="white" />
        </g>
        <circle cx={1700} cy={540} r={20} fill="none" stroke={C.accent} strokeWidth={6} />
        <circle cx={1700} cy={540} r={7} fill={C.accent} />
      </svg>
      {s.target && <Label text={s.target} at={2} x={1700} y={590} size={46} align="center" color={C.accent} />}
      {s.wind && <Label text={`${s.wind} >>>`} at={it.dur * 0.1} x={170} y={210} size={52} color={C.ice} />}
      {s.note && <Label text={s.note} at={it.dur * 0.45} x={960} y={110} size={72} align="center" />}
    </AbsoluteFill>
  );
};

/* Stacked rows that appear one by one. props: {title, steps: [{k, v}]} */
const Steps: React.FC<P> = ({it}) => {
  const s = pr(it) as {title?: string; steps: {k: string; v: string}[]};
  const n = s.steps.length;
  const top = 540 - (n * 190) / 2;
  return (
    <AbsoluteFill style={{background: MG_BG}}>
      <Snow seed={it.id} count={30} />
      {s.title && <Label text={s.title} at={0} x={960} y={90} size={60} align="center" color={C.accent} />}
      {s.steps.map((r, i) => (
        <React.Fragment key={r.k}>
          <Label text={r.k} at={it.dur * (0.04 + (i * 0.8) / n)} x={880} y={top + i * 190 - 30} size={96} align="right" color={C.ice} />
          <Label text={r.v} at={it.dur * (0.08 + (i * 0.8) / n)} x={950} y={top + i * 190 - 30} size={110} color={C.warm} />
        </React.Fragment>
      ))}
    </AbsoluteFill>
  );
};

/* A phone alarm banner holding one question. props: {kicker, text} */
const Alert: React.FC<P> = ({it}) => {
  const f = useCurrentFrame();
  const s = pr(it) as {kicker?: string; text: string};
  const y = interpolate(f, [0, 12], [-80, 0], {...clamp, easing: ease});
  const o = interpolate(f, [0, 8], [0, 1], clamp);
  const shake = f < 30 ? Math.sin(f * 1.6) * 3 : 0;
  return (
    <AbsoluteFill style={{background: MG_BG}}>
      <div style={{position: 'absolute', left: 260, right: 260, top: 300, padding: '44px 60px', borderRadius: 40, opacity: o, transform: `translate(${shake}px, ${y}px)`,
        background: 'rgba(240,244,250,0.96)', boxShadow: '0 30px 90px rgba(0,0,0,0.6)'}}>
        <div style={{fontFamily: BODY, fontWeight: 700, fontSize: 36, color: '#b3362c'}}>{s.kicker}</div>
        <div style={{fontFamily: BODY, fontWeight: 700, fontSize: 76, lineHeight: 1.25, color: '#10151d', marginTop: 16}}>{s.text}</div>
      </div>
    </AbsoluteFill>
  );
};

/* Values along one scale, revealed in turn. props: {title, max, note, points: [{value, text, at, main}]}; at = fraction of the shot */
const Range: React.FC<P> = ({it}) => {
  const f = useCurrentFrame();
  const s = pr(it) as {title?: string; note?: string; max: number; points: {value: number; text: string; at: number; main?: boolean}[]};
  const xOf = (v: number) => 180 + (v / s.max) * 1560;
  return (
    <AbsoluteFill style={{background: MG_BG}}>
      {s.title && <Label text={s.title} at={0} x={960} y={130} size={68} align="center" color={C.accent} />}
      <svg width={1920} height={1080} style={{position: 'absolute'}}>
        <rect x={180} y={540} width={1560} height={22} rx={11} fill="rgba(228,233,240,0.2)" />
        {s.points.map((p) => {
          const o = interpolate(f, [p.at * it.dur, p.at * it.dur + 8], [0, 1], clamp);
          return <g key={p.value} opacity={o}>
            <line x1={xOf(p.value)} x2={xOf(p.value)} y1={490} y2={612} stroke={p.main ? C.warm : 'white'} strokeWidth={p.main ? 10 : 6} />
            {p.main && <rect x={180} y={540} width={xOf(p.value) - 180} height={22} rx={11} fill={C.warm} />}
          </g>;
        })}
      </svg>
      {s.points.map((p) => (
        <Label key={p.value} text={p.text} at={p.at * it.dur} x={Math.min(xOf(p.value), 1540)} y={p.main ? 340 : 640} size={p.main ? 120 : 76} align="center" color={p.main ? C.warm : 'white'} />
      ))}
      {s.note && <Label text={s.note} at={it.dur * 0.3} x={960} y={790} size={34} align="center" font={BODY} weight={500} color={C.ice} />}
    </AbsoluteFill>
  );
};

/* A small portrait photo beside a name, for images too small to fill the frame. props: {name, sub} */
const Portrait: React.FC<P> = ({it}) => {
  const f = useCurrentFrame();
  const zoom = interpolate(f, [0, it.dur], [1, 1.05]);
  return (
    <AbsoluteFill style={{background: MG_BG}}>
      <div style={{position: 'absolute', left: 170, top: 150, width: 640, height: 720, overflow: 'hidden', borderRadius: 12, boxShadow: '0 30px 80px rgba(0,0,0,0.6)'}}>
        {it.src && <Img src={staticFile(it.src)} style={{width: '100%', height: '100%', objectFit: 'cover', filter: 'grayscale(1) contrast(1.05)', transform: `scale(${zoom})`}} />}
      </div>
      <Label text={pr(it).name ?? ''} at={6} x={900} y={370} size={116} />
      <Label text={pr(it).sub ?? ''} at={14} x={904} y={530} size={52} font={BODY} weight={500} color={C.ice} />
      {it.credit && <Credit text={it.credit} />}
    </AbsoluteFill>
  );
};

export const Graphic: React.FC<P> = (p) => {
  if (p.it.kind === 'quote') return <Quote {...p} />;
  switch (p.it.mg) {
    case 'thermo': return <Thermo {...p} />;
    case 'title': return <Title {...p} />;
    case 'map': return <RouteMap {...p} />;
    case 'timer': return <Timer {...p} />;
    case 'vessels': return <Vessels {...p} />;
    case 'layers': case 'stack': return <Layers {...p} />;
    case 'delta': case 'compare': return <Delta {...p} />;
    case 'permafrost': return <Permafrost {...p} />;
    case 'wall': return <Wall {...p} />;
    case 'boiler': return <Boiler {...p} />;
    case 'rules': case 'card': return <Rules {...p} />;
    case 'school': case 'scale': return <School {...p} />;
    case 'stat': return <Stat {...p} />;
    case 'strata': return <Strata {...p} />;
    case 'portrait': return <Portrait {...p} />;
    case 'rec': return <Rec {...p} />;
    case 'flip': return <Flip {...p} />;
    case 'course': return <Course {...p} />;
    case 'steps': return <Steps {...p} />;
    case 'alert': return <Alert {...p} />;
    case 'range': return <Range {...p} />;
    case 'endcard': return <EndCard {...p} />;
    case 'credits': return <Credits {...p} />;
    case 'count': return <Count {...p} />;
    case 'bars': return <Bars {...p} />;
    case 'rank': return <Rank {...p} />;
    case 'bowl': return <Bowl {...p} />;
    default: return <AbsoluteFill style={{background: MG_BG}} />;
  }
};
