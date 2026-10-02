
import React, { useState } from "react";
import {
  View,
  Text,
  TextInput,
  Pressable,
  StyleSheet,
} from "react-native";

export default function SignupScreen() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const [submitted, setSubmitted] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSignup = async () => {
    setSubmitted(true);
    setError("");

    if (
      !name.trim() ||
      !email.includes("@") ||
      password.length < 8 ||
      password !== confirmPassword
    ) {
      return;
    }

    setLoading(true);

    try {
      // TODO: replace with the real API import when the frontend scaffolding is merged.
      const result = await api.signup(email, password, name);

      // TODO: store.setAuth(token, user) (Aces#05)

      console.log("Signup successful:", result);
    } catch (err) {
      setError("Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Create Account</Text>

      <TextInput
        style={styles.input}
        placeholder="Name"
        value={name}
        onChangeText={setName}
      />
      {submitted && !name.trim() && (
        <Text style={styles.error}>Name is required.</Text>
      )}

      <TextInput
        style={styles.input}
        placeholder="Email"
        value={email}
        onChangeText={setEmail}
        keyboardType="email-address"
        autoCapitalize="none"
      />
      {submitted && !email.includes("@") && (
        <Text style={styles.error}>Please enter a valid email.</Text>
      )}

      <TextInput
        style={styles.input}
        placeholder="Password"
        value={password}
        onChangeText={setPassword}
        secureTextEntry
      />
      {submitted && password.length < 8 && (
        <Text style={styles.error}>
          Password must be at least 8 characters.
        </Text>
      )}

      <TextInput
        style={styles.input}
        placeholder="Confirm Password"
        value={confirmPassword}
        onChangeText={setConfirmPassword}
        secureTextEntry
      />
      {submitted && password !== confirmPassword && (
        <Text style={styles.error}>Passwords do not match.</Text>
      )}

      {error !== "" && <Text style={styles.error}>{error}</Text>}

      <Pressable
        style={styles.button}
        onPress={handleSignup}
        disabled={loading}
      >
        <Text style={styles.buttonText}>
          {loading ? "Creating Account..." : "Sign Up"}
        </Text>
      </Pressable>

      <Pressable>
        <Text style={styles.loginText}>
          Already have an account? Log in
        </Text>
      </Pressable>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 24,
    justifyContent: "center",
  },
  title: {
    fontSize: 28,
    fontWeight: "bold",
    marginBottom: 24,
  },
  input: {
    borderWidth: 1,
    marginTop: 16, 
}, 
});