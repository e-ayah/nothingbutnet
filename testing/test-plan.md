# NothingButNet Test Plan

## Sprint Testing

### Sprint 1 (Aces): September 25–October 1

Test each feature when its implementation is available. Record
unavailable features as blocked, not passed.

| Area | What to test | Tool or method |
| --- | --- | --- |
| Backend setup | Follow the README, start the backend, and confirm `/health` returns the expected response. | Terminal and Postman |
| API contract and schemas | Check request/response models against the contract's example JSON, including error formats. | Automated schema tests and contract review |
| Authentication helpers | Check password hashing, correct/incorrect password checks, and valid/invalid login tokens. | Automated tests |
| Database | Apply the first migration and confirm the expected tables are created. | Migration commands and database inspection |
| API client and app state | Check mock responses and storage of the login token, user, and current session. | Automated tests and iPhone/Expo Go |
| Login and Signup | Check required fields, invalid email, password confirmation, error messages, and mock login/signup behavior. | iPhone/Expo Go |
| App navigation and components | Check placeholder navigation, button states, text-field errors/password mode, and screen layouts. | iPhone/Expo Go |
| Video upload helper | Upload a sample video and confirm the returned URL opens the intended video. | Provided upload test script and web browser |
| ML calculations | Check known joint angles, shooting-hand detection, missing joints, feedback rules, and scores. | Automated tests using sample joint data |
| Video-reading helpers | Check frame reading, frame rate, dimensions, and duration against a known small clip. | Provided test script |
| Broadcast footage | Check pose detection on crowded scenes, camera cuts, replays, wrong angles, and cropped players. | Pose-detection script and visual review |
| Design and labeling | Review the three design directions for the planned screens and confirm the labeling guide separates shooting form from made/missed outcomes. | Web browser |
| GitHub templates | Confirm issue and PR templates appear after activation on the default branch. Create and close a clearly marked test issue. | Web browser |

Login and Signup use mock data during this sprint. Real authentication
integration will be tested when the backend endpoints are available.

### Remaining Sprint Coverage

Based on NothingButNet Sched - Schedule.pdf. All dates are in 2026.
These are planned checks, not completed test results.

| Sprint | Dates | What gets tested | Tools |
| --- | --- | --- | --- |
| 2A: Core pipeline and endpoints | Oct 2–5 | Signup, login, token checks, video upload, saved mock analysis, and session list/detail endpoints on the deployed backend. Check user isolation. Check pose extraction and release-frame detection using the selected 10-clip test set and answer key. | Postman; ML test scripts; visual video review |
| 2B: Upload and Results screens | Oct 6–8 | Video picking/recording, preview, tips, and upload progress. Check mock Results and History, real login/signup, logged-in navigation, and loading/error/empty states. Compare screens with the selected design. | iPhone/Expo Go; web browser for design review |
| 3A: Real analysis and deployment | Oct 9–12 | All deployed endpoints, real analysis output, processing/done/failed status, invalid-video rejection, and clear errors. Check skeleton overlays, angle labels, release-frame accuracy, and annotated-video playback. | Postman; ML accuracy scripts and answer key; iPhone/Expo Go; web browser |
| 3B: Real app flow and midterm | Oct 13–15 | Complete login → upload → processing → results flow. Check failed analysis, annotated video, real History/Profile, and the deployed web app. Rehearse the demo and check the backup recording before the midterm. | iPhone/Expo Go; web browser; Postman for investigating API failures |
| 4A: Progress backend | Oct 16–19 | Session comparisons, trends, recurring mistakes, progress summaries, goal calculations, session deletion, and upload format/size/length validation. Recheck pose fixes and angle ranges; validate training-data output. | Postman; automated auth tests; ML test scripts; real clips and edge-case videos |
| 4B: Progress screens | Oct 20–22 | Check charts against five real sessions, side-by-side comparisons, goal creation/progress, recurring-mistake alerts, and deletion from History. Check empty states and chart behavior on web. | iPhone/Expo Go; web browser; Postman to compare displayed values with API data |
| 5A: Backend beta preparation | Oct 23–26 | Production/staging separation, feedback endpoint, session tests, full pipeline, job logging, and security checks. Test 10 simultaneous uploads and the under-30-second-per-clip target. Compare classifiers with angle rules and rerun edge cases on staging. | Postman; concurrent load-test script; automated backend/ML tests; timing and evaluation scripts; iPhone uploads to staging |
| 5B: App beta preparation | Oct 27–29 | External tester access through Expo or the web fallback, production connection, small screens, feedback submission, first-launch onboarding, persistent login, empty states, and Results. Check survey/guide access and cross-browser behavior; record the beta go/no-go decision. | iPhone/Expo Go; web browsers including iPhone Safari; manual beta checklist |
| 6A: Backend and ML beta fixes | Oct 30–Nov 2 | Reproduce beta issues and have a teammate verify each fix. Check auth, uploads, sessions, analysis, progress, goals, and feedback. Recheck rejected videos, updated tips, and classifier flag/fallback behavior if enabled. Review logs for failures. | Postman; automated backend/ML tests; beta clips; server logs |
| 6B: App beta fixes | Nov 3–5 | Rerun the full app checklist on web and iPhone. Verify reported screen/component fixes, web loading performance, screen-reader behavior, and larger text sizes. Rehearse the draft showcase flow. | iPhone/Expo Go; web browser and browser developer tools; iPhone VoiceOver |
| 7A: Final fixes and code freeze | Nov 6–9 | Final backend and all 10 edge-case checks. Confirm no open Critical/High issues, verify final accuracy figures, check production demo data, review secrets/API documentation, and confirm the offline backup works. | Postman; automated backend/ML tests; GitHub issue review; iPhone/Expo Go; web browser |
| 7B: Showcase | Nov 10–12 | Final smoke tests of login, upload, analysis, results, and history on web and iPhone. Rehearse the live demo, verify the backup recording is downloaded and playable offline, and complete the showcase-day checklist. | iPhone/Expo Go; web browser; local video player |

