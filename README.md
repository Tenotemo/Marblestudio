# Mystery Marble Studio V19 — experimental shot-aware test

Deploy with Vercel framework **Vite** (build: `npm run build`, output: `dist`).

## Changes from V18
- Approximate camera-cut detection using frame brightness samples; resets stale segmentation mask at cuts.
- Adjustable focus region and mask persistence.
- Optional manual goal placement and ball location anchors; interpolation between ball anchors. **Not automatic ball tracking.**
- Black-and-silver marble rendering and offline frame processing, then original-timing replay.

## Limitations
This is **not** a football-specific detection model. MediaPipe selfie segmentation can miss small distant footballers, and close-up bodies may extend outside the video frame. A proper person/object detection and instance-segmentation pipeline is still needed for automatic penalty taker, goalkeeper, ball, and goal tracking. No MP4 export. iPhone memory constraints apply. Markers are baked into frames during processing, so reprocess after placing anchors. A goal drawn at a manual anchor does not yet follow camera motion.

## Test
1. Select a short football clip; load model; set 8 fps; process.
2. Inspect shot boundaries and timeline; compare frame persistence with V18.
3. Optional: set a goal anchor and two ball anchors at different timeline positions, then reprocess.
