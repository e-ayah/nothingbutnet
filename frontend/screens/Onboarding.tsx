import { useRef, useState } from "react";
import { ActivityIndicator, Platform, Pressable, ScrollView, Text as NativeText, type TextProps, useWindowDimensions, View } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import AsyncStorage from "@react-native-async-storage/async-storage";
import type { NativeStackNavigationProp } from "@react-navigation/native-stack";
import type { ParamListBase } from "@react-navigation/native";
import Svg, { Circle, Path, Rect } from "react-native-svg";

const slides = [
  { title: "Get instant feedback on your free throw form!" },
  {
    title: "How to film your free throw:",
    tips: [
      "Face your shooting side towards the camera",
      "Keep your whole body in the frame",
      "Use good lighting",
      "Keep your phone steady while filming",
    ],
  },
  { title: "After uploading your video, you will see:" },
];

function Text({ style, ...props }: TextProps) {
  return <NativeText {...props} style={[{ fontFamily: Platform.OS === "web" ? "Inter, Arial, sans-serif" : Platform.OS === "ios" ? "System" : "sans-serif" }, style]} />;
}

const orange = "#A34A00";
const layers = [orange, "#BD5C08", "#D57521", "#EF913B"];

// Local vectors keep the illustration sharp on both phones and larger screens.
function PlayerIllustration() {
  return (
    <Svg width={140} height={160} viewBox="0 0 140 160" accessible={false}>
      <Rect width="140" height="160" rx="10" fill="#8C471D" />
      <Path d="M12 143H128M30 143L52 110H105" stroke="#E8AE7E" strokeWidth="2" fill="none" />
      <Circle cx="77" cy="43" r="10" fill="#FFD3AF" />
      <Path d="M72 57L59 91L82 99L96 137M61 91L48 117L35 138M75 64L91 45L94 23M70 65L69 42L85 23" stroke="#FFD3AF" strokeWidth="8" strokeLinecap="round" fill="none" />
      <Path d="M67 60L80 65L70 89L57 84Z" fill="#FFFFFF" />
      <Circle cx="94" cy="16" r="10" fill="#EF913B" stroke="#FFD3AF" strokeWidth="1.5" />
      <Path d="M84 16H104M94 6C89 12 89 20 94 26M94 6C100 12 100 20 94 26" stroke="#8C471D" fill="none" />
      <Path d="M70 45L70 64L87 48M59 88L80 98L86 115" stroke="#00D75A" strokeWidth="2" fill="none" />
    </Svg>
  );
}

interface Props {
  navigation: NativeStackNavigationProp<ParamListBase>;
  onComplete?: () => void;
}

