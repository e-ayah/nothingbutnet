# Progress

Figma: https://www.figma.com/design/IQVHZ6RXr0zA6EzIyTMcix/Design?node-id=1-3

The design is in my personal file and can be copied into the team file.

- Mobile: 393 × 852. Desktop: 1440 × 900.
- The headline shows elbow improvement from 84° to 86.2° (+2.2°).
- Separate elbow, knee, and shoulder charts show four sessions and shaded optimal-range bands.
- An orange card highlights shoulder alignment falling below the range in all four sessions.
- Empty, loading, and error layouts are below the main screens. The empty example has one saved session and explains that two are needed.
- Both main frames use Auto Layout. Each mobile chart is now a reusable component (elbow, knee, shoulder); desktop charts and remaining repeated controls still need component reuse.
- Font: Inter. Card radius: 12.
- Colors: cream #FFF8F0, burnt orange #B93815, brown #2D201B, secondary text #6F5D55, green #1F7A4D, pale green #E8F3EC, orange #B45309, pale orange #FFF0DC, white #FFFFFF, borders #DCCFC7.

I kept the same warm colors and Inter font as Compare and Goals so the pages feel connected. Separate charts keep each checkpoint easy to read, while the shaded bands show where the target range sits. The orange card gives the user one clear thing to focus on next practice.

Sample data, in degrees:

| Date (2026) | Elbow | Knee | Shoulder |
| --- | ---: | ---: | ---: |
| Sep 20 | 84 | 136 | 53 |
| Sep 24 | 85 | 142 | 51 |
| Sep 28 | 82 | 139 | 52 |
| Oct 2 | 86.2 | 145 | 49 |

Illustrative optimal ranges: elbow 90–100°, knee 140–150°, shoulder 55–65°. Charts use individually labeled angle scales. These are sample design values, not validated coaching guidance.

The screens are editable design mockups. Cloud saving needs verification because Figma showed a reconnect warning during editing. This notes file still needs placing in the project repository at docs/design/progress.md.
