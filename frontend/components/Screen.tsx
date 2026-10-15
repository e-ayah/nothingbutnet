/**
 * Screen:
 * 
 * Non-scrollable layout:
 * <Screen>
 *   <Text>Fixed Content</Text>
 * </Screen>
 * 
 * Scrollable layout:
 * <Screen scroll={true}>
 *   <Text>Scrollable Content</Text>
 * </Screen>
 */

import React from 'react';
import { View, ScrollView } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';

interface ScreenProps {
  children: React.ReactNode;
  scroll?: boolean;
}

export const Screen: React.FC<ScreenProps>= ({children, scroll = false}) => {
  let content;
  if (scroll === true) {
    content = (
      <ScrollView className = "p-4">
        {children}
      </ScrollView>
    );
  }
  else {
    content = (
      <View className = "p-4 flex-1">
        {children}
      </View>
    );
  }

  return (
    <SafeAreaView className = "flex-1 bg-gray-100">
      {content}
    </SafeAreaView>
  );
};