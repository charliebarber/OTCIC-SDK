from typing import Any


def collapse_avg(real_time: list[tuple[float, Any]], start: int, interval: int) -> tuple[Any, list[tuple[float, Any]]]:
    end = start + interval
    avg = 0
    new_real_time = real_time.copy()
    list_len = len(real_time)
    for i in range(list_len):
        log = real_time[i]
        if log[0] > end:
            break
        
        if i == list_len - 1 or real_time[i + 1][0] > end:
            leng = end - log[0]
            avg += log[1] * leng

            new_real_time.pop(0)
            new_real_time.insert(0, (end, log[1]))

        else:
            leng = real_time[i + 1][0] - log[0]
            avg += log[1] * leng

            new_real_time.pop(0)
    
    avg /= interval
    
    return avg, new_real_time