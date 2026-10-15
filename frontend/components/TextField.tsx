import React, {useState} from 'react';
import {KeyboardTypeOptions, StyleSheet, Text, TextInput, View} from 'react-native';

type TextFieldProps = {
    label: string;
    value: string;
    onChangeText: (text: string) => void;
    error?: string;
    secure?: boolean;
    keyboardType?: KeyboardTypeOptions;
    autoCapitalize?: 'none' | 'sentences' | 'words' | 'characters';
}
// created under the assumption that aces #10 works and react.jsx-runtime exists
export default function TextField({ 
    label, 
    value, 
    onChangeText, 
    error,
    secure,
    keyboardType,
    autoCapitalize = 'none',
}: TextFieldProps) {
    const [isFocused, setIsFocused] = useState(false);

    return (
     <View style={styles.container}>
      <Text style={styles.label}>{label}</Text>
      <TextInput
        style={[
          styles.input,
          isFocused ? styles.inputFocused : null,
          error ? styles.inputError : null,
        ]}
        value={value}
        onChangeText={onChangeText}
        secureTextEntry={secure}
        keyboardType={keyboardType}
        autoCapitalize={autoCapitalize}
        onFocus={() => setIsFocused(true)}
        onBlur={() => setIsFocused(false)}
      />
      {error ? <Text style={styles.errorText}>{error}</Text> : null}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { marginBottom: 16 },
  label: { fontSize: 14, marginBottom: 6 },
  input: {
    borderWidth: 1,
    borderColor: '#999999',
    borderRadius: 8,
    paddingHorizontal: 12,
    paddingVertical: 10,
    fontSize: 16,
  },
  inputFocused: {borderColor: '#00FF00'},
  inputError: { borderColor: 'red' },
  errorText: { color: 'red', fontSize: 12, marginTop: 4 },
});