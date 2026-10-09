# chose 3 in total as in general people should focus on more
# general errrs rather than a random three that they occasionally
# miss in a row

def recurring(sessions, min_count=3):
    counts = {}
    latest_tips = {}

    for session in sessions:
        for item in session["feedback"]:
            if item["status"] == "needs_work":
                name = item["checkpoint"]
                counts[name] = counts.get(name, 0) + 1
                latest_tips[name] = item["tip"]
    
    results = []
    for checkpoint, count in counts.items():
        if count >= min_count:
            results.append(
                {
                    "checkpoint": checkpoint,
                    "count": count,
                    "latest_tip": latest_tips[checkpoint],
                }
            )
            
    return results