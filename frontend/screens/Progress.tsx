import React, { useState, useCallback } from 'react';
import { View, Text, ScrollView, useWindowDimensions } from 'react-native';
import { useFocusEffect } from '@react-navigation/native';
import { getProgress } from '../services/api';
import { friendlyError } from '../services/errorMessages';
import { useStore } from '../store/useStore';
import { Card } from '../components/Card';

import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';
import EmptyState from '../components/EmptyState';

import { RANGES } from '../constants/ranges';
import ProgressChart from '../components/ProgressChart';

type ProgressData = {
  sessions: any[];
  trends: {
    [key: string]: (number | null)[];
  };
  improvement_summary: string;
};

export default function ProgressScreen() {
  const { width } = useWindowDimensions();
  const token = useStore((s) => s.token);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  
  const [progress, setProgress] = useState<ProgressData | null>(null);

  const fetchProgressData = useCallback(() => {
    if (!token) return;
    setLoading(true);
    setError(null);
    getProgress(token)
      .then((res) => {
        setProgress(res);
        setLoading(false);
      })
      .catch((err) => {
        setError(friendlyError(err));
        setLoading(false);
      });
  }, [token]);

  useFocusEffect(
    useCallback(() => {
      fetchProgressData();
    }, [fetchProgressData])
  );

  if (loading) {
    return (
      <View className="flex-1 justify-center items-center bg-[#FFD3AF]">
        <LoadingSpinner />
      </View>
    );
  }

  if (error) {
    return (
      <View className="flex-1 justify-center items-center bg-[#FFD3AF] p-4">
        <ErrorMessage message={error} onRetry={fetchProgressData} />
      </View>
    );
  }

  if (!progress || !progress.sessions || progress.sessions.length < 2) {
    return (
      <ScrollView className="flex-1 bg-[#FFD3AF]" contentContainerStyle={{ flexGrow: 1 }}>
        <View className="w-full max-w-[480px] mx-auto px-6 flex-1 justify-between pt-16 pb-12">

          <View className="mb-8">
            <Text className="text-[19px] font-bold tracking-widest text-[#A34A00] uppercase mb-1" style={{ fontFamily: 'Inter' }}>
              NOTHINGBUTNET
            </Text>
            <Text className="text-[33px] font-extrabold text-black" style={{ fontFamily: 'Inter' }}>
              Your progress
            </Text>
          </View>

          <EmptyState 
            title="One more session to go"
            message="You have 1 session. Analyze a second session to see how your angles change over time."
            actionLabel="Analyze a shot"
            onAction={() => {
              console.log("Navigate to upload screen");
            }}
          />
        </View>
      </ScrollView>
    );
  }

  return (
    <ScrollView className="flex-1 bg-[#FFD3AF] p-4">
      <View className="w-full max-w-6xl mx-auto my-4">
        <Text className="text-[19px] font-bold tracking-widest text-[#A34A00] uppercase mb-1" style={{ fontFamily: 'Inter' }}>
          NOTHINGBUTNET
        </Text>
        <Text className="text-[33px] font-bold mb-4 text-[#000000]" style={{ fontFamily: 'Inter' }}>
          Your progress
        </Text>

        {progress.improvement_summary ? (
          <View className="mb-6 p-4 bg-[#E8F3EC] rounded-[12px]">
            <Text className="text-[19px] font-bold text-[#1F7A4D]" style={{ fontFamily: 'Inter' }}>
              {progress.improvement_summary}
            </Text>
          </View>
        ) : null}

        <View className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          {(Object.keys(RANGES) as (keyof typeof RANGES)[]).map((key) => (
            <Card key={key} className="bg-white p-5 rounded-[20px]">
              <ProgressChart 
                label={RANGES[key].label} 
                values={progress.trends[key] || []}
                low={RANGES[key].min} 
                high={RANGES[key].max} 
                width={width > 768 ? Math.min((width - 120) / 3, 320) : width - 72}
              />
            </Card>
          ))}
        </View>
      </View>
    </ScrollView>
  );
}