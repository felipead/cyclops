import unittest
from unittest import TestCase

from ..graph.Digraph import *
from ..domain.Solution import *


class SolutionTest(TestCase):

    """Test initialization"""
    def setUp(self):

        self.digraph = Digraph()
        self.digraph.putEdge('a', 'b', 5)
        self.digraph.putEdge('a', 'e', 4)
        self.digraph.putEdge('b', 'a', 6)
        self.digraph.putEdge('b', 'c', 2)
        self.digraph.putEdge('b', 'd', 4)
        self.digraph.putEdge('c', 'b', 3)
        self.digraph.putEdge('c', 'd', 1)
        self.digraph.putEdge('c', 'e', 7)
        self.digraph.putEdge('d', 'b', 8)
        self.digraph.putEdge('e', 'b', 5)
        self.digraph.putEdge('e', 'd', 7)

        self.solution = Solution(self.digraph)


    def testComputeRouteDistance(self):
        assert self.solution.computeRouteDistance(['a', 'b']) == 5
        assert self.solution.computeRouteDistance(['b', 'c']) == 2
        assert self.solution.computeRouteDistance(['c', 'd']) == 1

        assert self.solution.computeRouteDistance(['a', 'b', 'c']) == (5 + 2)
        assert self.solution.computeRouteDistance(['a', 'b', 'c', 'd']) == (5 + 2 + 1)
        assert self.solution.computeRouteDistance(['a', 'b', 'a', 'e', 'b', 'd']) == (5 + 6 + 4 + 5 + 4)

        assert self.solution.computeRouteDistance(['a']) == None
        assert self.solution.computeRouteDistance([]) == None


    def testComputeRouteHops(self):
        assert self.solution.computeRouteHops(['a', 'b']) == 1
        assert self.solution.computeRouteHops(['b', 'c']) == 1
        assert self.solution.computeRouteHops(['c', 'd']) == 1

        assert self.solution.computeRouteHops(['a', 'b', 'c']) == 1 + 1
        assert self.solution.computeRouteHops(['a', 'b', 'c', 'd']) == (1 + 1 + 1)
        assert self.solution.computeRouteHops(['a', 'b', 'a', 'e', 'b', 'd']) == (1 + 1 + 1 + 1 + 1)

        assert self.solution.computeRouteHops(['a']) == None
        assert self.solution.computeRouteHops([]) == None


    def testComputeRoutes(self):

        # Compute routes with 3 or less hops
        routes = self.solution.computeRoutes('a', 'c', (lambda v, hops, dist: hops <= 3))
        assert ['a', 'b', 'c'] in routes
        assert ['a', 'e', 'b', 'c'] in routes
        assert len(routes) == 2

        # Compute routes with 4 or less hops
        routes = self.solution.computeRoutes('a', 'c', (lambda v, hops, dist: hops <= 4))
        assert ['a', 'b', 'c'] in routes
        assert ['a', 'b', 'c', 'b', 'c'] in routes
        assert ['a', 'b', 'a', 'b', 'c'] in routes
        assert ['a', 'b', 'd', 'b', 'c'] in routes
        assert ['a', 'e', 'd', 'b', 'c'] in routes
        assert ['a', 'e', 'b', 'c'] in routes
        assert len(routes) == 6

        # Compute routes with distance less than 17
        routes = self.solution.computeRoutes('a', 'c', (lambda v, hops, dist: dist < 16))
        assert ['a', 'b', 'c'] in routes
        assert self.solution.computeRouteDistance(['a', 'b', 'c']) == 7
        assert ['a', 'b', 'c', 'b', 'c'] in routes
        assert self.solution.computeRouteDistance(['a', 'b', 'c', 'b', 'c']) == 12
        assert ['a', 'e', 'b', 'c'] in routes
        assert self.solution.computeRouteDistance(['a', 'e', 'b', 'c']) == 11
        assert len(routes) == 3


    def testComputeShortestRoute(self):
        route = self.solution.computeShortestRoute('a', 'c')
        assert ['a', 'b', 'c'] == route

        route = self.solution.computeShortestRoute('e', 'e')
        assert ['e', 'b', 'c', 'e'] == route



if __name__ == "__main__":
    unittest.main()
