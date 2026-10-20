import Svg, { Circle } from 'react-native-svg';
import { Text, View } from 'react-native';
 
export default function ScoreCircle({ score, size = 140 }: { score: number | null; size?: number }) {
  const stroke = 12;
  const r = (size - stroke) / 2;
  const c = 2 * Math.PI * r; // circumference
  const filled = score == null ? 0 : (score / 100) * c;
  const color = score == null ? '#cccccc' : score >= 80 ? '#2d8a2d' : score >= 60 ? '#4a4a8a' : '#cc6600';      return (
    <View style={{ width: size, height: size }} className="items-center justify-center">
      <Svg width={size} height={size} style={{ position: 'absolute', transform: [{ rotate: '-90deg' }] }}>
        <Circle cx={size / 2} cy={size / 2} r={r} stroke="#eeeeee" strokeWidth={stroke} fill="none" />
        <Circle cx={size / 2} cy={size / 2} r={r} stroke={color} strokeWidth={stroke} fill="none"
                strokeDasharray={`${filled} ${c}`} strokeLinecap="round" />
      </Svg>
      <Text className="text-3xl font-bold">{score ?? '—'}</Text>
    </View>
 );
}
// swap the hex colors for the ones in docs/design/style-guide.md
