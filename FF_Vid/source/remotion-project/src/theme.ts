import {Easing} from 'remotion';

/**
 * THE NEXT YES — art direction tokens.
 *
 * Read: a late-evening apartment, restraint, editorial calm. Not a "motivational"
 * video: the type behaves like a printed programme, the graphics like margin
 * annotations from a documentary. Nothing bounces, nothing shouts.
 */
export const C = {
  ink: '#07090C',
  ink2: '#0E1218',
  paper: '#F5EFE4',
  paperSoft: 'rgba(245,239,228,0.78)',
  paperDim: 'rgba(245,239,228,0.52)',
  warm: '#E9B888',
  ember: '#DC8352',
  cool: '#86A6BE',
  mist: 'rgba(196,209,219,0.72)',
  hair: 'rgba(245,239,228,0.20)',
  hairSoft: 'rgba(245,239,228,0.13)',
};

/** YouTube Shorts UI-safe box (top 8%, right 12%, bottom 20%). */
export const SAFE = {
  left: 72,
  right: 1008,
  top: 154,
  bottom: 1512,
};

export const EASE = {
  out: Easing.bezier(0.16, 1, 0.3, 1),
  inOut: Easing.bezier(0.65, 0, 0.35, 1),
  soft: Easing.bezier(0.33, 0, 0.2, 1),
};

export const SERIF = '"Cormorant Garamond", Georgia, serif';
export const SANS = 'Inter, "Helvetica Neue", Arial, sans-serif';

export const FPS = 30;
