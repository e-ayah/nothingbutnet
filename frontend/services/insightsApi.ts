
import { API_URL, MOCKS } from "./config";

export type RecurringMistake = {
  checkpoint: string;
  label: string;
  count: number;
  out_of: number;
  latest_tip: string;
};

const MOCK_RECURRING: RecurringMistake[] = [
  {
    checkpoint: "elbow_alignment",
    label: "Elbow",
    count: 4,
    out_of: 5,
    latest_tip: "Keep your elbow aligned with the basket."
  }
];

export async function getRecurring(
  token: string
): Promise<RecurringMistake[]> {
  if (MOCKS) {
    return MOCK_RECURRING;
  }

  const response = await fetch(`${API_URL}/insights/recurring`, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json"
    }
  });

  if (!response.ok) {
    throw new Error("Failed to fetch recurring mistakes");
  }

  return response.json();
}
