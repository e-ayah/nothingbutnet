// The server address. Set EXPO_PUBLIC_API_URL in frontend/.env.local (on your machine)
// and in Vercel's settings (for the web version). Expo only reads variables starting with EXPO_PUBLIC_.
export const API_URL = process.env.EXPO_PUBLIC_API_URL ?? 'http://localhost:8000';
 
// One switch per area: true = fake data from mocks.ts, false = the real server.
export const MOCKS = {
  auth: false,
  upload: false,
  sessions: false,
  analysis: false,
  progress: true, // GET /progress is built in Sprint 6 — flip this to false then
};
