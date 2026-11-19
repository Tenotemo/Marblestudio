# Mystery Marble Studio V17

Vercel/Vite project. Upload all files to a GitHub repository root. In Vercel, framework Vite, build `npm run build`, output `dist`. Install `npm install`.

## Test order
1. Select a video and verify an original frame appears in the preview.
2. Tap Play without loading detector. Confirm moving original video and increasing Frames count.
3. Pause, load player detector, then Play again to test marble silhouettes.
4. If detector fails, the original preview remains usable; copy the status and diagnostics text.

The selfie segmentation model is not a multi-person football detector and may miss small/distant players. The model and WASM load from external CDNs and need internet. Mobile browser decoding/recording support varies.
