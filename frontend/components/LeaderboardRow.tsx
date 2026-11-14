import React from 'react';
import { View, Text } from 'react-native';
import type { Row } from '../services/leaderboardApi';

type Props = {
  row: Row;
};

export default function LeaderboardRow({ row }: Props) {
  const rankLabel = row.rank === null ? '–' : String(row.rank);

  const containerClass = row.is_me
    ? 'flex-row items-center rounded-card border border-success bg-success/10 px-4 py-3 mb-2'
    : 'flex-row items-center rounded-card border border-accent/20 bg-white px-4 py-3 mb-2';

  return (
    <View className={containerClass}>
      <Text className="w-8 text-lg font-bold text-primary">{rankLabel}</Text>

      <View className="flex-1">
        <Text className="text-base font-bold text-primary">{row.name}</Text>
        <Text className="text-xs text-accent">
          {row.made}/{row.attempts}
          {row.avg_score !== null ? ` · Form ${row.avg_score}` : ''}
        </Text>
      </View>

      <Text className="text-2xl font-bold text-primary">{Math.round(row.make_pct)}%</Text>
    </View>
  );
}