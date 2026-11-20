# Mystery Marble Studio V24 — Clean static build

This is a self-contained HTML application. There is NO app.js, no vercel.json, no npm install, and no Vite build.

## Reliable deployment

**Recommended:** create a NEW EMPTY GitHub repository (for example Marblestudio-V24) and upload only index.html from this ZIP. Connect that new repository to a NEW Vercel project. Framework: Other; Root Directory: ./; Build Command: none; Output Directory: .

Alternatively, remove legacy src/, web/, processor/, package.json and old deployment configuration from the old repository first. Do not just add V24 files to the old repository without checking deployment settings.

Test /index.html and the page buttons. There is intentionally no /app.js URL in V24.

## Functions

- Video: upload local MP4/MOV supported by the browser; preview full-frame black/silver marble conversion; export PNG frames in ZIP. iOS memory and video codec restrictions apply.
- Guess studio: 78 country flag presets loaded from flagcdn.com (requires internet); 52 brand-name placeholder cards; 57 people name presets (requires uploaded photo); custom image upload. Reveal animation and ZIP export.
- Exports are limited to 400 frames to reduce browser crashes. For CapCut import PNGs in order and set duration 1/FPS.
- All video frames preserve original aspect ratio and timestamps sampled at chosen FPS, but output frame rate is chosen by user.

This version is not guaranteed to support all iPhone MOV codecs, and it has not been browser-tested on an iPhone.
