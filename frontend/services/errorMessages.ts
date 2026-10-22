import axios from 'axios';

export function friendlyError(err: unknown): string {
  if (axios.isAxiosError(err)) {
    if (!err.response) return "Can't reach the server. Check your connection.";
    const status = err.response.status;
    const detail = (err.response.data as { detail?: unknown })?.detail;
    if (status === 401) return 'Please log in again.';
    if (status === 404) return "We couldn't find that.";
    if (status === 413) return 'That video is too big. Try a shorter clip.';
    if (status >= 500) return 'Something went wrong on our side. Try again in a minute.';
    if (typeof detail === 'string') return detail;
  }
  return 'Something went wrong. Try again.';
}
