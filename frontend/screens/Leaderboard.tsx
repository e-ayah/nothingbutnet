import React, { useCallback, useState } from 'react';
import { View, Text, FlatList, Pressable } from 'react-native';
import { useFocusEffect, useNavigation } from '@react-navigation/native';
import { useStore } from '../store/useStore';
import { getLeaderboard } from '../services/leaderboardApi';
import type { Row } from '../services/leaderboardApi';
import { friendlyError } from '../services/errorMessages';
import LeaderboardRow from '../components/LeaderboardRow';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';
import EmptyState from '../components/EmptyState';

type Period = 'week' | 'all';

const TABS: { key: Period; label: string }[] = [
  { key: 'week', label: 'This week' },
  { key: 'all', label: 'All time' },
];

export default function Leaderboard() {
  const navigation = useNavigation<any>();
  const token = useStore((s) => s.token);

  const [period, setPeriod] = useState<Period>('week');
  const [rows, setRows] = useState<Row[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      setRows(await getLeaderboard(period, token));
    } catch (err) {
      setError(friendlyError(err));
    } finally {
      setLoading(false);
    }
  }, [period, token]);

  // Runs when the screen opens, and again whenever the tab (period) changes
  useFocusEffect(
    useCallback(() => {
      load();
    }, [load])
  );

  const ranked = rows.filter((r) => r.rank !== null);
  const unranked = rows.filter((r) => r.rank === null);

  let content;
  if (loading) {
    content = <LoadingSpinner />;
  } else if (error) {
    content = <ErrorMessage message={error} onRetry={load} />;
  } else if (rows.length === 0) {
    content = (
      <EmptyState
        title="No friends yet"
        message="Add friends to see how you stack up."
        actionLabel="Go to Friends"
        onAction={() => navigation.navigate('Friends')}
      />
    );
  } else {
    content = (
      <FlatList
        data={ranked}
        keyExtractor={(item) => item.user_id}
        renderItem={({ item }) => <LeaderboardRow row={item} />}
        ListFooterComponent={
          unranked.length > 0 ? (
            <View className="mt-4">
              <Text className="mb-2 text-sm text-accent">Not ranked yet — 5 shots needed</Text>
              {unranked.map((r) => (
                <LeaderboardRow key={r.user_id} row={r} />
              ))}
            </View>
          ) : undefined
        }
      />
    );
  }

  return (
    <View className="flex-1 bg-background px-4 pt-12">
      <Text className="text-3xl font-bold text-primary">Leaderboard</Text>
      <Text className="mb-4 text-xs text-accent">Makes are self-reported</Text>

      <View className="mb-4 flex-row">
        {TABS.map((tab) => {
          const active = tab.key === period;
          return (
            <Pressable
              key={tab.key}
              onPress={() => setPeriod(tab.key)}
              className={`mr-2 rounded-full px-4 py-2 ${active ? 'bg-primary' : 'bg-white border border-accent/20'}`}
            >
              <Text className={active ? 'text-white font-bold' : 'text-primary'}>{tab.label}</Text>
            </Pressable>
          );
        })}
      </View>

      {content}
    </View>
  );
}