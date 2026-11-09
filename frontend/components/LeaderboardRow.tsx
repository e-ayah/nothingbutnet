import React from 'react';
import { View, Text } from 'react-native';
import type { Row } from '../services/leaderboardApi';

type Props = {
  row: Row;
};

export default function LeaderboardRow({ row }: Props) {
  const rankLabel = row.rank === null ? '–' : String(row.rank);

  // Swap these two class names for the project's green if tailwind.config.js defines one
  const containerClass = row.is_me
    ? 'flex-row items-center rounded-xl border border-green-500 bg-green-100 px-4 py-3 mb-2'
    : 'flex-row items-center rounded-xl border border-gray-200 bg-white px-4 py-3 mb-2';

  return (
    <View className={containerClass}>
      <Text className="w-8 text-lg font-bold text-gray-700">{rankLabel}</Text>

      <View className="flex-1">
        <Text className="text-base font-semibold text-gray-900">{row.name}</Text>
        <Text className="text-xs text-gray-500">
          {row.made}/{row.attempts}
          {row.avg_score !== null ? ` · Form ${row.avg_score}` : ''}
        </Text>
      </View>

      <Text className="text-2xl font-bold text-gray-900">{Math.round(row.make_pct)}%</Text>
    </View>
  );
}