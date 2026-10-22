import { Pressable, Text, View } from 'react-native';
import { Card } from './Card';
import { SessionSummary } from '../services/types';

type Props = SessionSummary & { onPress: () => void };

const STATUS_LABEL = {
  done: { text: 'Done', className: 'text-success' },
  processing: { text: 'Processing', className: 'text-accent' },
  failed: { text: 'Failed', className: 'text-warning' },
} as const;

export default function SessionCard({ created_at, overall_score, status, onPress }: Props) {
  const date = new Date(created_at).toLocaleString('en-US', {
    month: 'short',
    day: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
  }); // e.g. "Oct 3, 4:12 PM"

  const score = status === 'processing' || overall_score == null ? '—' : overall_score;
  const label = STATUS_LABEL[status];

  return (
    <Pressable onPress={onPress}>
      <Card>
        <View className="flex-row items-center justify-between">
          <View>
            <Text className="text-primary text-base">{date}</Text>
            <Text className={`text-sm font-semibold ${label.className}`}>{label.text}</Text>
          </View>
          <Text className="text-primary text-3xl font-bold">{score}</Text>
        </View>
      </Card>
    </Pressable>
  );
}