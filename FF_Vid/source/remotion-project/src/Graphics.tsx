import {AbsoluteFill, Easing, interpolate, useCurrentFrame} from 'remotion';
import {C, EASE, FPS, SANS, SERIF} from './theme';

/** progress 0→1 between two local times, eased out. */
const P = (t: number, start: number, dur: number, ease = EASE.out): number =>
  interpolate(t, [start, start + dur], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: ease,
  });

const useT = (): number => useCurrentFrame() / FPS;

const label = (size = 14, color = C.mist, spacing = '0.30em'): React.CSSProperties => ({
  fontFamily: SANS,
  fontSize: size,
  fontWeight: 500,
  letterSpacing: spacing,
  textTransform: 'uppercase',
  color,
  lineHeight: 1,
});

/* ---------------------------------------------------------------- 01 · AGE MARK */
export const AgeMark: React.FC = () => {
  const t = useT();
  const line = P(t, 0.0, 0.55);
  const num = P(t, 0.06, 0.55);
  const lab = P(t, 0.34, 0.5);
  const out = interpolate(t, [2.62, 3.05], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{opacity: out}}>
      <div style={{position: 'absolute', left: 76, top: 196, display: 'flex', alignItems: 'flex-end', gap: 18}}>
        <div
          style={{
            width: 1,
            height: 132,
            background: 'linear-gradient(180deg, rgba(245,239,228,0) 0%, rgba(245,239,228,0.55) 40%, rgba(233,184,136,0.9) 100%)',
            transform: `scaleY(${line.toFixed(3)})`,
            transformOrigin: 'bottom',
          }}
        />
        <div style={{display: 'flex', flexDirection: 'column', gap: 4}}>
          <div style={label(14, C.warm, '0.44em')}>Age</div>
          <div
            style={{
              fontFamily: SERIF,
              fontSize: 124,
              fontWeight: 500,
              lineHeight: 0.86,
              color: C.paper,
              opacity: num,
              transform: `translateY(${(1 - num) * 16}px)`,
              textShadow: '0 6px 30px rgba(0,0,0,0.55)',
              letterSpacing: '-0.01em',
            }}
          >
            52
          </div>
          <div style={{...label(12.5, 'rgba(245,239,228,0.66)', '0.28em'), opacity: lab, marginTop: 14}}>not afraid of alone</div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

/* ------------------------------------------------------------------ 02 · TWO PATHS */
export const TwoPaths: React.FC = () => {
  const t = useT();
  const a = P(t, 0.25, 0.75, EASE.soft);
  const b = P(t, 0.55, 0.95, EASE.soft);
  const end = P(t, 1.45, 0.45);
  const W = 700;
  return (
    <AbsoluteFill>
      <div style={{position: 'absolute', left: 76, top: 1024, width: W + 130}}>
        {[
          {y: 0, name: 'What she knew', color: 'rgba(245,239,228,0.34)', p: a, dot: false},
          {y: 74, name: 'What she risked', color: C.ember, p: b, dot: true},
        ].map((row) => (
          <div key={row.name} style={{display: 'flex', alignItems: 'center', height: 40, marginTop: row.y ? 34 : 0}}>
            <div style={{...label(13, row.name.startsWith('What she risked') ? C.ember : C.paperDim, '0.28em'), width: 214, opacity: 0.55 + row.p * 0.45}}>
              {row.name}
            </div>
            <div style={{position: 'relative', flex: 1, height: 12}}>
              <div
                style={{
                  position: 'absolute',
                  top: 5,
                  left: 0,
                  height: row.dot ? 2.2 : 1.2,
                  width: `${row.p * 100}%`,
                  background: row.color,
                }}
              />
              {row.dot && (
                <div
                  style={{
                    position: 'absolute',
                    top: 5 - 3.2,
                    left: `calc(${row.p * 100}% - 4px)`,
                    width: 8,
                    height: 8,
                    borderRadius: 4,
                    background: C.ember,
                    opacity: end * 0.9 + 0.1,
                    boxShadow: '0 0 18px rgba(220,131,82,0.55)',
                  }}
                />
              )}
            </div>
          </div>
        ))}
      </div>
    </AbsoluteFill>
  );
};

/* -------------------------------------------------------------- 03 · MESSAGE CARD */
const MESSAGE = 'Would you like to get dinner this Friday?';

export const MessageCard: React.FC = () => {
  const t = useT();
  const enter = P(t, 0.0, 0.5);
  const typing = t < 1.30;
  const out = interpolate(t, [4.02, 4.42], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const words = MESSAGE.split(' ');
  return (
    <AbsoluteFill style={{opacity: out}}>
      <div
        style={{
          position: 'absolute',
          left: 64,
          top: 1052,
          width: 600,
          padding: '18px 22px 22px',
          borderRadius: 26,
          background: 'linear-gradient(160deg, rgba(20,25,32,0.80) 0%, rgba(11,14,19,0.74) 100%)',
          border: '1px solid rgba(245,239,228,0.14)',
          boxShadow: '0 24px 60px rgba(0,0,0,0.55), inset 0 1px 0 rgba(255,255,255,0.06)',
          backdropFilter: 'blur(16px)',
          opacity: enter,
          transform: `translateY(${(1 - enter) * -18}px)`,
        }}
      >
        <div style={{display: 'flex', alignItems: 'center', gap: 10, marginBottom: 16}}>
          <div style={{width: 7, height: 7, borderRadius: 4, background: C.ember, boxShadow: '0 0 12px rgba(220,131,82,0.8)'}} />
          <div style={{...label(11.5, C.mist, '0.30em')}}>Message</div>
          <div style={{flex: 1}} />
          <div style={{fontFamily: SANS, fontSize: 12, color: C.paperDim, letterSpacing: '0.02em'}}>6:42 PM</div>
        </div>
        <div style={{height: 1, background: C.hairSoft, marginBottom: 16}} />
        {typing ? (
          <div style={{display: 'flex', gap: 7, alignItems: 'center', height: 44}}>
            {[0, 1, 2].map((i) => {
              const ph = Math.max(0, Math.sin((t * 6.5 - i * 0.7) * Math.PI * 0.5));
              return (
                <div
                  key={i}
                  style={{
                    width: 7,
                    height: 7,
                    borderRadius: 4,
                    background: C.paperSoft,
                    opacity: 0.25 + ph * 0.55,
                  }}
                />
              );
            })}
          </div>
        ) : (
          <div
            style={{
              fontFamily: SANS,
              fontSize: 30,
              fontWeight: 500,
              lineHeight: 1.36,
              color: C.paper,
              letterSpacing: '-0.005em',
            }}
          >
            {words.map((w, i) => {
              const p = P(t, 1.32 + i * 0.075, 0.3);
              return (
                <span
                  key={`${w}-${i}`}
                  style={{display: 'inline-block', opacity: p, transform: `translateY(${(1 - p) * 8}px)`, marginRight: '0.26em'}}
                >
                  {w}
                </span>
              );
            })}
          </div>
        )}
      </div>
    </AbsoluteFill>
  );
};

/* ---------------------------------------------------------- 04 · HESITATION GAUGE */
export const HesitationGauge: React.FC = () => {
  const t = useT();
  const rows = [
    {name: 'Yes', color: C.warm},
    {name: 'Not yet', color: C.paper},
    {name: 'No', color: C.cool},
  ];
  // the cursor drifts toward "no", stops, then retreats
  const move = interpolate(t, [0.55, 1.9, 2.75, 3.5], [1, 2, 2, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: EASE.inOut,
  });
  const enter = P(t, 0.0, 0.45);
  return (
    <AbsoluteFill style={{opacity: enter}}>
      <div style={{position: 'absolute', left: 76, top: 1032, width: 560}}>
        {rows.map((row, i) => {
          const active = 1 - Math.min(1, Math.abs(move - i));
          return (
            <div key={row.name} style={{display: 'flex', alignItems: 'center', height: 62}}>
              <div style={{...label(13.5, row.color, '0.30em'), width: 126, opacity: 0.34 + active * 0.6}}>{row.name}</div>
              <div style={{position: 'relative', flex: 1, height: 1}}>
                <div style={{position: 'absolute', inset: 0, background: 'rgba(245,239,228,0.18)'}} />
                <div
                  style={{
                    position: 'absolute',
                    left: 0,
                    top: 0,
                    height: 1,
                    width: `${(0.18 + active * 0.52) * 100}%`,
                    background: i === 1 ? C.paper : row.color,
                    opacity: 0.25 + active * 0.6,
                  }}
                />
              </div>
              <div style={{width: 74}} />
            </div>
          );
        })}
        <div
          style={{
            position: 'absolute',
            left: 300,
            top: 62 * move + 4,
            width: 2,
            height: 46,
            background: `linear-gradient(180deg, rgba(220,131,82,0) 0%, ${C.ember} 40%, ${C.ember} 100%)`,
            boxShadow: '0 0 16px rgba(220,131,82,0.5)',
          }}
        />
        <div
          style={{
            position: 'absolute',
            left: 303,
            top: 62 * move + 50,
            ...label(11, C.ember, '0.26em'),
            opacity: 0.75,
          }}
        >
          nearly
        </div>
      </div>
    </AbsoluteFill>
  );
};

/* ---------------------------------------------------------------- 05 · THEN / NOW */
/** A ledger, not a caption: two columns on a dark plate, so it holds up over
 *  the window reflection without stealing the frame. */
export const ThenNow: React.FC = () => {
  const t = useT();
  const plate = P(t, 0.18, 0.65);
  const l = P(t, 0.42, 0.6);
  const r = P(t, 0.9, 0.6);
  const out = interpolate(t, [3.72, 4.12], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{opacity: out}}>
      <div
        style={{
          position: 'absolute',
          left: 60,
          right: 60,
          top: 972,
          height: 244,
          borderRadius: 16,
          background: 'linear-gradient(165deg, rgba(10,13,18,0.78) 0%, rgba(8,10,14,0.66) 100%)',
          border: '1px solid rgba(245,239,228,0.10)',
          boxShadow: '0 22px 50px rgba(0,0,0,0.42)',
          opacity: plate,
          transform: `translateY(${(1 - plate) * 12}px)`,
        }}
      />
      <div
        style={{
          position: 'absolute',
          left: 120,
          top: 1032,
          width: 348,
          opacity: l,
          transform: `translateX(${(1 - l) * -14}px)`,
          textAlign: 'right',
        }}
      >
        <div style={{...label(12, C.mist, '0.36em'), marginBottom: 12}}>Then</div>
        <div style={{fontFamily: SERIF, fontSize: 46, fontWeight: 600, color: 'rgba(245,239,228,0.72)', lineHeight: 1.04}}>
          someone else&rsquo;s
          <br />
          choice
        </div>
      </div>
      <div
        style={{
          position: 'absolute',
          left: 540,
          top: 1012,
          width: 1,
          height: 166,
          background: 'linear-gradient(180deg, rgba(245,239,228,0) 0%, rgba(245,239,228,0.28) 30%, rgba(245,239,228,0.28) 70%, rgba(245,239,228,0) 100%)',
          transform: `scaleY(${plate.toFixed(3)})`,
        }}
      />
      <div
        style={{
          position: 'absolute',
          left: 612,
          top: 1032,
          width: 348,
          opacity: r,
          transform: `translateX(${(1 - r) * 14}px)`,
        }}
      >
        <div style={{...label(12, C.ember, '0.36em'), marginBottom: 12}}>Now</div>
        <div style={{fontFamily: SERIF, fontSize: 46, fontWeight: 600, color: C.paper, lineHeight: 1.04}}>
          her own
          <br />
          judgement
        </div>
      </div>
    </AbsoluteFill>
  );
};

/* ----------------------------------------------------- 06 · CHAPTER MARKER */
/**
 * The turning point is marked, not illustrated: a margin rule that draws itself
 * down the left edge, with the chapter named in the gutter. The frame stays on
 * her face — the graphic is furniture, not scenery.
 */
export const ChapterMarker: React.FC = () => {
  const t = useT();
  const draw = P(t, 0.15, 1.25, EASE.soft);
  const label_ = P(t, 0.95, 0.7);
  const dot = P(t, 1.5, 0.5);
  const out = interpolate(t, [5.55, 6.15], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{opacity: out}}>
      <div
        style={{
          position: 'absolute',
          left: 70,
          top: 386,
          width: 1,
          height: 542,
          background: 'linear-gradient(180deg, rgba(233,184,136,0.0) 0%, rgba(233,184,136,0.55) 18%, rgba(220,131,82,0.85) 78%, rgba(220,131,82,0) 100%)',
          transform: `scaleY(${draw.toFixed(3)})`,
          transformOrigin: 'top',
        }}
      />
      <div
        style={{
          position: 'absolute',
          left: 64,
          top: 372 + 556 * draw - 3,
          width: 13,
          height: 13,
          borderRadius: 7,
          border: `1px solid rgba(220,131,82,${0.9 * dot})`,
          background: `rgba(220,131,82,${0.35 * dot})`,
          boxShadow: dot > 0.4 ? '0 0 18px rgba(220,131,82,0.6)' : undefined,
        }}
      />
      <div
        style={{
          position: 'absolute',
          left: 92,
          top: 356,
          ...label(13, C.ember, '0.42em'),
          opacity: label_ * 0.95,
          whiteSpace: 'nowrap',
          textShadow: '0 2px 14px rgba(0,0,0,0.8)',
        }}
      >
        The turning point
      </div>
    </AbsoluteFill>
  );
};

