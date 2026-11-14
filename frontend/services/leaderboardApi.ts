import axios from 'axios';
import { API_URL } from './config';

// true = fake data (this week). A Sprint 8 ticket flips it to false once the endpoint is live.
const USE_MOCK = false;
const wait = (ms: number) => new Promise((r) => setTimeout(r, ms));
const auth = (token: string | null) => ({ headers: { Authorization: `Bearer ${token}` } });

export type Row = {
  rank: number | null;
  user_id: string;
  name: string;
  made: number;
  attempts: number;
  make_pct: number;
  avg_score: number | null;
  is_me: boolean;
};

const mock: Record<'week' | 'all', Row[]> = {
  week: [
    { rank: 1, user_id: 'u2', name: 'Maya Chen', made: 8, attempts: 10, make_pct: 80, avg_score: 74, is_me: false },
    { rank: 2, user_id: 'me', name: 'You', made: 18, attempts: 25, make_pct: 72, avg_score: 68, is_me: true },
    { rank: null, user_id: 'u3', name: 'Leo Park', made: 3, attempts: 3, make_pct: 100, avg_score: 61, is_me: false },
  ],
  all: [
    { rank: 1, user_id: 'u2', name: 'Maya Chen', made: 62, attempts: 80, make_pct: 78, avg_score: 76, is_me: false },
    { rank: 2, user_id: 'me', name: 'You', made: 140, attempts: 200, make_pct: 70, avg_score: 69, is_me: true },
    { rank: 3, user_id: 'u4', name: 'Sam Rivera', made: 35, attempts: 55, make_pct: 64, avg_score: 63, is_me: false },
    { rank: 4, user_id: 'u3', name: 'Leo Park', made: 12, attempts: 20, make_pct: 60, avg_score: 62, is_me: false },
    { rank: null, user_id: 'u5', name: 'Ava Patel', made: 2, attempts: 4, make_pct: 50, avg_score: null, is_me: false },
  ],
};

export async function getLeaderboard(period: 'week' | 'all', token: string | null): Promise<Row[]> {
  if (USE_MOCK) {
    await wait(300);
    return mock[period];
  }
  return (await axios.get(`${API_URL}/leaderboard`, { params: { period }, ...auth(token) })).data;
}