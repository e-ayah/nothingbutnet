import React from 'react';
import { ActivityIndicator, Text, View } from 'react-native';

type LoadingSpinnerProps = {
  message?: string;
};

export default function LoadingSpinner({ message }: LoadingSpinnerProps) {
  return (
    <View className="flex-1 items-center justify-center bg-background">
      <ActivityIndicator size="large" color="#1a1a2e" />
      {message ? (
        <Text className="mt-3 text-base text-primary text-center">{message}</Text>
      ) : null}
    </View>
  );
}