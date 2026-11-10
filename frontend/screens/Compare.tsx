
import React, { useEffect, useState } from "react";
import {
  View,
  Text,
  ScrollView,
  Pressable,
  ActivityIndicator,
  useWindowDimensions,
} from "react-native";

import { getSessions } from "../services/api";
import { SessionSummary } from "../services/types";
import {
  compareSessions,
  CompareResult,
  CompareShot,
} from "../services/compareApi";
import { useStore } from "../store/useStore";

import VideoPlayer from "../components/VideoPlayer";
import ScoreCircle from "../components/ScoreCircle";
import AngleCard from "../components/AngleCard";
import EmptyState from "../components/EmptyState";

const COLORS = {
  background: "#FFF8F0",
  primary: "#B93815",
  text: "#2D201B",
  secondary: "#6F5D55",
  green: "#1F7A4D",
  orange: "#B45309",
  white: "#FFFFFF",
  border: "#DCCFC7",
};

const ANGLES = [
  { key: "elbow_angle", name: "Elbow", min: 85, max: 100 },
  { key: "knee_angle", name: "Knee", min: 150, max: 175 },
  { key: "shoulder_angle", name: "Shoulder", min: 45, max: 75 },
] as const;

type AngleKey = (typeof ANGLES)[number]["key"];

function distance(value: number, min: number, max: number) {
  if (value < min) return min - value;
  if (value > max) return value - max;
  return 0;
}

function formatDate(date: string) {
  return new Date(date).toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  });
}

function ShotPicker({
  label,
  sessions,
  selected,
  onSelect,
}: {
  label: string;
  sessions: SessionSummary[];
  selected: string;
  onSelect: (id: string) => void;
}) {
  const [open, setOpen] = useState(false);
  const current = sessions.find((s) => s.session_id === selected);

  return (
    <View style={{ flex: 1, minWidth: 0 }}>
      <Text style={{ color: COLORS.secondary, marginBottom: 8 }}>
        {label}
      </Text>

      <Pressable
        onPress={() => setOpen(!open)}
        style={{
          backgroundColor: COLORS.white,
          borderWidth: 1,
          borderColor: COLORS.border,
          borderRadius: 12,
          padding: 12,
        }}
      >
        <Text style={{ color: COLORS.text }}>
          {current
            ? `${formatDate(current.created_at)} · ${current.overall_score ?? "—"}`
            : "Select shot"}
        </Text>
        <Text style={{ color: COLORS.secondary, marginTop: 4 }}>
          {open ? "▲" : "▼"}
        </Text>
      </Pressable>

      {open &&
        sessions.map((session) => (
          <Pressable
            key={session.session_id}
            onPress={() => {
              onSelect(session.session_id);
              setOpen(false);
            }}
            style={{
              padding: 12,
              backgroundColor: COLORS.white,
              borderBottomWidth: 1,
              borderColor: COLORS.border,
            }}
          >
            <Text style={{ color: COLORS.text }}>
              {formatDate(session.created_at)} ·{" "}
              {session.overall_score ?? "—"}
            </Text>
          </Pressable>
        ))}
    </View>
  );
}

function ShotColumn({
  shot,
  label,
}: {
  shot: CompareShot;
  label: string;
}) {
  const video = shot.annotated_video_url || shot.video_url;

  return (
    <View style={{ flex: 1, minWidth: 0 }}>
      <Text
        style={{
          color: COLORS.text,
          fontSize: 17,
          fontWeight: "700",
          marginBottom: 12,
        }}
      >
        {label}
      </Text>

      <View
        style={{
          borderRadius: 12,
          overflow: "hidden",
          marginBottom: 16,
          backgroundColor: COLORS.white,
        }}
      >
        {video ? (
          <VideoPlayer uri={video} />
        ) : (
          <View
            style={{
              aspectRatio: 16 / 9,
              justifyContent: "center",
              alignItems: "center",
              backgroundColor: "#EDE5DD",
            }}
          >
            <Text style={{ color: COLORS.secondary }}>
              Video preview
            </Text>
          </View>
        )}
      </View>

      <View style={{ alignItems: "center", marginBottom: 16 }}>
        <ScoreCircle score={shot.score} size={100} />
      </View>

      {ANGLES.map((angle) => {
        const value = shot.angles[angle.key];
        const good =
          value !== null &&
          value >= angle.min &&
          value <= angle.max;

        return (
          <AngleCard
            key={angle.key}
            name={angle.name}
            value={value}
            min={angle.min}
            max={angle.max}
            status={good ? "good" : "needs_work"}
          />
        );
      })}
    </View>
  );
}

