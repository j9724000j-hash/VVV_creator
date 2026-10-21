import {AbsoluteFill, Sequence} from 'remotion';
import {AudioBed} from './AudioBed';
import {FONT_CSS} from './fontData';
import {FontGate} from './fonts';
import {Captions} from './Captions';
import {
  AgeMark,
  FinalQuestion,
  HesitationGauge,
  MessageCard,
  OneCoffee,
  ProgressRail,
  ChapterMarker,
  ThenNow,
  TwoPaths,
} from './Graphics';
import {Bookends, Grain, SceneClip} from './SceneClip';
import {C} from './theme';
import type {Props} from './types';

/**
 * THE NEXT YES — 9:16 short, 45.1 s, hand-authored (Atelier mode).
 *
 * Every beat has its own primary subject: a numeral, two diverging paths, a
 * phone card, a gauge, a split ledger, an arc, a tally, a rail, a question.
 * Nothing is reused as scaffolding — the arc and the rail are the only devices
 * that appear twice, and only as bookends.
 */
export const Film: React.FC<Props> = (props) => {
  const {fps} = props;
  const S = (i: number) => props.scenes[i - 1];
  const seq = (i: number, fromLocal: number, toLocal: number) => ({
    from: Math.round((S(i).from + fromLocal) * fps),
    durationInFrames: Math.max(2, Math.round((toLocal - fromLocal) * fps)),
  });
  const sceneLen = (i: number) => S(i).to - S(i).from;

  return (
    <AbsoluteFill style={{backgroundColor: C.ink}}>
      <style>{FONT_CSS}</style>
      <FontGate>{null}</FontGate>
      {/* ---- picture ---------------------------------------------------- */}
      {props.scenes.map((s) => (
        <Sequence
          key={s.idx}
          from={Math.round(s.from * fps)}
          durationInFrames={Math.round((s.to - s.from) * fps) + Math.round(s.extend * fps)}
          name={`scene-${s.idx}-${s.label}`}
        >
          <SceneClip scene={s} />
        </Sequence>
      ))}

      {/* ---- motion graphics / infographics ----------------------------- */}
      <Sequence {...seq(1, 0.55, 3.2)} name="g-age">
        <AgeMark />
      </Sequence>
      <Sequence {...seq(1, 0.35, sceneLen(1))} name="g-rail-in">
        <ProgressRail active={1} mode="intro" />
      </Sequence>

      <Sequence {...seq(2, 0.28, sceneLen(2))} name="g-paths">
        <TwoPaths />
      </Sequence>

      <Sequence {...seq(3, 0.72, 5.15)} name="g-message">
        <MessageCard />
      </Sequence>

      <Sequence {...seq(4, 0.18, sceneLen(4))} name="g-gauge">
        <HesitationGauge />
      </Sequence>

      <Sequence {...seq(5, 0.28, sceneLen(5))} name="g-thennow">
        <ThenNow />
      </Sequence>

      <Sequence {...seq(6, 0.10, sceneLen(6))} name="g-chapter">
        <ChapterMarker />
      </Sequence>

      <Sequence {...seq(7, 0.42, sceneLen(7))} name="g-coffee">
        <OneCoffee />
      </Sequence>

      <Sequence {...seq(8, 0.0, sceneLen(8))} name="g-rail-out">
        <ProgressRail active={8} mode="outro" />
      </Sequence>
      <Sequence {...seq(8, 8.45, sceneLen(8))} name="g-final-question">
        <FinalQuestion />
      </Sequence>

      {/* ---- subtitles -------------------------------------------------- */}
      <Captions cues={props.captions} />

      {/* ---- print / finish --------------------------------------------- */}
      <Grain />
      <Bookends total={props.durationInFrames} />

      {/* ---- sound ------------------------------------------------------ */}
      <AudioBed vo={props.vo} music={props.audio.music} sfx={props.audio.sfx} />
    </AbsoluteFill>
  );
};
