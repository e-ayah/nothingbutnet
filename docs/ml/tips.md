Basketball Coaching Tips

Purpose

The coaching-tip engine converts measured joint angles into simple, actionable feedback for beginner basketball players. Each checkpoint has a tip for an angle within the target range, below the range, and above the range.

Optimal Angle Ranges

| Checkpoint        | Angle range | Purpose                                                |
| ----------------- | ----------- | ------------------------------------------------------ |
| Elbow alignment   |     85–100° | Encourages consistent elbow positioning under the ball |
| Knee bend         |    150–175° | Helps players use their legs during the shot           |
| Shoulder position |      45–75° | Helps players maintain a controlled shooting position  |

Coaching Tips

| Checkpoint        | Status   | Tip                                                            |
| ----------------- | -------- | -------------------------------------------------------------- |
| Elbow alignment   | Good     | Great elbow alignment — keep your elbow under the ball.        |
| Elbow alignment   | Too low  | Raise your elbow so it lines up under the ball.                |
| Elbow alignment   | Too high | Lower your elbow so it stays under the ball.                   |
| Knee bend         | Good     | Great knee bend — keep your legs ready to drive the shot.      |
| Knee bend         | Too low  | Straighten your legs slightly before releasing the ball.       |
| Knee bend         | Too high | Bend your knees a little more before shooting.                 |
| Shoulder position | Good     | Great shoulder position — keep it steady as you shoot.         |
| Shoulder position | Too low  | Raise your shooting shoulder slightly as you prepare to shoot. |
| Shoulder position | Too high | Lower your shooting shoulder slightly as you prepare to shoot. |

Implementation

The `get_tip(checkpoint, angle, low, high)` function selects a tip based on whether the measured angle falls below, within, or above the supplied range. The boundary values are considered within the optimal range.

Sources

How to Shoot a Basketball (https://jr.nba.com/shooting)
How to Shoot a Basketball: 3 Steps to Get Your Shot Down (https://www.adidas.com/us/blog/how-to-shoot-a-basketball-3-steps-to-get-your-shot-down)
USA Basketball - 7 Tips to Improve Your Shooting Mechanics (https://www.usab.com/news/2014/01/7-tips-to-improve-your-shooting-mechanics)
