import { create } from 'zustand'
import { createJSONStorage, persist } from 'zustand/middleware'
import AsyncStorage from '@react-native-async-storage/async-storage'
import * as SecureStore from 'expo-secure-store'
import { Platform } from 'react-native'

const secureStorage = {
    getItem: (key: string) => SecureStore.getItemAsync(key),
    setItem: (key: string, value: string) => SecureStore.setItemAsync(key, value),
    removeItem: (key: string) => SecureStore.deleteItemAsync(key),
}

interface State {
    token: string | null
    user: {id: string; name: string; email: string} | null
    currentSessionId: string | null
}

interface Actions {
    setAuth: (token: string, user: {id: string; name: string; email: string}) => void
    logout: () => void
    setCurrentSession: (id: string) => void
}

export const useStore = create<State & Actions>()(persist((set) => ({
    token: null,
    user: null,
    currentSessionId: null,
    
    setAuth: (token, user) => set((state) => ({token: token, user: user})),
    logout: () => set((state) => ({token: null, user: null, currentSessionId: null})),
    setCurrentSession: (id) => set((state) => ({currentSessionId: id})),
}), {
    name: 'nbn-auth',
    storage: createJSONStorage(() => Platform.OS === 'web' ? AsyncStorage : secureStorage),
    partialize: (state) => ({ token: state.token, user: state.user }),
}))
