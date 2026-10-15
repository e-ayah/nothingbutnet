import React from 'react';
import { ActivityIndicator, Pressable, Text } from 'react-native';

// keep in sync with `primary` in tailwind.config.js (spinner color can't use className)
const PRIMARY_COLOR = '#1a1a2e';

type ButtonProps = {
  title: string;
  onPress: () => void;
  variant?: 'primary' | 'secondary';
  loading?: boolean;
  disabled?: boolean;
};

export default function Button({
  title,
  onPress,
  variant = 'primary',
  loading = false,
  disabled = false,
}: ButtonProps) {
  const isPrimary = variant === 'primary';
  const isInactive = disabled || loading;

  return (
    <Pressable
      onPress={onPress}
      disabled={isInactive}
      className={[
        'min-h-[44px] px-5 rounded-lg items-center justify-center border',
        isPrimary ? 'bg-primary border-primary' : 'bg-white border-primary',
        isInactive ? 'opacity-50' : '',
      ].join(' ')}
    >
      {loading ? (
        <ActivityIndicator color={isPrimary ? '#ffffff' : PRIMARY_COLOR} />
      ) : (
        <Text
          className={isPrimary ? 'text-white font-semibold' : 'text-primary font-semibold'}
        >
          {title}
        </Text>
      )}
    </Pressable>
  );
}
