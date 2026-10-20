/**
 * Remotion configuration for this sandboxed environment.
 *
 * The default Remotion behavior downloads its own Chrome Headless Shell from
 * Google storage, which is not reachable from this environment. Instead we
 * point Remotion at the self-contained Chromium 153 headless-shell build
 * (from @sparticuz/chromium) installed at ~/.local/bin/chromium, which ships
 * its own NSS/Vulkan/SwiftShader libraries and needs no system GUI libs.
 */
import {Config} from '@remotion/cli/config';

Config.setBrowserExecutable(`${process.env.HOME}/.local/bin/chromium`);
// Software GL via SwiftShader (no GPU in this environment).
Config.setChromiumOpenGlRenderer('swangle');
// 2 vCPUs available — keep render concurrency modest.
Config.setConcurrency(2);
Config.setOverwriteOutput(true);
