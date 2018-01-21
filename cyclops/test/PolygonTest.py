import math

from ..geometry.Polygon import *
from ..geometry.Vector import *
from ..util.MathUtil import *


def test_can_not_create_polygon_with_less_than_3_vertexes():
    exepction_thrown = False
    try:
        Polygon([(1, 2), (3, 4)])
    except BaseException:
        exepction_thrown = True
    assert exepction_thrown


def test_create_polygon_with_3_vertexes():
    v1 = (1, 2)
    v2 = (2, 3)
    v3 = (3, 4)
    polygon = Polygon((v1, v2, v3))
    assert polygon[0] == polygon.vertexes[0] == v1
    assert polygon[1] == polygon.vertexes[1] == v2
    assert polygon[2] == polygon.vertexes[2] == v3
    assert len(polygon) == 3


def test_create_polygon_with_5_vertexes():
    v1 = (1, 2)
    v2 = (2, 3)
    v3 = (3, 4)
    v4 = (5, 6)
    v5 = (7, 8)
    polygon = Polygon((v1, v2, v3, v4, v5))
    assert polygon[0] == polygon.vertexes[0] == v1
    assert polygon[1] == polygon.vertexes[1] == v2
    assert polygon[2] == polygon.vertexes[2] == v3
    assert polygon[3] == polygon.vertexes[3] == v4
    assert polygon[4] == polygon.vertexes[4] == v5
    assert len(polygon) == 5


def test_get_sides():
    v1 = (1, 2)
    v2 = (2, 3)
    v3 = (3, 4)
    v4 = (5, 6)
    polygon = Polygon((v1, v2, v3, v4))
    assert polygon.sides == ((v1, v2), (v2, v3), (v3, v4), (v4, v1))


def test_get_contour():
    v1 = (1, 2)
    v2 = (2, 3)
    v3 = (3, 4)
    v4 = (5, 6)
    v5 = (7, 8)
    polygon = Polygon((v1, v2, v3, v4, v5))
    assert polygon.contour == (Vector(v2, v1), Vector(v3, v2), Vector(v4, v3), Vector(v5, v4), Vector(v1, v5))


def test_sum_of_square_interior_angles_is_360_degrees():
    v1 = (0, 0)
    v2 = (0, 1)
    v3 = (1, 1)
    v4 = (1, 0)
    quadrilateral = Polygon((v1, v2, v3, v4))
    interior_angles = quadrilateral.interior_angles
    assert len(interior_angles) == 4
    MathUtil.equal_within_error(sum(interior_angles), 2 * math.pi, 0.00000000000001)


def test_sum_of_quadrilateral_interior_angles_is_360_degrees():
    v1 = (0, 0)
    v2 = (7, 0)
    v3 = (16, 16)
    v4 = (14, 3)
    quadrilateral = Polygon((v1, v2, v3, v4))
    interior_angles = quadrilateral.interior_angles
    assert len(interior_angles) == 4
    MathUtil.equal_within_error(sum(interior_angles), 2 * math.pi, 0.00000000000001)


def test_square_interior_angles_are_90_degrees():
    v1 = (0, 0)
    v2 = (0, 1)
    v3 = (1, 1)
    v4 = (1, 0)
    square = Polygon((v1, v2, v3, v4))
    interior_angles = square.interior_angles
    for angle in interior_angles:
        assert angle == math.pi / 2


def test_sum_of_triangle_interior_angles_is_180_degrees():
    v1 = (0, 0)
    v2 = (5, 6)
    v3 = (3, 3)
    triangle = Polygon((v1, v2, v3))
    interior_angles = triangle.interior_angles
    assert len(interior_angles) == 3
    assert MathUtil.equal_within_error(sum(interior_angles), math.pi, 0.00000000000001)


def test_rectangle_triangle_angles_are_45_and_90_degrees():
    v1 = (0, 0)
    v2 = (15, 15)
    v3 = (15, 0)
    triangle = Polygon((v1, v2, v3))
    interior_angles = triangle.interior_angles
    assert MathUtil.equal_within_error(interior_angles[0], math.pi / 4, 0.00000000000001)
    assert MathUtil.equal_within_error(interior_angles[1], math.pi / 4, 0.00000000000001)
    assert MathUtil.equal_within_error(interior_angles[2], math.pi / 2, 0.00000000000001)
    assert len(interior_angles) == 3


def test_triangle_is_convex():
    v1 = (0, 0)
    v2 = (15, 15)
    v3 = (15, 0)
    triangle = Polygon((v1, v2, v3))
    assert triangle.is_convex


def test_digon_is_not_convex():
    v1 = (0, 0)
    v2 = (5, 0)
    v3 = (7, 0)
    digon = Polygon((v1, v2, v3))
    assert not digon.is_convex


