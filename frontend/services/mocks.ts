import {
  Angles, FeedbackItem, SessionSummary, SessionDetail, UploadResponse,
  Progress, Goal, AuthResponse, Analysis,
} from './types';

// Mock data for USE_MOCKS in api.ts — one export per API response

export const mockAngles: Angles = { elbow_angle: 92.3, knee_angle: 165.1, shoulder_angle: 58.7 };

export const mockFeedback: FeedbackItem[] = [
  { checkpoint: 'elbow_alignment',
    angle: 92.3,
    status: 'good',
    tip: 'Great elbow alignment' },
  { checkpoint: 'knee_bend',
    angle: 142.0,
    status: 'needs_work',
    tip: 'Bend your knees a bit less to drive into the shot' }
];

export const mockAuth: AuthResponse = {
    user_id: "12345",
    token: "example_token"
};

export const mockUpload: UploadResponse = {
    session_id: "s2",
    video_url: "https://cloudinary.com/...",
    status: "processing"
};

export const mockSessions: SessionSummary[] = [
  { session_id: 's1', created_at: '2026-10-01T16:12:00Z', overall_score: 67, status: 'done', error: null },
  { session_id: 's2', created_at: '2026-10-01T18:12:00Z', overall_score: null, status: 'processing', error: null },
  { session_id: 's3', created_at: '2026-10-01T20:12:00Z', overall_score: null, status: 'failed', error: 'No person found in the video' }
];

export const mockSession: SessionDetail = {
    session_id: 's1',
    video_url: "https://cloudinary.com/...",
    annotated_video_url: "https://file-examples.com/storage/fef447ccea6abefa1a29bd2/2017/04/file_example_MP4_480_1_5MG.mp4",
    angles: mockAngles,
    feedback: mockFeedback,
    score: 67,
    status: 'done',
    error: null
};

export const mockAnalysis: Analysis = {
    session_id: "abc123",
    release_frame: 45,
    angles: mockAngles,
    feedback: [
    { checkpoint: 'elbow_alignment', angle: 92.3, status: 'good', tip: 'Great elbow alignment' }
    ],
    overall_score: 67,
    annotated_video_url: "https://file-examples.com/storage/fef447ccea6abefa1a29bd2/2017/04/file_example_MP4_480_1_5MG.mp4",
    processed_at: '2026-09-15T10:30:00Z'
};

export const mockProgress: Progress = {
    sessions: [
      { session_id: 's1', created_at: '2026-10-01T16:12:00Z', angles: { elbow_angle: 92.3, knee_angle: 165.1, shoulder_angle: 58.7 }, score: 67 },
      { session_id: 's2', created_at: '2026-10-01T16:13:00Z', angles: { elbow_angle: 97.2, knee_angle: 162.1, shoulder_angle: 55.7 }, score: 68 },
      { session_id: 's3', created_at: '2026-10-01T16:14:00Z', angles: { elbow_angle: 98.3, knee_angle: 160.1, shoulder_angle: 51.7 }, score: 71 }
    ],
    trends: {
      elbow_angle: [92.3, 97.2, 98.3],
      knee_angle: [165.1, 162.1, 160.1],
      shoulder_angle: [58.7, 55.7, 51.7]
    },
    improvement_summary: "Your knee angle dropped 5 degrees"
};

export const mockGoals: Goal[] = [
    {id: "12345",
    checkpoint: "elbow_alignment",
    target_angle: 92.3,
    current_angle: 81.6,
    progress: 0.86}
];

// POST /goals returns the created goal
export const mockGoal: Goal = mockGoals[0];
