# Mystery Marble Studio V16 — Vercel deployment

This is a Vite app using MediaPipe Tasks Vision for browser-side person segmentation. It attempts to fill detected human silhouettes with glossy marble dots and draws a generic football pitch. It does not provide guaranteed detection of small or overlapping football players, and it is not a 3D character reconstruction.

## Deploy
1. Unzip and upload the folder to a GitHub repository.
2. In Vercel select **Add New → Project → Import Git Repository**.
3. Framework: **Vite**; Build command: `npm run build`; Output directory: `dist`.
4. Deploy, open the HTTPS URL on your iPhone, upload a video, and tap **Load player detector**.

The MediaPipe JavaScript is bundled at build time, avoiding dynamic JavaScript module imports from a CDN. MediaPipe WASM and the segmentation model are still downloaded over HTTPS when the detector starts; these external resources must be reachable. If detection fails, check the Safari console or network restrictions. No video is uploaded to a server by this app; processing happens in the browser.

For local development: `npm install`, then `npm run dev`.
