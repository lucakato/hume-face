from typing import Any, Dict, List
from collections import defaultdict

all_emotions = [
    'Admiration', 'Adoration', 'Aesthetic Appreciation', 'Amusement', 'Anger',
    'Anxiety', 'Awe', 'Awkwardness', 'Boredom', 'Calmness',
    'Concentration', 'Confusion', 'Contemplation', 'Contentment',
    'Craving', 'Desire', 'Determination', 'Disappointment', 'Disgust',
    'Distress', 'Doubt', 'Embarrassment', 'Empathic Pain', 'Entrancement',
    'Envy', 'Excitement', 'Fear', 'Guilt', 'Horror', 'Interest',
    'Joy', 'Love', 'Nostalgia', 'Pain', 'Pride', 'Realization', 'Relief',
    'Romance', 'Sadness', 'Satisfaction', 'Shame', 'Surprise (negative)',
    'Surprise (positive)', 'Sympathy', 'Tiredness', 'Triumph'
]

def get_emotions(emotions: List[Dict[str, Any]]) -> None:
    emotion_map = {e["name"]: e["score"] for e in emotions}
    top_three_emotions = []
    max_heap = []

    for emotion in all_emotions:
        max_heap.append((-round(emotion_map[emotion], 3), emotion))
        #print(f"- {emotion}: {emotion_map[emotion]:4f}")
    
    for _ in range(3):
        score, emotion = max_heap.pop()
        top_three_emotions.append((emotion, -score))
    
    return top_three_emotions