from collections import deque
from typing import Any, Dict, List, Tuple, Optional

# Import here you guys AC3 (placeholder)
from Ac3 import AC3


House = Any
Category = Any
Value = Any

Domains = Dict[House, Dict[Category, List[Value]]]
Constraint = List[Any]  # [house_operator, kat_a, var_a, kat_b, var_b]


def _house_pos(h: House) -> int:
    # Supports both Enum-like houses (with .value) and raw ints.
    return getattr(h, "value", h)


class BacktrackingSolver:
    """
    - AC-3 preprocessing (optional, uses you guys AC3 implementation)
    - Backtracking search with MRV
    - Forward checking via incremental AC-3 after each assignment
    - All-different pruning per category across houses
    """

    def __init__(self, domains: Domains, constraints: List[Constraint], houses: List[House]):
        self.domains = domains
        self.constraints = constraints
        self.houses = houses
        self.steps = 0  # initialize counter

        # Cache categories (keys in domains[any_house])
        any_house = next(iter(domains))
        self.categories = list(domains[any_house].keys())

        # Stats (optional, useful for grading/debugging)
        self.nodes = 0
        self.backtracks = 0

    # ---------- Public API ----------

    def solve(self, use_ac3_preprocess: bool = True) -> Optional[Domains]:
        """
        Returns solved domains (all singleton lists) or None if no solution.
        """
        if use_ac3_preprocess:
            AC3(self.domains, self.constraints, self.houses).solve()

        if self._has_empty_domain(self.domains):
            return None

        ok = self._backtrack()
        return self.domains if ok else None

    # ---------- Core Backtracking ----------

    def _backtrack(self) -> bool:
        self.steps += 1
        if self._is_complete(self.domains):
            return True

        var = self._select_unassigned_var_mrv(self.domains)
        if var is None:
            return True  # nothing left

        house, cat = var
        values = list(self.domains[house][cat])  # copy

        # (Optional) LCV wasn't required as everything else is already enough (MRV and forward checking does enough pruning)
        for v in values:
            self.nodes += 1

            trail: List[Tuple[House, Category, Value]] = []

            if self._assign(house, cat, v, self.domains, trail):
                # Forward checking:
                # 1) all-different pruning in the same category
                if self._apply_all_different(house, cat, v, self.domains, trail):
                    # 2) incremental AC-3 using their constraint semantics
                    if self._incremental_ac3(self.domains, trail):
                        if not self._has_empty_domain(self.domains):
                            if self._backtrack():
                                return True

            # undo
            self._undo(trail, self.domains)
            self.backtracks += 1

        return False

    # ---------- Completion / Failure Checks ----------

    def _is_complete(self, domains: Domains) -> bool:
        for h in self.houses:
            for cat in self.categories:
                if len(domains[h][cat]) != 1:
                    return False
        return True

    def _has_empty_domain(self, domains: Domains) -> bool:
        for h in self.houses:
            for cat in self.categories:
                if len(domains[h][cat]) == 0:
                    return True
        return False

    # ---------- MRV Variable Selection ----------

    def _select_unassigned_var_mrv(self, domains: Domains) -> Optional[Tuple[House, Category]]:
        best = None
        best_size = 10**9

        for h in self.houses:
            for cat in self.categories:
                d = domains[h][cat]
                if 1 < len(d) < best_size:
                    best_size = len(d)
                    best = (h, cat)

        return best

    # ---------- Assignment + Trail ----------

    def _assign(self, house: House, cat: Category, value: Value, domains: Domains,
                trail: List[Tuple[House, Category, Value]]) -> bool:
        """
        Force (house, cat) = value by removing all other values.
        """
        current = domains[house][cat]
        if value not in current:
            return False

        # remove all other values
        for other in list(current):
            if other != value:
                self._remove_value(house, cat, other, domains, trail)

        return True

    def _remove_value(self, house: House, cat: Category, value: Value, domains: Domains,
                      trail: List[Tuple[House, Category, Value]]) -> None:
        d = domains[house][cat]
        if value in d:
            d.remove(value)
            trail.append((house, cat, value))

    def _undo(self, trail: List[Tuple[House, Category, Value]], domains: Domains) -> None:
        # Reverse removals
        for house, cat, value in reversed(trail):
            domains[house][cat].append(value)

    # ---------- All-different Propagation ----------

    def _apply_all_different(self, assigned_house: House, cat: Category, value: Value,
                             domains: Domains, trail: List[Tuple[House, Category, Value]]) -> bool:
        """
        If (assigned_house, cat) = value, then remove value from (other_house, cat).
        """
        for h in self.houses:
            if h == assigned_house:
                continue
            self._remove_value(h, cat, value, domains, trail)
            if len(domains[h][cat]) == 0:
                return False
        return True

    # ---------- Incremental AC-3 (Forward Checking) ----------

    def _incremental_ac3(self, domains: Domains, trail: List[Tuple[House, Category, Value]]) -> bool:
        """
        Run AC-3 style propagation using *their exact revise semantics*:
        constraints are 5-item arrays:
        [house_operator, kat_a, var_a, kat_b, var_b]
        and house_operator checks positions like in their AC3.revise_domain.
        """
        q = deque()
        for ha in self.houses:
            for hb in self.houses:
                if ha != hb:
                    q.append((ha, hb))

        while q:
            ha, hb = q.popleft()

            revised_any = False
            for c in self.constraints:
                revised = self._revise_with_trail(domains, c, ha, hb, trail)
                if revised:
                    revised_any = True
                    if len(domains[ha][c[1]]) == 0:  # kat_a domain empty
                        return False

            if revised_any:
                for hk in self.houses:
                    if hk != ha:
                        q.append((hk, ha))

        return True

    def _revise_with_trail(self, domains: Domains, constraint: Constraint,
                           entity_a: House, entity_b: House,
                           trail: List[Tuple[House, Category, Value]]) -> bool:
        """
        Trail-based version of their AC3.revise_domain logic.
        """
        house_operator = constraint[0]
        kat_a = constraint[1]
        var_a = constraint[2]
        kat_b = constraint[3]
        var_b = constraint[4]

        if not house_operator(_house_pos(entity_a), _house_pos(entity_b)):
            return False

        domain_a = list(domains[entity_a][kat_a])
        domain_b = list(domains[entity_b][kat_b])

        revised = False

        for v_a in domain_a:
            has_support = False
            for v_b in domain_b:
                is_v_a_var = (v_a == var_a)
                is_v_b_var = (v_b == var_b)

                # Their equivalence support check:
                if is_v_a_var == is_v_b_var:
                    has_support = True
                    break

            if not has_support:
                self._remove_value(entity_a, kat_a, v_a, domains, trail)
                revised = True

        return revised