import heapq
from typing import Any, Dict, List

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

    for emotion, score in emotion_map.items():
        heapq.heappush(max_heap, (-round(score, 3), emotion))
    
    for _ in range(3):
        score, emotion = heapq.heappop(max_heap)
        top_three_emotions.append((emotion, -score))
    
    return top_three_emotions