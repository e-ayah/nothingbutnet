
import { useCallback, useState } from "react";
import { View, Text, ScrollView } from "react-native";
import { useFocusEffect } from "@react-navigation/native";

import * as api from "../services/api";
import type { SessionSummary } from "../services/types";
import { useStore } from "../store/useStore";
import { friendlyError } from "../services/errorMessages";

import { getRecurring, type RecurringMistake } from "../services/insightsApi";

import Button from "../components/Button";
import SessionCard from "../components/SessionCard";
import RecurringMistakeCard from "../components/RecurringMistakeCard";
import LoadingSpinner from "../components/LoadingSpinner";
import ErrorMessage from "../components/ErrorMessage";
import EmptyState from "../components/EmptyState";

export default function HomeScreen({ navigation }: any) {
  const token = useStore((s) => s.token);
  const user = useStore((s) => s.user);

  const [latest, setLatest] = useState<SessionSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Store recurring mistakes
  const [recurringMistakes, setRecurringMistakes] =
    useState<RecurringMistake[]>([]);

  const load = useCallback(async () => {
    try {
      setError(null);

      // Get latest sessions
      const sessions = await api.getSessions(token ?? "");

      const newest = [...sessions].sort((a, b) =>
        b.created_at.localeCompare(a.created_at)
      )[0];

      setLatest(newest ?? null);

      // Get recurring mistakes
      try {
        const mistakes = await getRecurring(token ?? "");
        setRecurringMistakes(mistakes);
      } catch (e) {
        console.error("Failed to load recurring mistakes:", e);
        setRecurringMistakes([]);
      }

    } catch (e) {
      setError(friendlyError(e));
    } finally {
      setLoading(false);
    }
  }, [token]);

  useFocusEffect(
    useCallback(() => {
      load();
    }, [load])
  );

  const goUpload = () => navigation.navigate("Upload");

  const firstName = user?.name?.split(" ")[0];
  const greeting = firstName ? `Hi, ${firstName}` : "Hi there";

  let latestSection;

  if (loading) {
    latestSection = <LoadingSpinner />;
  } else if (error) {
    latestSection = <ErrorMessage message={error} onRetry={load} />;
  } else if (!latest) {
    latestSection = (
      <EmptyState
        title="No shots yet"
        message="Analyze your first free throw. Your past shots will appear here."
        actionLabel="Analyze a shot"
        onAction={goUpload}
      />
    );
  } else {
    latestSection = (
      <SessionCard
        {...latest}
        onPress={() =>
          navigation.navigate("Results", { sessionId: latest.session_id })
        }
      />
    );
  }

  return (
    <ScrollView
      className="flex-1 bg-background px-6 pt-6"
      contentContainerStyle={{ paddingBottom: 30 }}
    >
      <Text className="text-2xl font-bold text-primary">{greeting}</Text>

      <View className="mt-6">
        <Button title="Analyze a shot" onPress={goUpload} />
      </View>

      {/* Latest result */}
      <View className="mt-6 h-40">
        {latestSection}
      </View>

      {/* Recurring mistakes */}
      {!loading && !error && recurringMistakes.length > 0 && (
        <View className="mt-4 gap-4">
          {recurringMistakes.map((mistake) => (
            <RecurringMistakeCard
              key={mistake.checkpoint}
              mistake={mistake}
            />
          ))}
        </View>
      )}

      {/* Navigation links */}
      <View className="mt-10 flex-row flex-wrap justify-around gap-3">
        <Button
          title="History"
          variant="secondary"
          onPress={() => navigation.navigate("History")}
        />

        <Button
          title="Progress"
          variant="secondary"
          onPress={() => navigation.navigate("Progress")}
        />

        <Button
          title="Profile"
          variant="secondary"
          onPress={() => navigation.navigate("Profile")}
        />

        <Button
          title="Friends"
          variant="secondary"
          onPress={() => navigation.navigate("Friends")}
        />

        <Button
          title="Leaderboard"
          variant="secondary"
          onPress={() => navigation.navigate("Leaderboard")}
        />

        <Button
          title="Compare"
          variant="secondary"
          onPress={() => navigation.navigate("Compare")}
        />
      </View>
    </ScrollView>
  );
}
