import axios from "axios";
import { API_BASE, USE_MOCKS } from './config';
import {
  mockAuth, mockUpload, mockAnalysis, mockSessions, mockSession,
  mockProgress, mockGoals, mockGoal,
} from './mocks';
import {
  AuthResponse, UploadResponse, Analysis, SessionSummary, SessionDetail,
  Progress, Goal,
} from './types';

const client = axios.create({baseURL: API_BASE, timeout: 12000});

const authHeader = (token?:string) =>
    token ? {headers:{Authorization: `Bearer ${token}`}} : {}; /// if token is given, create authorization helper

const mock = <T>(data: T): Promise<T> =>
  new Promise((resolve) => setTimeout(() => resolve(data), 500));

export const signup = async (email: string, password: string, name: string): Promise<AuthResponse> =>
  USE_MOCKS // if USE_MOCK is true
    ? mock(mockAuth)
    : (await client.post('/auth/signup', { email, password, name })).data;

export const login = async (email: string, password: string): Promise<AuthResponse> =>
  USE_MOCKS
    ? mock(mockAuth)
    : (await client.post('/auth/login', { email, password })).data;

export const uploadVideo = async (
  formData: FormData,
  token: string,
  onProgress?: (percent: number) => void
): Promise<UploadResponse> =>
  USE_MOCKS
    ? mock(mockUpload)
    : (
        await client.post('/sessions/upload', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
            Authorization: `Bearer ${token}`,
          },
          onUploadProgress: (e) => {
            if (onProgress && e.total) {
              onProgress(Math.round((e.loaded / e.total) * 100));
            }
          },
        })
      ).data;

export const analyze = async (sessionId: string, videoUrl: string, token: string): Promise<Analysis> =>
  USE_MOCKS
    ? mock(mockAnalysis)
    : (
        await client.post(
          '/analysis/analyze',
          { session_id: sessionId, video_url: videoUrl },
          authHeader(token)
        )
      ).data;

export const getSessions = async (token: string): Promise<SessionSummary[]> =>
  USE_MOCKS
    ? mock(mockSessions)
    : (await client.get('/sessions', authHeader(token))).data;

export const getSession = async (id: string, token: string): Promise<SessionDetail> =>
  USE_MOCKS
    ? mock(mockSession)
    : (await client.get(`/sessions/${id}`, authHeader(token))).data;

export const deleteSession = async (id: string, token: string): Promise<void> =>
  USE_MOCKS
    ? mock(undefined)
    : (await client.delete(`/sessions/${id}`, authHeader(token))).data;

export const getProgress = async (token: string): Promise<Progress> =>
  USE_MOCKS
    ? mock(mockProgress)
    : (await client.get('/progress', authHeader(token))).data;

export const getGoals = async (token: string): Promise<Goal[]> =>
  USE_MOCKS
    ? mock(mockGoals)
    : (await client.get('/goals', authHeader(token))).data;

export const createGoal = async (
  goal: { checkpoint: string; target_angle: number },
  token: string
): Promise<Goal> =>
  USE_MOCKS
    ? mock(mockGoal)
    : (await client.post('/goals', goal, authHeader(token))).data;

export const sendFeedback = async (
  data: { message: string; rating: number; screen: string },
  token: string
): Promise<void> =>
  USE_MOCKS
    ? mock(undefined)
    : (await client.post('/feedback', data, authHeader(token))).data;