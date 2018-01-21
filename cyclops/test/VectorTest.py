import math

from ..util.MathUtil import *
from ..geometry.Vector import *


def test_create_2d_vector_instance_with_head_point_as_tuple():
    (x, y) = (1, 2)
    v = Vector((x,y))
    assert v.x == x
    assert v.y == y
    assert v.z == 0

def test_create_2d_vector_instance_with_head_and_tail_points_as_tuples():
    (x0, y0) = (1, 2)
    (x1, y1) = (5, -6)
    v = Vector((x1,y1), (x0,y0))
    assert v.x == x1 - x0
    assert v.y == y1 - y0
    assert v.z == 0

def test_create_2d_vector_instance_with_head_and_tail_points_as_vectors():
    (x0, y0) = (1, 2)
    (x1, y1) = (5, -6)
    v = Vector(Vector((x1,y1)), Vector((x0,y0)))
    assert v.x == x1 - x0
    assert v.y == y1 - y0
    assert v.z == 0

def test_create_3d_vector_instance_with_head_point_as_tuple():
    (x, y, z) = (1, 2, 3)
    v = Vector((x,y,z))
    assert v.x == x
    assert v.y == y
    assert v.z == z

def test_create_3d_vector_instance_with_head_and_tail_points_as_tuples():
    (x0, y0, z0) = (1, 2, 7)
    (x1, y1, z1) = (5, -6, -4)
    v = Vector((x1,y1,z1), (x0,y0,z0))
    assert v.x == x1 - x0
    assert v.y == y1 - y0
    assert v.z == z1 - z0

def test_create_3d_vector_instance_with_head_and_tail_points_as_vectors():
    (x0, y0, z0) = (1, 2, -3)
    (x1, y1, z1) = (5, -6, 9)
    v = Vector(Vector((x1,y1,z1)), Vector((x0,y0,z0)))
    assert v.x == x1 - x0
    assert v.y == y1 - y0
    assert v.z == z1 - z0

def test_access_2d_vector_coordinates():
    (x, y) = (9, 5)
    v = Vector((x,y))
    assert v[0] == v.x == v.coordinates[0] == x
    assert v[1] == v.y == v.coordinates[1] == y
    assert v[2] == v.z == v.coordinates[2] == 0

def test_access_3d_vector_coordinates():
    (x, y, z) = (9, 5, 8)
    v = Vector((x,y,z))
    assert v[0] == v.x == v.coordinates[0] == x
    assert v[1] == v.y == v.coordinates[1] == y
    assert v[2] == v.z == v.coordinates[2] == z

def test_1d_vector_has_length_1():
    v1 = Vector((5,))
    assert len(v1) == len(v1.coordinates) == 1
    v2 = Vector((5,0))
    assert len(v2) == len(v2.coordinates) == 1
    v3 = Vector((5,0,0))
    assert len(v3) == len(v3.coordinates) == 1

def test_2d_vector_has_length_2():
    v = Vector((5,3))
    assert len(v) == len(v.coordinates) == 2

def test_3d_vector_has_length_3():
    v = Vector((5,3,8))
    assert len(v) == len(v.coordinates) == 3


def test_vector_is_not_equal_to_object_with_different_type():
    assert Vector((5,5)) != (5,5)
    assert Vector((5,5)) != 5

def test_vectors_with_same_coordinates_are_equal():
    (x,y,z) = (3,2,10)

    assert Vector((x,y)) == Vector((x,y)) == Vector((x,y,0))
    assert Vector((x,y,z)) == Vector((x,y,z))
    assert Vector((-7,4,0)) == Vector((-7,4,0))
    assert not (Vector((-7,4,0)) != Vector((-7,4,0)))

def test_vectors_with_different_coordinates_are_different():
    assert Vector((5,3)) != Vector((3,5))
    assert Vector((5,3)) != Vector((5,3,9))

def test_hash_code_should_be_a_function_of_the_coordinates():
    assert hash(Vector((5,5))) != hash(Vector((5,5.1)))
    assert hash(Vector((7,8))) != hash(Vector((7,8,9)))
    assert hash(Vector((7,8,9))) == hash(Vector((7,8,9)))

def test_to_string():
    assert str(Vector((3,2,5))) == 'Vector' + str((3,2,5))
    assert str(Vector((3,2))) == 'Vector' + str((3,2))

def test_iterable():
    (x,y,z) = (3,5,7)
    sum = 0
    for i in Vector((x,y,z)):
        sum += i
    assert sum == x + y + z


