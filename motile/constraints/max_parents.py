from __future__ import annotations

from typing import TYPE_CHECKING

import ilpy
from ilpy.expressions import Constant

from ..variables import EdgeSelected
from .constraint import Constraint

if TYPE_CHECKING:
    from motile.solver import Solver


class MaxParents(Constraint):
    r"""Ensures that every selected node has no more than ``max_parents``
    selected edges to the previous frame.

    Adds the following linear constraint for each node :math:`v`:

    .. math::

      \sum_{e \in \\text{in_edges}(v)} x_e \leq \\text{max_parents}

    Args:

        max_parents (int):
            The maximum number of parents allowed.
    """

    def __init__(self, max_parents: int) -> None:
        self.max_parents = max_parents

    def instantiate(self, solver: Solver) -> list[ilpy.LinearConstraint]:
        edge_indicators = solver.get_variables(EdgeSelected)

        constraints = []
        for node in solver.graph.nodes:
            # all incoming edges
            s = sum(
                (edge_indicators.expr(e) for e in solver.graph.prev_edges[node]),
                start=Constant(0),
            )
            constraints.append((s <= self.max_parents).constraint())

        return constraints
