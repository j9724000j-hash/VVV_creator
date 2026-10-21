# THE NEXT YES — art direction (Atelier mode)

Declared for OpenMontage `edit_decisions.bespoke.art_direction`. This is the
commitment the composition was built to; nothing in it is reusable from another
piece.

## Design read

A late-evening apartment, one woman, one invitation. The film is **editorial,
not motivational**: it behaves like a short documentary insert — margin
annotations, a printed programme's typography, restrained camera. Emotion is
carried by performance, light and silence; graphics annotate, they never
narrate. Nothing bounces. Nothing persuades.

`visual_variance`: medium-high (every beat has its own primary subject).
`motion_intensity`: low (single-direction drifts, ≤ 7 % scale, no whips).
`information_density`: low (one idea per beat; max three lines on screen).

## Palette

| Role | Value | Use |
|---|---|---|
| ink | `#07090C` | fades, scrims, plate fills |
| paper | `#F5EFE4` | type, hairlines |
| warm | `#E9B888` | lamp light, spoken word highlight |
| ember | `#DC8352` | the single accent: emphasis, active markers, the question |
| cool | `#86A6BE` | window light, "no" register |
| mist | `rgba(196,209,219,.72)` | labels, gutter text |

Two temperatures only: cool window / warm practical. Graphics live in paper +
ember; they never introduce a third hue.

## Type

- **Cormorant Garamond 500–600** — display: the number 52, the ledger, the
  closing question. Carries the "printed" register.
- **Inter 500–700** — subtitles and labels: uppercase, +0.26–0.52 em tracking at
  12–15 px for annotations, 46 px / 600 for captions.

Rules: no drop shadows on graphics (only on type over picture), no gradients on
type, no centred-and-bold subtitle clichés — captions sit in a fixed column and
arrive line by line, never reflowing.

## Motion character

- Camera: one slow drift per shot, direction written per beat (push-in, lateral
  away from the empty chair, ease-back as she types).
- Graphics: **draw** (rules extend, strokes trace) or **cut in** on the beat.
  No spring, no overshoot, no rotation, nothing that reads as "template".
- Subtitles: line rise 10 px / 7 frames; the currently spoken word tints warm.
  Emphasis words are 700 + ember — three per film, never more.
- Transitions: clean cuts, two 13-frame dissolves (café, street), one rise from
  black, one dim to close.

## Signature devices (used once each)

1. **The age slug** — a hairline rule plus `AGE / 52` slug in the upper-left
   gutter. Appears once, in the hook, and never returns.
2. **The margin rule** — a vertical ember rule that draws down the left margin to
   name "the turning point". The only graphic that touches the frame edge.
3. **The eight-tick rail** — a scale down the right margin; lit tick = the beat
   you are in. Bookends only (beat 1 in, beat 8 out, where it fills as a timer).

None of these repeats as scaffolding. Remove any one and its scene still works —
which is why each is allowed exactly one appearance.

## Not allowed (anti-patterns for this piece)

- Kinetic-typography "quote card" scenes, zoom-punch captions, emoji, progress
  bars with percentage labels, stock "inspirational" b-roll, voice-actor
  whisper, music swells over the narration.
- Any graphic crossing the face. Safe margins: top 154 px, bottom 408 px,
  right 72 px (YouTube Shorts UI).
- Text baked into the AI footage: every word on screen is live text in the
  composition, so it is editable and re-renderable.

## Distinctness check

Could this be any other video's graphics? No: the gutter slug, the margin rule
and the tick rail are authored for this story's beats (age → fear → invitation →
hesitation → cost → turning → yes → future), and the palette is taken from the
footage's own lamp/window light. If the film were about a different subject, all
three devices would have to be rebuilt.