### Test Results and Release Checks

- Record Pass, Fail, or Blocked for each check, with the tester,
  date, commit/build, environment, and evidence.
- Link failures to GitHub bug reports.
- Recheck affected features after fixes.
- Backend/ML checks support Monday PR deadlines; frontend checks
  support Thursday reviews.
- Follow the Nov 9 code freeze. Escalate failures to a PM;
  only PM-approved emergency changes are allowed afterward.
- The schedule also lists a Nov 30 club run-through and Dec 3 final.
  Repeat the demo smoke checks and offline-backup check before each.

## Required Edge Cases
Run these checks when the relevant features are available.
Record each result as Pass, Fail, or Blocked, with evidence.
Confirm unspecified limits and thresholds with the feature owner.

| # | Test case | What to check | Tool or method |
| --- | --- | --- | --- |
| 1 | Video too dark | Check joint detection confidence. If detection is unreliable, confirm the app gives clear feedback instead of misleading results. | Pose-detection script and iPhone/Expo Go |
| 2 | Player too far from camera | Check whether confidence falls below the team's threshold and whether low-confidence results are handled clearly. | Pose-detection script |
| 3 | Multiple people in frame | Confirm the intended shooter is analyzed. Record any incorrect person selection. | Pose-detection script and visual review |
| 4 | Video shorter than 1 second | Confirm the app handles insufficient footage without crashing and explains when analysis cannot be completed. | Postman and iPhone/Expo Go |
| 5 | Video longer than 2 minutes | Check the agreed duration limit, processing time, and timeout behavior. Confirm the app does not remain stuck loading. | Postman and iPhone/Expo Go |
| 6 | No person in the video | Confirm a clear error appears and no misleading analysis is shown. | Pose-detection script and iPhone/Expo Go |
| 7 | Wrong file format, such as PNG | Confirm unsupported uploads are rejected with a clear message by both the app and backend. | Postman and iPhone/Expo Go |
| 8 | Slow network | Confirm upload progress reflects activity and success or failure is communicated clearly. | iPhone/Expo Go on a throttled test connection |
| 9 | User logs out during analysis | Confirm logout clears local authentication and another user cannot view the previous user's results. Check processing behavior against the agreed session rules. | iPhone/Expo Go and Postman |
| 10 | Two users upload simultaneously | Confirm each upload and result stays associated with the correct user and session. | Two test accounts using Postman or separate app sessions |

## How to Report a Bug
- Create a GitHub issue using the Bug report template.
- Use a short title describing the problem.
- Record the app version or commit, device, and test environment.
- Include any setup needed, such as the test account or video used.
- Write numbered steps so another teammate can reproduce the bug.
- Explain the expected behavior and the actual behavior.
- Add a severity label and the relevant area label.
- Attach screenshots, video, or relevant logs when useful.
- Never include passwords, API keys, tokens, or private user data.

Example steps:
1. Log in with a test account.
2. Open the Upload screen.
3. Select a PNG file and submit it.
4. Observe whether the app rejects it with a clear error message.

## Verification Before Merging
A fix is verified when:

1. A teammate follows the original reproduction steps on the proposed
   fix and confirms the expected behavior.
2. Relevant automated tests pass, where available.
3. Related features and edge cases are checked for new problems.
4. The issue or PR records the tester, date, commit tested,
   environment, steps, results, and supporting evidence.
5. Failed or blocked checks are resolved before marking the fix verified.

Link the original bug issue in the fix's PR.
A PM reviews and merges into develop; contributors do not merge
their own work.

For the GitHub templates:
- Before merge, check the file locations, YAML front matter,
  and Markdown formatting.
- After the templates reach the default branch, confirm the issue
  and PR templates appear.
- Create a clearly labeled test issue, confirm the template contents
  and bug label, then close it.
- Record the outcome only after performing the check.