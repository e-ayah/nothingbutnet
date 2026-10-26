import React from 'react';
import { Text, View } from 'react-native';
import Button from './Button';
import { friendlyError } from '../services/errorMessages';

type ErrorMessageProps = {
  message?: string;
  error?: unknown;
  onRetry?: () => void;
};

export default function ErrorMessage({ message, error, onRetry }: ErrorMessageProps) {
  const text = message ?? (error ? friendlyError(error) : 'Something went wrong. Try again.');

  return (
    <View className="flex-1 items-center justify-center bg-background px-6">
      <Text className="text-3xl text-warning mb-2">⚠</Text>
      <Text className="text-base text-primary text-center">{text}</Text>
      {onRetry ? (
        <View className="mt-4">
          <Button title="Try again" onPress={onRetry} />
        </View>
      ) : null}
    </View>
  );
}