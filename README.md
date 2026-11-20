# Mystery Marble Studio V22

Two browser-based modes:

1. **Football video → PNG frames**: grayscale full-frame marble conversion, including all original scene objects, with original timing preserved by sequential sampling at a chosen FPS.
2. **Guess the picture**: gradual marble reveals for country flags, stylized logo text placeholders, famous people (upload your own photo), and custom images.

## Deploy

Upload `index.html`, `app.js`, and `vercel.json` to the root of your GitHub repository. Deploy to Vercel using the **Other** framework preset; no npm installation or build command is needed. A simple static site is sufficient.

## CapCut

Extract the exported ZIP, import numbered frames in ascending order, and set each image duration to 1/FPS seconds (12 FPS = 0.083333 seconds). CapCut versions differ in whether bulk duration changes are supported. If that is difficult, on a laptop run FFmpeg in the extracted folder:

`ffmpeg -framerate 12 -i frame_%05d.png -c:v libx264 -pix_fmt yuv420p output.mp4`

For 24 FPS, change `12` to `24`. Frame extraction uses the selected sampling rate; 12 FPS will look less smooth than the original 60 FPS clip, even though total playback duration matches.

## Limits

- Browser PNG export is memory-intensive. Begin with a 5–10 second video, 480 px and 8–12 FPS, especially on iPhone.
- Some MOV codecs cannot be decoded in all browsers. Convert to H.264 MP4 if needed.
- Flag presets load from flagcdn.com and require an internet connection and CORS support. Upload an image if loading fails.
- Brand logo presets are *stylized text placeholders*, not official brand artwork. Famous people presets supply names only; upload a photo to reveal.
- The original historical image library and exact V11 styling are not included because those assets were not provided with this project.
- This is an image sequence exporter, not an automatic CapCut integration or an MP4 encoder.
