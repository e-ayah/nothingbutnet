import axios from 'axios';
import { API_URL } from './config';

// Sprint 8 switches this off when the friends endpoints are live.
const USE_MOCK = true;
const wait = () => new Promise<void>((resolve) => setTimeout(resolve, 300));
const auth = (token: string | null) => ({ headers: { Authorization: `Bearer ${token}` } });

export type Friend = { user_id: string; name: string; username: string };
export type IncomingRequest = { request_id: string; from: Friend };
export type OutgoingRequest = { request_id: string; to: Friend };
export type Requests = { incoming: IncomingRequest[]; outgoing: OutgoingRequest[] };
export type SentRequest = { request_id: string; status: 'pending' };

let mockFriends: Friend[] = [{ user_id: 'u2', name: 'Maya Chen', username: 'maya' }];
let mockIncoming: IncomingRequest[] = [{ request_id: 'r1', from: { user_id: 'u3', name: 'Leo Park', username: 'leo' } }];
let mockOutgoing: OutgoingRequest[] = [{ request_id: 'r2', to: { user_id: 'u4', name: 'Sam Ortiz', username: 'sam' } }];
let nextId = 5;

export async function getFriends(token: string | null): Promise<Friend[]> {
  if (!USE_MOCK) return (await axios.get<Friend[]>(`${API_URL}/friends`, auth(token))).data;
  await wait();
  return mockFriends.map((friend) => ({ ...friend }));
}

export async function getRequests(token: string | null): Promise<Requests> {
  if (!USE_MOCK) return (await axios.get<Requests>(`${API_URL}/friends/requests`, auth(token))).data;
  await wait();
  return {
    incoming: mockIncoming.map((request) => ({ ...request, from: { ...request.from } })),
    outgoing: mockOutgoing.map((request) => ({ ...request, to: { ...request.to } })),
  };
}

export async function sendRequest(username: string, token: string | null): Promise<SentRequest> {
  const exactUsername = username.trim();
  if (!USE_MOCK) return (await axios.post<SentRequest>(`${API_URL}/friends/requests`, { username: exactUsername }, auth(token))).data;
  await wait();
  if (!exactUsername) throw new Error('Enter an exact username');
  const match = (friend: Friend) => friend.username.toLowerCase() === exactUsername.toLowerCase();
  if (exactUsername.toLowerCase() === 'nobody') throw new Error('No user with that username');
  if (mockFriends.some(match)) throw new Error('You are already friends');
  if (mockIncoming.some((request) => match(request.from)) || mockOutgoing.some((request) => match(request.to))) {
    throw new Error('A pending friend request already exists');
  }
  const id = nextId++;
  const request: OutgoingRequest = {
    request_id: `r${id}`,
    to: { user_id: `u${id}`, name: exactUsername, username: exactUsername },
  };
  mockOutgoing = [...mockOutgoing, request];
  return { request_id: request.request_id, status: 'pending' };
}

export async function accept(id: string, token: string | null): Promise<{ friend: Friend }> {
  if (!USE_MOCK) return (await axios.post<{ friend: Friend }>(`${API_URL}/friends/requests/${encodeURIComponent(id)}/accept`, undefined, auth(token))).data;
  await wait();
  const request = mockIncoming.find((item) => item.request_id === id);
  if (!request) throw new Error('Friend request not found');
  mockIncoming = mockIncoming.filter((item) => item.request_id !== id);
  mockFriends = [...mockFriends, { ...request.from }];
  return { friend: { ...request.from } };
}

export async function decline(id: string, token: string | null): Promise<void> {
  if (!USE_MOCK) {
    await axios.post(`${API_URL}/friends/requests/${encodeURIComponent(id)}/decline`, undefined, auth(token));
    return;
  }
  await wait();
  if (!mockIncoming.some((item) => item.request_id === id)) throw new Error('Friend request not found');
  mockIncoming = mockIncoming.filter((item) => item.request_id !== id);
}

export async function removeFriend(userId: string, token: string | null): Promise<void> {
  if (!USE_MOCK) {
    await axios.delete(`${API_URL}/friends/${encodeURIComponent(userId)}`, auth(token));
    return;
  }
  await wait();
  if (!mockFriends.some((friend) => friend.user_id === userId)) throw new Error('Friend not found');
  mockFriends = mockFriends.filter((friend) => friend.user_id !== userId);
}
