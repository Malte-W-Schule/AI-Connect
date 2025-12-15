class AC3:

    def __init__(self, domain, constraints, houses):
        self.domain = domain
        self.houses = houses
        self.constraints = constraints
        self.queue = []
        self.all_house_combinations = []
        self.generate_all_combinations()
        #starting queue
        for entity_a in self.houses:
            for entity_b in self.houses:
                if entity_a != entity_b:
                    self.queue.append((entity_a, entity_b))

    def solve(self):

        while len(self.queue) > 0:

            hl, hr = self.queue.pop(0)  
            result = False

            for c in self.constraints:
                result = self.revise_domain(self.domain, c, hl, hr)
                if result:
                    for h in self.houses:
                        if h != hl:
                            self.queue.append((hl, hr))

            #print((hl, hr,result))

    def revise_domain(self,domains, constraint, entity_a_id, entity_b_id):
        """
        Adjusts the domain of Entity A by removing all values for which
        no supporting value exists in the domain of Entity B, conditional
        on the House Operator.

        :param domains: The CSP_DOMAINS structure.
        :param constraint: The 5-element constraint array.
        :param entity_a_id: ID of the entity being revised (e.g., House.H1).
        :param entity_b_id: ID of the supporting entity (e.g., House.H2).
        :return: True if the domain of Entity A was revised (reduced), otherwise False.
        """
        # 1. Extract Constraint Parts
        house_operator = constraint[0]

        kat_a = constraint[1]
        var_a = constraint[2] # Specific value A (e.g., Name.PETER)

        kat_b = constraint[3]
        var_b = constraint[4] # Specific value B (e.g., Color.RED)

        # 2. Domain Access
        domain_a = domains[entity_a_id][kat_a]
        domain_b = domains[entity_b_id][kat_b]

        revised = False
        new_domain_a = []

        # A. CHECK HOUSE POSITIONS
        # The constraint only applies if the House Operator (e.g., equality) is True
        if house_operator(entity_a_id.value, entity_b_id.value):

            # B. DOMAIN REDUCTION (Arc Consistency Check)

            # 3. Revision: Check every value in Domain A (v_a)
            for v_a in domain_a:
                has_support = False

                # Check for Support in Domain B (v_b)
                for v_b in domain_b:

                    # CONSISTENCY CHECK (Equivalence: PETER <-> RED)
                    is_v_a_var = (v_a == var_a)
                    is_v_b_var = (v_b == var_b)

                    # Check if the boolean states match (True==True or False==False)
                    # This ensures that if v_a is PETER, v_b must be RED, and vice versa.
                    if is_v_a_var == is_v_b_var:
                        has_support = True
                        break  # Support found

                # 4. Update Domain based on Support
                if has_support:
                    new_domain_a.append(v_a) # Keep value
                else:
                    # No support: Value must be removed
                    revised = True

            # 5. Replace Domain (only if the House Operator was True)
            if revised or len(new_domain_a) < len(domain_a):
                domains[entity_a_id][kat_a] = new_domain_a

            return revised

        else:
            # House Operator is False (e.g., H1 != H2)
            # Skip revision, return False (no change made)
            return False


    def print_domains(self,domains):
        """
        prints the domains structure.
        """
        print("\n--- CSP-Domain ---")

        for house_entity, categories in domains.items():

            print(f"\nEntität: {house_entity.name} (Position: {house_entity.value})")

            for category_class, domain_list in categories.items():
                domain_names = [member.name for member in domain_list]

                print(f"  ▪︎  {category_class.__name__}: {domain_names}")

        print("\n--- --- ---")

    def generate_all_combinations(self):
        """
        Generiert ALLE möglichen Kombinationen (Paare) von Werten aus der Domäne
        der Länge 2 (x, y) und speichert sie in self.all_house_combinations.
        """
        self.all_house_combinations.clear()

        # Wir erzwingen die Tiefe auf 2, da der Benutzer nur Paare (x, y) wünscht.
        TARGET_DEPTH = 2

        if not self.domain:
            # Nur leere Liste, falls keine Domäne vorhanden ist
            self.all_house_combinations.append([])
            return

        # Startet die Rekursion mit der festen Tiefe 2
        self._recursive_generate([], TARGET_DEPTH)

    def _recursive_generate(self, current_combination, remaining_depth):
        """
        Generiert rekursiv Kombinationen der Länge 2 aus self.domain.
        """
        if remaining_depth == 0:
            # Basisfall: Die Kombination (x, y) ist vollständig
            self.all_house_combinations.append(tuple(current_combination))
            return

        # Rekursiver Schritt
        for value in self.domain:
            current_combination.append(value)

            # Gehe zur nächsten Tiefe (Position)
            self._recursive_generate(current_combination, remaining_depth - 1)

            # Backtracking
            current_combination.pop()

    def queue_append_combinations_for_house(self, target_house_value):
        """
        Fügt alle Kombinationen (Paare) zur Queue hinzu, die den Zielwert enthalten.
        """
        for combination in self.all_house_combinations:
            if target_house_value in combination:
                self.queue.append(combination)