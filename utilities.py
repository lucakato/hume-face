from typing import Any, Dict, List
from collections import defaultdict

def get_emotions(emotions: List[Dict[str, Any]]) -> None:
    emotion_map = {e["name"]: e["score"] for e in emotions}
    res = defaultdict(float)
    for emotion in ["Joy", "Sadness", "Anger"]:
        res[emotion] += emotion_map[emotion]
        #print(f"- {emotion}: {emotion_map[emotion]:4f}")
    
    rounded_res = {key: round(value, 3) for key, value in res.items()}
    return rounded_res