# Mystery Marble Studio V20 — local offline processor (experimental)

## Why this version is local
Vercel's static site deployments cannot run long CPU/GPU video-processing jobs. V20 therefore provides a **local FastAPI studio** that runs on your laptop. It is not a Vercel cloud processing backend. A future hosted system would require a separate GPU/CPU worker, storage, and job queue.

## Windows 10/11 setup
1. Install Python 3.11 or 3.12 and FFmpeg (both `python` and `ffmpeg` should work in a terminal).
2. Extract this ZIP and open PowerShell in its folder.
3. `py -3.11 -m venv .venv` (or `python -m venv .venv`)
4. `.\.venv\Scripts\Activate.ps1` (or `.venv\Scripts\python.exe` for subsequent commands if execution policy blocks activation)
5. `python -m pip install -r requirements.txt`
6. `python -m uvicorn server:app --host 127.0.0.1 --port 8000`
7. Open `http://127.0.0.1:8000` in a browser on the laptop.

**First run requires internet:** Ultralytics downloads `yolo11n-seg.pt` weights. Later runs can be offline if weights are cached. Install FFmpeg for H.264 output. CPU inference can be slow. Use short 5–12 second clips at 12 fps and 640 resolution first.

## What works / limitations
- Frame-by-frame processing (not real-time), preserving video duration and speed at selected output fps.
- Segmented person masks filled with black/silver beads. Model tracking via ByteTrack.
- General COCO sports-ball detection (may miss the small ball). Metadata includes detected ball points.
- Optional manually placed static goal overlay; no true net physics or camera-aware goal tracking.
- No goalkeeper role classification. No manual silhouette corrections. Camera cuts use a conservative heuristic, not validated shot classification.
- V20 is an engineering prototype. It has NOT been validated on the user's footage or on Windows/iPhone.

## CLI (optional)
`python processor/render.py input.mp4 output.mp4 --fps 12 --size 640 --spacing 7`
The CLI writes MP4V video. To make it Safari compatible, convert with FFmpeg:
`ffmpeg -i output.mp4 -c:v libx264 -pix_fmt yuv420p -movflags +faststart output_h264.mp4`

## Privacy
Files remain on the computer hosting the server under `jobs/`. No automatic cleanup. Delete the `jobs` folder after use. The browser sends the uploaded video to the local server at 127.0.0.1, not to Vercel.
