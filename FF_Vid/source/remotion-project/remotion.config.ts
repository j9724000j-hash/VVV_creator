/**
 * Remotion config for the sandboxed build (no Google-storage Chrome download).
 * Chromium comes from @sparticuz/chromium with its own NSS/SwiftShader libs.
 */
import {Config} from '@remotion/cli/config';

Config.setBrowserExecutable(`${process.env.HOME}/.local/bin/chromium`);
Config.setChromiumOpenGlRenderer('swangle');
Config.setConcurrency(2);
Config.setOverwriteOutput(true);
// PNG intermediates + explicit BT.709: a delivery master in limited-range
// yuv420p, not the yuvj420p you get from JPEG frames.
Config.setVideoImageFormat('png');
Config.setColorSpace('bt709');
Config.setCodec('h264');
Config.setCrf(16);
Config.setPixelFormat('yuv420p');
