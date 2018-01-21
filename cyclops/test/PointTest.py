from ..geometry.Point import *


def test_point_coordinates_should_be_dimension_agnostic():
    p1 = Point((1,2,3))
    assert p1[0] == p1.x == 1
    assert p1[1] == p1.y == 2
    assert p1[2] == p1.z == 3
    assert p1[3] == p1[4] == p1[5] == p1[6] == 0 # ...

    p2 = Point((1,2))
    assert p2[0] == p2.x == 1
    assert p2[1] == p2.y == 2
    assert p2[2] == p2.z == 0
    assert p2[3] == p2[4] == p2[5] == p2[6] == 0 # ...

    p3 = Point((1,))
    assert p3[0] == p3.x == 1
    assert p3[1] == p3.y == 0
    assert p3[2] == p3.z == 0
    assert p3[3] == p3[4] == p3[5] == p3[6] == 0 # ...

    p4 = Point()
    assert p4[0] == p4.x == 0
    assert p4[1] == p4.y == 0
    assert p4[2] == p4.z == 0
    assert p4[3] == p4[4] == p4[5] == p4[6] == 0 # ...

def test_empty_point_is_equal_to_zero():
    assert Point() == Point(()) == Point([]) == Point((0,)) == Point((0,0)) == Point((0,0,0))

def test_equal_points_with_same_dimensions_are_equal():
    assert Point((1,)) == Point((1,))
    assert Point((1,2.5)) == Point((1,2.5))
    assert Point((1,2,3.99)) == Point((1,2,3.99))
    assert Point((1,2,3.99,7)) == Point((1,2,3.99,7))

def test_equivalent_points_with_different_dimensions_are_equal():
    assert Point((1,)) == Point((1,0)) == Point((1,0,0)) == Point((1,0,0,0))
    assert Point((1,2)) == Point((1,2,0)) == Point((1,2,0,0)) == Point((1,2,0,0))
    assert Point((1,2,3)) == Point((1,2,3,0))

def test_slightly_different_points_with_same_dimensions_are_not_equal():
    assert Point((1,2)) != Point((1,2.3))
    assert Point((0,2)) != Point((1,2))
    assert Point((1,2,3)) != Point((1,2,4))

def test_very_different_points_with_same_dimensions_are_not_equal():
    assert Point((1,2)) != Point((66,50))
    assert Point((90.99,23)) != Point((1,2))
    assert Point((5,6,7)) != Point((1,2,4))

def test_slightly_different_points_with_different_dimensions_are_not_equal():
    assert Point((1,)) != Point((1,2))
    assert Point((1,2)) != Point((0,2,0))
    assert Point((1,2,4)) != Point((1,2,3,0))
    assert Point((1,2)) != Point((1,2,0,3))

def test_very_different_points_with_different_dimensions_are_not_equal():
    assert Point((1,)) != Point((1,38))
    assert Point((1,2)) != Point((0,673,0))
    assert Point((66,666,6666)) != Point((66,2,3,0))
    assert Point((7,8)) != Point((1,2,0,3))

def test_equality_with_duck_typing():
    assert Point((1,)) == (1,)
    assert Point((1,2,3)) == [1,2,3]
    assert Point((1,2)) == (1,2,0)

def test_hash_code_should_be_a_function_of_coordinates():
    assert hash(Point((1,4))) == hash(Point((1,4)))
    assert hash(Point((88.3,99.5))) == hash(Point((88.3,99.5)))
    assert hash(Point((88.3,99.5))) != hash(Point((88.3,99.6)))
    assert hash(Point((88.3,99.5))) != hash(Point((88.4,99.5)))

def test_hash_code_should_be_dimension_agnostic():
    assert hash(Point((1,4))) == hash(Point((1,4,0))) == hash(Point((1,4,0,0)))
    assert hash(Point((88.3,99.5))) == hash(Point((88.3,99.5,0))) == hash(Point((88.3,99.5,0,0)))

def test_length_of_zero_point_is_zero():
    assert len(Point()) == len(Point((0,))) == len(Point((0,0))) == len(Point((0,0,0))) == len(Point((0,0,0,0))) == 0

def test_length_of_one_dimension_point_is_one():
    assert len(Point((2,))) == len(Point((2,0))) == len(Point((2,0,0))) == 1

def test_length_of_two_dimension_point_is_two():
    assert len(Point((2,3))) == len(Point((2,3,0))) == len(Point((2,3,0,0))) == 2

def test_length_of_three_dimension_point_is_three():
    assert len(Point((2,3,4))) == len(Point((2,3,4,0))) == len(Point((2,3,4,0))) == 3

def test_point_as_2d_tuple():
    t = Point((5,0)).as_2d_tuple()
    assert t == (5,0)
    assert not isinstance(t, Point)
    assert isinstance(t, tuple)

def test_point_inside_point_as_2d_tuple():
    t = Point(Point((5,4,0))).as_2d_tuple()
    assert t == (5,4)
    assert not isinstance(t, Point)
    assert isinstance(t, tuple)

def test_point_as_3d_tuple():
    t = Point((5,4,0)).as_3d_tuple()
    assert t == (5,4,0)
    assert not isinstance(t, Point)
    assert isinstance(t, tuple)

def test_point_inside_point_as_3d_tuple():
    t = Point(Point((5,4,0))).as_3d_tuple()
    assert t == (5,4,0)
    assert not isinstance(t, Point)
    assert isinstance(t, tuple)
