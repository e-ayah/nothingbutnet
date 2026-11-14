
import { View, Text, StyleSheet } from "react-native";
import type { RecurringMistake } from "../services/insightsApi";

type Props = {
  mistake: RecurringMistake;
};

export default function RecurringMistakeCard({ mistake }: Props) {
  return (
    <View style={styles.card}>
      <View style={styles.container}>
        <Text style={styles.label}>RECURRING FORM ISSUE</Text>

        <Text style={styles.headline}>
          {mistake.label} needed work in {mistake.count} of your last{" "}
          {mistake.out_of} shots
        </Text>

        <View style={styles.divider} />

        <Text style={styles.tipLabel}>LATEST TIP</Text>

        <Text style={styles.tip}>
          {mistake.latest_tip}
        </Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: "#FFFFFF",
    borderRadius: 12,
    padding: 16,
    borderWidth: 1,
    borderColor: "#E2E8F0",
  },
  container: {
    gap: 10,
  },
  label: {
    fontSize: 11,
    fontWeight: "700",
    color: "#64748b",
    letterSpacing: 1,
  },
  headline: {
    fontSize: 18,
    fontWeight: "700",
    color: "#1e293b",
  },
  divider: {
    height: 1,
    backgroundColor: "#e2e8f0",
    marginVertical: 4,
  },
  tipLabel: {
    fontSize: 11,
    fontWeight: "700",
    color: "#64748b",
    letterSpacing: 1,
  },
  tip: {
    fontSize: 14,
    color: "#475569",
    lineHeight: 21,
  },
});
