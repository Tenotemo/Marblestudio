# Mystery Marble Studio V18

Upload this folder to a GitHub repository root, import it into Vercel as a Vite project, and deploy. The app uses MediaPipe ImageSegmenter 0.10.21 and loads its model and WASM assets at runtime (requires network access). Run `npm install` and `npm run build` locally to check installation and build.

## Workflow
1. Choose a browser-supported football video. The original frame should appear.
2. Load the silhouette model.
3. Choose analysis FPS (start with 8 on iPhone), then Process frames. Processing may be slower than real time.
4. Play processed frames; they are replayed with original video timing based on selected FPS.

## Limitations
- The bundled selfie segmentation model detects foreground people as a group. It is not a football-specific multi-person detector, and can fail on distant players, overlapping people, and goalkeepers. Stabilization is a simple temporal mask hold, not true object tracking.
- Goalposts and nets are a static illustrative overlay. The ball overlay is a synthetic animation, NOT tracked from the original video. Disable it for honest visualization. Precise goal geometry, goalkeeper identity, ball tracking, and net reactions require additional dedicated tracking or manual keyframing.
- This proof-of-concept stores full processed frames in memory. Keep clips short (e.g. 5–10 seconds) especially on phones. It does not yet export MP4.
- Video audio is not reproduced in processed replay. Output is black/silver monochrome and does not preserve jersey or skin colors.
