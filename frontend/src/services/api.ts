import { Video, ProcessingStatus, TranscriptSegment, Chapter, Note, ChatMessage, HealthInfo } from '../types';

const API_BASE = '/api';

export async function fetchHealth(): Promise<HealthInfo> {
  const res = await fetch(`${API_BASE}/health`);
  if (!res.ok) throw new Error('Failed to fetch health info');
  return res.json();
}

export async function fetchVideos(): Promise<{ videos: Video[]; total: number }> {
  const res = await fetch(`${API_BASE}/videos`);
  if (!res.ok) throw new Error('Failed to fetch videos');
  return res.json();
}

export async function fetchVideo(id: string): Promise<Video> {
  const res = await fetch(`${API_BASE}/videos/${id}`);
  if (!res.ok) throw new Error('Failed to fetch video');
  return res.json();
}

export async function createVideo(payload: { url?: string; title?: string; enable_vision?: boolean }): Promise<Video> {
  const res = await fetch(`${API_BASE}/videos`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Failed to create video' }));
    throw new Error(err.detail || 'Failed to create video');
  }
  return res.json();
}

export async function deleteVideo(id: string): Promise<void> {
  const res = await fetch(`${API_BASE}/videos/${id}`, { method: 'DELETE' });
  if (!res.ok) throw new Error('Failed to delete video');
}

export async function fetchProcessing(videoId: string): Promise<ProcessingStatus> {
  const res = await fetch(`${API_BASE}/videos/${videoId}/processing`);
  if (!res.ok) throw new Error('Failed to fetch processing status');
  return res.json();
}

export async function startProcessing(videoId: string, forceRestart = false): Promise<ProcessingStatus> {
  const res = await fetch(`${API_BASE}/videos/${videoId}/process`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ force_restart: forceRestart }),
  });
  if (!res.ok) throw new Error('Failed to start processing');
  return res.json();
}

export async function fetchTranscript(videoId: string, search?: string): Promise<{ segments: TranscriptSegment[]; duration_seconds: number }> {
  const url = new URL(`${window.location.origin}${API_BASE}/videos/${videoId}/transcript`);
  if (search) url.searchParams.append('search', search);
  const res = await fetch(url.toString());
  if (!res.ok) throw new Error('Failed to fetch transcript');
  return res.json();
}

export async function fetchChapters(videoId: string): Promise<{ chapters: Chapter[] }> {
  const res = await fetch(`${API_BASE}/videos/${videoId}/chapters`);
  if (!res.ok) throw new Error('Failed to fetch chapters');
  return res.json();
}

export async function fetchNotes(videoId: string): Promise<Note[]> {
  const res = await fetch(`${API_BASE}/videos/${videoId}/notes`);
  if (!res.ok) throw new Error('Failed to fetch notes');
  return res.json();
}

export async function updateNote(videoId: string, noteId: string, markdown_content: string): Promise<Note> {
  const res = await fetch(`${API_BASE}/videos/${videoId}/notes/${noteId}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ markdown_content }),
  });
  if (!res.ok) throw new Error('Failed to update note');
  return res.json();
}

export async function fetchChatMessages(videoId: string): Promise<ChatMessage[]> {
  const res = await fetch(`${API_BASE}/videos/${videoId}/chat/messages`);
  if (!res.ok) throw new Error('Failed to fetch messages');
  return res.json();
}

export async function sendChatMessage(videoId: string, message: string): Promise<ChatMessage> {
  const res = await fetch(`${API_BASE}/videos/${videoId}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message }),
  });
  if (!res.ok) throw new Error('Failed to send chat message');
  return res.json();
}
