from typing import Any
import random as r

def generate_real_time_list(start: int, min_range: int = 3) -> list[tuple[float, int]]:
    t = start
    real_time = []
    for i in range(r.randint(min_range * 10, min_range * 20)):
        real_time.append((t, r.randint(1, 16) * 256))
        t += (1 + r.random()) / 10
    
    return real_time