def test_square_is_convex():
    v1 = (0, 0)
    v2 = (0, 15)
    v3 = (15, 15)
    v4 = (15, 0)
    rectangle = Polygon((v1, v2, v3, v4))
    assert rectangle.is_convex


def test_rectangle_is_convex():
    v1 = (0, 0)
    v2 = (0, 15)
    v3 = (10, 15)
    v4 = (10, 0)
    rectangle = Polygon((v1, v2, v3, v4))
    assert rectangle.is_convex


def test_trapezoid_is_convex():
    v1 = (0, 0)
    v2 = (7, 0)
    v3 = (5, 4)
    v4 = (2, 4)
    quadrilateral = Polygon((v1, v2, v3, v4))
    assert quadrilateral.is_convex


def test_lozenge_is_convex():
    v1 = (0, 0)
    v2 = (5, 0)
    v3 = (8, 4)
    v4 = (3, 4)
    rectangle = Polygon((v1, v2, v3, v4))
    assert rectangle.is_convex


def test_convex_quadrilateral_is_convex():
    v1 = (0, 0)
    v2 = (7, 0)
    v3 = (7, 7)
    v4 = (2, 5)
    quadrilateral = Polygon((v1, v2, v3, v4))
    assert quadrilateral.is_convex


def test_butterfly_quadrilateral_is_not_convex():
    v1 = (0, 0)
    v2 = (3, 6)
    v3 = (0, 6)
    v4 = (4, 2)
    quadrilateral = Polygon((v1, v2, v3, v4))
    assert not quadrilateral.is_convex


def test_quadrilateral_with_collinear_vertexes_is_not_convex():
    v1 = (0, 0)
    v2 = (5, 0)
    v3 = (8, 0)
    v4 = (-5, 6)
    polygon = Polygon((v1, v2, v3, v4))
    assert not polygon.is_convex


def test_convex_pentagon_is_convex():
    v1 = (0, 0)
    v2 = (4, 0)
    v3 = (4, 3)
    v4 = (2, 5)
    v5 = (0, 3)
    pentagon = Polygon((v1, v2, v3, v4, v5))
    assert pentagon.is_convex


def test_concave_pentagon_is_not_convex():
    v1 = (0, 0)
    v2 = (4, 0)
    v3 = (4, 3)
    v4 = (2, 1)
    v5 = (0, 3)
    pentagon = Polygon((v1, v2, v3, v4, v5))
    assert not pentagon.is_convex


def test_convex_octagon_is_convex():
    v1 = (0, 0)
    v2 = (2, 0)
    v3 = (3, 2)
    v4 = (3, 4)
    v5 = (2, 6)
    v6 = (0, 6)
    v7 = (-1, 4)
    v8 = (-1, 2)
    octagon = Polygon((v1, v2, v3, v4, v5, v6, v7, v8))
    assert octagon.is_convex


def test_concave_octagon_is_not_convex():
    v1 = (0, 0)
    v2 = (2, 0)
    v3 = (3, 2)
    v4 = (3, 4)
    v5 = (2, 2)
    v6 = (0, 2)
    v7 = (-1, 4)
    v8 = (-1, 2)
    octagon = Polygon((v1, v2, v3, v4, v5, v6, v7, v8))
    assert not octagon.is_convex


def test_polygons_are_different_if_vertexes_are_different_or_have_different_order():
    assert Polygon([(1, 2), (3, 4), (5, 6)]) != Polygon([(1, 2), (99, 100), (5, 6)])
    assert Polygon([(1, 2), (3, 4), (5, 6)]) != Polygon([(1, 2), (5, 6), (3, 4)])
    assert Polygon([(1, 2), (3, 4), (5, 6)]) != Polygon([(1, 2), (3, 4), (5, 6), (7, 8)])


def test_polygons_are_equal_if_vertexes_are_equal_in_the_same_order():
    assert Polygon([(1, 2), (3, 4), (5, 6)]) == Polygon([(1, 2), (3, 4), (5, 6)]) == Polygon(((1, 2), (3, 4), (5, 6)))


def test_hash_code_is_a_function_of_vertexes():
    assert hash(Polygon([(1, 2), (3, 4), (5, 6)])) != hash(Polygon([(1, 2), (99, 101), (5, 6)]))
    assert hash(Polygon([(1, 2), (3, 4), (5, 6)])) != hash(Polygon([(1, 2), (5, 6), (3, 4)]))
    assert hash(Polygon([(1, 2), (3, 4), (5, 6)])) != hash(Polygon([(1, 2), (3, 4), (5, 6), (7, 8)]))

    assert hash(Polygon([(1, 2), (3, 4), (5, 6)])) == hash(Polygon([(1, 2), (3, 4), (5, 6)])) == hash(Polygon(((1, 2), (3, 4), (5, 6))))
