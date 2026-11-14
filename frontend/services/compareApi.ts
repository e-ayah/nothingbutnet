
import axios from "axios";
import { API_URL } from "./config";

export type CompareShot = {
  session_id: string;
  created_at: string;
  video_url: string;
  annotated_video_url: string | null;
  angles: {
    elbow_angle: number | null;
    knee_angle: number | null;
    shoulder_angle: number | null;
  };
  score: number | null;
};

export type CompareResult = {
  a: CompareShot;
  b: CompareShot;
  changes: {
    elbow_angle: number | null;
    knee_angle: number | null;
    shoulder_angle: number | null;
    score: number | null;
  };
};

const USE_MOCK = false;

const MOCK_COMPARE: CompareResult = {
  a: {
    session_id: "1",
    created_at: "2026-09-28T12:00:00",
    video_url: "",
    annotated_video_url: null,
    angles: {
      elbow_angle: 82,
      knee_angle: 139,
      shoulder_angle: 52,
    },
    score: 72,
  },
  b: {
    session_id: "2",
    created_at: "2026-10-02T12:00:00",
    video_url: "",
    annotated_video_url: null,
    angles: {
      elbow_angle: 86.2,
      knee_angle: 145,
      shoulder_angle: 49,
    },
    score: 81,
  },
  changes: {
    elbow_angle: 4.2,
    knee_angle: 6,
    shoulder_angle: -3,
    score: 9,
  },
};

export async function compareSessions(
  a: string,
  b: string,
  token: string | null
): Promise<CompareResult> {
  if (USE_MOCK) {
    await new Promise((resolve) => setTimeout(resolve, 300));

    return {
      ...MOCK_COMPARE,
      a: { ...MOCK_COMPARE.a, session_id: a },
      b: { ...MOCK_COMPARE.b, session_id: b },
    };
  }

  const response = await axios.get(
    `${API_URL}/sessions/compare`,
    {
      params: { a, b },
      headers: token
        ? { Authorization: `Bearer ${token}` }
        : {},
    }
  );

  return response.data;
}
