import { useCallback, useState } from "react";
import { View, Text, ScrollView, TouchableOpacity } from "react-native";
import { useFocusEffect } from "@react-navigation/native";

import * as api from "../services/api";
import type { SessionSummary } from "../services/types";
import { useStore } from "../store/useStore";
import { friendlyError } from "../services/errorMessages";

import { getRecurring, type RecurringMistake } from "../services/insightsApi";

import RecurringMistakeCard from "../components/RecurringMistakeCard";
import LoadingSpinner from "../components/LoadingSpinner";
import ErrorMessage from "../components/ErrorMessage";
import EmptyState from "../components/EmptyState";

// Shared brown button used everywhere on this screen
function BrownButton({
  title,
  onPress,
  big = false,
  className = "",
}: {
  title: string;
  onPress: () => void;
  big?: boolean;
  className?: string;
}) {
  return (
    <TouchableOpacity
      onPress={onPress}
      className={`min-h-[56px] bg-[#A34A00] rounded-xl items-center justify-center px-4 py-3 ${
        big ? "w-full min-h-[64px]" : ""
      } ${className}`}
    >
      <Text
        className={`font-sans font-bold text-white text-center ${
          big ? "text-xl" : "text-lg"
        }`}
      >
        {title}
      </Text>
    </TouchableOpacity>
  );
}

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
  const greeting = firstName ? `Welcome back, ${firstName}!` : "Welcome back!";

  const latestScore = (latest as any)?.score;

  return (
    <View className="flex-1 bg-[#FFD3AF]">
      <ScrollView
        contentContainerStyle={{
          flexGrow: 1,
          justifyContent: "center",
          alignItems: "center",
          paddingHorizontal: 24,
          paddingVertical: 40,
        }}
      >
        <View className="w-full max-w-[460px] items-center">
          <Text className="font-sans font-bold text-[36px] text-black text-center mb-8">
            {greeting}
          </Text>

          <BrownButton title="Analyze a shot" onPress={goUpload} big />

          {/* Latest score + History */}
          <View className="w-full flex-row gap-2 mt-2">
            {!loading && !error && latest && (
              <BrownButton
                title={`Latest score: ${latestScore ?? "—"}`}
                onPress={() =>
                  navigation.navigate("Results", { sessionId: latest.session_id })
                }
                className="flex-1"
              />
            )}
            <BrownButton
              title="History"
              onPress={() => navigation.navigate("History")}
              className="flex-1"
            />
          </View>

          {/* Loading / error / empty states */}
          {loading && (
            <View className="w-full mt-6">
              <LoadingSpinner />
            </View>
          )}
          {!loading && error && (
            <View className="w-full mt-6">
              <ErrorMessage message={error} onRetry={load} />
            </View>
          )}
          {!loading && !error && !latest && (
            <View className="w-full mt-6">
              <EmptyState
                title="No shots yet"
                message="Analyze your first free throw. Your past shots will appear here."
                actionLabel="Analyze a shot"
                onAction={goUpload}
              />
            </View>
          )}

          {/* Recurring mistakes */}
          {!loading && !error && recurringMistakes.length > 0 && (
            <View className="w-full mt-6 gap-4">
              {recurringMistakes.map((mistake) => (
                <RecurringMistakeCard
                  key={mistake.checkpoint}
                  mistake={mistake}
                />
              ))}
            </View>
          )}

          {/* Remaining navigation buttons */}
          <View className="w-full flex-row flex-wrap gap-2 mt-2">
            <BrownButton
              title="Progress"
              onPress={() => navigation.navigate("Progress")}
              className="flex-1 min-w-[45%]"
            />
            <BrownButton
              title="Profile"
              onPress={() => navigation.navigate("Profile")}
              className="flex-1 min-w-[45%]"
            />
            <BrownButton
              title="Friends"
              onPress={() => navigation.navigate("Friends")}
              className="flex-1 min-w-[45%]"
            />
            <BrownButton
              title="Leaderboard"
              onPress={() => navigation.navigate("Leaderboard")}
              className="flex-1 min-w-[45%]"
            />
            <BrownButton
              title="Compare"
              onPress={() => navigation.navigate("Compare")}
              className="flex-1 min-w-[45%]"
            />
          </View>
        </View>
      </ScrollView>
    </View>
  );
}