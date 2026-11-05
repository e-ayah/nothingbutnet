import { useEffect, useRef, useState } from 'react';
import * as ImagePicker from 'expo-image-picker';
import { Platform, Text, View } from 'react-native';
import { useVideoPlayer, VideoView } from 'expo-video';
import { useStore } from '../store/useStore';
import { uploadVideo, analyze, getSession } from '../services/api';
import { Screen } from '../components/Screen';
import Button from '../components/Button';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';

const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));

export default function UploadScreen({ navigation }: any) {
    const token = useStore((s) => s.token);
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

    return (
    <Screen scroll>
      <Button title="Choose video" onPress={pick} />
      <Button title="Record" onPress={record} />

      {error ? <Text>{error}</Text> : null}

      {video && (
        <VideoView player={player} style={{ width: '100%', height: 240 }} />
      )}

      <View>
        <Text>Filming tips</Text>
        <Text>• Film from the side</Text>
        <Text>• Keep your whole body in frame</Text>
      </View>

      <Button
        title="Upload"
        onPress={upload}
        loading={stage === 'uploading'}
        disabled={!video || stage === 'uploading'}
      />
      {stage === 'uploading' && <Text>{`Uploading… ${progress}%`}</Text>}
    </Screen>
  );
}