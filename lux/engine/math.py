from pyglet.math import Vec2


def get_intersection(o1: Vec2, d1: Vec2, o2: Vec2, d2: Vec2) -> Vec2 | None:
    # If the two directions are parallel then just return None as they won't intersect
    dot = d1.dot(d2)
    if 1 <= dot or dot <= -1:
        return None

    # If the second vector has an x of 0 then we can simplify the entire equation down (t2 no longer matters)
    if d2.x == 0.0:
        t1 = (o2.x - o1.x) / d1.x
    else:
        ta = (o1.y - o2.y) - (o1.x - o2.x) * (d2.y / d2.x)
        tb = d1.x * (d2.y / d2.x) - d1.y

        # protecting against precision errors not catching that two lines are parallel.
        if tb == 0.0:
            return None

        t1 = ta / tb

    return o1 + d1 * t1


def get_segment_intersection(s1: Vec2, e1: Vec2, s2: Vec2, e2: Vec2, d1: Vec2 | None = None, d2: Vec2 | None = None):
    d1 = d1 or (e1 - s1).normalize()
    d2 = d2 or (e2 - s2).normalize()

    dot = d1.dot(d2)
    if 1.0 <= dot or dot <= -1.0:
        return None

    if d2.x == 0.0:
        t1 = (s2.x - s1.x) / d1.x
        t2 = ((s1.y - s2.y) + d1.y * t1) / d2.y
    else:
        ta = (s1.y - s2.y) - (s1.x - s2.x) * (d2.y / d2.x)
        tb = d1.x * (d2.y / d2.x) - d1.y

        # Precision errors kill me plz.
        if tb == 0.0:
            return None

        t1 = ta / tb
        t2 = ((s1.x - s2.x) + t1 * d1.x) / d2.x

    # t1 and t2 must be greater than 0.0 for the two segments to intersect
    if (t1 < 0.0) or (t2 < 0.0):
        return None

    v1 = e1 - s1
    v2 = e2 - s2

    # if t1 and t2 are greater than start to end of either segment then they aren't intersecting.
    if (t1**2 > v1.dot(v1)) or (t2**2 > v2.dot(v2)):
        return None

    return s1 + d1 * t1
