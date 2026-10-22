import { useState } from 'react';
import * as ImagePicker from 'expo-image-picker';
import { Platform, Text, View } from 'react-native';
import { useVideoPlayer, VideoView } from 'expo-video';
import { useStore } from '../store/useStore';
import { uploadVideo } from '../services/api';
import { Screen } from '../components/Screen';
import Button from '../components/Button';

export default function UploadScreen({ navigation }: any) {
    const token = useStore((s) => s.token);
    const [video, setVideo] = useState<ImagePicker.ImagePickerAsset | null>(null);
    const [error, setError] = useState('');
    const [progress, setProgress] = useState(0);
    const [uploading, setUploading] = useState(false);
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

    const upload = async () => {
    if (!video) return;
    setUploading(true);
    setError('');
    try {
        const form = await buildForm(video.uri);
        const result = await uploadVideo(form, token ?? '', (p: number) => setProgress(p));
        navigation.navigate('Results', { sessionId: result.session_id });
    } catch {
        setError('Upload failed. Try again.');
    } finally {
        setUploading(false);
    }
    
    };
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
        loading={uploading}
        disabled={!video || uploading}
      />
      {uploading && <Text>{progress}%</Text>}
    </Screen>
  );
}
