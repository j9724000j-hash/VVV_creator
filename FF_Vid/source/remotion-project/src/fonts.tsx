import {useEffect, useState} from 'react';
import {cancelRender, continueRender, delayRender} from 'remotion';
import {FONT_CSS} from './fontData';

/**
 * Type is inlined as data-URI @font-face rules (src/fontData.ts), so no render
 * ever waits on a font request. The gate only waits for the browser to finish
 * decoding those already-present faces, with a hard 4 s ceiling so a stalled
 * tab degrades to the CSS fallbacks instead of failing the render.
 */
export const FontGate: React.FC<{children: React.ReactNode}> = ({children}) => {
  const [handle] = useState(() => delayRender('Decoding typefaces', {timeoutInMilliseconds: 12000}));
  const [ready, setReady] = useState(false);

  useEffect(() => {
    let released = false;
    let cancelled = false;
    const release = () => {
      if (released || cancelled) {
        return;
      }
      released = true;
      continueRender(handle);
      setReady(true);
    };
    const guard = setTimeout(release, 4000);
    Promise.all([
      document.fonts.load('600 40px Inter'),
      document.fonts.load('400 40px "Cormorant Garamond"'),
      document.fonts.load('600 40px "Cormorant Garamond"'),
    ])
      .then(() => document.fonts.ready)
      .then(() => {
        clearTimeout(guard);
        release();
      })
      .catch((err) => {
        console.warn('font decode issue — CSS fallbacks in use', err);
        clearTimeout(guard);
        release();
      });
    return () => {
      cancelled = true;
      clearTimeout(guard);
      if (!released) {
        released = true;
        continueRender(handle);
      }
    };
  }, [handle]);

  if (!ready) {
    // keep the tree mounted so the style tag is parsed immediately
    return <>{children}</>;
  }
  return <>{children}</>;
};

export const cancelIfBroken = (message: string): void => {
  cancelRender(new Error(message));
};
