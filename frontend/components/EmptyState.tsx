import React from 'react';
import { Text, View } from 'react-native';
import Button from './Button';

type EmptyStateProps = {
  title: string;
  message: string;
  actionLabel?: string;
  onAction?: () => void;
};

export default function EmptyState({ title, message, actionLabel, onAction }: EmptyStateProps) {
  return (
    <View className="flex-1 items-center justify-center bg-background px-6">
      <Text className="text-xl font-semibold text-primary text-center">{title}</Text>
      <Text className="mt-2 text-base text-accent text-center">{message}</Text>
      {actionLabel && onAction ? (
        <View className="mt-4">
          <Button title={actionLabel} onPress={onAction} />
        </View>
      ) : null}
    </View>
  );
}
