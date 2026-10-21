import {AbsoluteFill, Easing, Sequence, interpolate, useCurrentFrame} from 'remotion';
import {C, FPS, SANS, SERIF} from './theme';
import type {Cue, Word} from './types';

type Register = 'lower' | 'kicker' | 'hero';

/** Beats that stop being subtitles and become typography. */
const REGISTER: Record<number, Register> = {6: 'kicker', 7: 'hero'};

/**
 * Placement is by first line, not by bottom edge: the block grows downward as
 * the next line arrives, so an earlier line never jumps upward mid-sentence.
 */
const LAYOUT = {
  lower: {top: 1286, size: 46, lineHeight: 1.30, family: SANS, weight: 600, letter: '-0.006em'},
  hero: {top: 1202, size: 60, lineHeight: 1.18, family: SERIF, weight: 600, letter: '0.002em'},
  kicker: {top: 1230, size: 15, lineHeight: 1.4, family: SANS, weight: 600, letter: '0.34em'},
} as const;

/**
 * The line is revealed as a unit (a subtitle never looks half-built), and the
 * word being spoken is tinted — karaoke, but quiet: no scale, no reflow.
 */
const WordSpan: React.FC<{word: Word; localFrame: number; register: Register}> = ({
  word,
  localFrame,
  register,
}) => {
  const start = Math.round(word.from * FPS);
  const end = Math.round(word.to * FPS);
  const speaking = localFrame >= start && localFrame <= end + 2;
  const hero = register === 'hero';
  const warm = speaking || word.e;
  return (
    <span
      style={{
        display: 'inline-block',
        color: warm ? (hero ? C.ember : C.warm) : undefined,
        fontWeight: word.e && !hero ? 700 : undefined,
        textShadow: warm && !hero ? '0 0 22px rgba(220,131,82,0.38)' : undefined,
        transition: 'none',
      }}
    >
      {word.t}
    </span>
  );
};

const Line: React.FC<{cue: Cue; register: Register; localFrame: number; fade: number; base: number}> = ({
  cue,
  register,
  localFrame,
  fade,
  base,
}) => {
  const L = LAYOUT[register];
  const k = register === 'kicker';
  const rise = interpolate(localFrame, [base, base + 7], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.out(Easing.cubic),
  });
  return (
    <div
      style={{
        fontFamily: L.family,
        fontSize: k ? 16 : L.size,
        fontWeight: L.weight,
        lineHeight: L.lineHeight,
        letterSpacing: k ? '0.34em' : L.letter,
        color: k ? C.mist : C.paper,
        textAlign: 'center',
        whiteSpace: 'nowrap',
        opacity: fade * (k ? 0.9 : rise),
        textShadow: k ? 'none' : '0 2px 20px rgba(0,0,0,0.66), 0 1px 3px rgba(0,0,0,0.5)',
        textTransform: k ? 'uppercase' : undefined,
        transform: `translateY(${((1 - rise) * 10).toFixed(2)}px)`,
      }}
    >
      {cue.words.map((w, i) => (
        <span key={`${w.t}-${i}`}>
          <WordSpan word={w} localFrame={localFrame} register={register} />
          {i < cue.words.length - 1 ? ' ' : ''}
        </span>
      ))}
    </div>
  );
};

const Block: React.FC<{cues: Cue[]; from: number; to: number; register: Register}> = ({
  cues,
  from,
  to,
  register,
}) => {
  const frame = useCurrentFrame();
  const local = frame + Math.round(from * FPS);
  const dur = Math.round((to - from) * FPS);
  const fade = interpolate(frame, [Math.max(0, dur - 6), dur], [1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const L = LAYOUT[register];
  return (
    <AbsoluteFill style={{opacity: fade}}>
      <div
        style={{
          position: 'absolute',
          left: 56,
          right: 56,
          top: L.top,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
        }}
      >
        {cues.map((c) => (
          <Line
            key={c.key}
            cue={c}
            register={register}
            localFrame={local}
            fade={1}
            base={Math.round(c.from * FPS) - Math.round(from * FPS)}
          />
        ))}
      </div>
    </AbsoluteFill>
  );
};

export const Captions: React.FC<{cues: Cue[]}> = ({cues}) => {
  const byVo = new Map<number, Cue[]>();
  cues.forEach((c) => byVo.set(c.vo, [...(byVo.get(c.vo) ?? []), c]));
  const blocks = [...byVo.entries()]
    .map(([vo, list]) => {
      const sorted = [...list].sort((a, b) => a.from - b.from);
      return {
        vo,
        cues: sorted,
        from: sorted[0].from - 0.05,
        to: sorted[sorted.length - 1].to + (vo === 10 ? 0.12 : 0.30),
        register: REGISTER[vo] ?? ('lower' as Register),
      };
    })
    .sort((a, b) => a.from - b.from);

  return (
    <>
      {blocks.map((b) => {
        const from = Math.round(b.from * FPS);
        const duration = Math.max(3, Math.round((b.to - b.from) * FPS));
        return (
          <Sequence key={b.vo} from={from} durationInFrames={duration} name={`sub-${b.vo}`}>
            <Block cues={b.cues} from={b.from} to={b.to} register={b.register} />
          </Sequence>
        );
      })}
    </>
  );
};
