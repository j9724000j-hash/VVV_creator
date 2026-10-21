import {AbsoluteFill, Easing, Img, OffthreadVideo, interpolate, staticFile, useCurrentFrame} from 'remotion';
import {C, FPS} from './theme';
import type {Scene} from './types';

/**
 * Camera move per shot. These are the script's own directions ("slow push-in",
 * "lateral move from the empty chair", "ease backward"), expressed as a drift
 * that never exceeds ~7% scale — restrained enough to read as a locked-off
 * dolly rather than a Ken Burns effect.
 */
const MOVE: Record<number, {s: [number, number]; x: [number, number]; y: [number, number]}> = {
  1: {s: [1.02, 1.075], x: [0, -10], y: [0, -8]},
  2: {s: [1.075, 1.03], x: [-18, 8], y: [0, -4]},
  3: {s: [1.03, 1.085], x: [0, -6], y: [0, -10]},
  4: {s: [1.02, 1.07], x: [5, -7], y: [0, -6]},
  5: {s: [1.05, 1.10], x: [0, 7], y: [0, -8]},
  6: {s: [1.10, 1.045], x: [7, -4], y: [0, 2]},
  7: {s: [1.02, 1.075], x: [0, 9], y: [0, -6]},
  8: {s: [1.075, 1.018], x: [7, -4], y: [0, 0]},
};

export const SceneClip: React.FC<{scene: Scene}> = ({scene}) => {
  const frame = useCurrentFrame();
  const seqLen = Math.round((scene.to - scene.from) * FPS) + Math.round(scene.extend * FPS);
  const p = interpolate(frame, [0, Math.max(seqLen - 1, 1)], [0, 1], {
    extrapolateRight: 'clamp',
    easing: Easing.bezier(0.35, 0, 0.5, 1),
  });
  const move = MOVE[scene.idx] ?? MOVE[1];
  const scale = interpolate(p, [0, 1], move.s);
  const tx = interpolate(p, [0, 1], move.x);
  const ty = interpolate(p, [0, 1], move.y);

  const stillAt = scene.stillSrc && scene.stillFrom != null ? Math.round(scene.stillFrom * FPS) : Infinity;
  const useStill = frame >= stillAt;

  // incoming dissolve: the previous shot keeps running underneath
  const inOpacity =
    scene.cut === 'dissolve'
      ? interpolate(frame, [0, 13], [0, 1], {extrapolateRight: 'clamp', easing: Easing.bezier(0.4, 0, 0.3, 1)})
      : 1;

  return (
    <AbsoluteFill style={{opacity: inOpacity}}>
      <AbsoluteFill
        style={{
          transform: `scale(${scale.toFixed(5)}) translate3d(${tx.toFixed(2)}px, ${ty.toFixed(2)}px, 0)`,
        }}
      >
        {useStill ? (
          <Img
            src={staticFile(scene.stillSrc as string)}
            style={{width: '100%', height: '100%', objectFit: 'cover'}}
          />
        ) : (
          <OffthreadVideo
            src={staticFile(scene.file)}
            muted
            endAt={scene.cutFrames}
            style={{width: '100%', height: '100%', objectFit: 'cover'}}
          />
        )}
      </AbsoluteFill>
      <SceneGrade idx={scene.idx} />
    </AbsoluteFill>
  );
};

/** Per-shot colour temperature: cool, lamplit interior → warm, honest daylight. */
const SceneGrade: React.FC<{idx: number}> = ({idx}) => {
  const warm = [0.07, 0.05, 0.09, 0.07, 0.11, 0.05, 0.20, 0.24][idx - 1] ?? 0.08;
  const cool = [0.16, 0.11, 0.15, 0.13, 0.15, 0.17, 0.06, 0.04][idx - 1] ?? 0.12;
  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      <AbsoluteFill
        style={{
          background: `radial-gradient(72% 46% at 78% 26%, rgba(240,168,110,${warm}) 0%, rgba(240,168,110,0) 72%)`,
          mixBlendMode: 'soft-light',
        }}
      />
      <AbsoluteFill
        style={{
          background: `radial-gradient(82% 58% at 16% 64%, rgba(110,160,200,${cool}) 0%, rgba(110,160,200,0) 74%)`,
          mixBlendMode: 'soft-light',
        }}
      />
      {/* legibility bands: top for the kicker, bottom for captions */}
      <AbsoluteFill
        style={{
          background:
            'linear-gradient(180deg, rgba(5,7,10,0.62) 0%, rgba(5,7,10,0.08) 18%, rgba(5,7,10,0) 38%, rgba(5,7,10,0) 48%, rgba(5,7,10,0.58) 72%, rgba(5,7,10,0.90) 93%, rgba(5,7,10,0.95) 100%)',
        }}
      />
      <AbsoluteFill
        style={{
          background:
            'radial-gradient(118% 80% at 50% 42%, rgba(0,0,0,0) 36%, rgba(0,0,0,0.32) 74%, rgba(0,0,0,0.58) 100%)',
        }}
      />
    </AbsoluteFill>
  );
};

/** Animated emulsion grain + faint scanline warmth, applied over the whole film. */
export const Grain: React.FC = () => {
  const f = useCurrentFrame();
  const tile = ['grain/grain-0.png', 'grain/grain-1.png', 'grain/grain-2.png'][f % 3];
  const dx = ((f * 41) % 420) - 210;
  const dy = ((f * 67) % 700) - 350;
  return (
    <AbsoluteFill
      style={{
        pointerEvents: 'none',
        opacity: 0.062,
        mixBlendMode: 'overlay',
        transform: `translate(${dx * 0.45}px, ${dy * 0.45}px) scale(1.7)`,
      }}
    >
      <Img src={staticFile(tile)} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
    </AbsoluteFill>
  );
};

/** Opening rise from black and closing dim — the only global fades in the cut. */
export const Bookends: React.FC<{total: number}> = ({total}) => {
  const f = useCurrentFrame();
  const open = interpolate(f, [0, 16], [1, 0], {extrapolateRight: 'clamp'});
  const close = interpolate(f, [total - 16, total - 1], [0, 0.62], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  return (
    <AbsoluteFill
      style={{pointerEvents: 'none', backgroundColor: C.ink, opacity: Math.max(open, close)}}
    />
  );
};
