# Mystery Marble Studio V21 — Full-frame monochrome

No dependencies or MediaPipe. The application uses a browser video element and a canvas to transform every frame into grayscale black-and-silver glossy marbles. The original football footage, camera motion, players, ball, net and goalposts are all transformed together. It does not isolate or track individual objects.

## Deploy on Vercel

1. Extract this ZIP.
2. Upload `index.html` and `vercel.json` to the ROOT of your `Tenotemo/Marblestudio` repository, replacing the existing root `index.html`.
3. Remove any old `package.json`, `package-lock.json`, `vite.config.*`, and `src` directory from earlier versions if they are no longer needed, or set Vercel Framework Preset to **Other** and Build Command to blank (override) with Output Directory blank (override).
4. Commit to `main`; Vercel should deploy a static site without installing npm packages.
5. On iPhone Safari, select a compatible video and press Play. A MOV may fail depending on its codec; try H.264 MP4 if necessary.

## Notes

- Full-frame effect uses no segmentation, detection, AI model, or internet connection after loading.
- Playback follows the original video time; rendering performance varies with device. Use Performance detail on slower phones.
- Recording works only on browsers that support canvas.captureStream and MediaRecorder WebM; not guaranteed on iPhone. It records video only (no audio).
- 9:16 and 16:9 formats letterbox the source footage to avoid stretching. Marbles replace the whole frame including letterbox areas.
- There is no MP4 export or server processing in this version.
