# NothingButNet Test Plan

## Sprint Testing
### Sprint Aces: September 24–October 1

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
| Design and labeling | Review the six design pages and confirm the labeling guide separates shooting form from made/missed outcomes. | Web browser |
| GitHub templates | Confirm issue and PR templates appear after activation on the default branch. Create and close a clearly marked test issue. | Web browser |

Login and Signup use mock data during this sprint. Real authentication
integration will be tested when the backend endpoints are available.

### Future Sprints

Pending PM confirmation of the semester roadmap. Add one section per
sprint with its dates, planned features, test cases, and tools.
This section must be completed to finalize semester-wide coverage.
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