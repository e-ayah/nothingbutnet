# Cavs#11 — Loading, error, and empty states

Figma: https://www.figma.com/design/IQVHZ6RXr0zA6EzIyTMcix/Design?node-id=38-910

Page: States. Eight editable mobile state components sit in the named collection. These are visual mockups, not wired interactions.

## Exact UI wording

| State | Heading | Supporting text | Action |
| --- | --- | --- | --- |
| Upload loading | Uploading… | Keep this screen open while your video uploads. | None |
| Results loading | Analyzing your shot… | This takes about a minute. / Checking elbow, knee, and shoulder angles | None |
| History loading | Loading your shots… | Three skeleton list rows | None |
| Upload error | Upload failed | Your video couldn’t finish uploading. / Check your connection and try again. | Try again |
| Results error | Analysis failed | We couldn’t find a player — film from the side. / Keep your full body visible, then try again. | Try again |
| Offline | No internet connection | Check your Wi-Fi or mobile data, / then try again. | Try again |
| History empty | No shots yet | Analyze your first free throw. / Your past shots will appear here. | Analyze a shot |
| Progress empty | One more session to go | You have 1 session. Analyze a second session / to see how your angles change over time. | Analyze a shot |

Slashes above indicate visual line breaks, not literal UI characters. Upload progress example: “65% · free-throw-01.mp4”, with a bar filled to 65%. Page titles: Upload a shot, Your results, Shot history, Your progress. Navigation: Upload / History / Progress.

## Behavior for implementation

- Upload loading: display real progress rather than a simulated percentage.
- Results loading: use indeterminate activity; the minute estimate is approximate.
- Retry preserves the selected video when possible. For a player-detection failure, let the user replace the video before retrying.
- Offline state can be used wherever network access is required.
- Progress empty applies below two sessions; for zero sessions use “Analyze two sessions to see how your angles change over time.”
- Analyze a shot opens Upload. History skeleton rows are placeholders, not selectable shots.

State cards use a 20 px radius; actions use 12 px. Text and recovery actions explain what to do next. Neutral skeletons avoid implying data exists, and errors use both text and an icon rather than color alone.

## Current style

Personal cream/orange design, requested by Ryan. This is not yet verified against the chosen team aesthetic or Cavs#07 styles/components.

- Inter; primary text #2D201B; secondary text #6F5D55.
- Background #FFF8F0; surfaces #FFFFFF; primary action #B93815 with white text.
- Success #1F7A4D on #E8F3EC; warning #B45309 on #FFF0DC.
- State icon background #F5E6D6; error icon background #FDEBE7; skeleton #E8DDD6.
- Mobile frames: 393 × 852. Screen headings 28–32 px; body 13–17 px; action labels 16 px.

## Handoff status

Created in the personal file. Shared Cavs#07 styles/components and the team-file transfer are pending. Verify these new changes are available online before handoff; earlier sync verification predates this work.
