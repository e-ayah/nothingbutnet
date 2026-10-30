import { useCallback, useEffect, useState } from 'react';
import { View, Text, ScrollView, TouchableOpacity, useWindowDimensions } from "react-native";
import { useStore } from '../store/useStore'; 
import { getSession } from '../services/api';
import VideoPlayer from '../components/VideoPlayer';
import ScoreCircle from '../components/ScoreCircle';
import AngleCard from '../components/AngleCard';
import FeedbackItem from '../components/FeedbackItem';
import { RANGES } from '../constants/ranges';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';
import Button from '../components/Button';
import { friendlyError } from '../services/errorMessages';
import { useNavigation } from '@react-navigation/native';

export default function ResultsScreen({ route }: { route: any }) {
  const sessionId = route?.params?.sessionId || 'mock-session-id';
  const token = useStore((state: any) => state.token);
  const navigation = useNavigation<any>();
  
  const { width } = useWindowDimensions();
  const isMobile = width < 768;

  const [session, setSession] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(() => {
    getSession(sessionId, token || '')
      .then((data) => { setSession(data); setError(null); })
      .catch((err) => setError(friendlyError(err)))
      .finally(() => setLoading(false));
  }, [sessionId, token]);

  const retry = () => { setLoading(true); load(); };

  useEffect(() => { setLoading(true); load(); }, [load]);

  // check again every 3 seconds while still analyzing
  useEffect(() => {
    if (session?.status !== 'processing') return;
    const id = setInterval(load, 3000);
    return () => clearInterval(id); // stops when done, failed, or the screen closes
  }, [session?.status, load]);

  if (loading) return <LoadingSpinner />;

  if (error || !session) {
    return <ErrorMessage message={error ?? 'Session not found'} onRetry={retry} />;
  }

  if (session.status === 'processing') {
    return <LoadingSpinner message="Still analyzing…" />;
  }

  if (session.status === 'failed') {
    return (
      <View className="flex-1 items-center justify-center p-6 bg-[#FDF6ED]">
        <Text className="text-xl font-bold text-black mb-2">Analysis failed</Text>
        <ErrorMessage message={session.error ?? "We couldn't find a player — film from the side."} />
        {/* filming tip, wording from docs/design/states.md */}
        <Text className="text-base text-black text-center mb-4">Keep your full body visible, then try again.</Text>
        <Button title="Try another video" onPress={() => navigation.navigate('Upload')} />
      </View>
    );
  }

  const hasAngles = session.angles !== undefined && session.angles !== null;
  const videoUri = session.annotated_video_url || session.video_url || '';

  return (
    <ScrollView style={{ flex: 1, backgroundColor: '#FFD3AF' }} contentContainerStyle={{ paddingBottom: 40, alignItems: 'center' }}>
      <View className="flex-1 w-full items-center justify-start px-8 py-10">
        <Text className="text-[42px] font-bold font-sans text-black mt-8 mb-6 text-center">Results</Text>
        <View className={isMobile ? "w-full px-6 justify-between items-stretch flex-col space-y-5" : "w-full px-6 justify-between items-stretch flex-row max-w-[1000px]"}>

          <View className={isMobile ? "w-full space-y-4" : "w-[48%] space-y-4"}>

            <VideoPlayer uri={videoUri} />
            {hasAngles && (
              <View className="w-full space-y-3 pt-2">
                {(Object.keys(RANGES) as (keyof typeof RANGES)[]).map((key) => {
                  const r = RANGES[key];
                  const fb = session.feedback?.find((f: any) => f.checkpoint === r.checkpoint);
                  return (
                    <AngleCard
                      key={key}
                      name={r.label}
                      value={session.angles?.[key] ?? null}
                      min={r.min}
                      max={r.max}
                      status={fb?.status ?? 'needs_work'}
                    />
                  );
                })}
              </View>
            )}

          </View>

          <View className={isMobile ? "w-full space-y-[16px]" : "w-[48%] space-y-[16px]"}>
            
            {/* Form Score*/}
            <View className="w-full bg-[#A34A0040] p-8 rounded-[16px] flex-row items-center justify-start mb-2">
              <ScoreCircle score={session.score ?? null} />
              <View>
                <Text className="text-[48px] font-sans font-bold text-[#A34A00] ml-[24px]">Form</Text>
                <Text className="text-[48px] font-sans font-bold text-[#A34A00] ml-[24px]">Score</Text>
              </View>
            </View>

            {/*Feedback*/}
            <View style={{ backgroundColor: 'rgba(255, 255, 255, 0.5)' }} className="w-full p-6 rounded-2xl flex-1 justify-start">
              <Text className="text-[24px] font-sans font-bold text-[#000000] mb-4">Feedback</Text>
                {session.feedback && session.feedback.length > 0 ? (
                <View className="space-y-3">
                  {session.feedback.map((f: any) => (
                    <FeedbackItem key={f.checkpoint} item={f} />                  ))}
                </View>
              ) : (
                <Text className="text-[18px] text-[#000000]">No feedback comments recorded</Text>
              )}
            </View>
          </View>
        </View>

        <View className={isMobile ? "w-full justify-center px-6 mt-10 flex-col space-y-3 items-center" : "flex-row space-x-12 mt-10 w-full justify-center max-w-[1000px] px-6"}>
          {!isMobile && (
            <TouchableOpacity className="bg-[#A34A00] px-10 py-3 rounded-xl mr-[25rem]">
              <Text className="text-white text-base font-sans font-bold">Back</Text>
            </TouchableOpacity>
          )}
          <TouchableOpacity className={isMobile ? "bg-[#A34A00] py-4 rounded-2xl items-center justify-center w-full max-w-[340px]" : "bg-[#A34A00] px-10 py-3 rounded-xl"}>
            <Text className="text-white text-base font-sans font-bold">Continue</Text>
          </TouchableOpacity>
        </View>
      </View>
    </ScrollView>
  );
}