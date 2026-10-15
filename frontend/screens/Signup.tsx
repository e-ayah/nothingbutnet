import { useState } from "react";
import { View, Text, Pressable } from "react-native"; //basic UI pieces
import { useNavigation } from "@react-navigation/native"; //to switch screens
import TextField from "../components/TextField";
import Button from "../components/Button";
import { signup } from "../services/api";
import { useStore } from "../store/useStore";

export default function SignupScreen() {
  const navigation = useNavigation<any>();
  const setAuth = useStore((s) => s.setAuth);

  //state variables
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [nameError, setNameError] = useState("");
  const [emailError, setEmailError] = useState("");
  const [passwordError, setPasswordError] = useState("");
  const [confirmError, setConfirmError] = useState("");
  const [loading, setLoading] = useState(false);
  const [formError, setFormError] = useState("");

  //runs after "Sign up"
  const handleSubmit = async () => {
    //validation
    const cleanName = name.trim();
    const cleanEmail = email.trim();
    const nErr = cleanName ? "" : "Name is required";
    const eErr = cleanEmail.includes("@") ? "" : "Enter a valid email";
    const pErr = password.length >= 8 ? "" : "Password must be at least 8 characters";
    const cErr = password === confirmPassword ? "" : "Passwords do not match";
    setNameError(nErr);
    setEmailError(eErr);
    setPasswordError(pErr);
    setConfirmError(cErr);
    if (nErr || eErr || pErr || cErr) return; //stop if there is an error

    //try signing up
    setFormError("");
    setLoading(true);
    try {
      const res = await signup(cleanEmail, password, cleanName);
      setAuth(res.token, { id: res.user_id, name: cleanName, email: cleanEmail });
      navigation.reset({ index: 0, routes: [{ name: "Home" }] });
    } catch (err: any) {
      //show a readable message instead of axios's "Request failed with status code 409"
      const status = err?.response?.status;
      if (status === 409) setFormError("An account with this email already exists");
      else if (status === 400) setFormError("Please check your details and try again.");
      else if (!err?.response) setFormError("Can't reach the server. Check your connection.");
      else setFormError("Sign up failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  //screen ui
  return (
    <View className="flex-1 justify-center p-6">
      <Text className="text-2xl font-semibold mb-4">Create Account</Text>

      <TextField label="Name" value={name} onChangeText={setName}
        autoCapitalize="words" error={nameError} />
      <TextField label="Email" value={email} onChangeText={setEmail}
        keyboardType="email-address" error={emailError} />
      <TextField label="Password" value={password} onChangeText={setPassword}
        secure error={passwordError} />
      <TextField label="Confirm Password" value={confirmPassword} onChangeText={setConfirmPassword}
        secure error={confirmError} />

      {formError ? <Text className="text-red-600 mb-2">{formError}</Text> : null}

      <Button title="Sign up" onPress={handleSubmit}
        loading={loading} disabled={loading} />

      <Pressable onPress={() => navigation.navigate("Login")} className="mt-4">
        <Text className="text-center">
          Already have an account? <Text className="text-primary font-semibold">Log in</Text>
        </Text>
      </Pressable>
    </View>
  );
}
