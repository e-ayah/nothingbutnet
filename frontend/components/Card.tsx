/**
 * Card: Puts content in a white box with shadows
 * <Card className="optional-classes-here">
 *   <Text>This is the content that goes in the card</Text>
 * </Card>
 */

import React from 'react';
import { View } from 'react-native';

interface CardProps {
  children: React.ReactNode;
  className?: string;
}

export const Card: React.FC<CardProps> = ({ children, className }) => {
  return (
    <View className={`bg-white rounded-xl p-4 shadow-sm ${className || ''}`}>
      {children}
    </View>
  );
};