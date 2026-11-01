# FaultSense AI - Landing Page (Vite + React)

## Run
```
npm install
npm run dev        # http://localhost:5173
npm run build      # production build in dist/
```

## What to edit (all in `src/config/siteConfig.js`)
| Want to change | Edit |
|---|---|
| Hero tagline, stats strip | `tagline`, `stats`, `showStats` |
| "Try It Live" link | `liveDemoUrl` (default: FastAPI docs at http://127.0.0.1:8000/docs) |
| Demo video | `demoVideo.src` |
| Team names / roles / photos | `team` |
| Email, GitHub, LinkedIn | `contact` |

## Adding the demo video later
1. Copy your file to `public/videos/demo.mp4`
2. In `siteConfig.js` set `demoVideo.src` to `"/videos/demo.mp4"` (optionally `poster`)
   - or paste a YouTube link, e.g. `"https://www.youtube.com/watch?v=XXXXXXXXXXX"`
3. The placeholder disappears automatically.

## Team photos
Put `safa.jpg`, `izma.jpg`, `yusra.jpg`, `areeba.jpg` in `public/team/`.
Missing photos show initials.

## Hero photo
Replace `public/images/hero-machine.svg` or point `heroImage` to your own image.
