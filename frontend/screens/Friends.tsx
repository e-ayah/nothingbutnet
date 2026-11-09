import { useCallback, useRef, useState, type ComponentRef } from 'react';
import { Keyboard, Pressable, ScrollView, Text, View } from 'react-native';
import { useFocusEffect } from '@react-navigation/native';
import axios from 'axios';
import Button from '../components/Button';
import TextField from '../components/TextField';
import { Screen } from '../components/Screen';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';
import EmptyState from '../components/EmptyState';
import { friendlyError } from '../services/errorMessages';
import * as friendsApi from '../services/friendsApi';
import type { Friend, Requests } from '../services/friendsApi';
import { useStore } from '../store/useStore';

function actionError(error: unknown): string {
  const friendly = friendlyError(error);
  // Mock errors carry the exact user-facing message from the ticket.
  return error instanceof Error && !axios.isAxiosError(error) ? error.message : friendly;
}

function Person({ person }: { person: Friend }) {
  return (
    <View className="min-w-0 flex-1">
      <Text className="font-bold text-base text-[#62320D]">{person.name}</Text>
      <Text className="mt-1 font-sans text-sm text-[#744821]">@{person.username}</Text>
    </View>
  );
}

function Action({ label, text, disabled, onPress }: { label: string; text: string; disabled: boolean; onPress: () => void }) {
  return (
    <Pressable accessibilityRole="button" accessibilityLabel={label} accessibilityState={{ disabled }} disabled={disabled} onPress={onPress}
      className={`min-h-[44px] justify-center rounded-lg border border-[#A34A00] px-3 active:opacity-70 ${disabled ? 'opacity-50' : ''}`}>
      <Text className="font-bold text-sm text-[#A34A00]">{text}</Text>
    </Pressable>
  );
}