/* ------------------------------------------------------------- 07 · ONE COFFEE */
export const OneCoffee: React.FC = () => {
  const t = useT();
  const pop = interpolate(t, [1.1, 1.28, 1.55], [1, 1.7, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.inOut(Easing.quad),
  });
  const fill = P(t, 1.1, 0.35);
  const ring = P(t, 1.1, 0.9);
  const lab = P(t, 1.5, 0.5);
  const out = interpolate(t, [4.95, 5.35], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{opacity: out}}>
      <div style={{position: 'absolute', left: 76, top: 1060, width: 700}}>
        <div style={{...label(12, C.mist, '0.34em'), marginBottom: 22, opacity: P(t, 0.25, 0.45)}}>One invitation</div>
        <div style={{display: 'flex', alignItems: 'center', gap: 30}}>
          {Array.from({length: 9}, (_, i) => {
            const on = i === 0;
            const appear = P(t, 0.3 + i * 0.05, 0.3);
            return (
              <div key={i} style={{position: 'relative', width: 16, height: 16, opacity: appear}}>
                {on && (
                  <div
                    style={{
                      position: 'absolute',
                      inset: -9 * ring,
                      borderRadius: '50%',
                      border: `1px solid rgba(220,131,82,${0.55 * (1 - ring)})`,
                    }}
                  />
                )}
                <div
                  style={{
                    position: 'absolute',
                    inset: 0,
                    borderRadius: '50%',
                    border: `1px solid ${on ? C.ember : 'rgba(245,239,228,0.30)'}`,
                    background: on ? `rgba(220,131,82,${fill})` : 'transparent',
                    transform: `scale(${on ? pop : 1})`,
                    boxShadow: on && fill > 0.5 ? '0 0 22px rgba(220,131,82,0.45)' : undefined,
                  }}
                />
              </div>
            );
          })}
        </div>
        <div style={{...label(12.5, C.paperDim, '0.28em'), marginTop: 22, opacity: lab}}>
          one coffee &mdash; not a promise
        </div>
      </div>
    </AbsoluteFill>
  );
};

