import {Audio, Sequence, interpolate, staticFile, useVideoConfig} from 'remotion';
import type {AudioItem, VoiceOver} from './types';

/**
 * Audio is authored as a fixed bed, not as a ducked guess: narration sits at a
 * constant level, music and effects are static gains well beneath it, and the
 * only automation is the fades written into the EDL.
 */
const Fade: React.FC<{item: AudioItem; frames: number}> = ({item, frames}) => {
  const {fps} = useVideoConfig();
  const fi = Math.round(item.fadeIn * fps);
  const fo = Math.round(item.fadeOut * fps);
  return (
    <Audio
      src={staticFile(item.file)}
      loop={item.loop}
      volume={(f) => {
        const a = fi > 0 ? interpolate(f, [0, fi], [0, 1], {extrapolateRight: 'clamp'}) : 1;
        const b =
          fo > 0 && frames > fo
            ? interpolate(f, [frames - fo, frames], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})
            : 1;
        return item.gain * Math.min(a, b);
      }}
    />
  );
};

export const AudioBed: React.FC<{vo: VoiceOver[]; music: AudioItem[]; sfx: AudioItem[]}> = ({
  vo,
  music,
  sfx,
}) => {
  const {fps, durationInFrames} = useVideoConfig();
  return (
    <>
      {vo.map((v) => (
        <Sequence
          key={v.file}
          from={Math.round(v.start * fps)}
          durationInFrames={Math.round(v.dur * fps)}
          name={`vo-${v.file}`}
        >
          <Audio src={staticFile(v.file)} />
        </Sequence>
      ))}

      {music.map((m) => {
        const from = Math.round(m.start * fps);
        const to = Math.round((m.end ?? from / fps) * fps);
        const frames = Math.min(durationInFrames - from, Math.max(2, to - from));
        return (
          <Sequence key={m.file + m.start} from={from} durationInFrames={frames} name={`music-${m.file}`}>
            <Fade item={m} frames={frames} />
          </Sequence>
        );
      })}

      {sfx.map((s, i) => {
        const from = Math.round(s.start * fps);
        const endSec = s.end ?? s.start + (s.dur ?? 2);
        const frames = Math.min(durationInFrames - from, Math.max(2, Math.round((endSec - s.start) * fps)));
        return (
          <Sequence key={`${s.file}-${i}`} from={from} durationInFrames={frames} name={`sfx-${s.file}`}>
            <Fade item={s} frames={frames} />
          </Sequence>
        );
      })}
    </>
  );
};
