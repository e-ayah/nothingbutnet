// Types for every API response — field names match docs/api-contract.md and backend/schemas/

export type Angles = {
    elbow_angle: number;
    knee_angle: number;
    shoulder_angle: number;
}

export type FeedbackItem = {
    checkpoint: string;
    angle: number;
    status: 'good' | 'needs_work';
    tip: string;
}

// POST /analysis/analyze
export type Analysis = {
    session_id: string;
    release_frame: number;
    angles: Angles;
    feedback: FeedbackItem[];
    overall_score: number;
    annotated_video_url: string;
    processed_at: string;
}

export type SessionStatus = 'processing' | 'done' | 'failed';

export type SessionError = string | null;

// POST /sessions/upload
export type UploadResponse = {
    session_id: string;
    video_url: string;
    status: SessionStatus;
}

// one item from GET /sessions
export type SessionSummary = {
  session_id: string;
  created_at: string;
  overall_score: number | null; // null while processing
  status: SessionStatus;
  error: SessionError;
};

// GET /sessions/:id — score/video/angles/feedback are null while processing
export type SessionDetail = {
    session_id: string;
    video_url: string;
    annotated_video_url: string | null;
    angles: Angles | null;
    feedback: FeedbackItem[] | null;
    score: number | null;
    status: SessionStatus;
    error: SessionError;
}

// one item in GET /progress sessions
export type ProgressSession = {
    session_id: string;
    created_at: string;
    angles: Angles;
    score: number;
}

// GET /progress — trends hold one list of values per angle, oldest first
export type Progress = {
    sessions: ProgressSession[];
    trends: {
        elbow_angle: number[];
        knee_angle: number[];
        shoulder_angle: number[];
    };
    improvement_summary: string;
}

export type Goal = {
    id: string;
    checkpoint: string;
    target_angle: number;
    current_angle: number;
    progress: number; // 0–1
}

export type AuthResponse = {
    user_id: string;
    token: string;
}
