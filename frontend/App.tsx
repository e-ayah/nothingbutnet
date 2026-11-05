import "./global.css";

import { useEffect, useState } from "react";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import AsyncStorage from "@react-native-async-storage/async-storage";
import HomeScreen from "./screens/Home";
import AppButton from "./components/Button";
import { useStore } from "./store/useStore";

import UploadScreen from "./screens/UploadScreen";
import ResultsScreen from "./screens/Results";
import HistoryScreen from "./screens/History";
import ProfileScreen from "./screens/Profile";
import LoginScreen from "./screens/Login";
import SignupScreen from "./screens/Signup";
import ProgressScreen from "./screens/Progress";
import CompareScreen from "./screens/Compare";
import GoalsScreen from "./screens/Goals";
import OnboardingScreen from "./screens/Onboarding";
import FeedbackScreen from "./screens/Feedback";

const Stack = createNativeStackNavigator();

export default function App() {
  const [ready, setReady] = useState(useStore.persist.hasHydrated());
  useEffect(() => {
    const unsubscribe = useStore.persist.onFinishHydration(() => setReady(true));
    setReady(useStore.persist.hasHydrated());
    return unsubscribe;
  }, []);
  const [onboarded, setOnboarded] = useState<boolean | null>(null);
  useEffect(() => {
    let active = true;
    AsyncStorage.getItem("nbn-onboarded")
      .then((value) => { if (active) setOnboarded(value === "yes"); })
      .catch(() => { if (active) setOnboarded(false); });
    return () => { active = false; };
  }, []);
  const token = useStore((s) => s.token);
  const logout = useStore((s) => s.logout);

  if (!ready || onboarded === null) return null;

  return (
    <NavigationContainer>
      <Stack.Navigator>
        {token == null ? (
          <>
            {!onboarded && (
              <Stack.Screen name="Onboarding" options={{ headerShown: false }}>
                {(props) => (
                  <OnboardingScreen {...props} onComplete={() => setOnboarded(true)} />
                )}
              </Stack.Screen>
            )}
            <Stack.Screen name="Login" component={LoginScreen} options={{ headerShown: false }} />
            <Stack.Screen name="Signup" component={SignupScreen} />
          </>
        ) : (
          <Stack.Group screenOptions={{
            headerRight: () => <AppButton title="Log out" variant="secondary" onPress={logout} />,
          }}>
            <Stack.Screen name="Home" component={HomeScreen} />
            <Stack.Screen name="Upload" component={UploadScreen} />
            <Stack.Screen name="Results" component={ResultsScreen} />
            <Stack.Screen name="History" component={HistoryScreen} />
            <Stack.Screen name="Profile" component={ProfileScreen} />
            <Stack.Screen name="Progress" component={ProgressScreen} />
            <Stack.Screen name="Compare" component={CompareScreen} />
            <Stack.Screen name="Goals" component={GoalsScreen} />
            <Stack.Screen name="Feedback" component={FeedbackScreen} />
          </Stack.Group>
        )}
      </Stack.Navigator>
    </NavigationContainer>
  );
}
