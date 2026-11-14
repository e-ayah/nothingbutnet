import axios from 'axios';
import { API_URL } from './config';

const USE_MOCK = false;
const wait = (ms: number) => new Promise((r) => setTimeout(r, ms));
const auth = (token: string | null) => ({ headers: { Authorization: `Bearer ${token}` } });

const mockMade: Record<string, boolean> = {};

export async function setMade(sessionId: string, made: boolean, token: string | null) {
  if (USE_MOCK) {
    await wait(300);
    mockMade[sessionId] = made;
    return { session_id: sessionId, made };
  }
  const res = await axios.patch(`${API_URL}/sessions/${sessionId}`, { made }, auth(token));
  return res.data;
}