export default function FriendsScreen() {
  const token = useStore((state) => state.token);
  const user = useStore((state) => state.user);
  const [username, setUsername] = useState('');
  const [friends, setFriends] = useState<Friend[]>([]);
  const [requests, setRequests] = useState<Requests>({ incoming: [], outgoing: [] });
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [feedback, setFeedback] = useState<{ text: string; error: boolean } | null>(null);
  const [busy, setBusy] = useState<string | null>(null);
  const focused = useRef(false);
  const generation = useRef(0);
  const pending = useRef(false);
  const scroll = useRef<ComponentRef<typeof ScrollView>>(null);

  const load = useCallback(async () => {
    const current = ++generation.current;
    setLoadError(null);
    try {
      const [nextFriends, nextRequests] = await Promise.all([friendsApi.getFriends(token), friendsApi.getRequests(token)]);
      if (!focused.current || current !== generation.current) return;
      setFriends(nextFriends);
      setRequests(nextRequests);
    } catch (error) {
      if (focused.current && current === generation.current) setLoadError(actionError(error));
    } finally {
      if (focused.current && current === generation.current) setLoading(false);
    }
  }, [token]);

  useFocusEffect(useCallback(() => {
    focused.current = true;
    setLoading(true);
    setFeedback(null);
    void load();
    return () => { focused.current = false; generation.current += 1; };
  }, [load]));

  const runAction = async (key: string, work: (current: () => boolean) => Promise<string>) => {
    if (pending.current) return;
    pending.current = true;
    const currentGeneration = ++generation.current;
    const current = () => focused.current && currentGeneration === generation.current;
    setBusy(key);
    setFeedback(null);
    Keyboard.dismiss();
    try {
      const text = await work(current);
      if (current()) setFeedback({ text, error: false });
    } catch (error) {
      if (current()) setFeedback({ text: actionError(error), error: true });
    } finally {
      pending.current = false;
      if (focused.current) setBusy(null);
    }
  };

  const add = () => {
    const exact = username.trim();
    if (!exact) { setFeedback({ text: 'Enter an exact username', error: true }); return; }
    if (user && exact.toLowerCase() === (user as typeof user & { username?: string }).username?.toLowerCase()) {
      setFeedback({ text: "You can't add yourself", error: true });
      return;
    }
    void runAction('add', async (current) => {
      await friendsApi.sendRequest(exact, token);
      if (current()) setUsername('');
      try {
        const next = await friendsApi.getRequests(token);
        if (current()) setRequests(next);
      } catch {
        throw new Error('Request sent, but the list could not refresh. Use Reload below.');
      }
      return `Friend request sent to @${exact}`;
    });
  };

  return (
    <Screen>
      {loading ? <LoadingSpinner message="Loading friends…" /> : loadError ? (
        <ErrorMessage message={loadError} onRetry={() => { setLoading(true); void load(); }} />
      ) : (
        <ScrollView ref={scroll} keyboardShouldPersistTaps="handled" contentContainerStyle={{ flexGrow: 1, paddingBottom: 32 }}>
          <View className="w-full max-w-3xl self-center gap-6 rounded-card bg-[#FFD3AF] p-5 sm:p-8">
            <View className="gap-2">
              <Text accessibilityRole="header" className="font-bold text-3xl text-[#62320D]">Friends</Text>
              <Text className="font-sans text-base text-[#744821]">Build your basketball circle.</Text>
            </View>
            <View className="rounded-card bg-[#E7B282] p-4">
              <Text accessibilityRole="header" className="mb-4 font-bold text-xl text-[#62320D]">Add a friend</Text>
              <TextField label="Exact username" value={username} onChangeText={setUsername} autoCapitalize="none" />
              <Button title="Add" onPress={add} loading={busy === 'add'} disabled={busy !== null || !username.trim()} />
              {feedback && <Text accessibilityRole={feedback.error ? 'alert' : undefined} accessibilityLiveRegion="polite" className={`mt-3 font-sans text-base ${feedback.error ? 'text-[#85210E]' : 'text-[#28522A]'}`}>{feedback.text}</Text>}
              {feedback?.text.includes('could not refresh') && <View className="mt-3"><Button title="Reload" variant="secondary" disabled={busy !== null} onPress={() => { void load(); }} /></View>}
            </View>
            <View className="gap-3">
              <Text accessibilityRole="header" className="font-bold text-2xl text-[#62320D]">Requests</Text>
              <Text accessibilityRole="header" className="font-bold text-base text-[#744821]">Incoming requests</Text>
              {requests.incoming.length === 0 && <Text className="font-sans text-sm text-[#744821]">No incoming requests.</Text>}
              {requests.incoming.map((request) => (
                <View key={request.request_id} className="gap-3 rounded-card bg-[#E7B282] p-4">
                  <Person person={request.from} />
                  <View className="flex-row flex-wrap gap-2">
                    <Action label={`Accept ${request.from.name}`} text={busy === `accept-${request.request_id}` ? 'Accepting…' : 'Accept'} disabled={busy !== null} onPress={() => { void runAction(`accept-${request.request_id}`, async (current) => {
                      const { friend } = await friendsApi.accept(request.request_id, token);
                      if (current()) {
                        setFriends((items) => [...items.filter((item) => item.user_id !== friend.user_id), friend]);
                        setRequests((items) => ({ ...items, incoming: items.incoming.filter((item) => item.request_id !== request.request_id) }));
                      }
                      return `You and ${friend.name} are now friends`;
                    }); }} />
                    <Action label={`Decline ${request.from.name}`} text={busy === `decline-${request.request_id}` ? 'Declining…' : 'Decline'} disabled={busy !== null} onPress={() => { void runAction(`decline-${request.request_id}`, async (current) => {
                      await friendsApi.decline(request.request_id, token);
                      if (current()) setRequests((items) => ({ ...items, incoming: items.incoming.filter((item) => item.request_id !== request.request_id) }));
                      return `Request from ${request.from.name} declined`;
                    }); }} />
                  </View>
                </View>
              ))}
              <Text accessibilityRole="header" className="mt-2 font-bold text-base text-[#744821]">Outgoing requests</Text>
              {requests.outgoing.length === 0 && <Text className="font-sans text-sm text-[#744821]">No outgoing requests.</Text>}
              {requests.outgoing.map((request) => (
                <View key={request.request_id} className="flex-row items-center gap-3 rounded-card bg-[#E7B282] p-4">
                  <Person person={request.to} />
                  <Text className="font-bold text-sm text-[#744821]">Pending</Text>
                </View>
              ))}
            </View>
            <View className="gap-3">
              <Text accessibilityRole="header" className="font-bold text-2xl text-[#62320D]">Friends · {friends.length}</Text>
              {friends.length === 0 ? (
                <View className="min-h-[200px] overflow-hidden rounded-card">
                  <EmptyState title="Add your first friend" message="Know someone who shoots hoops? Send them a request by username." actionLabel="Add a friend" onAction={() => scroll.current?.scrollTo({ y: 0, animated: true })} />
                </View>
              ) : friends.map((friend) => (
                <View key={friend.user_id} className="flex-row items-center gap-3 rounded-card bg-[#E7B282] p-4">
                  <Person person={friend} />
                  <Action label={`Remove ${friend.name}`} text={busy === `remove-${friend.user_id}` ? 'Removing…' : 'Remove ×'} disabled={busy !== null} onPress={() => { void runAction(`remove-${friend.user_id}`, async (current) => {
                    await friendsApi.removeFriend(friend.user_id, token);
                    if (current()) setFriends((items) => items.filter((item) => item.user_id !== friend.user_id));
                    return `${friend.name} removed from friends`;
                  }); }} />
                </View>
              ))}
            </View>
          </View>
        </ScrollView>
      )}
    </Screen>
  );
}