export default function OnboardingScreen({ navigation, onComplete }: Props) {
  const [index, setIndex] = useState(0);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const finishing = useRef(false);
  const { width, height } = useWindowDimensions();
  const desktop = width >= 768;
  const slide = slides[index];
  const last = index === slides.length - 1;

  const finish = async () => {
    if (finishing.current) return;
    finishing.current = true;
    setSaving(true);
    setError(null);
    try {
      await AsyncStorage.setItem("nbn-onboarded", "yes");
    } catch {
      setError("We couldn't save your progress. Please try again.");
      finishing.current = false;
      setSaving(false);
      return;
    }
    navigation.replace("Login");
    onComplete?.();
  };

  return (
    <SafeAreaView className="flex-1 bg-[#FFD3AF]">
      <View pointerEvents="none" accessibilityElementsHidden importantForAccessibility="no-hide-descendants" className="absolute inset-0 overflow-hidden">
        {index === 0 && !desktop ? (
          layers.map((color, layer) => (
            <View key={color} style={{ position: "absolute", top: 90 + layer * 13, alignSelf: "center", width: 320 - layer * 26, height: 350 - layer * 26, borderRadius: 180, backgroundColor: color }} />
          ))
        ) : index === 0 ? (
          <Svg width="100%" height="100%" viewBox="0 0 1440 900" preserveAspectRatio="none">
            {layers.map((color, layer) => (
              <Path key={color} d={`M${880 + layer * 28} 0 C${920 + layer * 28} 250 1210 40 1440 ${310 - layer * 28} L1440 0Z M0 ${460 + layer * 28} C300 ${480 + layer * 28} 90 760 ${490 - layer * 28} 900 H0Z`} fill={color} />
            ))}
          </Svg>
        ) : desktop ? (
          layers.map((color, layer) => (
            <View key={color} style={{ position: "absolute", top: 28 + layer * 12, bottom: -60, left: 34 + layer * 12, right: 34 + layer * 12, borderWidth: 13, borderColor: color, borderTopLeftRadius: 160 - layer * 12, borderTopRightRadius: 160 - layer * 12 }} />
          ))
        ) : (
          layers.map((color, layer) => (
            <View key={color} style={{ position: "absolute", width: 210 - layer * 28, height: 210 - layer * 28, borderRadius: 120, bottom: -100, left: -100, backgroundColor: color }} />
          ))
        )}
      </View>
      <ScrollView contentContainerStyle={{ flexGrow: 1, minHeight: height - 80 }}>
        <View className="w-full flex-1 self-center px-6 py-4" style={{ maxWidth: desktop ? 900 : 440 }}>
          <View className="items-end">
            <Pressable accessibilityRole="button" accessibilityLabel="Skip onboarding" disabled={saving} onPress={finish} className="min-h-[44px] min-w-[64px] items-center justify-center rounded-lg px-3">
              <Text className="text-base font-semibold text-[#A34A00]">Skip</Text>
            </Pressable>
          </View>
          <View className="flex-1 items-center justify-center py-8" style={{ minHeight: desktop ? 450 : 410, justifyContent: index === 0 && !desktop ? "flex-start" : "center", paddingTop: index === 0 && !desktop ? 135 : 32 }}>
            <Text key={index} accessibilityRole="header" accessibilityLiveRegion="polite" className="text-center font-bold text-black" style={{ fontSize: desktop ? 36 : 28, lineHeight: desktop ? 44 : 35, maxWidth: desktop ? 650 : 310, marginBottom: index === 0 ? 0 : 28 }}>
              {slide.title}
            </Text>
            {slide.tips && (
              <View className="gap-5" style={{ maxWidth: desktop ? 600 : 310 }}>
                {slide.tips.map((tip) => (
                  <View key={tip} className="flex-row items-start gap-3">
                    <Text className="font-bold text-[#A34A00]" style={{ fontSize: desktop ? 22 : 17 }}>•</Text>
                    <Text className="flex-1 text-black" style={{ fontSize: desktop ? 22 : 17, lineHeight: desktop ? 30 : 25 }}>{tip}</Text>
                  </View>
                ))}
              </View>
            )}
            {last && (
              <View className="items-center gap-5">
                <PlayerIllustration />
                <View className="items-center gap-2 rounded-xl bg-[#E8AE7E] px-6 py-5" style={{ maxWidth: 430 }}>
                  <Text className="text-center font-bold text-[#A34A00]" style={{ fontSize: desktop ? 24 : 20 }}>Form score: 78/100</Text>
                  <Text className="text-center text-black" style={{ fontSize: desktop ? 20 : 16 }}>Great elbow and shoulder alignment!</Text>
                  <Text className="text-center text-black" style={{ fontSize: desktop ? 20 : 16 }}>Try bending your knees more.</Text>
                </View>
              </View>
            )}
          </View>
          <View className="items-center gap-5 pb-6">
            {error && <Text accessibilityRole="alert" className="text-center text-base text-[#A34A00]">{error}</Text>}
            <Pressable accessibilityRole="button" accessibilityLabel={last ? "Get started" : "Next"} accessibilityState={{ disabled: saving, busy: saving }} disabled={saving} onPress={last ? finish : () => setIndex((current) => Math.min(current + 1, slides.length - 1))} className="min-h-[48px] min-w-[132px] items-center justify-center rounded-lg bg-[#A34A00] px-6 py-3" style={({ pressed }) => ({ opacity: pressed || saving ? 0.7 : 1 })}>
              {saving ? <ActivityIndicator color="#FFFFFF" /> : <Text className="text-base font-semibold text-white">{last ? "Get started" : "Next"}</Text>}
            </Pressable>
            <View accessible accessibilityLabel={`Step ${index + 1} of ${slides.length}`} className="flex-row gap-3">
              {slides.map((_, dot) => <View key={dot} className="h-2.5 w-2.5 rounded-full" style={{ backgroundColor: dot === index ? orange : "#FFFFFF" }} />)}
            </View>
          </View>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}