def test_dot_product_between_2d_vectors():
    (v1,v2) = (3,4.23)
    v = Vector((v1,v2))
    (w1,w2) = (8.65,3.5)
    w = Vector((w1,w2))

    assert v.dot_product(w) == v1*w1 + v2*w2

def test_dot_product_between_3d_vectors():
    (v1,v2,v3) = (3,4.23,8)
    v = Vector((v1,v2,v3))
    (w1,w2,w3) = (8.65,3.5,13.9)
    w = Vector((w1,w2,w3))

    assert v.dot_product(w) == v1*w1 + v2*w2 + v3*w3

def test_dot_product_between_2d_and_3d_vectors():
    (v1,v2) = (3,4.23)
    v = Vector((v1,v2))

    (w1,w2,w3) = (8.65,3.5,13.9)
    w = Vector((w1,w2,w3))

    assert v.dot_product(w) == v1*w1 + v2*w2

def test_dot_product_between_vector_and_zero_is_zero():
    vector = Vector((5,5,7))
    zero = Vector((0,0))

    assert vector.angle_between(zero) == 0
    assert zero.angle_between(vector) == 0

def test_dot_product_between_two_vectors_90_degrees_away_is_zero():
    v1 = Vector((0,50))
    v2 = Vector((100,0))
    assert v1.dot_product(v2) == 0
    assert v2.dot_product(v1) == 0


def test_perpendicular_dot_product_between_2d_vectors():
    (v1,v2) = (3,4.23)
    v = Vector((v1,v2))
    (w1,w2) = (8.65,3.5)
    w = Vector((w1,w2))

    assert v.perpendicular_dot_product(w) == v.counterclockwise_rotation_by_90_degrees().dot_product(w)

def test_perpendicular_dot_product_between_3d_vectors_is_not_implemented():
    v = Vector((3,4.23,50))
    w = Vector((8.65,3.5,40))

    exception_thrown = False
    try:
        v.perpendicular_dot_product(w)
    except NotImplementedError:
        exception_thrown = True
    assert exception_thrown


def test_clockwise_cross_product_between_two_2d_vectors_90_degrees_away_has_negative_z():
    v1 = Vector((0,50))
    v2 = Vector((100,0))
    clockwise = v1.cross_product(v2)
    assert clockwise[0] == 0
    assert clockwise[1] == 0
    assert clockwise[2] == -clockwise.norm == - (v1.norm * v2.norm) < 0

def test_counterclockwise_cross_product_between_two_2d_vectors_90_degrees_away_has_positive_z():
    v1 = Vector((0,50))
    v2 = Vector((100,0))
    counterclockwise = v2.cross_product(v1)
    assert counterclockwise[0] == 0
    assert counterclockwise[1] == 0
    assert counterclockwise[2] == counterclockwise.norm == (v1.norm * v2.norm) > 0

def test_cross_product_between_canonical_basis():
    i = Vector((1,0,0))
    j = Vector((0,1,0))
    k = Vector((0,0,1))

    assert i.cross_product(j) == Vector((0,0,1))
    assert j.cross_product(i) == Vector((0,0,-1))

    assert k.cross_product(i) == Vector((0,1,0))
    assert i.cross_product(k) == Vector((0,-1,0))

    assert k.cross_product(j) == Vector((-1,0,0))
    assert j.cross_product(k) == Vector((1,0,0))

def test_cross_product_between_parallel_vectors_is_zero():
    (x,y,z) = (100,50,5)
    v1 = Vector((x,y,z))
    v2 = Vector((x*2,y*2,z*2))
    assert v1.cross_product(v2) == Vector((0,0,0))
    assert v2.cross_product(v1) == Vector((0,0,0))

def test_cross_product_between_vector_and_its_reflection_is_zero():
    v = Vector((100,50,5))
    reflection = v.reflection()
    assert v.cross_product(reflection) == Vector((0,0,0))
    assert reflection.cross_product(v) == Vector((0,0,0))


def test_norm_of_2d_vector():
    (v1,v2) = (3,4)
    v = Vector((v1,v2))
    assert v.norm == math.sqrt(v1*v1 + v2*v2)

def test_norm_of_3d_vector():
    (v1,v2,v3) = (3,4,5)
    v = Vector((v1,v2,v3))
    assert v.norm == math.sqrt(v1*v1 + v2*v2 + v3*v3)


def test_angle_between_vector_and_zero_is_zero():
    zero = Vector((0,0))
    vector = Vector((5,-31,3))

    assert zero.angle_between(vector) == 0
    assert vector.angle_between(zero) == 0

