import { useEffect, useState } from "react";
import { View, Text, Pressable, ActivityIndicator } from "react-native";
import { getMe, getSessions } from "../services/api";
import { useStore } from "../store/useStore";

export default function ProfileScreen() {
  const token = useStore((state) => state.token);
  const logout = useStore((state) => state.logout);

  const [user, setUser] = useState<any>(null);
  const [shotsAnalyzed, setShotsAnalyzed] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadProfile = async () => {
      if (!token) return;

      try {
        setLoading(true);
        setError("");

        const [userData, sessions] = await Promise.all([
          getMe(token),
          getSessions(token)
        ]);

        setUser(userData);
        setShotsAnalyzed(sessions.length);

      } catch (err) {
        setError("Couldn't load profile information.");
      } finally {
        setLoading(false);
      }
    };

    loadProfile();
  }, [token]);

  if (loading) {
    return (
      <View className="flex-1 justify-center items-center">
        <ActivityIndicator size="large" />
      </View>
    );
  }

  if (error) {
    return (
      <View className="flex-1 justify-center items-center p-6">
        <Text>{error}</Text>
      </View>
    );
  }

  return (
    <View className="flex-1 p-6">
      <Text className="text-2xl font-semibold mb-6">Profile</Text>

      <Text className="text-lg font-semibold mb-4">
        Account Information
      </Text>

      <Text className="mb-2">Name: {user?.name ?? "—"}</Text>
      <Text className="mb-2">Email: {user?.email ?? "—"}</Text>
      <Text className="mb-2">Username: {user?.username ?? "—"}</Text>

      <View className="mt-6">
        <Text className="text-lg font-semibold mb-2">
          Activity
        </Text>
        <Text>Shots analyzed: {shotsAnalyzed}</Text>
      </View>

      <Pressable
        onPress={logout}
        className="mt-8 bg-red-600 rounded-lg p-4"
      >
        <Text className="text-white text-center font-semibold">
          Log out
        </Text>
      </Pressable>
    </View>
  );
}