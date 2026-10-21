import {Composition, getInputProps, registerRoot} from 'remotion';
import {Film} from './src/Film';
import type {Props} from './src/types';
import timeline from './public/props.json';

const input = getInputProps() as Partial<Props>;
const props = {...(timeline as unknown as Props), ...input} as Props;

const Root: React.FC = () => (
  <Composition
    id="TheNextYes"
    component={Film}
    durationInFrames={props.durationInFrames}
    fps={props.fps}
    width={props.width}
    height={props.height}
    defaultProps={props}
  />
);

registerRoot(Root);
