import { useEffect, useState } from 'react';
import { View, Text, ScrollView, TouchableOpacity, useWindowDimensions } from "react-native";
import { useStore } from '../store/useStore'; 
import { getSession } from '../services/api';
import VideoPlayer from '../components/VideoPlayer';

export default function ResultsScreen({ route }: { route: any }) {
  const sessionId = route?.params?.sessionId || 'mock-session-id';
  const token = useStore((state: any) => state.token);
  
  const { width } = useWindowDimensions();
  const isMobile = width < 768;

  const [session, setSession] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let ignore = false;
    setLoading(true);
    setError(null);

  getSession(sessionId, token || '')
  .then((data) => {
    if (!ignore) {
      setSession(data);
      setLoading(false);
    }
  })
  .catch((err) => {
      if (!ignore) {
        setError(err?.message || 'Failed to fetch analysis details');
        setLoading(false);
      }
    });
    return () => {
      ignore = true;
    };
  }, [sessionId, token]);

  if (loading) {
    return (
      <View className="flex-1 items-center justify-center bg-[#FDF6ED]">
        <Text className="text-lg font-bold text-amber-950">Loading…</Text>
      </View>
    );
  }

  if (error || !session) {
    return (
      <View className="flex-1 items-center justify-center p-6 bg-[#FDF6ED]">
        <Text className="text-lg font-medium text-red-600 text-center">
          {error || 'Session not found'}
        </Text>
      </View>
    );
  }

  const hasAngles = session.angles !== undefined && session.angles !== null;
  const rawUri = session.annotated_video_url || session.video_url || '';
  const videoUri = (rawUri.includes('file-examples.com') || rawUri === '')
    ? 'local-fallback'
    : rawUri;

  const currentScore = session.score ?? '--';
  const elbowAngle = session.angles?.elbow_angle ?? '--';
  const shoulderAngle = session.angles?.shoulder_angle ?? '--';
  const kneeAngle = session.angles?.knee_angle ?? '--';

  const isElbowOptimal = typeof elbowAngle === 'number' && elbowAngle >= 85 && elbowAngle <= 100;
  const isShoulderOptimal = typeof shoulderAngle === 'number' && shoulderAngle >= 45 && shoulderAngle <= 75;
  const isKneeOptimal = typeof kneeAngle === 'number' && kneeAngle >= 150 && kneeAngle <= 175;

  return (
    <ScrollView style={{ flex: 1, backgroundColor: '#FFD3AF' }} contentContainerStyle={{ paddingBottom: 40, alignItems: 'center' }}>
      <View className="flex-1 w-full items-center justify-start px-8 py-10">
        <Text className="text-[42px] font-bold font-sans text-black mt-8 mb-6 text-center">Results</Text>
        <View className={isMobile ? "w-full px-6 justify-between items-stretch flex-col space-y-5" : "w-full px-6 justify-between items-stretch flex-row max-w-[1000px]"}>

          <View className={isMobile ? "w-full space-y-4" : "w-[48%] space-y-4"}>

            <VideoPlayer uri={videoUri} />
            {hasAngles && (
              <View className="flex-row justify-between w-full space-x-2 pt-2 pb-2">
                {/* Elbow Card */}
                <View className={isElbowOptimal 
                  ? "flex-1 bg-[#00D75A80] p-3 rounded-xl items-center justify-center" 
                  : "flex-1 bg-[#D79E0080] p-3 rounded-xl items-center justify-center"}
                >
                  <Text className="text-[11px] font-bold font-sans text-white text-center mb-1">Elbow Angle:</Text>
                  <Text className="text-lg font-bold font-sans text-white">{elbowAngle}°</Text>
                </View>

                {/* Shoulder Card */}
                <View className={isShoulderOptimal 
                  ? "flex-1 bg-[#00D75A80] p-3 rounded-xl items-center justify-center ml-2 mr-2" 
                  : "flex-1 bg-[#D79E0080] p-3 rounded-xl items-center justify-center ml-2 mr-2"}
                >
                  <Text className="text-[11px] font-bold font-sans text-white text-center mb-1">Shoulder Angle:</Text>
                  <Text className="text-lg font-bold font-sans text-white">{shoulderAngle}°</Text>
                </View>

                {/* Knee Card */}
                <View className={isKneeOptimal 
                  ? "flex-1 bg-[#00D75A80] p-3 rounded-xl items-center justify-center" 
                  : "flex-1 bg-[#D79E0080] p-3 rounded-xl items-center justify-center"}
                >
                  <Text className="text-[11px] font-bold font-sans  text-white text-center mb-1">Knee Angle:</Text>
                  <Text className="text-lg font-bold font-sans text-white">{kneeAngle}°</Text>
                </View>
              </View>
            )}

          </View>

          <View className={isMobile ? "w-full space-y-[16px]" : "w-[48%] space-y-[16px]"}>
            
            {/* Form Score*/}
            <View className="w-full bg-[#A34A0040] p-8 rounded-[16px] flex-row items-center justify-start mb-2">
              <View className="w-32 h-32 rounded-full border-8 border-[#A34A00] items-center justify-center bg-white/20">
                  <Text className="text-[36px] font-sans font-bold text-[#A34A00]">{currentScore}</Text>
                </View>
              <View>
                <Text className="text-[48px] font-sans font-bold text-[#A34A00] ml-[24px]">Form</Text>
                <Text className="text-[48px] font-sans font-bold text-[#A34A00] ml-[24px]">Score</Text>
              </View>
            </View>

            {/*Feedback*/}
            <View style={{ backgroundColor: 'rgba(255, 255, 255, 0.5)' }} className="w-full p-6 rounded-2xl flex-1 justify-start">
              <Text className="text-[24px] font-sans font-bold text-[#000000] mb-4">Feedback</Text>
                {session.feedback && Array.isArray(session.feedback) && session.feedback.length > 0 ? (
                  <View className="space-y-3">
                  {session.feedback.map((tip: any, index: number) => (
                    <Text key={index} className="text-[18px] text-[#000000] leading-relaxed">
                      • {tip.tip || tip.message || tip.text || String(tip)}
                    </Text>
                  ))}
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