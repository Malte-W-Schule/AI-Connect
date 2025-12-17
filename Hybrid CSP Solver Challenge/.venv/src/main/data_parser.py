import pandas as pd
import os
import re
from enum import Enum

class DataParser:

    def __init__(self, path = os.path.join(
            "..", "..",
            "dataset",
            "grid_mode",
            "test-00000-of-00001.parquet")):


        self.houses = []
        self.enums = []
        self.constraints = []
        self.categories = {}
        self.categories_norm = []
        self.csp_domains = {}
        self.path = path
        #setup
        self.setup()

    equal = lambda x, y: x == y
    nequal = lambda x, y: x != y
    left = lambda x, y: x < y
    right = lambda x, y: x > y
    dleft = lambda x, y: x-y == -1
    dright = lambda x, y: x-y == 1
    nextto = lambda x, y: abs(x-y) == 1
    betw = lambda x, y: abs(x-y) == 2

    def setup(self):

        k = 0
        df = pd.read_parquet(self.path)
        puzzle = df["puzzle"].iloc[k]
        #print(puzzle)
        text = puzzle.split("##")[0].split(":", 1)[1].split("\n")
        text = [s for s in text if s.strip()]  # remove empty strings
        count = 1
        list_values = {}
        for t in range(len(text)):
            values2 = self.get_enums(text[t], count)
            list_values[self.enums[t]] = values2
            count += 1
        # print("Enums:", enums[0]["Peter"])
        # print("Categories:", categories)
        size = df["size"].iloc[k]
        houses_amount = size[0]
        self.get_houses(houses_amount)
        self.csp_domains = {h: list_values for h in self.houses}
        # print("Domains", csp_domains)
        clues = puzzle.split('Clues:\n')[1]  # split the puzzle string to only get the clues
        clues = clues.split('\n')  # split clues at each newline
        self.get_constraints(clues)
        #
        #print()
        #counter = 1
        #
        #for c in self.constraints:
        #    print(f"C:{counter}", c)
        #    print()
        #    counter += 1

    def get_houses(self,h):
        #global houses
        for i in range(1, int(h)+1):
            self.houses.append(f"H{i}")
        
        if _houses is None:
            _houses = Enum("Houses", houses)

        for i in range(len(houses)):
            self.houses[i] = self._houses[self.houses[i]]

        #print("Houses:", houses)
            
        return self.houses

    def get_enums(self,text, count):
        #global enums
        #global categories
        #global categories_norm

        #serach for Strings between two `
        values = re.findall(r"`(.*?)`", text)

        name = text.split(":")[0]
        name_list = name.split()
        name_list = [s for s in name_list if s != "" and s != "-"]

        category = " ".join(name_list)

        self.categories[count] = category

        self.category_norm = "_".join(name_list) #Category names normalized for Enums
        self.categories_norm.append(self.category_norm)

        for v in range(len(values)):
            values[v] = values[v].lower()

        self.enums.append(Enum(self.category_norm, values))

        enums_list = []
        for v in values:
            enums_list.append(self.enums[len(self.enums)-1][v])

        return enums_list

    def get_constraints(self,clues):
        #global csp_domains
        h = ["first house", "second house", "third house", "fourth house", "fifth house", "sixth house"]

        for c in clues:
            #if line in clues is empty
            if c == '':
                continue
            val = []
            key = next(iter(self.csp_domains))
            for i in self.csp_domains[key]:
                for j in range(len(self.csp_domains[key][i])):
                    skip = False
                    if re.search(self.csp_domains[key][i][j].name, c, re.IGNORECASE):
                        # if the name of a value is partly existing in another for example 'tall' in 'super tall'
                        for v in range(1, len(val), 2):
                            if val[v-1] == i:
                                if re.search(val[v].name, self.csp_domains[key][i][j].name, re.IGNORECASE):
                                    print("delete:", val[v])
                                    val[v] = self.csp_domains[key][i][j]
                                    skip = True
                                    break
                                if re.search(self.csp_domains[key][i][j].name, val[v].name, re.IGNORECASE):
                                    print("skip")
                                    skip = True
                                    break
                        if not skip:
                            val.append(i)
                            val.append(self.csp_domains[key][i][j])

            #if order wrong, switch
            #print(val)
            if len(val) >= 4:
                if c.lower().find(val[1].name.lower()) > c.lower().find(val[3].name.lower()):
                    val[0], val[2], val[1], val[3] = val[2], val[0], val[3], val[1]
                val[1] = val[0][val[1].name]
                val[3] = val[2][val[3].name]

            #converting string to enum
            if len(val) == 2:
                val[1] = val[0][val[1].name]

            # check if a value is directly set in one of the Houses
            for i in range(len(h)):
                if re.search(h[i], c):
                    val.append(i+1)
                    break

            if len(val) < 3 or len(val) > 4:
                continue

            #check for directional operations in clues
            if re.search(r"\bleft\b", c):
                if re.search(r"\bdirectly\b", c):
                    val.insert(0, self.dleft)
                else:
                    val.insert(0, self.left)
                self.constraints.append(val)
                continue
            if re.search(r"\bright\b", c):
                if re.search(r"\bdirectly\b", c):
                    val.insert(0, self.dright)
                else:
                    val.insert(0, self.right)
                self.constraints.append(val)
                continue
            if re.search(r"\bnext to each other\b", c):
                #if subtracting two Houses from another equals +/-1 would mean their next to each other for example House 4 - House 5 = -1 or House 4 - House 3 = 1
                val.insert(0, self.nextto)
                self.constraints.append(val)
                continue
            if re.search(r"\bbetween\b", c):
                # if subtracting two Houses from another equals +/-2 would mean theirs a House between them for example 4 - 2 = 2 or 2 - 4 = -2
                val.insert(0, self.betw)
                self.constraints.append(val)
                continue

            # if no directional operation was found, set equal
            if re.search(r"\bnot\b", c):
                val.insert(0, self.nequal)
            else:
                val.insert(0, self.equal)

            #how val should look like: [<operation>, <category1>, <value1>, <category2>, <value2>]
            self.constraints.append(val)


