import { useEffect, useRef, useState } from 'react';
import * as ImagePicker from 'expo-image-picker';
import { Platform, Text, TouchableOpacity, useWindowDimensions, View } from 'react-native';
import { useVideoPlayer, VideoView } from 'expo-video';
import { useStore } from '../store/useStore';
import { uploadVideo, analyze, getSession } from '../services/api';
import { Screen } from '../components/Screen';
import Button from '../components/Button';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';

const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));

const TIPS = [
  'Face shooting side to camera',
  'Keep your full body in frame',
  'Keep your phone steady',
  'Use good lighting',
];

export default function UploadScreen({ navigation }: any) {
    const token = useStore((s) => s.token);
    const { width } = useWindowDimensions();
    const isWide = width >= 768;

    const [video, setVideo] = useState<ImagePicker.ImagePickerAsset | null>(null);
    const [error, setError] = useState('');
    const [progress, setProgress] = useState(0);
    const [stage, setStage] = useState<'idle' | 'uploading' | 'analyzing' | 'error'>('idle');
    const [uploadError, setUploadError] = useState<unknown>(null);
    const cancelled = useRef(false);
    useEffect(() => () => { cancelled.current = true; }, []); // stop when the screen closes
    const player = useVideoPlayer(video?.uri ?? null);
    
    const pick = async () => {
    const perm = await ImagePicker.requestMediaLibraryPermissionsAsync();
    if (!perm.granted) return setError('Allow photo access to choose a video.');
    const res = await ImagePicker.launchImageLibraryAsync({ mediaTypes: ['videos'] });
    if (!res.canceled) setVideo(res.assets[0]); // { uri, ... }
    };

    const record = async () => { //camera code
    const perm = await ImagePicker.requestCameraPermissionsAsync();
    if (!perm.granted) return setError('Allow camera access to record a video.');
    const res = await ImagePicker.launchCameraAsync({ mediaTypes: ['videos'] });
    if (!res.canceled) setVideo(res.assets[0]);
    };

    const buildForm = async (uri: string) => {
    const form = new FormData();
    if (Platform.OS === 'web') {
        const blob = await (await fetch(uri)).blob(); // web needs a Blob
        form.append('file', blob, 'shot.mp4');
    } else {
        form.append('file', { uri, name: 'shot.mp4', type: 'video/mp4' } as unknown as Blob); // React Native accepts this shape
    }
    return form;
    };

    const waitForResult = async (sessionId: string) => {
    for (let i = 0; i < 100; i++) { // about 5 minutes
        if (cancelled.current) return null;
        const s = await getSession(sessionId, token ?? '');
        if (s.status === 'done') return s;
        if (s.status === 'failed') throw new Error(s.error ?? "We couldn't analyze this video.");
        await sleep(3000);
    }
    throw new Error('This is taking longer than usual. Check History in a few minutes.');
    };

    const upload = async () => {
    if (!video) return;
    setStage('uploading');
    setError('');
    try {
        const form = await buildForm(video.uri);
        const up = await uploadVideo(form, token ?? '', (p: number) => setProgress(p));
        setStage('analyzing');
        // Start analysis but don't wait for it here — the status check below does the waiting.
        analyze(up.session_id, up.video_url, token ?? '').catch((e) => {
            if (e?.response) { setUploadError(e); setStage('error'); } // a real error from the server
            // no response (e.g. a timeout) → keep checking the status
        });
        const done = await waitForResult(up.session_id);
        if (done) navigation.navigate('Results', { sessionId: up.session_id });
    } catch (e) {
        setUploadError(e);
        setStage('error');
    }
    };

    const reset = () => {
    setVideo(null);
    setProgress(0);
    setError('');
    setUploadError(null);
    setStage('idle');
    };

    const goBack = () => {
      if (navigation.canGoBack()) navigation.goBack();
      else navigation.navigate('Home');
    };

    if (stage === 'analyzing') {
    return (
        <Screen>
          <LoadingSpinner message="Analyzing your shot… this can take a few minutes" />
        </Screen>
    );
    }

    if (stage === 'error') {
    return (
        <Screen>
          <ErrorMessage error={uploadError} onRetry={reset} />
        </Screen>
    );
    }

    const uploading = stage === 'uploading';
    const canUpload = !!video && !uploading;

    const title = (
      <Text className="font-sans font-bold text-[32px] text-black text-center">
        Upload Your Video
      </Text>
    );

    const pickButtons = (
      <View className="flex-row w-full gap-3">
        <TouchableOpacity
          onPress={pick}
          disabled={uploading}
          className="flex-1 min-h-[44px] bg-[#A34A00] rounded-xl items-center justify-center px-4 py-3"
        >
          <Text className="font-sans font-bold text-base text-white">Choose Video</Text>
        </TouchableOpacity>
        <TouchableOpacity
          onPress={record}
          disabled={uploading}
          className="flex-1 min-h-[44px] bg-[#A34A00] rounded-xl items-center justify-center px-4 py-3"
        >
          <Text className="font-sans font-bold text-base text-white">Record</Text>
        </TouchableOpacity>
      </View>
    );

    const errorText = error ? (
      <Text className="font-sans text-base text-red-600">{error}</Text>
    ) : null;

    const tips = (
      <View className="w-full bg-white/50 rounded-2xl p-6">
        <Text className="font-sans font-bold text-xl text-black text-center mb-4">Filming Tips</Text>
        <View className="gap-3 px-2">
          {TIPS.map((t) => (
            <Text key={t} className="font-sans text-base text-black">{`•  ${t}`}</Text>
          ))}
        </View>
      </View>
    );

    const preview = (
      <View
        className={`w-full bg-[#A34A00]/25 rounded-2xl items-center justify-center overflow-hidden ${
          isWide ? 'min-h-[320px]' : 'min-h-[160px]'
        }`}
      >
        {video ? (
          <VideoView player={player} style={{ width: '100%', height: isWide ? 320 : 220 }} />
        ) : (
          <View className="p-6 items-center">
            <Text className="font-sans font-bold text-xl text-[#3F3F3F] text-center mb-3">Video Preview</Text>
            <Text className="font-sans text-base text-[#3F3F3F] text-center">
              Once uploaded, a preview of your video will appear here.
            </Text>
          </View>
        )}
      </View>
    );

    const progressBlock = uploading ? (
      <View className="w-full mb-2">
        <Text className="font-sans text-sm text-[#3F3F3F] mb-1">{`Uploading… ${progress}%`}</Text>
        <View className="w-full h-2 rounded-full bg-[#A34A00]/25 overflow-hidden">
          <View
            className="h-2 rounded-full bg-[#A34A00]"
            style={{ width: `${Math.min(100, Math.max(0, progress))}%` }}
          />
        </View>
      </View>
    ) : null;

    const uploadButton = (
      <TouchableOpacity
        onPress={upload}
        disabled={!canUpload}
        className={`w-full min-h-[48px] bg-[#A34A00] rounded-xl items-center justify-center px-6 py-3 ${
          canUpload ? '' : 'opacity-50'
        }`}
      >
        <Text className="font-sans font-bold text-xl text-white">
          {uploading ? 'Uploading…' : 'Upload Video'}
        </Text>
      </TouchableOpacity>
    );

    // ---------- WIDE (laptop / web) ----------
    if (isWide) {
      return (
        <Screen scroll>
          <View className="w-full max-w-[1000px] self-center px-6 py-10">
            <View className="mb-10">{title}</View>

            <View className="flex-row gap-6">
              <View className="w-[40%] gap-4">
                {pickButtons}
                {errorText}
                {tips}
              </View>
              <View className="flex-1">{preview}</View>
            </View>

            <View className="flex-row items-end gap-6 mt-8">
              <View className="w-[40%] items-center">
                <TouchableOpacity
                  onPress={goBack}
                  className="min-h-[48px] bg-[#A34A00] rounded-xl items-center justify-center px-10 py-3"
                >
                  <Text className="font-sans font-bold text-xl text-white">Back</Text>
                </TouchableOpacity>
              </View>
              <View className="flex-1">
                {progressBlock}
                {uploadButton}
              </View>
            </View>
          </View>
        </Screen>
      );
    }

    // ---------- NARROW (phone, 375 px) ----------
    return (
      <Screen scroll>
        <View className="w-full px-4 pt-4 pb-8 gap-4">
          <View className="flex-row items-center">
            <TouchableOpacity
              onPress={goBack}
              accessibilityLabel="Go back"
              className="w-11 h-11 rounded-full bg-[#A34A00]/25 items-center justify-center"
            >
              <Text className="font-sans font-bold text-xl text-black">‹</Text>
            </TouchableOpacity>
          </View>
          {title}
          {pickButtons}
          {errorText}
          {preview}
          {tips}
          <View>
            {progressBlock}
            {uploadButton}
          </View>
        </View>
      </Screen>
    );
}