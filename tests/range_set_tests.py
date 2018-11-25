# -*- coding: utf-8 -*-


import cherries
import itertools
import os
import unittest


TEST_BIT_STRING_RANGE = -5, 25


PLUS_INF = float('+inf')
MINUS_INF = float('-inf')


class bitset(object):
    def __init__(self, initial_value=0):
        self.begin, self.end = TEST_BIT_STRING_RANGE
        self.bits = [initial_value] * (self.end - self.begin)

    def normalize_range(self, r):
        b, e = r
        assert b <= e, (b, e)

        if b == MINUS_INF:
            b = self.begin

        if e == PLUS_INF:
            e = self.end

        return b, e

    def set(self, r, value):
        b, e = self.normalize_range(r)

        for i in range(b, e):
            if self.begin <= i < self.end:
                self.bits[i - self.begin] = int(value)

    def invert(self, r):
        b, e = self.normalize_range(r)

        for i in range(b, e):
            if self.begin <= i < self.end:
                k = i - self.begin
                self.bits[k] = not self.bits[k]

    def get_bit_string(self):
        return ''.join('x' if x else '-' for x in self.bits)


class combined_set(object):
    def __init__(self, log, points, initial_value=False):
        self.log_lines = log[:]

        self.rs = cherries.RangeSet(initial_value)
        self.bs = bitset(initial_value)

        self.set_points(points)
        self.match()

    def log(self, line):
        self.log_lines.append(line)

    def report(self):
        for line in self.log_lines:
            print(line)

    def match(self):
        # Validate range set points.
        for i, p in enumerate(self.rs._points):
            assert i == 0 or self.rs._points[i - 1] < p, self.rs._points

        # Match bit strings.
        rs_bits = self.rs.get_bit_string(*TEST_BIT_STRING_RANGE,
                                         chars=['-', 'x'])
        bs_bits = self.bs.get_bit_string()
        self.log('RangeSet: %s' % repr(rs_bits))
        self.log('  bitset: %s' % repr(bs_bits))

        if rs_bits != bs_bits:
            self.report()
            assert 0

        # Convert bit string back to range set and match the
        # lists of points.
        bits_points = self.bit_string_to_points(bs_bits)
        if bits_points != self.rs._points:
            self.report()
            assert 0, (bits_points, self.rs._points)

    def bit_string_to_points(self, bits):
        bits = [x == 'x' for x in bits]
        groups = [list(g) for k, g in itertools.groupby(bits)]

        points = []
        pos = TEST_BIT_STRING_RANGE[0]
        for i, g in enumerate(groups):
            if i > 0:
                points.append(pos)
            pos += len(g)

        return points

    def set(self, r, value=True):
        self.log('set: %s %s' % (repr(r), value))

        try:
            self.rs.set(*r, value=value)
            self.bs.set(r, value)
        except BaseException:
            self.report()
            raise

        self.match()
        self.log('')

    def invert(self, r):
        self.log('invert: %s' % repr(r))

        try:
            self.rs.invert_range(*r)
            self.bs.invert(r)
        except BaseException:
            self.report()
            raise

        self.match()
        self.log('')

    def set_points(self, points):
        self.rs._points = points[:]
        bits = self.rs.get_bit_string(*TEST_BIT_STRING_RANGE)
        self.bs.bits = [x == '1' for x in bits]


def get_test_cases():
    tests_dir = os.path.join(os.path.dirname(__file__), 'range_set_tests')

    for filename in ['generated.tests', 'special_cases.tests']:
        with open(os.path.join(tests_dir, filename)) as f:
            log = []
            for line in f:
                log.append(line.rstrip())
                if line == '\n' or line.startswith('#'):
                    continue

                points = [int(x) for x in line.split()]
                assert points[0] == len(points) - 1
                points = points[1:]

                line = None
                for line in f:
                    break

                assert line is not None
                log.append(line.rstrip())

                range = [int(x) for x in line.split()]

                infs = {-99: MINUS_INF, 99: PLUS_INF}
                range = tuple(infs.get(x, x) for x in range)

                yield log, points, range

                log = []


def test_setting_range(log, points, range, value):
    s = combined_set(log, points)
    s.set(range, value)


def test_inverting_range(log, points, range):
    s = combined_set(log, points)
    s.invert(range)


def test(log, points, range):
    test_setting_range(log, points, range, value=True)
    test_setting_range(log, points, range, value=False)

    test_inverting_range(log, points, range)


class RangeSetTests(unittest.TestCase):
    def runTest(self):
        for log, points, range in get_test_cases():
            test(log, points, range)


if __name__ == '__main__':
    unittest.main()
