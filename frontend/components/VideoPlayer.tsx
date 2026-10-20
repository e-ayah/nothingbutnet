import { useEffect, useState } from 'react';
import { Text, View, Platform } from 'react-native';
import { useVideoPlayer, VideoView } from 'expo-video';

interface VideoPlayerProps {
  uri: string;
}

export default function VideoPlayer({ uri }: VideoPlayerProps) {
  const player = useVideoPlayer(uri ? { uri } : {}, (playerInstance) => {
  playerInstance.muted = true; 
  playerInstance.loop = true;
  playerInstance.play();
});

  useEffect(() => {
    if (uri && uri.startsWith('http')) {
      player.replace({ uri });
      player.play();
    }
  }, [uri, player]);

  const [status, setStatus] = useState<'loading' | 'ready' | 'error'>('loading');

  useEffect(() => {
    const sub = player.addListener('statusChange', ({ status: playerStatus }) => {
      if (playerStatus === 'readyToPlay') {
        setStatus('ready');
      } else if (playerStatus === 'error') {
        setStatus('error');
      }
    });
    return () => {
      sub.remove();
    };
  }, [player]);

  if (Platform.OS === 'web') {
    const assetSource = require('../assets/demo.mp4');
    const videoSrc = typeof assetSource === 'object' && assetSource.uri ? assetSource.uri : assetSource;

    return (
      <View className="w-full relative bg-black overflow-hidden" style={{ aspectRatio: 16 / 9 }}>
        <video
          src={videoSrc}
          controls
          autoPlay
          muted
          loop
          style={{ width: '100%', height: '100%', objectFit: 'contain' }}
        />
      </View>
    );
  }

  return (
    <View className="w-full relative bg-black overflow-hidden" style={{ aspectRatio: 16 / 9 }}>
      <VideoView 
        player={player} 
        nativeControls 
        style={{ width: '100%', height: '100%' }} 
      />
      
      {status !== 'ready' && (
        <View className="absolute inset-0 flex items-center justify-center bg-black/60 p-4">
          <Text className="text-white text-base font-semibold text-center">
            {status === 'loading' ? 'Loading video…' : "Couldn't load this video"}
          </Text>
        </View>
      )}
    </View>
  );
}