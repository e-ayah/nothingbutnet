import { useState } from "react";
import { View, Text, Pressable } from "react-native"; //basic UI pieces
import { useNavigation } from "@react-navigation/native"; //to switch screens
import TextField from "../components/TextField";
import Button from "../components/Button";
import { login } from "../services/api";
import { useStore } from "../store/useStore";

export default function LoginScreen() {
  const navigation = useNavigation<any>();
  const setAuth = useStore((s) => s.setAuth);

  //state variables
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [emailError, setEmailError] = useState("");
  const [passwordError, setPasswordError] = useState("");
  const [loading, setLoading] = useState(false);
  const [formError, setFormError] = useState("");

  //runs after "Log in"
  const handleSubmit = async () => {
    //validation
    const eErr = email.includes("@") ? "" : "Enter a valid email";
    const pErr = password ? "" : "Password is required";
    setEmailError(eErr);
    setPasswordError(pErr);
    if (eErr || pErr) return; //stop if there is an error

    //try logging in
    setFormError("");
    setLoading(true);
    try {
      const res = await login(email, password);
      setAuth(res.token, { id: res.user_id, name: "", email });
      navigation.reset({ index: 0, routes: [{ name: "Home" }] });
    } catch (err: any) {
      setFormError(err?.message ?? "Login failed");
    } finally {
      setLoading(false);
    }
  };

  //screen ui
  return (
    <View className="flex-1 justify-center p-6">
      <TextField label="Email" value={email} onChangeText={setEmail}
        keyboardType="email-address" error={emailError} />
      <TextField label="Password" value={password} onChangeText={setPassword}
        secure error={passwordError} />

      {formError ? <Text className="text-red-600 mb-2">{formError}</Text> : null}

      <Button title="Log in" onPress={handleSubmit}
        loading={loading} disabled={loading} />

      <Pressable onPress={() => navigation.navigate("Signup")} className="mt-4">
        <Text className="text-center">
          No account? <Text className="text-primary font-semibold">Sign up</Text>
        </Text>
      </Pressable>
    </View>
  );
}