def test_angle_between_zero_and_zero_is_zero():
    zero = Vector((0,0))
    assert zero.angle_between(zero) == 0

def test_angle_between_equal_vectors_is_zero():
    error = 0.01
    v = Vector((-63,326,5))
    w = Vector(v.coordinates)

    assert MathUtil.equal_within_error(v.angle_between(w), 0, error)
    assert MathUtil.equal_within_error(w.angle_between(v), 0, error)

def test_angle_between_opposite_vectors_is_180_degrees():
    error = 0.0000001
    v = Vector((5, 5))
    w = Vector((-5, -5))

    assert v.dot_product(w) < 0

    expected_angle = math.pi
    assert MathUtil.equal_within_error(v.angle_between(w), expected_angle, error)
    assert MathUtil.equal_within_error(w.angle_between(v), expected_angle, error)

def test_angle_between_parallel_vectors_is_zero():
    error = 0.0000001
    v = Vector((7,14.6))
    w = Vector((3.5,7.3))

    assert v.dot_product(w) > 0

    expected_angle = 0
    assert MathUtil.equal_within_error(v.angle_between(w), expected_angle, error)
    assert MathUtil.equal_within_error(w.angle_between(v), expected_angle, error)

def test_angle_between_vectors_is_45_degrees():
    error = 0.00000000001
    v = Vector((6,0))
    w = Vector((3,3))

    assert v.dot_product(w) > 0

    expected_angle = math.pi/4
    assert MathUtil.equal_within_error(v.angle_between(w), expected_angle, error)
    assert MathUtil.equal_within_error(w.angle_between(v), expected_angle, error)

def test_angle_between_vectors_is_90_degrees():
    error = 0.00000000001
    v = Vector((0,5))
    w = Vector((14.293,0))

    assert MathUtil.equal_within_error(v.dot_product(w), 0, error)

    expected_angle = math.pi/2
    assert MathUtil.equal_within_error(v.angle_between(w), expected_angle, error)
    assert MathUtil.equal_within_error(w.angle_between(v), expected_angle, error)

def test_angle_between_vectors_is_less_than_90_degrees():
    v = Vector((4,5))
    w = Vector((1,2))

    assert v.dot_product(w) > 0

    maximum_angle = math.pi/2
    assert v.angle_between(w) < maximum_angle
    assert w.angle_between(v) < maximum_angle

def test_angle_between_vectors_is_less_than_90_degrees():
    v = Vector((4,5,9))
    w = Vector((1,2,9))

    assert v.dot_product(w) > 0

    maximum_angle = math.pi/2
    assert v.angle_between(w) < maximum_angle
    assert w.angle_between(v) < maximum_angle

def test_angle_between_vectors_is_more_than_90_degrees():
    v = Vector((-6,2))
    w = Vector((5,1))

    assert v.dot_product(w) < 0

    minimum_angle = (math.pi/2)
    assert v.angle_between(w) > minimum_angle
    assert w.angle_between(v) > minimum_angle

def test_angle_between_vectors_is_180_degrees():
    error = 0.0000001
    v = Vector((-7,-14.6))
    w = Vector((3.5,7.3))

    assert v.dot_product(w) < 0

    expected_angle = math.pi
    assert MathUtil.equal_within_error(v.angle_between(w), expected_angle, error)
    assert MathUtil.equal_within_error(w.angle_between(v), expected_angle, error)

def test_reflection():
    error = 0.0000001
    v = Vector((3,2,-3), (4,5,1))
    mirror = v.reflection()
    assert mirror.tail == v.head
    assert mirror.head == v.tail
    assert v.norm == mirror.norm
    assert MathUtil.equal_within_error(v.angle_between(mirror), math.pi, error)

def test_reflection_from_reflection_is_the_original_vector():
    v = Vector((436,-13,40), (-950,30,2.35))
    mirror = v.reflection()
    assert mirror.reflection() == v


def test_vector_is_clockwise_distance_from_anoter_vector():
    v1 = Vector((5,5))
    v2 = Vector((5,-5))
    assert v1.is_clockwise_distance_from(v2)
    assert not v2.is_clockwise_distance_from(v1)

def test_vector_is_counterclockwise_distance_from_anoter_vector():
    v1 = Vector((5,-5))
    v2 = Vector((5,5))
    assert v1.is_counterclockwise_distance_from(v2)
    assert not v2.is_counterclockwise_distance_from(v1)