/* ------------------------------------------------------------ 08 · BOOKEND RAIL */
export const ProgressRail: React.FC<{active: number; mode: 'intro' | 'outro'}> = ({active, mode}) => {
  const t = useT();
  const top = 316;
  const step = 158;
  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      <div style={{position: 'absolute', left: 928, top, width: 26, height: step * 7 + 8}}>
        <div
          style={{
            position: 'absolute',
            left: -22,
            top: -34,
            width: 56,
            height: step * 7 + 76,
            borderRadius: 26,
            background: 'linear-gradient(90deg, rgba(6,8,11,0) 0%, rgba(6,8,11,0.34) 60%, rgba(6,8,11,0.42) 100%)',
          }}
        />
        <div style={{position: 'absolute', left: 0, top: 0, width: 1, height: step * 7, background: 'rgba(245,239,228,0.22)'}} />
        {Array.from({length: 8}, (_, i) => {
          const isActive = i + 1 === active;
          const p = mode === 'intro' ? P(t, 0.45 + i * 0.24, 0.32) : 1;
          return (
            <div
              key={i}
              style={{
                position: 'absolute',
                left: 0,
                top: i * step,
                width: isActive ? 26 : 12,
                height: 1,
                background: isActive ? C.ember : 'rgba(245,239,228,0.72)',
                opacity: (isActive ? 1 : 0.62) * p,
                boxShadow: isActive ? '0 0 14px rgba(220,131,82,0.6)' : undefined,
              }}
            />
          );
        })}
        {mode === 'outro' && (
          <div
            style={{
              position: 'absolute',
              left: 0,
              top: 0,
              width: 1,
              height: step * 7,
              background: 'linear-gradient(180deg, rgba(233,184,136,0.9) 0%, rgba(220,131,82,0.35) 100%)',
              transform: `scaleY(${P(t, 0.2, 5.4, EASE.soft).toFixed(3)})`,
              transformOrigin: 'top',
            }}
          />
        )}
      </div>
    </AbsoluteFill>
  );
};

