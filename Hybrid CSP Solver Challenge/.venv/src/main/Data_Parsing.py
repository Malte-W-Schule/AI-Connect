import pandas as pd
import re

houses = []
values = []
constraints = []

def get_houses(h):
    global houses
    for i in range(1, int(h)+1):
        houses.append(i)
    print("Houses:", houses)

def get_values(text):
    global values
    #serach for Strings between two `
    values = re.findall(r"`(.*?)`", text)
    print("Values:", values)

def get_constraints(clues):
    global constraints
    h = ["first house", "second house", "third house", "fourth house", "fifth house", "sixth house"]

    for c in clues:
        #if line in clues is empty
        if c == '':
            continue

        val = []
        #search for values in clues
        for i in range(len(values)):
            skip = False
            if re.search(values[i], c, re.IGNORECASE):
                # if the name of a value is partly existing in another for example 'tall' in 'super tall'
                for v in val:
                    if re.search(v, values[i], re.IGNORECASE):
                        val.remove(v)
                        break
                    if re.search(values[i], v, re.IGNORECASE):
                        skip = True
                        break
                if not skip:
                    val.append(values[i])

        #check order
        if len(val) == 2:
            #if order wrong, switch
            if c.lower().find(val[0]) > c.lower().find(val[1]):
                val[0], val[1] = val[1], val[0]

        #check for directional operations in clues
        if re.search(r"\bleft\b", c):
            if re.search(r"\bdirectly\b", c):
                val.append(+1)
            else:
                val.append("<")
            constraints.append(val)
            continue
        if re.search(r"\bright\b", c):
            if re.search(r"\bdirectly\b", c):
                val.append(-1)
            else:
                val.append(">")
            constraints.append(val)
            continue
        if re.search(r"\bnext to each other\b", c):
            # if subtracting two Houses from another equals +/-1 would mean their next to each other for example House 4 - House 5 = -1 or House 4 - House 3 = 1
            val.append("|1|")
            constraints.append(val)
            continue
        if re.search(r"\bbetween\b", c):
            # if subtracting two Houses from another equals +/-2 would mean theirs a House between them for example 4 - 2 = 2 or 2 - 4 = -2
            val.append("|2|")
            constraints.append(val)
            continue
        # check if a value is directly set in one of the Houses
        for i in range(len(h)):
            if re.search(h[i], c):
                val.append(i+1)
                break

        # if no directional operation was found, set equal
        if re.search(r"\bnot\b", c):
            val.append("!=")
        else:
            val.append("=")

        #how val should look like: [<value1>, <value2>, <operation>] or [<value>, <operation>, <House number>]
        constraints.append(val)

def main():
    df = pd.read_parquet('test-00000-of-00001.parquet')

    puzzle = df["puzzle"].iloc[0]
    print(puzzle)

    size = df["size"].iloc[0]
    houses_amount = size[0]

    get_houses(houses_amount)

    get_values(puzzle)

    clues = puzzle.split('Clues:\n')[1] #split the puzzle string to only get the clues
    clues = clues.split('\n') #split clues at each newline

    get_constraints(clues)
    print("Constraints:", constraints)

if __name__ == '__main__':
    main()