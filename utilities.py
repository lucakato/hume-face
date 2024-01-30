from typing import Any, Dict, List
from collections import defaultdict

def print_emotions(emotions: List[Dict[str, Any]]) -> None:
    emotion_map = {e["name"]: e["score"] for e in emotions}
    res = defaultdict(float)
    for emotion in ["Joy", "Sadness", "Anger"]:
        res[emotion] += emotion_map[emotion]
        #print(f"- {emotion}: {emotion_map[emotion]:4f}")
    
    #print(res)
    return res