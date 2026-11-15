# Beta go/no-go — Thu 10/29

Server: https://nothingbutnet-0l0a.onrender.com/health → ok, db: true · https://nothingbutnet-0l0a.onrender.com/health/ml → ok
Web: https://nothingbutnet-op.vercel.app

| # | Step | iPhone (Expo Go) | Web (phone browser) | Web (laptop) | Notes |
|---|---|---|---|---|---|
| 1 | Sign up a new account | [ ] | [ ] | [ ] | First sign-up of the day may take ~1 min (server waking up) — not a fail |
| 2 | Close + reopen → still logged in | [ ] | [ ] | [ ] | |
| 3 | Upload a 10 s clip, see upload % | [ ] | [ ] | [ ] | Web: camera button may not work; use "choose video" → phone offers "Take Video" |
| 4 | Analyzing… then Results open by themselves | [ ] | [ ] | [ ] | |
| 5 | Results: video plays, score, 3 angles, tips | [ ] | [ ] | [ ] | |
| 6 | A no-person video → friendly failed screen | [ ] | [ ] | [ ] | |
| 7 | History lists both, newest first → Results | [ ] | [ ] | [ ] | |
| 8 | Log out → Login; log in again | [ ] | [ ] | [ ] | |
| 9 | Wi-Fi off → friendly "can't reach" message | [ ] | [ ] | [ ] | |

**Go** = steps 1–7 pass on web + at least one iPhone.
Anything failing → GitHub Issue, labelled `beta`.

Time from upload to Results: ____ s (write it down — testers will ask)

## Who tests what
- iPhone (Expo Go): TBD
- Web (phone browser): TBD
- Web (laptop): TBD


## Finals additions: social features, Compare and onboarding

Mark each cell PASS, FAIL (with the Issue number, e.g. FAIL #112), or N/A. Leave a cell blank if not yet run. Use a throwaway account, never the demo account.

| # | Feature | Steps | Expected result | Pass 1 web | Pass 1 iPhone | Pass 2 web | Pass 2 iPhone |
|---|---------|-------|-----------------|------------|---------------|------------|---------------|
| N1 | Did it go in? | Record or upload a shot and open the result | The screen asks or shows whether the shot went in, and the answer is saved with the session | | | | |
| N2 | Did it go in? | Open History and the same session | The make/miss answer matches what you chose | | | | |
| N3 | Share | Open a finished session and tap Share | The share sheet or link opens with no error | | | | |
| N4 | Share | Open the shared link in a private/incognito window or on another device | The shared content loads correctly | | | | |
| N5 | Friends | Open the Friends screen | The screen loads with no crash and shows an empty or current friend list | | | | |
| N6 | Friends | Search for or add another test account as a friend | A request is sent and shows as pending | | | | |
| N7 | Friends | On the second account, accept the request | Both accounts show each other in the friends list | | | | |
| N8 | Leaderboard | Open the Leaderboard screen | Rankings load, with you and your friends listed, and no blank rows or NaN values | | | | |
| N9 | Compare | Open Compare and pick two sessions or two friends | The comparison renders with real values and no blank or NaN fields | | | | |
| N10 | Recurring-mistake card | After 3 or more analyzed sessions, open the screen where the card appears | The card appears and its text is readable and makes sense for the sessions | | | | |
| N11 | Profile | Open Profile | Name and username display correctly | | | | |
| N12 | Profile | Edit your name, save, then log out and back in | The new name is still shown | | | | |
| N13 | Onboarding | Sign up with a brand new throwaway account | The onboarding screens appear in order with no crash | | | | |
| N14 | Onboarding | Finish onboarding | You land on the main screen, and onboarding does not repeat on the next login | | | | |