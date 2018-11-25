#!/usr/bin/env python3


# A simplified representation of infinities of both signs in the
# tests. Helps to not bother with handling real infinite values.
INF = 99


# Generates pairs of range sets and ranges by varying the number
# of points before the start of the range, between its points and
# after its end.
def generate_range_set_schemes():
    for before in range(3):
        for between in range(7):
            for after in range(3):
                yield before, between, after


# Generates various paddings for a finite end of a range.
def generate_point_paddings(head_paddings, tail_paddings):
    for head in range(3 if head_paddings else 1):
        for tail in range(3 if tail_paddings else 1):
            yield head, tail


# Generates combinations of paddings for points of a range. For
# infinite points it always yields empty paddings.
def generate_range_paddings(scheme):
    # Paddings only make sense for finite points:
    #
    # --- P . P --- P . P ---
    # --- P . P ---   .
    # --- P . P       . P ---
    # ---   .         .
    #       .   --- P . P ---
    #       .   ---   .
    #       .         .   ---
    #       .         .
    points_before, points_between, points_after = scheme
    is_finite_start = (points_before and (points_between or points_after))
    is_finite_end = ((points_before or points_between) and points_after)

    start_paddings = generate_point_paddings(head_paddings=is_finite_start,
                                             tail_paddings=is_finite_start)

    for start in start_paddings:
        end_paddings = generate_point_paddings(
            head_paddings=is_finite_end and points_between,
            tail_paddings=is_finite_end)

        for end in end_paddings:
            yield start, end


# Generates range sets layouts to test.
def generate_range_set_layouts():
    for scheme in generate_range_set_schemes():
        for padding in generate_range_paddings(scheme):
            yield scheme, padding


# Returns the array of range set points by given scheme and padding.
def get_range_set_points(layout):
    scheme, padding = layout
    points_before, points_between, points_after = scheme
    start_padding, end_padding = padding

    points = []
    pos = 0
    for i in range(points_before):
        points.append(pos)
        pos += 1

    pos += start_padding[0]
    pos += start_padding[1]

    for i in range(points_between):
        points.append(pos)
        pos += 1

    pos += end_padding[0]
    pos += end_padding[1]

    for i in range(points_after):
        points.append(pos)
        pos += 1
    return points


# Generates the pattern of a range set by its points.
def get_range_set_pattern(points):
    v = False
    pattern = [v]

    pos = 0
    for p in points:
        range_size = p - pos
        pattern.extend([v] * range_size)
        v = not v
        pos = p

    if points:
        pattern.append(v)

    return ''.join('x' if x else '-' for x in pattern)


# Returns range points by range set scheme and padding.
def get_range_points(layout):
    scheme, padding = layout
    points_before, points_between, points_after = scheme
    start_padding, end_padding = padding

    start = points_before + start_padding[0]
    end = start + start_padding[1] + points_between + end_padding[0]

    return start, end


# Returns a string with cursors indicating the position of range points.
def get_range_cursors(layout):
    cursors = ''
    for pos in sorted(set(get_range_points(layout))):
        cursors += ' ' * (pos - len(cursors)) + '^'
    return cursors


# Generates values to test for a given range point.
def generate_range_point_values(p, range_set_points, is_start_point):
    # For a point in the beginning of the range set we want to
    # try -INF and some small enough finite value.
    points = set()
    if p == 0:
        points.add(-INF)
        if range_set_points:
            points.add(range_set_points[0] - 1)
        else:
            points.add(0 if is_start_point else 1)

    # Similarly, for a point in the end of the range set we wany
    # to try +INF and some finite value that is large enough.
    if not range_set_points:
        end_of_range_set = 0
    else:
        end_of_range_set = range_set_points[-1] + 1

    if p == end_of_range_set:
        points.add(INF)
        if range_set_points:
            points.add(range_set_points[-1] + 1)
        else:
            points.add(0 if is_start_point else 1)

    if not points:
        points.add(p - 1)

    return points


# Generates all combinations of values for points of the range to test.
def generate_ranges(layout):
    start, end = get_range_points(layout)
    points = get_range_set_points(layout)
    for b in generate_range_point_values(start, points,
                                         is_start_point=True):
        for e in generate_range_point_values(end, points,
                                             is_start_point=False):
            if b == e:
                continue
            if b == INF or e == -INF:
                continue
            yield b, e


def main():
    # Generate test cases.
    tests = []
    for layout in generate_range_set_layouts():
        points = get_range_set_points(layout)
        for range in generate_ranges(layout):
            tests.append((points, range, layout))

    for points, range, layout in sorted(tests, key=lambda x: (len(x[0]), x)):
        print()
        points = get_range_set_points(layout)
        print('# %s' % get_range_set_pattern(points))
        print('# %s' % get_range_cursors(layout))
        print(' '.join([str(len(points))] + [str(x) for x in points]))
        print(' '.join([str(x) for x in range]))


if __name__ == '__main__':
    main()
