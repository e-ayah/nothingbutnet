
import { useCallback, useEffect, useState } from "react";
import {
  View,
  Text,
  FlatList,
  Pressable,
  ActivityIndicator,
  useWindowDimensions,
  StyleSheet,
} from "react-native";
import Svg, { Line, Polyline, Circle } from "react-native-svg";
import { useNavigation } from "@react-navigation/native";

import * as api from "../services/api";
import { USE_MOCKS } from "../services/config";
import type { SessionSummary } from "../services/types";
import { useStore } from "../store/useStore";
import { useFocusEffect } from '@react-navigation/native';
import LoadingSpinner from "../components/LoadingSpinner";
import ErrorMessage from "../components/ErrorMessage";
import EmptyState from "../components/EmptyState";
import SessionCard from "../components/SessionCard";


const COLORS = {
  peach: "#FFD3AF",
  orange: "#A34A00",
  brown: "#573317",
  card: "#E2B486",
  cream: "#FFF0DF",
  skeleton: "#E8AE7E",
  white: "#FFFFFF",
  black: "#000000",
};

function EmptyView({ onUpload }: { onUpload: () => void }) {
  return (
    <View style={styles.emptyContainer}>
      <Text style={styles.emptyTitle}>No shots yet</Text>

      <Text style={styles.emptyText}>
        Analyze your first free throw.
        {"\n"}
        Your past shots will appear here.
      </Text>

      <Pressable
        onPress={onUpload}
        style={styles.primaryButton}
      >
        <Text style={styles.primaryButtonText}>Analyze a shot</Text>
      </Pressable>
    </View>
  );
}

function LoadingRows() {
  return (
    <View>
      {[1, 2, 3].map((row) => (
        <View key={row} style={styles.sessionRow}>
          <View style={styles.thumbnail} />
          <View style={styles.sessionDetails}>
            <View style={[styles.skeletonLine, { width: "75%" }]} />
            <View style={[styles.skeletonLine, { width: "55%" }]} />
          </View>
        </View>
      ))}
    </View>
  );
}

function ScoreSummary({ sessions }: { sessions: SessionSummary[] }) {
  const s = sessions
    .filter(
      (session) =>
        session.overall_score != null &&
        Number.isFinite(Number(session.overall_score))
    )
    .slice(0, 6)
    .reverse();
  const sortedSessions = [...s].sort(
  (a, b) =>
    new Date(b.created_at).getTime() -
    new Date(a.created_at).getTime()
  );
  const scores = sortedSessions
  const points = scores.map((session) => Number(session.overall_score));
  const chartWidth = 260;
  const chartHeight = 105;
  const padding = 16;

  const minScore = points.length ? Math.min(0, ...points) : 0;
  const maxScore = points.length
    ? Math.max(100, ...points)
    : 100;
  const range = maxScore - minScore || 1;

  const chartPoints = points
    .map((score, index) => {
      const x =
        points.length === 1
          ? chartWidth / 2
          : padding +
            (index * (chartWidth - padding * 2)) /
              (points.length - 1);

      const y =
        chartHeight -
        padding -
        ((score - minScore) / range) *
          (chartHeight - padding * 2);

      return `${x},${y}`;
    })
    .join(" ");

  return (
    <View style={styles.summaryCard}>
      <Text style={styles.sectionTitle}>Score Summary</Text>

      {points.length > 0 ? (
        <View style={styles.chartContainer}>
          <Svg
            width="100%"
            height={chartHeight}
            viewBox={`0 0 ${chartWidth} ${chartHeight}`}
          >
            {[0, 1, 2, 3].map((line) => (
              <Line
                key={line}
                x1={padding}
                x2={chartWidth - padding}
                y1={padding + line * 24}
                y2={padding + line * 24}
                stroke="#E8D8C7"
                strokeWidth={1}
              />
            ))}

            {points.length > 1 && (
              <Polyline
                points={chartPoints}
                fill="none"
                stroke={COLORS.orange}
                strokeWidth={2}
              />
            )}

            {points.map((score, index) => {
              const x =
                points.length === 1
                  ? chartWidth / 2
                  : padding +
                    (index * (chartWidth - padding * 2)) /
                      (points.length - 1);

              const y =
                chartHeight -
                padding -
                ((score - minScore) / range) *
                  (chartHeight - padding * 2);

              return (
                <Circle
                  key={`${index}-${score}`}
                  cx={x}
                  cy={y}
                  r={3}
                  fill={COLORS.orange}
                />
              );
            })}
          </Svg>
        </View>
      ) : (
        <View style={styles.chartPlaceholder}>
          <Text style={styles.summaryPlaceholderText}>
            Your score summary will appear here
            {"\n"}
            after you upload your first video.
          </Text>
        </View>
      )}
    </View>
  );
}

