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
```RAM Values:
seconds, bytes
 0 |   0
 2 |  12
 5 |  32
 6 |  48
 7 |  28
10 |  24
14 |  28
20 |  32
25 |  36
28 |  28
...
```

In this example, the average RAM calculated in a 30-second interval will go as follows:
The RAM chart is visualised as an area chart, with squares being drawn.

```
48 |     __
36 |     ||
32 |    _||
28 |    |||___
24 |    |||  |
12 | ___|||  |
 0 |_|  |||  |
   ' '  '''  '   '     '    '  ' '
   0 2  567 10  14    20   25 28 30
```

WIP

## WIP