function Changes({ result }: { result: CompareResult }) {
  return (
    <View
      style={{
        backgroundColor: COLORS.white,
        padding: 16,
        borderRadius: 12,
        marginTop: 20,
        borderWidth: 1,
        borderColor: COLORS.border,
      }}
    >
      <Text
        style={{
          fontSize: 20,
          fontWeight: "700",
          color: COLORS.text,
          marginBottom: 16,
        }}
      >
        What changed?
      </Text>

      {ANGLES.map((angle) => {
        const before = result.a.angles[angle.key];
        const after = result.b.angles[angle.key];
        const change = result.changes[angle.key];

        if (before === null || after === null || change === null) {
          return (
            <Text key={angle.key} style={{ marginBottom: 12 }}>
              {angle.name}: Not measured
            </Text>
          );
        }

        const oldDistance = distance(
          before,
          angle.min,
          angle.max
        );
        const newDistance = distance(
          after,
          angle.min,
          angle.max
        );

        const improved = newDistance < oldDistance;
        const worsened = newDistance > oldDistance;
        const color = improved
          ? COLORS.green
          : worsened
          ? COLORS.orange
          : COLORS.secondary;

        const direction = change > 0 ? "↑" : change < 0 ? "↓" : "→";
        const description = improved
          ? "Closer to target"
          : worsened
          ? "Farther from target"
          : "No change in distance";

        return (
          <View
            key={angle.key}
            style={{
              flexDirection: "row",
              justifyContent: "space-between",
              marginBottom: 14,
              flexWrap: "wrap",
            }}
          >
            <Text style={{ color: COLORS.text }}>
              {angle.name}
            </Text>
            <Text style={{ color, fontWeight: "600" }}>
              {direction} {Math.abs(change).toFixed(1)}° · {description}
            </Text>
          </View>
        );
      })}

      <View
        style={{
          borderTopWidth: 1,
          borderColor: COLORS.border,
          paddingTop: 12,
          flexDirection: "row",
          justifyContent: "space-between",
        }}
      >
        <Text style={{ fontWeight: "700", color: COLORS.text }}>
          Score change
        </Text>
        <Text style={{ fontWeight: "700", color: COLORS.green }}>
          {result.changes.score === null
            ? "—"
            : `${result.changes.score > 0 ? "+" : ""}${result.changes.score}`}
        </Text>
      </View>
    </View>
  );
}

export default function CompareScreen() {
  const token = useStore((s) => s.token);
  const { width } = useWindowDimensions();

  const [sessions, setSessions] = useState<SessionSummary[]>([]);
  const [shotA, setShotA] = useState("");
  const [shotB, setShotB] = useState("");
  const [result, setResult] = useState<CompareResult | null>(null);
  const [loading, setLoading] = useState(true);
  const [comparing, setComparing] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    let active = true;

    async function loadSessions() {
      try {
        setLoading(true);
        setError("");

        const data = await getSessions(token ?? "");
        const completed = data.filter((s) => s.status === "done");

        if (!active) return;

        setSessions(completed);

        if (completed.length >= 2) {
          setShotA(completed[0].session_id);
          setShotB(completed[1].session_id);
        }
      } catch {
        if (active) setError("Couldn't load your shots.");
      } finally {
        if (active) setLoading(false);
      }
    }

    loadSessions();

    return () => {
      active = false;
    };
  }, [token]);

  useEffect(() => {
    if (!shotA || !shotB || shotA === shotB) {
      setResult(null);
      return;
    }

    let active = true;

    async function loadComparison() {
      try {
        setComparing(true);
        setError("");
        setResult(null);

        const data = await compareSessions(shotA, shotB, token);

        if (active) setResult(data);
      } catch {
        if (active) setError("Couldn't compare these shots.");
      } finally {
        if (active) setComparing(false);
      }
    }

    loadComparison();

    return () => {
      active = false;
    };
  }, [shotA, shotB, token]);

  if (loading) {
    return (
      <View style={{ flex: 1, justifyContent: "center" }}>
        <ActivityIndicator size="large" color={COLORS.primary} />
      </View>
    );
  }

  if (error && sessions.length === 0) {
    return (
      <EmptyState
        title="Something went wrong"
        message={error}
      />
    );
  }

  if (sessions.length < 2) {
    return (
      <EmptyState
        title="Not enough shots"
        message="Analyze 2 shots to compare them"
      />
    );
  }

  return (
    <ScrollView
      style={{ flex: 1, backgroundColor: COLORS.background }}
      contentContainerStyle={{
        padding: 20,
        paddingBottom: 50,
        maxWidth: 1100,
        width: "100%",
        alignSelf: "center",
      }}
    >
      <Text
        style={{
          fontSize: 28,
          fontWeight: "700",
          color: COLORS.text,
          marginBottom: 8,
        }}
      >
        Compare Your Shots
      </Text>

      <Text
        style={{
          color: COLORS.secondary,
          marginBottom: 24,
        }}
      >
        See how your shooting form has changed over time.
      </Text>

      <View style={{ flexDirection: "row", gap: 12, marginBottom: 24 }}>
        <ShotPicker
          label="Shot A"
          sessions={sessions}
          selected={shotA}
          onSelect={setShotA}
        />
        <ShotPicker
          label="Shot B"
          sessions={sessions}
          selected={shotB}
          onSelect={setShotB}
        />
      </View>

      {shotA === shotB ? (
        <Text style={{ color: COLORS.orange }}>
          Choose two different shots to compare.
        </Text>
      ) : comparing ? (
        <ActivityIndicator color={COLORS.primary} />
      ) : error ? (
        <Text style={{ color: COLORS.primary }}>{error}</Text>
      ) : result ? (
        <>
          <View style={{ flexDirection: "row", gap: width < 600 ? 8 : 24 }}>
            <ShotColumn shot={result.a} label="Shot A" />
            <ShotColumn shot={result.b} label="Shot B" />
          </View>

          <Changes result={result} />
        </>
      ) : null}
    </ScrollView>
  );
}
