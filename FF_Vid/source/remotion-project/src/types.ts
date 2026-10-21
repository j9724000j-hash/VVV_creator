export type Scene = {
  idx: number;
  label: string;
  src: string;
  file: string;
  from: number;
  to: number;
  srcStart: number;
  srcEnd: number;
  rate: number;
  extend: number;
  cut: 'hard' | 'fade' | 'dissolve';
  clipDur: number;
  srcNeed: number;
  cutFrames: number;
  stillFrom: number | null;
  stillSrc?: string;
};

export type Word = {t: string; from: number; to: number; e: boolean};

export type Cue = {
  key: string;
  vo: number;
  text: string;
  from: number;
  to: number;
  words: Word[];
  emphasis: boolean;
};

export type AudioItem = {
  file: string;
  start: number;
  end?: number;
  dur?: number;
  gain: number;
  fadeIn: number;
  fadeOut: number;
  loop?: boolean;
};

export type VoiceOver = {file: string; start: number; dur: number};

export type Props = {
  fps: number;
  width: number;
  height: number;
  durationInFrames: number;
  totalSeconds: number;
  title: string;
  scenes: Scene[];
  vo: VoiceOver[];
  captions: Cue[];
  audio: {music: AudioItem[]; sfx: AudioItem[]};
};
