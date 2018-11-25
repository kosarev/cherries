
import bisect


class RangeSet(object):
    '''A set of finite and infinite ranges. Points of ranges are
       required to support the less-than ('<') and
       equals-to ('==') operators.'''

    def __init__(self, value=False):
        '''Initializes new empty range set. The optional value
           parameter specifies the initial value of the range
           set.'''
        self.clear(value)

    def is_inf(self, point):
        '''Tests for a positive or negative infinite point. The
           default implementation tests for floating-point
           infinities and can be overriden as necessary to
           support custom point types.'''
        return point in [float('-inf'), float('+inf')]

    def dump(self):
        '''Dumps the internal state of the range set.'''
        print(self._leftmost_segment_value, self._points)

    def clear(self, value=False):
        '''Empties existing range set. The optional value
           parameter specifies the initial value of the range
           set.'''

        # The array of points in this set. Points are stored in
        # strictly increasing order, meaning there shall be no
        # points that compare equal in this array. Every point
        # starts another segment. The value of a segment is the
        # inversion of the value of the segment it follows.
        #
        # Each range set has at least one segment, which is the
        # implicit left infinite segment that starts at -inf.
        # Its value is stored explicitly.
        #
        # In the context of this class, a range is a segment of a
        # specific value, so two consequitve ranges have a gap
        # segment between them.
        #
        # Point indexes are their indexes in this array of points.
        #
        # Segments and ranges are specified as indexes of their
        # end points, so the left infinite segment has index 0.
        self._points = []

        # The value of the left infinite segment.
        self._leftmost_segment_value = bool(value)

    def _get_num_of_points(self):
        return len(self._points)

    def _is_existing_point(self, point):
        return 0 <= point < self._get_num_of_points()

    def _get_first_point(self):
        return 0

    def _is_first_point(self, point):
        return point == self._get_first_point()

    def _get_past_last_point(self):
        return self._get_num_of_points()

    def _is_past_last_point(self, point):
        return point == self._get_past_last_point()

    def _is_last_point(self, point):
        return self._is_past_last_point(point + 1)

    # Makes sure the invariant is maintained for a given point.
    def _check_invariant(self, point):
        value = self._get_point_value(point)
        assert (self._is_first_point(point) or
                self._get_point_value(point - 1) < value)
        assert (self._is_last_point(point) or
                value < self._get_point_value(point + 1)), self._points

    def _get_point_value(self, point):
        assert self._is_existing_point(point)
        return self._points[point]

    def _set_point_value(self, point, value):
        assert self._is_existing_point(point)
        self._points[point] = value
        self._check_invariant(point)

    def _insert_point(self, point, value):
        self._points.insert(point, value)
        self._check_invariant(point)

    def _remove_point(self, point):
        assert self._is_existing_point(point)
        del self._points[point]

    def _remove_points(self, start, end):
        if start == end:
            return

        assert start < end
        assert self._is_existing_point(start)
        assert self._is_existing_point(end - 1)
        del self._points[start:end]

    # Replaces a range of points with a single point.
    def _replace_points(self, start, end, value):
        if start == end:
            self._insert_point(start, value)
            return

        assert start < end
        self._remove_points(start + 1, end)
        self._set_point_value(start, value)

    def _get_num_of_segments(self):
        # The implicit left infinite segment is always there.
        # Plus, every point starts another segment.
        return 1 + self._get_num_of_points()

    def _get_past_last_segment(self):
        return self._get_num_of_segments()

    def _is_valid_segment(self, segment):
        # The segment that immediately follows the current
        # rightmost infinite segment is considered valid, because
        # it can be added to the set as its new rightmost
        # infinite segment.
        return 0 <= segment <= self._get_past_last_segment()

    def _is_past_last_segment(self, segment):
        return segment == self._get_past_last_segment()

    def _has_finite_start(self, segment):
        assert self._is_valid_segment(segment)
        return segment > 0

    def _has_finite_end(self, segment):
        assert self._is_valid_segment(segment)
        return segment < self._get_num_of_points()

    def _has_infinite_start(self, segment):
        return not self._has_finite_start(segment)

    def _has_infinite_end(self, segment):
        return not self._has_finite_end(segment)

    def _get_start(self, segment):
        # The left infinite segment has no index for its
        # start point.
        assert self._has_finite_start(segment)

        # Segments are specified as indexes of their end points.
        end_point_index = segment
        start_point_index = end_point_index - 1

        return start_point_index

    def _get_end(self, segment):
        assert self._is_valid_segment(segment)

        # Segments are specified as indexes of their end points.
        end_point_index = segment

        return end_point_index

    def _get_start_value(self, segment):
        assert self._has_finite_start(segment)
        return self._get_point_value(self._get_start(segment))

    def _set_start_value(self, segment, point):
        assert self._has_finite_start(segment)
        self._set_point_value(self._get_start(segment), point)

    def _get_end_value(self, segment):
        assert self._has_finite_end(segment)
        return self._get_point_value(self._get_end(segment))

    def _set_end_value(self, segment, point):
        assert self._has_finite_end(segment)
        self._set_point_value(self._get_end(segment), point)

    def _get_next_segment(self, segment):
        assert self._is_valid_segment(segment)
        assert not self._is_past_last_segment(segment)
        return segment + 1

    def _get_segment_value(self, segment):
        assert self._is_valid_segment(segment)
        value = self._leftmost_segment_value
        inverted = (segment % 2 != 0)
        if inverted:
            value = not value
        return value

    # Returns the segment that contains the specified point.
    def _find_segment(self, value):
        return bisect.bisect_right(self._points, value)

    def _is_before_segment(self, value, segment):
        if self._has_infinite_start(segment):
            return False

        return value < self._get_start_value(segment)

    def _extend_segment_start(self, segment, value):
        if self._has_finite_start(segment):
            value = min(value, self._get_start_value(segment))
            self._set_start_value(segment, value)

    def _extend_segment_end(self, segment, value):
        if self._has_finite_end(segment):
            value = max(value, self._get_end_value(segment))
            self._set_end_value(segment, value)

    def _extend_segment(self, segment, start, end):
        self._extend_segment_start(segment, start)
        self._extend_segment_end(segment, end)

    def _insert_segment(self, segment, start, end):
        index = self._get_start(segment)
        self._insert_point(index, end)
        self._insert_point(index, start)

    def _is_first_range(self, range):
        # A set may contain two first ranges for each of the two
        # possible values.
        assert self._is_valid_segment(range)
        return range < 2

    def _is_past_last_range(self, range):
        assert self._is_valid_segment(range)
        return range == self._get_num_of_points() + 1

    def _get_prev_range(self, range):
        assert self._is_valid_segment(range)
        assert not self._is_first_range(range)
        return range - 2

    # Returns the range that contains or follows the specified point.
    def _find_range(self, point, value):
        segment = self._find_segment(point)
        if not (self._get_segment_value(segment) == value):
            segment = self._get_next_segment(segment)
        return segment

    def set(self, start, end, value=True):
        '''Sets a range to the specified value.'''
        if end < start:
            start, end = end, start

        if start == end:
            return

        if self.is_inf(start) and self.is_inf(end):
            self.clear(value)
            return

        if self.is_inf(start):
            range = self._find_range(end, value)

            if (self._is_past_last_range(range) or
                    self._is_before_segment(end, range)):
                self._replace_points(self._get_first_point(),
                                     self._get_start(range), end)
            else:
                # Make the existing range to be the new infinite
                # left segment.
                self._remove_points(self._get_first_point(),
                                    self._get_end(range))

            self._leftmost_segment_value = value
            return

        # Find an existing range that contains or follows the start point.
        range = self._find_range(start, value)

        # If the previous range ends where the new range starts,
        # move to that preceding range.
        if not self._is_first_range(range):
            prev_range = self._get_prev_range(range)
            if self._get_end_value(prev_range) == start:
                range = prev_range

        if self.is_inf(end):
            if self._has_infinite_start(range):
                self.clear(value)
                return

            if self._is_past_last_range(range):
                self._insert_point(self._get_start(range), start)
                return

            self._extend_segment_start(range, start)
            self._remove_points(self._get_end(range),
                                self._get_past_last_point())
            return

        if (self._is_past_last_range(range) or
                self._is_before_segment(end, range)):
            self._insert_segment(range, start, end)
            return

        # Combine the new range with possible following
        # intersecting ranges.
        end_range = self._find_range(end, value)

        if (self._is_past_last_range(end_range) or
                self._is_before_segment(end, end_range)):
            # The new range ends before the end range. Remove
            # ranges between the start and end ranges.
            self._remove_points(
                self._get_end(self._get_next_segment(range)),
                self._get_start(end_range))
        else:
            # The end range contains the end point of the new
            # range. Collapse the start and end ranges into a
            # single range.
            self._remove_points(self._get_end(range),
                                self._get_end(end_range))

        self._extend_segment(range, start, end)

    def invert(self):
        '''Inverts the whole range set.'''
        self._leftmost_segment_value = not self._leftmost_segment_value

    def _invert_at(self, value):
        assert not self.is_inf(value)
        segment = self._find_segment(value)

        if (self._has_infinite_start(segment) or
                self._get_start_value(segment) != value):
            self._insert_point(self._get_end(segment), value)
        else:
            self._remove_point(self._get_start(segment))

    def invert_range(self, start, end):
        '''Inverts specified range.'''
        if end < start:
            start, end = end, start

        if start == end:
            return

        if self.is_inf(start):
            self.invert()
        else:
            self._invert_at(start)

        if self.is_inf(end):
            pass
        else:
            self._invert_at(end)

    def get_segments(self, start, end):
        '''Within specified range generates a sequence of
           sub-ranges so that all points within each sub-range
           have the same value. The sub-ranges are represented as
           tuples of the form (start, end, value). Sub-ranges
           come in order, beginning from one with the least start
           point.'''
        if end < start:
            start, end = end, start

        segment = self._find_segment(start)
        value = self._get_segment_value(segment)

        while start < end:
            if self._has_infinite_end(segment):
                yield start, end, value
                return

            segment_end = min(end, self._get_end_value(segment))
            yield start, segment_end, value

            start = segment_end
            segment = self._get_next_segment(segment)
            value = not value

    def get_bit_string(self, start, end, chars=['0', '1']):
        '''Verbalizes the range set as a bit string.'''
        segments = self.get_segments(start, end)
        return ''.join(chars[v] * (e - s) for s, e, v in segments)
