# Deploying the web app (Vercel)

**Live URL:** https://nothingbutnet-op.vercel.app

## How it was deployed
- Vercel Hobby (free, no card), deployed with the Vercel CLI from `frontend/`:
  `npx vercel --prod`
- Build settings come from `frontend/vercel.json`:
  build `npx expo export --platform web` → output `dist/`
- ⏸ GitHub not connected yet (repo is on a personal account), so merges do NOT auto-redeploy.
  Pending: repo owner connects it, or the repo moves to a GitHub org.

## Environment variable
- `EXPO_PUBLIC_API_URL` = https://nothingbutnet-010a.onrender.com
- Add/change: `npx vercel env add EXPO_PUBLIC_API_URL production`, then redeploy

## Redeploying
- From `frontend/`: `npx vercel --prod`

## Test locally
- From `frontend/`: `npx expo export --platform web` (creates `dist/`, don't commit it)

## Troubleshooting
- Blank page → check `outputDirectory` and `rewrites` in `vercel.json`
- First request of the day is slow → Render server sleeps after ~15 min