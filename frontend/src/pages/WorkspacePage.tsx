import React, { useState, useEffect } from 'react';
import { 
  Play, Pause, RotateCcw, Search, FileText, MessageSquare, 
  BookOpen, Clock, Send, Save, Download, ArrowLeft
} from 'lucide-react';
import { Video, TranscriptSegment, Chapter, ChatMessage } from '../types';
import * as api from '../services/api';

interface WorkspacePageProps {
  video: Video;
  onBack: () => void;
}

export const WorkspacePage: React.FC<WorkspacePageProps> = ({ video, onBack }) => {
  const [activeTab, setActiveTab] = useState<'transcript' | 'notes' | 'chat'>('transcript');
  const [currentTime, setCurrentTime] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  
  // Data states
  const [transcript, setTranscript] = useState<TranscriptSegment[]>([]);
  const [chapters, setChapters] = useState<Chapter[]>([]);
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([]);
  const [chatInput, setChatInput] = useState('');
  const [isSendingChat, setIsSendingChat] = useState(false);

  // Editable note state
  const [noteContent, setNoteContent] = useState('');

  useEffect(() => {
    loadWorkspaceData();
  }, [video.id]);

  const loadWorkspaceData = async () => {
    try {
      const [tData, cData, nData, mData] = await Promise.all([
        api.fetchTranscript(video.id).catch(() => ({ segments: [], duration_seconds: 0 })),
        api.fetchChapters(video.id).catch(() => ({ chapters: [] })),
        api.fetchNotes(video.id).catch(() => []),
        api.fetchChatMessages(video.id).catch(() => []),
      ]);

      setTranscript(tData.segments);
      setChapters(cData.chapters);
      if (nData.length > 0) {
        setNoteContent(nData[0].markdown_content);
      }
      setChatMessages(mData);
    } catch (err) {
      console.error('Error loading workspace data:', err);
    }
  };

  const handleSeek = (seconds: number) => {
    setCurrentTime(seconds);
    setIsPlaying(true);
  };

  const handleSendChat = async (messageText?: string) => {
    const textToSend = messageText || chatInput;
    if (!textToSend.trim() || isSendingChat) return;
    setIsSendingChat(true);
    setChatInput('');

    try {
      const response = await api.sendChatMessage(video.id, textToSend);
      setChatMessages(prev => [...prev, response]);
    } catch (err) {
      console.error('Failed to send chat message:', err);
    } finally {
      setIsSendingChat(false);
    }
  };

  const formatTimestamp = (seconds: number) => {
    const h = Math.floor(seconds / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    const s = Math.floor(seconds % 60);
    if (h > 0) return `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
    return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
  };

  const starterQuestions = [
    "Summarize this video",
    "What are the key ideas?",
    "Explain the hardest concepts",
    "Create study notes",
    "Create flashcards",
    "Show me the important timestamps"
  ];

  return (
    <div className="flex flex-col h-[calc(100vh-65px)] overflow-hidden">
      {/* Workspace Top Toolbar */}
      <div className="bg-surface-800/90 border-b border-surface-700/80 px-6 py-2.5 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <button
            onClick={onBack}
            className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-surface-700/60 transition-colors"
            title="Back to Library"
          >
            <ArrowLeft className="w-4 h-4" />
          </button>
          <div>
            <h1 className="text-sm font-semibold text-white truncate max-w-lg">
              {video.title}
            </h1>
            <span className="text-[11px] text-slate-400">
              {video.source_type.toUpperCase()} • {formatTimestamp(video.duration_seconds || 3600)}
            </span>
          </div>
        </div>

        {/* Export & Actions */}
        <div className="flex items-center gap-2">
          <a
            href={`/api/videos/${video.id}/export/markdown`}
            download
            className="px-3 py-1.5 rounded-lg bg-surface-700 hover:bg-surface-600 text-slate-200 text-xs font-medium transition-colors flex items-center gap-1.5"
          >
            <Download className="w-3.5 h-3.5" />
            <span>Export Notes</span>
          </a>
          <a
            href={`/api/videos/${video.id}/export/srt`}
            download
            className="px-3 py-1.5 rounded-lg bg-surface-700 hover:bg-surface-600 text-slate-200 text-xs font-medium transition-colors flex items-center gap-1.5"
          >
            <Download className="w-3.5 h-3.5" />
            <span>SRT Subtitles</span>
          </a>
        </div>
      </div>

      {/* 3-Panel Workspace Body */}
      <div className="flex-1 grid grid-cols-12 overflow-hidden">
        {/* PANEL 1: LEFT CHAPTERS (3 cols) */}
        <aside className="col-span-12 md:col-span-3 border-r border-surface-700/80 bg-surface-900/60 flex flex-col overflow-hidden">
          <div className="p-3 border-b border-surface-700/80 flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
              <BookOpen className="w-3.5 h-3.5 text-brand-400" />
              <span>Chapters & Topics</span>
            </span>
            <span className="text-[10px] text-slate-500 bg-surface-800 px-2 py-0.5 rounded">
              {chapters.length}
            </span>
          </div>

          <div className="flex-1 overflow-y-auto p-2 space-y-1">
            {chapters.length === 0 ? (
              <div className="p-4 text-center text-xs text-slate-500">
                Chapters will appear once video analysis is complete.
              </div>
            ) : (
              chapters.map((ch) => (
                <div
                  key={ch.id}
                  onClick={() => handleSeek(ch.start_time)}
                  className={`p-2.5 rounded-lg text-xs cursor-pointer transition-all border ${
                    currentTime >= ch.start_time && currentTime < ch.end_time
                      ? 'bg-brand-600/20 border-brand-500/50 text-white'
                      : 'border-transparent text-slate-300 hover:bg-surface-800/80'
                  }`}
                >
                  <div className="flex items-center justify-between mb-1">
                    <span className="font-medium truncate">{ch.title}</span>
                    <span className="text-[10px] text-brand-400 font-mono">
                      {formatTimestamp(ch.start_time)}
                    </span>
                  </div>
                  {ch.summary && (
                    <p className="text-[11px] text-slate-400 line-clamp-2">
                      {ch.summary}
                    </p>
                  )}
                </div>
              ))
            )}
          </div>
        </aside>

        {/* PANEL 2: CENTER VIDEO PLAYER (5 cols) */}
        <main className="col-span-12 md:col-span-5 bg-black/40 flex flex-col items-center justify-between p-4 border-r border-surface-700/80 overflow-y-auto">
          {/* Mock or Real Video Container */}
          <div className="w-full aspect-video bg-surface-800 rounded-xl overflow-hidden border border-surface-700 shadow-2xl relative flex items-center justify-center group">
            {video.source_url && video.source_url.includes('youtube.com') ? (
              <iframe
                title="YouTube Player"
                src={`https://www.youtube.com/embed/${new URL(video.source_url).searchParams.get('v')}?start=${Math.floor(currentTime)}&autoplay=${isPlaying ? 1 : 0}`}
                className="w-full h-full border-0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowFullScreen
              />
            ) : (
              <div className="text-center p-6 space-y-3">
                <div className="w-16 h-16 rounded-full bg-brand-600/20 text-brand-400 flex items-center justify-center mx-auto border border-brand-500/30">
                  <Play className="w-8 h-8 fill-current ml-1" />
                </div>
                <div>
                  <p className="text-sm font-medium text-white">{video.title}</p>
                  <p className="text-xs text-slate-400 mt-1">
                    Time: {formatTimestamp(currentTime)} / {formatTimestamp(video.duration_seconds || 3600)}
                  </p>
                </div>
              </div>
            )}
          </div>

          {/* Player Controls & Scrubber */}
          <div className="w-full mt-4 glass-panel p-3 rounded-xl border border-surface-700/70 space-y-2">
            <div className="flex items-center justify-between text-xs font-mono text-slate-400">
              <span>{formatTimestamp(currentTime)}</span>
              <span>{formatTimestamp(video.duration_seconds || 3600)}</span>
            </div>
            <input
              type="range"
              min="0"
              max={video.duration_seconds || 3600}
              value={currentTime}
              onChange={(e) => handleSeek(Number(e.target.value))}
              className="w-full h-1.5 bg-surface-700 rounded-lg appearance-none cursor-pointer accent-brand-500"
            />
            <div className="flex items-center justify-center gap-4 pt-1">
              <button
                onClick={() => handleSeek(Math.max(0, currentTime - 10))}
                className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-surface-700 transition-colors"
                title="Rewind 10s"
              >
                <RotateCcw className="w-4 h-4" />
              </button>
              <button
                onClick={() => setIsPlaying(!isPlaying)}
                className="p-2 rounded-xl bg-brand-600 hover:bg-brand-500 text-white transition-colors"
              >
                {isPlaying ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4 fill-current ml-0.5" />}
              </button>
            </div>
          </div>
        </main>

        {/* PANEL 3: RIGHT TABBED AI PANEL (4 cols) */}
        <section className="col-span-12 md:col-span-4 bg-surface-900/80 flex flex-col overflow-hidden">
          {/* Tabs Header */}
          <div className="flex items-center border-b border-surface-700/80 bg-surface-800/60 p-1.5 gap-1">
            <button
              onClick={() => setActiveTab('transcript')}
              className={`flex-1 py-1.5 rounded-lg text-xs font-medium transition-all flex items-center justify-center gap-1.5 ${
                activeTab === 'transcript'
                  ? 'bg-brand-600 text-white shadow-sm'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-surface-700/50'
              }`}
            >
              <Clock className="w-3.5 h-3.5" />
              <span>Transcript</span>
            </button>
            <button
              onClick={() => setActiveTab('notes')}
              className={`flex-1 py-1.5 rounded-lg text-xs font-medium transition-all flex items-center justify-center gap-1.5 ${
                activeTab === 'notes'
                  ? 'bg-brand-600 text-white shadow-sm'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-surface-700/50'
              }`}
            >
              <FileText className="w-3.5 h-3.5" />
              <span>Notes</span>
            </button>
            <button
              onClick={() => setActiveTab('chat')}
              className={`flex-1 py-1.5 rounded-lg text-xs font-medium transition-all flex items-center justify-center gap-1.5 ${
                activeTab === 'chat'
                  ? 'bg-brand-600 text-white shadow-sm'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-surface-700/50'
              }`}
            >
              <MessageSquare className="w-3.5 h-3.5" />
              <span>Ask AI</span>
            </button>
          </div>

          {/* TAB CONTENT */}
          <div className="flex-1 overflow-y-auto p-4">
            {/* 1. TRANSCRIPT TAB */}
            {activeTab === 'transcript' && (
              <div className="space-y-3">
                <div className="relative mb-3">
                  <Search className="w-3.5 h-3.5 text-slate-500 absolute left-3 top-1/2 -translate-y-1/2" />
                  <input
                    type="text"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    placeholder="Search in transcript..."
                    className="w-full pl-9 pr-3 py-1.5 rounded-lg bg-surface-800 border border-surface-700 text-xs text-white placeholder-slate-500 outline-none focus:border-brand-500"
                  />
                </div>

                {transcript.length === 0 ? (
                  <div className="text-center py-10 text-xs text-slate-500">
                    No transcript segments yet. Processing will populate speech-to-text.
                  </div>
                ) : (
                  transcript
                    .filter(s => !searchQuery || s.text.toLowerCase().includes(searchQuery.toLowerCase()))
                    .map((seg) => (
                      <div
                        key={seg.id}
                        onClick={() => handleSeek(seg.start_time)}
                        className={`p-2.5 rounded-lg text-xs cursor-pointer transition-all border ${
                          currentTime >= seg.start_time && currentTime <= seg.end_time
                            ? 'bg-brand-600/20 border-brand-500/60 text-white'
                            : 'border-surface-800 hover:bg-surface-800/80 text-slate-300'
                        }`}
                      >
                        <div className="flex items-center justify-between mb-1 text-[10px] text-brand-400 font-mono">
                          <span>{formatTimestamp(seg.start_time)}</span>
                          {seg.speaker && <span className="text-slate-400">{seg.speaker}</span>}
                        </div>
                        <p className="leading-relaxed">{seg.text}</p>
                      </div>
                    ))
                )}
              </div>
            )}

            {/* 2. NOTES TAB */}
            {activeTab === 'notes' && (
              <div className="h-full flex flex-col space-y-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-1.5">
                    <span className="text-xs font-semibold text-white">Study Notes</span>
                    <span className="text-[10px] bg-brand-500/20 text-brand-300 px-2 py-0.5 rounded">
                      Standard
                    </span>
                  </div>
                  <button
                    onClick={() => {}}
                    className="p-1 rounded text-slate-400 hover:text-white"
                    title="Save Changes"
                  >
                    <Save className="w-3.5 h-3.5" />
                  </button>
                </div>

                {/* Note Editing Area */}
                <textarea
                  value={noteContent}
                  onChange={(e) => setNoteContent(e.target.value)}
                  placeholder="Generated notes and summaries will appear here. You can freely edit them..."
                  className="w-full flex-1 min-h-[300px] p-3 rounded-xl bg-surface-800/80 border border-surface-700 text-xs text-slate-200 placeholder-slate-500 outline-none focus:border-brand-500 font-mono resize-none"
                />

                {/* Note Action Toolbar */}
                <div className="flex flex-wrap gap-1.5 pt-1">
                  {['Explain', 'Simplify', 'Expand', 'Quiz', 'Flashcards'].map((btn) => (
                    <button
                      key={btn}
                      className="px-2.5 py-1 rounded bg-surface-800 hover:bg-surface-700 border border-surface-700 text-[11px] text-slate-300 font-medium transition-colors"
                    >
                      {btn}
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* 3. CHAT TAB */}
            {activeTab === 'chat' && (
              <div className="h-full flex flex-col space-y-3">
                {/* Starter Suggestions */}
                {chatMessages.length === 0 && (
                  <div className="space-y-2 mb-2">
                    <p className="text-[11px] text-slate-400 font-medium">Suggested queries:</p>
                    <div className="flex flex-wrap gap-1.5">
                      {starterQuestions.map((q) => (
                        <button
                          key={q}
                          onClick={() => handleSendChat(q)}
                          className="px-2.5 py-1 rounded-lg bg-surface-800 hover:bg-surface-700 border border-surface-700 text-[11px] text-slate-300 transition-colors text-left"
                        >
                          {q}
                        </button>
                      ))}
                    </div>
                  </div>
                )}

                {/* Message Log */}
                <div className="flex-1 overflow-y-auto space-y-3">
                  {chatMessages.map((m) => (
                    <div
                      key={m.id}
                      className={`p-3 rounded-xl text-xs space-y-2 ${
                        m.role === 'user'
                          ? 'bg-brand-600/30 border border-brand-500/40 text-white ml-6'
                          : 'bg-surface-800/90 border border-surface-700 text-slate-200 mr-6'
                      }`}
                    >
                      <p className="leading-relaxed whitespace-pre-wrap">{m.content}</p>

                      {/* Evidence Citations */}
                      {m.evidence_citations && m.evidence_citations.length > 0 && (
                        <div className="pt-2 border-t border-surface-700/60 space-y-1">
                          <span className="text-[10px] font-semibold text-brand-400 uppercase tracking-wider block">
                            Evidence & Timestamps:
                          </span>
                          <div className="flex flex-wrap gap-1.5">
                            {m.evidence_citations.map((c, idx) => (
                              <button
                                key={idx}
                                onClick={() => handleSeek(c.timestamp_start)}
                                className="px-2 py-0.5 rounded bg-surface-700 hover:bg-brand-600 text-[10px] font-mono text-slate-300 hover:text-white transition-colors"
                              >
                                [{formatTimestamp(c.timestamp_start)}]
                              </button>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  ))}
                </div>

                {/* Input form */}
                <form
                  onSubmit={(e) => {
                    e.preventDefault();
                    handleSendChat();
                  }}
                  className="flex items-center gap-2 pt-2 border-t border-surface-700"
                >
                  <input
                    type="text"
                    value={chatInput}
                    onChange={(e) => setChatInput(e.target.value)}
                    placeholder="Ask about this video (e.g. What did the speaker say about...)"
                    className="flex-1 px-3 py-2 rounded-xl bg-surface-800 border border-surface-700 text-xs text-white placeholder-slate-500 outline-none focus:border-brand-500"
                  />
                  <button
                    type="submit"
                    disabled={isSendingChat || !chatInput.trim()}
                    className="p-2 rounded-xl bg-brand-600 hover:bg-brand-500 disabled:opacity-50 text-white transition-colors"
                  >
                    <Send className="w-3.5 h-3.5" />
                  </button>
                </form>
              </div>
            )}
          </div>
        </section>
      </div>
    </div>
  );
};