export default function HistoryScreen() {
  const navigation = useNavigation<any>();
  const { width } = useWindowDimensions();
  const isDesktop = width >= 700;

  const token = useStore((state) => state.token);
  //const token = useStore((s) => s.token);
  const load = useCallback(async () => {
    try {
      setError(null);
      const data = await api.getSessions(token);
      setSessions([...data].sort((a, b) => b.created_at.localeCompare(a.created_at)));
    } catch (e) {
      setError(e);
    } finally {
      setLoading(false); setRefreshing(false);
    }
  }, [token]);

  const [sessions, setSessions] = useState<SessionSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState<string | null>(null);



  useEffect(() => {
    load();
  }, [load]);

  const openUpload = () => {
    navigation.navigate("Upload");
  };

  const renderSession = ({ item }: { item: SessionSummary }) => {
    const isProcessing = item.status
      ?.toLowerCase()
      .includes("process");

    return (
      <Pressable
        onPress={() =>
          navigation.navigate("Results", {
            sessionId: item.session_id,
          })
        }
        style={styles.sessionRow}
      >
        <View style={styles.thumbnail} />

        <View style={styles.sessionDetails}>
          <Text style={styles.sessionDate}>
            {new Date(item.created_at).toLocaleString([], {
              month: "long",
              day: "numeric",
              year: "numeric",
              hour: "numeric",
              minute: "2-digit",
            })}
          </Text>

          <Text style={styles.sessionScore}>
            {isProcessing ? "—" : `Form score: ${item.overall_score ?? "—"}`}
          </Text>

          <Text style={styles.sessionStatus}>{item.status}</Text>
        </View>
      </Pressable>
    );
  };
  useFocusEffect(
    useCallback(() => {
      load();
    }, [load])
  );
  const sessionsList = (
    <FlatList
      style={styles.sessionsList}
      contentContainerStyle={
        sessions.length === 0 ? styles.emptyListContent : undefined
      }
      data={sessions}
      keyExtractor={(item) => item.session_id}
      renderItem={renderSession}
      refreshing={refreshing}
      onRefresh={load}


      
      ListEmptyComponent={
        loading ? (
          <View style={styles.emptyContainer}>
            <LoadingSpinner />
          </View>
        ) : error ? (
          <View style={styles.emptyContainer}>
            <Text style={styles.emptyTitle}>Couldn't load your history</Text>
            <Text style={styles.emptyText}>{error}</Text>
            <Pressable onPress={load} style={styles.primaryButton}>
              <Text style={styles.primaryButtonText}>Try again</Text>
            </Pressable>
          </View>
        ) : (
          <View style={styles.emptyContainer}>
            <Text style={styles.emptyTitle}>No shots yet</Text>
            <Text style={styles.emptyText}>Analyze your first free throw</Text>
            <Pressable onPress={openUpload} style={styles.primaryButton}>
              <Text style={styles.primaryButtonText}>Analyze a shot</Text>
            </Pressable>
          </View>
        )
      }
    />
  );

  return (
    <View style={styles.screen}>
      <Text style={styles.pageTitle}>Your History</Text>

      <View
        style={[
          styles.content,
          isDesktop ? styles.desktopContent : styles.mobileContent,
        ]}
      >
        <View
          style={[
            styles.summaryColumn,
            isDesktop ? styles.desktopColumn : styles.mobileColumn,
          ]}
        >
          <ScoreSummary sessions={sessions} />
        </View>

        <View
          style={[
            styles.historyColumn,
            isDesktop ? styles.desktopColumn : styles.mobileColumn,
          ]}
        >
          <Text style={styles.sectionHeading}>Past Sessions</Text>

          {sessionsList}
        </View>
      </View>

      {isDesktop && (
        <Pressable
          onPress={() => navigation.goBack()}
          style={styles.backButton}
        >
          <Text style={styles.primaryButtonText}>Back</Text>
        </Pressable>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  screen: {
    flex: 1,
    backgroundColor: COLORS.peach,
    paddingHorizontal: 20,
    paddingTop: 20,
    paddingBottom: 16,
  },
  pageTitle: {
    fontSize: 26,
    fontWeight: "700",
    color: COLORS.black,
    textAlign: "center",
    marginBottom: 26,
  },
  content: {
    flex: 1,
    gap: 24,
    minHeight: 0,
  },
  desktopContent: {
    flexDirection: "row",
    alignItems: "stretch",
  },
  mobileContent: {
    flexDirection: "column",
  },
  summaryColumn: {
    minHeight: 0,
  },
  desktopColumn: {
    flex: 1,
  },
  mobileColumn: {
    width: "100%",
  },
  summaryCard: {
    backgroundColor: COLORS.card,
    borderRadius: 8,
    padding: 16,
    alignItems: "center",
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: "700",
    color: COLORS.black,
    textAlign: "center",
    marginBottom: 12,
  },
  chartContainer: {
    width: "100%",
    maxWidth: 320,
    backgroundColor: "#F9EBDD",
    borderRadius: 8,
    padding: 8,
  },
  chartPlaceholder: {
    width: "100%",
    minHeight: 120,
    alignItems: "center",
    justifyContent: "center",
    padding: 12,
  },
  summaryPlaceholderText: {
    color: COLORS.brown,
    fontSize: 13,
    textAlign: "center",
    lineHeight: 18,
  },
  historyColumn: {
    minHeight: 0,
  },
  sectionHeading: {
    fontSize: 18,
    fontWeight: "700",
    color: COLORS.black,
    marginBottom: 12,
  },
  sessionsList: {
    flex: 1,
  },
  sessionRow: {
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: COLORS.cream,
    borderRadius: 8,
    padding: 5,
    marginBottom: 8,
    minHeight: 58,
    gap: 10,
  },
  thumbnail: {
    width: 64,
    height: 46,
    borderRadius: 8,
    backgroundColor: COLORS.card,
  },
  sessionDetails: {
    flex: 1,
    gap: 3,
  },
  sessionDate: {
    color: COLORS.black,
    fontSize: 12,
    fontWeight: "700",
  },
  sessionScore: {
    color: COLORS.brown,
    fontSize: 12,
  },
  sessionStatus: {
    color: COLORS.brown,
    fontSize: 11,
  },
  emptyListContent: {
    flexGrow: 1,
  },
  emptyContainer: {
    alignItems: "center",
    justifyContent: "center",
    padding: 20,
    gap: 12,
  },
  emptyTitle: {
    color: COLORS.black,
    fontSize: 20,
    fontWeight: "700",
    textAlign: "center",
  },
  emptyText: {
    color: COLORS.brown,
    fontSize: 14,
    lineHeight: 20,
    textAlign: "center",
  },
  primaryButton: {
    backgroundColor: COLORS.orange,
    borderRadius: 12,
    paddingHorizontal: 22,
    paddingVertical: 11,
    alignItems: "center",
    justifyContent: "center",
  },
  primaryButtonText: {
    color: COLORS.white,
    fontSize: 14,
    fontWeight: "700",
  },
  skeletonLine: {
    height: 7,
    backgroundColor: COLORS.skeleton,
    borderRadius: 5,
    marginVertical: 3,
  },
  backButton: {
    alignSelf: "center",
    backgroundColor: COLORS.orange,
    borderRadius: 8,
    paddingHorizontal: 24,
    paddingVertical: 10,
    marginTop: 12,
  },
});
