import Svg, { Circle, Polyline, Rect } from 'react-native-svg';
import { Text, View } from 'react-native';


type Props = { label: string; values: (number | null)[]; low: number; high: number; width?: number; height?: number };


export default function ProgressChart({ label, values, low, high, width = 320, height = 140 }: Props) {
  const pad = 12;
  const pts = values
    .map((v, i) => ({ i, v }))
    .filter((p): p is { i: number; v: number } => p.v != null);
  const all = [...pts.map((p) => p.v), low, high];
  const min = Math.min(...all) - 5;
  const max = Math.max(...all) + 5;
  const x = (i: number) => pad + (values.length <= 1 ? 0 : (i / (values.length - 1)) * (width - 2 * pad));
  const y = (v: number) => pad + (1 - (v - min) / (max - min)) * (height - 2 * pad);


  const latestValue = pts.length > 0 ? pts[pts.length - 1].v : null;

  return (
    <View className="w-full">
      <View className="flex-row justify-between items-start mb-1">
        <View>
          <Text className="font-bold text-base text-black" style={{ fontFamily: 'Inter' }}>
            {label}
          </Text>
          <Text className="text-[14px] text-[#1F7A4D]" style={{ fontFamily: 'Inter' }}>
            Target {low}–{high}°
          </Text>
        </View>
        
        {latestValue !== null && (
          <Text className="text-[19px] font-extrabold text-black" style={{ fontFamily: 'Inter' }}>
            {latestValue.toFixed(1)}°
          </Text>
        )}
      </View>
      
      <View className="mt-2">
        <Svg width={width} height={height}>
          <Rect 
            x={0} 
            y={y(high)} 
            width={width} 
            height={y(low) - y(high)} 
            fill="#E8F3EC" 
          />
          
          {pts.length > 0 && (
            <Polyline 
              points={pts.map((p) => `${x(p.i)},${y(p.v)}`).join(' ')}
              fill="none" 
              stroke="#A34A00" 
              strokeWidth={3} 
            />
          )}
          
          {pts.map((p) => (
            <Circle 
              key={p.i} 
              cx={x(p.i)} 
              cy={y(p.v)} 
              r={4} 
              fill="#A34A00" 
            />
          ))}
        </Svg>
      </View>
    </View>
  );
}