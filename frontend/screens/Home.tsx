import { useCallback, useState } from "react";
import { View, Text } from "react-native";
import { useFocusEffect } from "@react-navigation/native";

import * as api from "../services/api";
import type { SessionSummary } from "../services/types";
import { useStore } from "../store/useStore";
import { friendlyError } from "../services/errorMessages";
import Button from "../components/Button";
import SessionCard from "../components/SessionCard";
import LoadingSpinner from "../components/LoadingSpinner";
import ErrorMessage from "../components/ErrorMessage";
import EmptyState from "../components/EmptyState";

export default function HomeScreen({ navigation }: any) {
  const token = useStore((s) => s.token);
  const user = useStore((s) => s.user);

  const [latest, setLatest] = useState<SessionSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async () => {
    try {
      setError(null);
      const sessions = await api.getSessions(token ?? "");
      const newest = [...sessions].sort((a, b) =>
        b.created_at.localeCompare(a.created_at)
      )[0];
      setLatest(newest ?? null);
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
    <View className="flex-1 bg-background px-6 pt-6">
      <Text className="text-2xl font-bold text-primary">{greeting}</Text>

      <View className="mt-6">
        <Button title="Analyze a shot" onPress={goUpload} />
      </View>

      <View className="mt-6 h-40">{latestSection}</View>

      <View className="mt-10 flex-row justify-around">
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
      </View>
    </View>
  );
}
