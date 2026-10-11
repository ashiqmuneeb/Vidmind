export interface Video {
  id: string;
  title: string;
  description?: string;
  channel?: string;
  duration_seconds: number;
  source_type: string;
  source_url?: string;
  thumbnail_url?: string;
  created_at: string;
  updated_at: string;
  metadata_json?: Record<string, any>;
}

export interface ProcessingStatus {
  job_id: string;
  video_id: string;
  status: 'pending' | 'running' | 'paused' | 'completed' | 'failed' | 'cancelled';
  current_stage: string;
  progress_pct: number;
  error_message?: string;
  retry_count: number;
  stage_timings: Record<string, any>;
  started_at: string;
  completed_at?: string;
}

export interface TranscriptSegment {
  id: string;
  video_id: string;
  segment_index: number;
  start_time: number;
  end_time: number;
  text: string;
  language: string;
  confidence: number;
  speaker?: string;
  source: string;
  is_flagged_qc: boolean;
  qc_flags_json: string[];
}

export interface Chapter {
  id: string;
  video_id: string;
  chapter_index: number;
  title: string;
  start_time: number;
  end_time: number;
  summary?: string;
  key_topics: string[];
  evidence_segment_ids: string[];
}

export interface Note {
  id: string;
  video_id: string;
  style: string;
  title: string;
  markdown_content: string;
  structured_json: Record<string, any>;
  is_user_edited: boolean;
  created_at: string;
  updated_at: string;
}

export interface CitationItem {
  segment_id?: string;
  timestamp_start: number;
  timestamp_end: number;
  excerpt: string;
  source_type: string;
}

export interface ChatMessage {
  id: string;
  session_id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  question_type?: string;
  evidence_citations: CitationItem[];
  confidence_score: number;
  created_at: string;
}

export interface HealthInfo {
  status: string;
  app_name: string;
  environment: string;
  database: string;
  storage: {
    data_directory: string;
    free_space_gb: number;
  };
  hardware: {
    profile: string;
    cpu_logical_cores: number;
    memory_total_gb: number;
    memory_available_gb: number;
    cuda_available: boolean;
    cuda_device?: string;
    ffmpeg_available: boolean;
  };
  ai_providers: {
    whisper_model: string;
    whisper_device: string;
    whisper_compute_type: string;
    recommended_whisper: string;
    ollama_base_url: string;
    ollama_active: boolean;
    ollama_model: string;
    embedding_model: string;
  };
}
