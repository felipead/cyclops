# -*- coding: utf-8 -*-

'''
Represents a dimension agnostic point in the Euclidean space.

Points are read-only objects.
'''
class Point(tuple):

    def __new__(cls, coordinates=(0,)):
        return super().__new__(cls, coordinates)

    @property
    def x(self):
        return self[0] if len(self) > 0 else 0

    @property
    def y(self):
        return self[1] if len(self) > 1 else 0

    @property
    def z(self):
        return self[2] if len(self) > 2 else 0

    '''
    Dimension agnostic equality check. For instance:
        Point(1,2) == Point(1,2,0) == Point(1,2,0,0)
    but:
        Point(1,2) != Point(1,2,3) != Point(1,2,3,5)
    .
    '''
    def __eq__(self, other):
        try:
            if len(self) >= len(other):
                largest_dimension_point = self
                smallest_dimension_point = other
            else:
                largest_dimension_point = other
                smallest_dimension_point = self

            for i in range(len(smallest_dimension_point)):
                if smallest_dimension_point[i] != largest_dimension_point[i]:
                    return False

            for i in range(len(largest_dimension_point) - len(smallest_dimension_point)):
                if largest_dimension_point[len(smallest_dimension_point) + i] != 0:
                    return False

            return True
        except TypeError:
            return False

    def as_2d_tuple(self):
        return tuple((self[0], self[1]))

    def as_3d_tuple(self):
        return tuple((self[0], self[1], self[2]))

    def __hash__(self):
        hash_code = 0
        for x in self:
            if x != 0:
                hash_code ^= 5167 * hash(x)
        return 7907 * hash_code

    def __getitem__(self, index):
        return super().__getitem__(index) if index < len(self) else 0

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return repr(self)

    def __len__(self):
        original_length = super().__len__()

        length = original_length
        zero_in_a_row = True
        for i in reversed(range(original_length)):
            x = super().__getitem__(i)
            if x == 0 and zero_in_a_row:
                length -= 1
            if x != 0:
                zero_in_a_row = False

        return length
