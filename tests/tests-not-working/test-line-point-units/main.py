from funcs import point as p
from funcs import line as l

if __name__ == '__main__':
    point = p.Point(1, 1)
    point.transpose(3, -1)
    print(f'({point})')
    line1 = l.Line(p.Point(1, 2), p.Point(3, 2))
    line2 = l.Line(p.Point(-1, -2), p.Point(-3, -2))
    line3 = line1 + line2
    print(line3)