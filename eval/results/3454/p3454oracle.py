from typing import List


class SegmentTree:
    def __init__(self, xs: List[int]):
        self.xs = xs  # sorted x coordinates
        self.n = len(xs) - 1
        self.count = [0] * (4 * self.n)
        self.covered = [0] * (4 * self.n)

    # be careful when you are reading over, we use right + 1 instead of right.
    # make sure you understand why.
    def update(self, qleft, qright, qval, left, right, pos):
        if self.xs[right + 1] <= qleft or self.xs[left] >= qright:  # no overlap
            return
        if qleft <= self.xs[left] and self.xs[right + 1] <= qright:  # full overlap
            self.count[pos] += qval
        else:  # partial overlap
            mid = (left + right) // 2
            self.update(qleft, qright, qval, left, mid, pos * 2 + 1)
            self.update(qleft, qright, qval, mid + 1, right, pos * 2 + 2)

        if self.count[pos] > 0:
            self.covered[pos] = self.xs[right + 1] - self.xs[left]
        else:
            if left == right:
                self.covered[pos] = 0
            else:
                self.covered[pos] = (
                    self.covered[pos * 2 + 1] + self.covered[pos * 2 + 2]
                )

    def query(self):
        return self.covered[0]


class Solution:
    def separateSquares(self, squares: List[List[int]]) -> float:
        events = []
        xs_set = set()
        for x, y, l in squares:
            events.append((y, 1, x, x + l))
            events.append((y + l, -1, x, x + l))
            xs_set.update([x, x + l])
        xs = sorted(xs_set)

        seg_tree = SegmentTree(xs)
        events.sort()

        # first sweep: compute total union area.
        total_area = 0.0
        prev_y = events[0][0]
        for y, start, xl, xr in events:
            total_area += seg_tree.query() * (y - prev_y)
            seg_tree.update(xl, xr, start, 0, seg_tree.n - 1, 0)
            prev_y = y

        # second sweep: find the minimal y where the area below equals half_area.
        seg_tree = SegmentTree(xs)  # reinitialize segment tree
        curr_area = 0.0
        prev_y = events[0][0]
        for y, start, xl, xr in events:
            combined_width = seg_tree.query()
            if curr_area + combined_width * (y - prev_y) >= total_area / 2.0:
                # curr_area + (combined_width * optimal_height_diff) = total_area / 2
                return prev_y + (total_area / 2.0 - curr_area) / combined_width
            curr_area += combined_width * (y - prev_y)
            seg_tree.update(xl, xr, start, 0, seg_tree.n - 1, 0)
            prev_y = y
