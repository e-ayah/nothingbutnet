# Deploying the web app (Vercel)

**Live URL:** https://nothingbutnet-op.vercel.app

## How it was deployed
- Vercel Hobby (free, no card), deployed with the Vercel CLI from `frontend/`:
  `npx vercel --prod`
- Build settings come from `frontend/vercel.json`:
  build `npx expo export --platform web --clear` → output `dist/` (`--clear` makes a changed `EXPO_PUBLIC_API_URL` take effect; without it the old address can stay cached)
- ⏸ GitHub not connected yet (repo is on a personal account), so merges do NOT auto-redeploy.
  Pending: repo owner connects it, or the repo moves to a GitHub org.

## Environment variable
- `EXPO_PUBLIC_API_URL` = https://nothingbutnet-0l0a.onrender.com
- Add/change: `npx vercel env add EXPO_PUBLIC_API_URL production`, then redeploy

## Redeploying
- From `frontend/`: `npx vercel --prod`

## Test locally
- From `frontend/`: `npx expo export --platform web` (creates `dist/`, don't commit it)

## Troubleshooting
- Visitors get sent to a Vercel login page → Deployment Protection is on. In the Vercel project: Settings → Deployment Protection → turn off "Vercel Authentication" (free on Hobby), so beta testers can open the site without a Vercel account.
- "Can't reach the server" on every request → check `EXPO_PUBLIC_API_URL` is exactly `https://nothingbutnet-0l0a.onrender.com` (zero, lowercase L, zero), then redeploy.
- Blank page → check `outputDirectory` and `rewrites` in `vercel.json`
- First request of the day is slow → Render server sleeps after ~15 min