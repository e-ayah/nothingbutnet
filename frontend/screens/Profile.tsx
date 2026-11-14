import { useCallback, useState } from 'react';
import { Linking, Pressable, Text, View } from 'react-native';
import { useFocusEffect } from '@react-navigation/native';
import Svg, { Circle, Path } from 'react-native-svg';
import * as api from '../services/api';
import { useStore } from '../store/useStore';

// beta feedback form (from docs/beta-guide.md)
const FEEDBACK_FORM_URL = 'https://forms.gle/d76Ve3R4DwmqWG4Q6';

// colors from docs/design/profile.md
const C = {
  darkRust: '#8A4416', rust: '#A0521D', lightOrange: '#E0914F',
  orange: '#CC6600', peach: '#F6D9BC', navy: '#1A1A2E', light: '#F8F8FF',
};
const BOLD = 'Inter_700Bold';
const REG = 'Inter_400Regular';

export default function ProfileScreen() {
  const token = useStore((s) => s.token);
  const logout = useStore((s) => s.logout);
  const [me, setMe] = useState<{
    name: string;
    email: string;
    username?: string | null;
  } | null>(null);
  const [count, setCount] = useState<number | null>(null);

  // reload name + shot count every time the screen opens
  useFocusEffect(
    useCallback(() => {
      if (!token) return;
      api.getMe(token).then(setMe).catch(() => setMe(null));
      api.getSessions(token).then((s) => setCount(s.length)).catch(() => setCount(null));
    }, [token])
  );

  const initials = (me?.name ?? '?').slice(0, 2).toUpperCase();

  return (
    <View style={{ flex: 1, backgroundColor: C.peach, overflow: 'hidden' }}>
      {/* top waves */}
      <Svg width="100%" height={260} viewBox="0 0 393 260" preserveAspectRatio="none" style={{ position: 'absolute', top: 0 }}>
        <Path d="M0 0H393V230C330 270 270 190 196 230C120 270 60 190 0 230Z" fill={C.rust} />
        <Path d="M0 0H393V190C330 230 270 150 196 190C120 230 60 150 0 190Z" fill={C.darkRust} />
      </Svg>
      {/* bottom waves */}
      <Svg width="100%" height={220} viewBox="0 0 393 220" preserveAspectRatio="none" style={{ position: 'absolute', bottom: 0 }}>
        <Path d="M0 20C80 -20 140 60 200 20C260 -20 320 60 393 20V220H0Z" fill={C.lightOrange} />
        <Path d="M0 80C80 40 140 120 200 80C260 40 320 120 393 80V220H0Z" fill={C.rust} />
        <Path d="M0 140C80 100 140 180 200 140C260 100 320 180 393 140V220H0Z" fill={C.darkRust} />
      </Svg>

      <View style={{ flex: 1, paddingHorizontal: 24, paddingTop: 32, paddingBottom: 32, maxWidth: 480, width: '100%', alignSelf: 'center' }}>
        {/* header: avatar, label, name, email */}
        <View style={{ width: 56, height: 56, borderRadius: 28, backgroundColor: C.navy, alignItems: 'center', justifyContent: 'center' }}>
          <Text style={{ fontFamily: BOLD, fontSize: 20, color: C.lightOrange }}>{initials}</Text>
        </View>
        <Text style={{ fontFamily: BOLD, fontSize: 14, letterSpacing: 2, color: C.lightOrange, marginTop: 16 }}>PROFILE</Text>
        <Text style={{ fontFamily: BOLD, fontSize: 45, lineHeight: 48, color: C.light }} numberOfLines={2}>{me?.name ?? '—'}</Text>
        <Text style={{ fontFamily: REG, fontSize: 16, color: C.lightOrange }}>{me?.email ?? ''}</Text>
        <Text style={{ fontFamily: REG, fontSize: 14, color: C.lightOrange, marginTop: 6 }}>
          Username: {me?.username ?? '—'}
        </Text>

        {/* stat card */}
        <View style={{ marginTop: 56, backgroundColor: C.navy, borderRadius: 24, padding: 24, flexDirection: 'row', alignItems: 'center' }}>
          <View style={{ flex: 1 }}>
            <Text style={{ fontFamily: BOLD, fontSize: 14, letterSpacing: 2, color: C.lightOrange }}>SHOTS ANALYZED</Text>
            <Text style={{ fontFamily: BOLD, fontSize: 64, color: C.light }}>{count ?? '—'}</Text>
          </View>
          {/* basketball icon */}
          <Svg width={68} height={68} viewBox="0 0 68 68">
            <Circle cx={34} cy={34} r={31} stroke={C.orange} strokeWidth={3} fill="none" />
            <Path d="M3 34H65M34 3V65M12 12C24 24 24 44 12 56M56 12C44 24 44 44 56 56" stroke={C.orange} strokeWidth={3} fill="none" />
          </Svg>
        </View>

        {/* send feedback row */}
        <Pressable
          onPress={() => Linking.openURL(FEEDBACK_FORM_URL)}
          style={{ marginTop: 16, backgroundColor: C.rust, borderRadius: 16, padding: 24, flexDirection: 'row', justifyContent: 'space-between' }}
        >
          <Text style={{ fontFamily: BOLD, fontSize: 18, color: C.light }}>Send feedback</Text>
          <Text style={{ fontFamily: BOLD, fontSize: 20, color: C.lightOrange }}>↗</Text>
        </Pressable>

        <View style={{ flex: 1 }} />

        {/* log out (navigation switches to Login automatically) */}
        <Pressable
          onPress={logout}
          style={{ height: 56, borderRadius: 16, backgroundColor: C.navy, alignItems: 'center', justifyContent: 'center' }}
        >
          <Text style={{ fontFamily: BOLD, fontSize: 16, color: C.lightOrange }}>Log out</Text>
        </Pressable>
      </View>
    </View>
  );
}