# NothingButNet app

Expo SDK 58 / React Native app for web and iPhone. TypeScript, React Navigation, NativeWind/Inter and Zustand provide the UI, routing and saved login.

Follow [the frontend setup guide](../docs/setup.md#frontend-web-and-iphone), including the API URL for your device, then:

```bash
cd frontend
npm ci
npm start
```

Press **w** for web or scan the QR code with compatible Expo Go on iPhone. Set `EXPO_PUBLIC_API_URL` in an untracked `frontend/.env.local` and restart Expo when it changes. That URL is public configuration; never put server secrets in `EXPO_PUBLIC_` variables.

```bash
# From frontend/:
npx tsc --noEmit
npx expo export --platform web --output-dir /tmp/nbn-web
```

Authentication/upload/sessions/analysis use the real API by default. Progress, made/missed, comparison and leaderboard still use mocks; recurring insights currently checks the whole `MOCKS` object and always returns mocks. Friends and Leaderboard navigation registration is pending on the audited `develop`. These are tracked integration gaps, not reasons to silently enable all mocks. See [feature status](../README.md#what-is-implemented) and [API contract](../docs/api-contract.md).

New screens must be registered by the relevant owner/PM. Only commit files assigned to your ticket; restore temporary navigator changes used for previewing an unregistered screen.
