# cherries

Library of utilities for Python 2.7 and 3+

[![Build Status](https://travis-ci.org/kosarev/cherries.svg?branch=master)](https://travis-ci.org/kosarev/cherries)

## Installation

```shell
pip install cherries
```


## cherries.RangeSet

A set of finite and infinite ranges.
Points of ranges are required to support the less-than (`<`) and
equals-to (`==`) operators.


### Example

```python
import cherries

# Create empty range.
rs = cherries.RangeSet()

# Add and remove some ranges.
rs.set(1, 7)
rs.set(9, 11)
rs.set(5, 8, False)

# Invert a range.
rs.invert_range(3, float('inf'))

# Verbalize resulting range set.
print(rs.get_bit_string(-5, 15, chars=['-', 'x']))
```

Output:

```
------xx--xxxx--xxxx
```

### Methods

* #### `RangeSet.__init__(value=False)`

  Initializes new empty range set.
  The optional value parameter specifies the initial value of the
  range set.


* #### `RangeSet.clear(value=False)`

  Empties existing range set.
  The optional value parameter specifies the initial value of the
  range set.


* #### `RangeSet.dump()`

  Dumps the internal state of the range set.


* #### `RangeSet.get_bit_string(start, end, chars=['0', '1'])`

  Verbalizes the range set as a bit string.


* #### `RangeSet.get_segments(start, end)`

  Within specified range generates a sequence of sub-ranges so
  that all points within each sub-range have the same value.
  The sub-ranges are represented as tuples of the form
  `(start, end, value)`.
  Sub-ranges come in order, beginning from one with the least
  start point.


* #### `RangeSet.invert()`

  Inverts the whole range set.


* #### `RangeSet.invert_range(start, end)`

  Inverts specified range.


* #### `RangeSet.is_inf(point_value)`

  Tests for a positive or negative infinite point.
  The default implementation tests for floating-point infinities
  and can be overriden as necessary to support custom point
  types.


* #### `RangeSet.set(start, end, value=True)`

  Sets a range to the specified value.
