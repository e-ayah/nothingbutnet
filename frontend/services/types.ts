export type Angles = {
    elbow_angle: number;
    knee_angle: number;
    shoulder_angle: number;
}

export type FeedbackItem = {
    checkpoint: string;
    angle: number
    status: 'good' | 'needs_work'
    tip: string
}

export type Analysis = {
    session_id: string;
    release_frame: number;
    angles: Angles | null;
    feedback: FeedbackItem | null;
    overall_score: number | null;
    annotated_video_url: string | null;
    processed_at: string;
}

export type SessionStatus = 'processing' | 'done' | 'failed';

export type SessionError = string | null;

export type SessionSummary = {
  session_id: string;
  created_at: string;
  overall_score: number | null;
  status: SessionStatus;
};

export type Progress = {
    sessions: SessionSummary[];
    trends: Angles[];
    improvement_summary: string;
}

export type Goal = {
    id: string;
    checkpoint: string;
    target_angle: number;
    current_angle: number;
    progress: number;
}

export type AuthResponse = {
    user_id: string;
    token: string;
}