# OTCIC Library Python Design

## Aggregate Model

The Aggregate Model consists of an Aggregate class, that stores the recorded data. This is done in the form of multiple subclasses that link back to the Aggregate class.

```Aggregate class
  |- RAM
  |- CPU
  |- Disk
  |- GPU
```



## RAM Tracing

Memory allocation will be tracked using `tracemalloc` library. Both `peak` and `average` RAM will be recorded.
-    `peak`: Maximum memory allocated within a time-slot - `high` value of a candle stick
- `average`: Average amount of memory allocated in a given time interval.

There are implications that RAM may consume more power when it is more utilised, but in a non-linear relationship. This may mean that energy values will have to be implemented client-side, and calculated in detail, using every timestamp instead of using a pre-calculated value and multiplying it with a modifier value.

Example:
```
RAM Values:
seconds, bytes
 0 |   0  |-|  10 |  24
 2 |  12  |-|  14 |  28
 5 |  32  |-|  20 |  32
 6 |  48  |-|  25 |  36
 7 |  28  |-|  28 |  28
...
cut off 30s
```

In this example, the average RAM calculated in a 30-second interval will go as follows:
The RAM chart is visualised as an area chart, with squares being drawn.

```
RAM Allocated
48 |     __
36 |     ||                 ____
32 |    _||            _____|  |
28 |    |||___   ______|    |  |__.
24 |    |||  |___|     |    |  | -
12 | ___|||  |   |     |    |  | -
 0 |_|  |||  |   |     |    |  | -
   ' '  '''  '   '     '    '  ' '
   0 2  567 10  14    20   25 28 30
Time
```

An average of the 30-second interval is calculated by multiplying the time and memory allocation, then dividing by total time

```
Average = (   ( 2 -  0) *  0 (=   0)
            + ( 5 -  2) * 12 (=  36)
            + ( 6 -  5) * 32 (=  32)
            + ( 7 -  6) * 48 (=  48)
            + (10 -  7) * 28 (=  84)
            + (14 - 10) * 24 (=  96)
            + (20 - 14) * 28 (= 168)
            + (25 - 20) * 32 (= 160)
            + (28 - 25) * 36 (= 108)
            + (30 - 28) * 28 (=  56)
          ) / 30

        = 788 / 30
        = ~26.267 bytes on average
```

Values are added to RAM Values as a Queue. When data from that queue is consolidated, the Queue is cleared of all the measured values, then replaced by a substitute value when necessary

```
Ram Values:
30 |  28
```

## WIP