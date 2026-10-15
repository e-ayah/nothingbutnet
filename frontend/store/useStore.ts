import { create } from 'zustand'

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

export const useStore = create<State & Actions>((set) => ({
    token: null,
    user: null,
    currentSessionId: null,
    
    setAuth: (token, user) => set((state) => ({token: token, user: user})),
    logout: () => set((state) => ({token: null, user: null, currentSessionId: null})),
    setCurrentSession: (id) => set((state) => ({currentSessionId: id})),
}))