def test_parallel_vectors_are_at_both_clockwise_and_couterclockwise_distance_from_each_other():
    a = 5
    v1 = Vector((a,a))
    v2 = Vector((2*a,2*a))
    assert v1.is_clockwise_distance_from(v2)
    assert v2.is_counterclockwise_distance_from(v1)

    a = 5
    v1 = Vector((a,a))
    v2 = Vector((-2*a,-2*a))
    assert v1.is_clockwise_distance_from(v2)
    assert v2.is_counterclockwise_distance_from(v1)

def test45_degree_clockwise_rotation_of_2d_vector():
    radians = math.radians(45)
    a = 5
    v = Vector((a,0))
    clockwise = v.clockwise_rotation_by(radians)
    assert v.angle_between(clockwise) == radians
    assert clockwise.is_counterclockwise_distance_from(v)
    assert clockwise.norm == v.norm == a

def test45_degree_counterclockwise_rotation_of_2d_vector():
    radians = math.radians(45)
    a = 5
    v = Vector((a,0))
    counterclockwise = v.counterclockwise_rotation_by(radians)
    assert v.angle_between(counterclockwise) == radians
    assert counterclockwise.is_clockwise_distance_from(v)
    assert counterclockwise.norm == v.norm == a

def test90_degree_clockwise_rotation_of_2d_vector():
    v = Vector((3,2), (-1,-50))
    clockwise = v.clockwise_rotation_by_90_degrees()
    assert clockwise.dot_product(v) == 0
    assert clockwise.angle_between(v) == math.pi/2
    assert clockwise.norm == v.norm
    assert clockwise == v.clockwise_rotation_by(math.pi/2)

def test90_degree_clockwise_rotation_is_clockwise_for_2d_vector():
    a = 4
    v = Vector((0, a))
    assert v.clockwise_rotation_by_90_degrees() == Vector((a,0))
    assert v.clockwise_rotation_by_90_degrees().clockwise_rotation_by_90_degrees() == Vector((0,-a))
    assert v.clockwise_rotation_by_90_degrees().clockwise_rotation_by_90_degrees().clockwise_rotation_by_90_degrees() == Vector((-a,0))
    assert v.clockwise_rotation_by_90_degrees().clockwise_rotation_by_90_degrees().clockwise_rotation_by_90_degrees().clockwise_rotation_by_90_degrees() == v

def test90_degree_clockwise_rotation_over_counterclockwise_rotation_is_the_original_2d_vector():
    v = Vector((312,460), (-93,517))
    counterclockwise = v.counterclockwise_rotation_by_90_degrees()
    assert counterclockwise.clockwise_rotation_by_90_degrees() == v

    v = Vector((312,460), (-93,517))
    counterclockwise = v.counterclockwise_rotation_by(math.pi/2)
    assert counterclockwise.clockwise_rotation_by(math.pi/2) == v


def test90_degree_counterclockwise_rotation_for_2d_vector():
    v = Vector((3,2), (-1,-50))
    counterclockwise = v.counterclockwise_rotation_by_90_degrees()
    assert counterclockwise.dot_product(v) == 0
    assert counterclockwise.angle_between(v) == math.pi/2
    assert counterclockwise.norm == v.norm
    assert counterclockwise == v.counterclockwise_rotation_by(math.pi/2)

def test90_degree_counterclockwise_rotation_is_counterclockwise_for_2d_vector():
    a = 4
    v = Vector((0, a))
    assert v.counterclockwise_rotation_by_90_degrees() == Vector((-a, 0))
    assert v.counterclockwise_rotation_by_90_degrees().counterclockwise_rotation_by_90_degrees() == Vector((0, -a))
    assert v.counterclockwise_rotation_by_90_degrees().counterclockwise_rotation_by_90_degrees().counterclockwise_rotation_by_90_degrees() == Vector((a, 0))
    assert v.counterclockwise_rotation_by_90_degrees().counterclockwise_rotation_by_90_degrees().counterclockwise_rotation_by_90_degrees().counterclockwise_rotation_by_90_degrees() == v

def test90_degree_counterclockwise_rotation_over_clockwise_rotation_is_the_original_2d_vector():
    v = Vector((312,460), (-93,517))
    clockwise = v.clockwise_rotation_by_90_degrees()
    assert clockwise.counterclockwise_rotation_by_90_degrees() == v

    v = Vector((312,460), (-93,517))
    clockwise = v.clockwise_rotation_by(math.pi/2)
    assert clockwise.counterclockwise_rotation_by(math.pi/2) == v

