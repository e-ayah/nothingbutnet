I recommend keeping the original pose model (model_complexity=1). Across three clips, complexity 0 reduced my average pose extraction time from 6.34 s to 3.62 s, about 43% faster. However, it moved clip 02’s release from frame 226 to 285, exceeding the one-frame limit. On clip 03, the release shifted by only one frame, but an angle changed by 108.7°, exceeding the 2° limit. Complexity 2 was slower at 17.43 s per clip and missed the release on clip 02.

My next step is to test the original model with drawing skipped on frames without landmarks. I’ll time the full pipeline to see whether that change saves time while preserving the original results.


| Configuration | Average pose time per clip | Clip 01 release | Clip 02 release | Clip 03 release | Largest angle change |
|---|---:|---:|---:|---:|---:|
| Original | 6.34 s | None | 226 | 46 | Baseline |
| Complexity 0 | 3.62 s | 178 | 285 | 47 | 167.3° |
| Complexity 0 + skip drawing | 3.55 s | 178 | 285 | 47 | 167.3° |
| Complexity 2 + skip drawing | 17.43 s | None | None | 43 | 151.3° |