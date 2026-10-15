import "./global.css";

import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import { View, Text, Button } from "react-native";

import UploadScreen from "./screens/Upload";
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

function HomeScreen({ navigation }: any) {
  return (
    <View>
      <Text className="text-primary text-2xl">Home</Text>

      <Button title="Upload" onPress={() => navigation.navigate("Upload")} />
      <Button title="Results" onPress={() => navigation.navigate("Results")} />
      <Button title="History" onPress={() => navigation.navigate("History")} />
      <Button title="Profile" onPress={() => navigation.navigate("Profile")} />
      <Button title="Login" onPress={() => navigation.navigate("Login")} />
      <Button title="Signup" onPress={() => navigation.navigate("Signup")} />
      <Button title="Progress" onPress={() => navigation.navigate("Progress")} />
      <Button title="Compare" onPress={() => navigation.navigate("Compare")} />
      <Button title="Goals" onPress={() => navigation.navigate("Goals")} />
      <Button title="Onboarding" onPress={() => navigation.navigate("Onboarding")} />
      <Button title="Feedback" onPress={() => navigation.navigate("Feedback")} />
    </View>
  );
}

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen name="Home" component={HomeScreen} />
        <Stack.Screen name="Upload" component={UploadScreen} />
        <Stack.Screen name="Results" component={ResultsScreen} />
        <Stack.Screen name="History" component={HistoryScreen} />
        <Stack.Screen name="Profile" component={ProfileScreen} />
        <Stack.Screen name="Login" component={LoginScreen} />
        <Stack.Screen name="Signup" component={SignupScreen} />
        <Stack.Screen name="Progress" component={ProgressScreen} />
        <Stack.Screen name="Compare" component={CompareScreen} />
        <Stack.Screen name="Goals" component={GoalsScreen} />
        <Stack.Screen name="Onboarding" component={OnboardingScreen} />
        <Stack.Screen name="Feedback" component={FeedbackScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}