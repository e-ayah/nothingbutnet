import { Text, TouchableOpacity, View } from 'react-native';

type Props = {
  value: boolean | null;
  onChange: (value: boolean) => void;
};

export default function MadeToggle({ value, onChange }: Props) {
  return (
    <View className="flex-row space-x-3">
      <TouchableOpacity
        onPress={() => onChange(true)}
        className={
          value === true
            ? 'bg-[#A34A00] px-6 py-3 rounded-xl'
            : 'bg-white border border-[#A34A00] px-6 py-3 rounded-xl'
        }
      >
        <Text
          className={
            value === true
              ? 'text-white text-base font-sans font-bold'
              : 'text-[#A34A00] text-base font-sans font-bold'
          }
        >
          ✓ Made
        </Text>
      </TouchableOpacity>

      <TouchableOpacity
        onPress={() => onChange(false)}
        className={
          value === false
            ? 'bg-[#A34A00] px-6 py-3 rounded-xl'
            : 'bg-white border border-[#A34A00] px-6 py-3 rounded-xl'
        }
      >
        <Text
          className={
            value === false
              ? 'text-white text-base font-sans font-bold'
              : 'text-[#A34A00] text-base font-sans font-bold'
          }
        >
          ✗ Missed
        </Text>
      </TouchableOpacity>
    </View>
  );
}
