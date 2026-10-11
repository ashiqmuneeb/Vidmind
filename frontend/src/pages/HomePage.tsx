import React, { useState } from 'react';
import { Youtube, Upload, Play, Clock, Sparkles, CheckCircle2, AlertCircle, ArrowRight, Trash2, RefreshCw } from 'lucide-react';
import { Video } from '../types';

interface HomePageProps {
  videos: Video[];
  isLoading: boolean;
  onAddVideo: (url: string) => Promise<void>;
  onSelectVideo: (videoId: string) => void;
  onDeleteVideo: (videoId: string) => Promise<void>;
}

export const HomePage: React.FC<HomePageProps> = ({
  videos,
  isLoading,
  onAddVideo,
  onSelectVideo,
  onDeleteVideo,
}) => {
  const [url, setUrl] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!url.trim()) return;
    setIsSubmitting(true);
    setErrorMsg(null);
    try {
      await onAddVideo(url.trim());
      setUrl('');
    } catch (err: any) {
      setErrorMsg(err.message || 'Failed to add video.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const formatDuration = (seconds: number) => {
    if (!seconds) return 'Pending...';
    const h = Math.floor(seconds / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    const s = Math.floor(seconds % 60);
    if (h > 0) return `${h}h ${m}m ${s}s`;
    return `${m}m ${s}s`;
  };

  return (
    <div className="max-w-6xl mx-auto px-6 py-10 space-y-12">
      {/* Hero Section */}
      <div className="text-center space-y-4 max-w-3xl mx-auto">
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full text-xs font-medium bg-brand-500/10 border border-brand-500/30 text-brand-300">
          <Sparkles className="w-3.5 h-3.5" />
          <span>Local Long-Video Intelligence • Up to 10+ Hours</span>
        </div>
        <h1 className="text-4xl md:text-5xl font-display font-bold tracking-tight text-white">
          Transform Massive Videos into <br />
          <span className="bg-gradient-to-r from-brand-400 via-sky-300 to-indigo-300 bg-clip-text text-transparent">
            Verifiable Knowledge & Notes
          </span>
        </h1>
        <p className="text-slate-400 text-base md:text-lg leading-relaxed">
          Extract timestamped transcripts, auto-generate chapter outlines, Cornell notes, flashcards, 
          and engage in evidence-grounded Q&A with zero hallucinations.
        </p>
      </div>

      {/* Main Input Box */}
      <div className="glass-panel p-6 md:p-8 rounded-2xl border border-surface-700/80 shadow-2xl relative overflow-hidden">
        <div className="absolute -right-20 -top-20 w-64 h-64 bg-brand-500/10 rounded-full blur-3xl pointer-events-none" />
        <div className="absolute -left-20 -bottom-20 w-64 h-64 bg-indigo-500/10 rounded-full blur-3xl pointer-events-none" />

        <form onSubmit={handleSubmit} className="space-y-4 relative z-10">
          <div className="flex flex-col md:flex-row gap-3">
            <div className="relative flex-1">
              <Youtube className="w-5 h-5 text-red-500 absolute left-4 top-1/2 -translate-y-1/2" />
              <input
                type="text"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                placeholder="Paste YouTube video or lecture URL (e.g. https://www.youtube.com/watch?v=...)"
                className="w-full pl-12 pr-4 py-3.5 rounded-xl bg-surface-800/90 border border-surface-600 focus:border-brand-500 focus:ring-2 focus:ring-brand-500/20 text-white placeholder-slate-500 text-sm outline-none transition-all"
                disabled={isSubmitting}
              />
            </div>
            <button
              type="submit"
              disabled={isSubmitting || !url.trim()}
              className="px-6 py-3.5 rounded-xl bg-brand-600 hover:bg-brand-500 disabled:opacity-50 disabled:hover:bg-brand-600 text-white font-medium text-sm flex items-center justify-center gap-2 shadow-lg shadow-brand-600/30 transition-all cursor-pointer"
            >
              {isSubmitting ? (
                <>
                  <RefreshCw className="w-4 h-4 animate-spin" />
                  <span>Analyzing...</span>
                </>
              ) : (
                <>
                  <span>Analyze Video</span>
                  <ArrowRight className="w-4 h-4" />
                </>
              )}
            </button>
          </div>

          {errorMsg && (
            <div className="flex items-center gap-2 text-rose-400 text-sm bg-rose-500/10 p-3 rounded-lg border border-rose-500/20">
              <AlertCircle className="w-4 h-4 shrink-0" />
              <span>{errorMsg}</span>
            </div>
          )}

          {/* Quick Upload Drag & Drop Area */}
          <div className="border border-dashed border-surface-700 hover:border-brand-500/50 rounded-xl p-4 text-center cursor-pointer bg-surface-800/40 hover:bg-surface-800/70 transition-all flex items-center justify-center gap-3">
            <Upload className="w-4 h-4 text-slate-400" />
            <span className="text-xs text-slate-400">
              Or drag & drop local MP4, MKV, MP3, WAV or lecture video files to process offline
            </span>
          </div>
        </form>
      </div>

      {/* Feature Highlights Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="glass-card p-5 rounded-xl space-y-2">
          <div className="w-8 h-8 rounded-lg bg-brand-500/10 flex items-center justify-center text-brand-400">
            <Clock className="w-4 h-4" />
          </div>
          <h3 className="font-semibold text-white text-sm">10+ Hour Video Architecture</h3>
          <p className="text-xs text-slate-400 leading-relaxed">
            Chunked acoustic streaming and bounded RAM processing handles massive multi-hour lectures without OOM crashes.
          </p>
        </div>

        <div className="glass-card p-5 rounded-xl space-y-2">
          <div className="w-8 h-8 rounded-lg bg-emerald-500/10 flex items-center justify-center text-emerald-400">
            <CheckCircle2 className="w-4 h-4" />
          </div>
          <h3 className="font-semibold text-white text-sm">Strict Grounding & Evidence</h3>
          <p className="text-xs text-slate-400 leading-relaxed">
            Every factual statement links directly to verified timestamp citations. Unverifiable questions are flagged immediately.
          </p>
        </div>

        <div className="glass-card p-5 rounded-xl space-y-2">
          <div className="w-8 h-8 rounded-lg bg-indigo-500/10 flex items-center justify-center text-indigo-400">
            <Sparkles className="w-4 h-4" />
          </div>
          <h3 className="font-semibold text-white text-sm">Multi-Style Study Artifacts</h3>
          <p className="text-xs text-slate-400 leading-relaxed">
            Generate Cornell notes, concise summaries, interactive flashcards, and conceptual quizzes from any video section.
          </p>
        </div>
      </div>

      {/* Recent Videos Section */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-semibold text-white flex items-center gap-2">
            <span>Video Library</span>
            <span className="text-xs font-normal text-slate-400 bg-surface-800 px-2.5 py-0.5 rounded-full border border-surface-700">
              {videos.length}
            </span>
          </h2>
        </div>

        {isLoading ? (
          <div className="text-center py-12 text-slate-500">
            <RefreshCw className="w-6 h-6 animate-spin mx-auto mb-2" />
            <p className="text-sm">Loading library...</p>
          </div>
        ) : videos.length === 0 ? (
          <div className="text-center py-14 border border-dashed border-surface-800 rounded-2xl space-y-2">
            <p className="text-slate-400 text-sm font-medium">No videos added yet</p>
            <p className="text-xs text-slate-500 max-w-sm mx-auto">
              Paste a YouTube URL above or upload a video file to begin extracting transcripts and generating notes.
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {videos.map((vid) => (
              <div
                key={vid.id}
                className="glass-card p-4 rounded-xl flex items-center justify-between gap-4 group cursor-pointer"
                onClick={() => onSelectVideo(vid.id)}
              >
                <div className="flex items-center gap-3.5 min-w-0">
                  <div className="w-12 h-12 rounded-lg bg-surface-700/80 flex items-center justify-center text-brand-400 shrink-0 group-hover:bg-brand-600 group-hover:text-white transition-colors">
                    <Play className="w-5 h-5 fill-current" />
                  </div>
                  <div className="min-w-0 space-y-1">
                    <h3 className="font-medium text-sm text-slate-200 truncate group-hover:text-white transition-colors">
                      {vid.title}
                    </h3>
                    <div className="flex items-center gap-3 text-xs text-slate-500">
                      <span className="flex items-center gap-1">
                        <Clock className="w-3 h-3" />
                        <span>{formatDuration(vid.duration_seconds)}</span>
                      </span>
                      <span>•</span>
                      <span className="capitalize">{vid.source_type}</span>
                    </div>
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      onDeleteVideo(vid.id);
                    }}
                    className="p-2 text-slate-500 hover:text-rose-400 hover:bg-surface-700/50 rounded-lg transition-colors"
                    title="Delete Video"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                  <button
                    onClick={() => onSelectVideo(vid.id)}
                    className="px-3 py-1.5 rounded-lg bg-surface-700 group-hover:bg-brand-600 text-slate-200 group-hover:text-white text-xs font-medium transition-colors flex items-center gap-1"
                  >
                    <span>Open</span>
                    <ArrowRight className="w-3 h-3" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
