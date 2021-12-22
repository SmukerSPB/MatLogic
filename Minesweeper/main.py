#!/usr/bin/python3

import itertools

digits = "0123456789"


def get_from_known_or_empty(known, r, c):
    # I'm lazy to do overflow checks
    try:
        return known[r][c]
    except IndexError:
        return ""


def valid_coord(coord, HEIGHT, WIDTH):
    r = coord[0]
    c = coord[1]
    return not (r < 0 or c < 0 or r >= HEIGHT or c >= WIDTH)


def have_neighbour_digit(known, r, c, HEIGHT, WIDTH):
    # returns True if neighbour is digit, False otherwise
    t = []
    t.append(get_from_known_or_empty(known, r - 1, c - 1) in digits)
    t.append(get_from_known_or_empty(known, r - 1, c) in digits)
    t.append(get_from_known_or_empty(known, r - 1, c + 1) in digits)
    t.append(get_from_known_or_empty(known, r, c - 1) in digits)
    t.append(get_from_known_or_empty(known, r, c + 1) in digits)
    t.append(get_from_known_or_empty(known, r + 1, c - 1) in digits)
    t.append(get_from_known_or_empty(known, r + 1, c) in digits)
    t.append(get_from_known_or_empty(known, r + 1, c + 1) in digits)
    return any(t)


# check all equations under an assignment
# busiest function
def check_all_eqs(eqs, assignment):
    for eq in eqs:
        result = 0
        for term in eq[0]:
            if term in assignment:
                result = result + assignment[term]
        if eq[1] != result:
            # at least one eq is UNSAT
            return "UNSAT"
    # all eqs are SAT
    return "SAT"


def chk_bomb(known, bomb, eqs):
    WIDTH = len(known[0])
    HEIGHT = len(known)

    to_be_assigned = []
    for r in range(HEIGHT):
        for c in range(WIDTH):
            if known[r][c] == "?" and have_neighbour_digit(known, r, c, HEIGHT, WIDTH) and bomb != (r, c):
                to_be_assigned.append((r, c))
    to_be_assigned_t = len(to_be_assigned)
    # bruteforce. try all 0/1 for all coords in to_be_assigned[]:
    # we do full bruteforce to be sure that no equation can be SAT under any assignment
    for assignment in itertools.product([0, 1], repeat=to_be_assigned_t):
        t = {}
        for i in zip(to_be_assigned, assignment):
            t[i[0]] = i[1]
        # add bomb to assignment:
        t[bomb] = 1
        if check_all_eqs(eqs, t) == "SAT":
            # bomb can be at $bomb$
            return None

    # all assignments checked at this point
    # UNSAT
    # no bomb can be at bomb
    return bomb


def find_safe_cells(known):
    WIDTH = len(known[0])
    HEIGHT = len(known)

    eqs = []
    # make a system of equations:
    for r in range(HEIGHT):
        for c in range(WIDTH):
            digit = known[r][c]
            if digit in digits:
                eq = []
                if valid_coord((r - 1, c - 1), HEIGHT, WIDTH):
                    eq.append((r - 1, c - 1))
                if valid_coord((r - 1, c), HEIGHT, WIDTH):
                    eq.append((r - 1, c))
                if valid_coord((r - 1, c + 1), HEIGHT, WIDTH):
                    eq.append((r - 1, c + 1))

                if valid_coord((r, c - 1), HEIGHT, WIDTH):
                    eq.append((r, c - 1))
                if valid_coord((r, c + 1), HEIGHT, WIDTH):
                    eq.append((r, c + 1))

                if valid_coord((r + 1, c - 1), HEIGHT, WIDTH):
                    eq.append((r + 1, c - 1))
                if valid_coord((r + 1, c), HEIGHT, WIDTH):
                    eq.append((r + 1, c))
                if valid_coord((r + 1, c + 1), HEIGHT, WIDTH):
                    eq.append((r + 1, c + 1))

                eqs.append((eq, int(digit)))

    # enumerate all hidden cells bordering to digit-in-cells:
    rt = []
    for r in range(HEIGHT):
        for c in range(WIDTH):
            if known[r][c] == "?" and have_neighbour_digit(known, r, c, HEIGHT, WIDTH):
                print("checking", r, c)
                rt.append(chk_bomb(known, (r, c), eqs))
    return list(filter(None, rt))


# known cells
# safe cells (as found by SAT or SMT solver)
Minefield = ["01110001?",
             "01?100011",
             "011100000",
             "000000000",
             "111110011",
             "?11?1001?",
             "???331011",
             "?????2110",
             "???????10"]


def main():
    print("Minefield", Minefield)
    safe_cells = find_safe_cells(Minefield)
    print("safe_cells", safe_cells)


main()