def test90_degree_clockwise_rotation_is_not_implemented_for_3d_vectors():
    v = Vector((5,7,9))
    exception_thrown = False
    try:
        v.clockwise_rotation_by_90_degrees()
    except NotImplementedError:
        exception_thrown = True
    assert exception_thrown

def test90_degree_counterclockwise_rotation_is_not_implemented_for_2d_vectors():
    v = Vector((5,7,9))
    exception_thrown = False
    try:
        v.counterclockwise_rotation_by_90_degrees()
    except NotImplementedError:
        exception_thrown = True
    assert exception_thrown

def test_clockwise_rotation_is_not_implemented_for_3d_vectors():
    v = Vector((5,7,9))
    exception_thrown = False
    try:
        v.clockwise_rotation_by(math.pi)
    except NotImplementedError:
        exception_thrown = True
    assert exception_thrown

def test_counterclockwise_rotation_is_not_implemented_for_2d_vectors():
    v = Vector((5,7,9))
    exception_thrown = False
    try:
        v.counterclockwise_rotation_by(math.pi)
    except NotImplementedError:
        exception_thrown = True
    assert exception_thrown

def test180_degree_clockwise_rotation_of_2d_vector():
    radians = math.pi
    a = 5
    v = Vector((a,0))
    clockwise = v.clockwise_rotation_by(radians)
    assert v.angle_between(clockwise) == radians
    assert clockwise.is_counterclockwise_distance_from(v)
    assert clockwise.norm == v.norm == a

def test180_degree_counterclockwise_rotation_of_2d_vector():
    radians = math.pi
    a = 5
    v = Vector((a,0))
    counterclockwise = v.counterclockwise_rotation_by(radians)
    assert v.angle_between(counterclockwise) == radians
    assert counterclockwise.is_clockwise_distance_from(v)
    assert counterclockwise.norm == v.norm == a

def test_multiplied_by_positive_scalar_with_zero_as_tail():
    head = (4, 32.3, 5.6, 0, 7)
    scalar = 5.3

    multiplied_vector = Vector(head).multiplied_by_scalar(scalar)

    for i in range(len(head)):
        assert multiplied_vector[i] == multiplied_vector.head[i] == scalar * head[i]

    assert multiplied_vector.tail == Point((0,))

def test_multiplied_by_positive_scalar_with_non_zero_as_tail():
    head = (4, 32.3, 5)
    tail = (5, -2, 3.5)
    scalar = 5

    vector = Vector(head, tail)
    multiplied_vector = vector.multiplied_by_scalar(scalar)

    for i in range(len(head)):
        assert multiplied_vector[i] == scalar * vector[i]

    assert multiplied_vector.tail == tail

def test_multiplied_by_negative_scalar_with_zero_as_tail():
    head = (4, 32.3, 5.6, 0, 7)
    scalar = -5.3

    vector = Vector(head)
    multiplied_vector = vector.multiplied_by_scalar(scalar)

    for i in range(len(head)):
        assert multiplied_vector[i] == multiplied_vector.head[i] == scalar * head[i]

    assert multiplied_vector.tail == Point((0,))
    assert MathUtil.equal_within_error(multiplied_vector.angle_between(vector), math.pi, 0.0000001)

def test_multiplied_by_positive_scalar_with_non_zero_as_tail():
    head = (4, 32.3, 5)
    tail = (5, -2, 3.5)
    scalar = 5

    vector = Vector(head, tail)
    multiplied_vector = vector.multiplied_by_scalar(scalar)

    for i in range(len(head)):
        assert multiplied_vector[i] == scalar * vector[i]

    assert multiplied_vector.tail == tail

def test_multiplied_by_negative_scalar_with_non_zero_as_tail():
    head = (4, 32.3, 5)
    tail = (5, -2, 3.5)
    scalar = -10.9

    vector = Vector(head, tail)
    multiplied_vector = vector.multiplied_by_scalar(scalar)

    for i in range(len(head)):
        assert multiplied_vector[i] == scalar * vector[i]

    assert multiplied_vector.tail == tail
    assert MathUtil.equal_within_error(multiplied_vector.angle_between(vector), math.pi, 0.0000001)

def test_multiplied_by_zero():
    head = (4, 32.3, 5)
    tail = (5, -2, 3.5)
    scalar = 0

    vector = Vector(head, tail)
    multiplied_vector = vector.multiplied_by_scalar(scalar)

    for i in range(len(head)):
        assert multiplied_vector[i] == scalar * vector[i]


    assert multiplied_vector.tail == tail
    assert multiplied_vector.head == multiplied_vector.tail
