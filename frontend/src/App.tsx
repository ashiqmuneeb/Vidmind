import { useState } from 'react';
import { QueryClient, QueryClientProvider, useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Navbar } from './components/Navbar';
import { HomePage } from './pages/HomePage';
import { WorkspacePage } from './pages/WorkspacePage';
import { SettingsPage } from './pages/SettingsPage';
import { Video } from './types';
import * as api from './services/api';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

function VidMindApp() {
  const [currentTab, setCurrentTab] = useState<'home' | 'workspace' | 'settings'>('home');
  const [selectedVideo, setSelectedVideo] = useState<Video | null>(null);

  // Queries
  const { data: health } = useQuery({
    queryKey: ['health'],
    queryFn: api.fetchHealth,
    refetchInterval: 30000,
  });

  const { data: videosData, isLoading: isLoadingVideos } = useQuery({
    queryKey: ['videos'],
    queryFn: api.fetchVideos,
  });

  const queryClientLocal = useQueryClient();

  const addVideoMutation = useMutation({
    mutationFn: (url: string) => api.createVideo({ url }),
    onSuccess: (newVideo) => {
      queryClientLocal.invalidateQueries({ queryKey: ['videos'] });
      setSelectedVideo(newVideo);
      setCurrentTab('workspace');
    },
  });

  const deleteVideoMutation = useMutation({
    mutationFn: (id: string) => api.deleteVideo(id),
    onSuccess: () => {
      queryClientLocal.invalidateQueries({ queryKey: ['videos'] });
      if (selectedVideo) setSelectedVideo(null);
    },
  });

  const handleSelectVideo = (videoId: string) => {
    const found = videosData?.videos.find((v) => v.id === videoId);
    if (found) {
      setSelectedVideo(found);
      setCurrentTab('workspace');
    }
  };

  return (
    <div className="min-h-screen bg-surface-900 text-slate-100 flex flex-col font-sans">
      <Navbar
        currentTab={currentTab}
        setCurrentTab={setCurrentTab}
        health={health}
      />

      <main className="flex-1 overflow-x-hidden">
        {currentTab === 'home' && (
          <HomePage
            videos={videosData?.videos || []}
            isLoading={isLoadingVideos}
            onAddVideo={async (url) => {
              await addVideoMutation.mutateAsync(url);
            }}
            onSelectVideo={handleSelectVideo}
            onDeleteVideo={async (id) => {
              await deleteVideoMutation.mutateAsync(id);
            }}
          />
        )}

        {currentTab === 'workspace' && (
          selectedVideo ? (
            <WorkspacePage
              video={selectedVideo}
              onBack={() => setCurrentTab('home')}
            />
          ) : (
            <div className="max-w-xl mx-auto text-center py-24 space-y-4 px-6">
              <h2 className="text-xl font-semibold text-white">No Video Selected</h2>
              <p className="text-sm text-slate-400">
                Please select or analyze a video from your library to open the workspace.
              </p>
              <button
                onClick={() => setCurrentTab('home')}
                className="px-5 py-2.5 rounded-xl bg-brand-600 hover:bg-brand-500 text-white text-sm font-medium transition-colors"
              >
                Go to Library
              </button>
            </div>
          )
        )}

        {currentTab === 'settings' && (
          <SettingsPage health={health} />
        )}
      </main>
    </div>
  );
}

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <VidMindApp />
    </QueryClientProvider>
  );
}