/* --------------------------------------------------------- 09 · FINAL QUESTION */
export const FinalQuestion: React.FC = () => {
  const t = useT();
  const l1 = P(t, 0.0, 0.75);
  const l2 = P(t, 0.22, 0.75);
  const line = P(t, 0.62, 0.95, EASE.soft);
  const mark = P(t, 1.15, 0.8);
  return (
    <AbsoluteFill>
      <AbsoluteFill
        style={{
          background:
            'radial-gradient(86% 42% at 50% 74%, rgba(6,8,11,0.72) 0%, rgba(6,8,11,0.42) 52%, rgba(6,8,11,0) 100%)',
          opacity: l1,
        }}
      />
      <div
        style={{
          position: 'absolute',
          left: 84,
          right: 84,
          bottom: 500,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
        }}
      >
        {[
          {txt: 'Would you give love', p: l1},
          {txt: 'another chance?', p: l2},
        ].map((row) => (
          <div
            key={row.txt}
            style={{
              fontFamily: SERIF,
              fontSize: 86,
              fontWeight: 600,
              lineHeight: 1.1,
              color: C.paper,
              textAlign: 'center',
              opacity: row.p,
              transform: `translateY(${(1 - row.p) * 14}px)`,
              textShadow: '0 4px 34px rgba(0,0,0,0.65)',
              letterSpacing: '0.002em',
            }}
          >
            {row.txt}
          </div>
        ))}
        <div
          style={{
            marginTop: 26,
            width: 300 * line,
            height: 1,
            background: `linear-gradient(90deg, rgba(220,131,82,0) 0%, ${C.ember} 50%, rgba(220,131,82,0) 100%)`,
            opacity: 0.85,
          }}
        />
        <div style={{...label(14, C.mist, '0.52em'), marginTop: 30, opacity: mark * 0.85}}>The Next Yes</div>
      </div>
    </AbsoluteFill>
  );
};
