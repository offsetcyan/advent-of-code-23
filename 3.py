# cells is a sparse, flat (would've been 2D) matrix of NumberRef,
# which is just saying "this index had this number", and a NumberRef
# is a "seen" and the number value.
NumberRef = dict[str, int | bool]
numbers: NumberRef = dict()

matrix_numbers: dict[int, NumberRef] = dict()
matrix_protogears: dict[int, bool | int] = dict()  # int if actually gear
matrix_symbols: dict[int, bool] = dict()


def computation_step(char: str, number: int, idx: int):
    if char.isdecimal():
        number = number * 10 + int(char)
        return (number, idx + 1)

    if number:
        length = len(str(number))
        cells = range(idx - length, idx)  # cells containing the current number

        ref = {"seen": False, "value": number}
        for cell in cells:
            matrix_numbers[cell] = ref

    # reset the number.
    number = 0

    if char == "*":
        matrix_protogears[idx] = False

    if char != ".":
        # char is symbolic
        matrix_symbols[idx] = True

    return (number, idx + 1)


def adjacency(value: int, line_length: int) -> list[int]:
    middle = [value - line_length, value, value + line_length]
    left = []
    right = []

    if 0 != value % line_length:
        # we are NOT at the left edge so -1
        left = [value - line_length - 1, value - 1, value + line_length - 1]

    if 0 != (value + 1) % line_length:
        # we are NOT at the right edge so +1
        right = [value - line_length + 1, value + 1, value + line_length + 1]

    return left + middle + right


with open("3.input.txt") as fp:
    line_length = 0
    number = 0
    idx = 0

    for line in fp:
        for char in line:
            if char == "\n":
                # this is a stupid hack because i like to pretend there's risk.
                # imagine if the line was 18237912837 characters long.
                # don't len(line). we don't increment idx bc newlines don't exist.
                line_length = line_length or idx
                continue

            number, idx = computation_step(char, number, idx)

    # calculate gears.
    for idx in matrix_protogears:
        refcount = 0
        gear_ratio = 1

        for jdx in adjacency(idx, line_length):
            if ref := matrix_numbers.get(jdx):
                if ref["seen"]:
                    continue
                ref["seen"] = True
                gear_ratio *= ref["value"]
                refcount += 1

        if refcount == 2:
            matrix_protogears[idx] = gear_ratio
        refcount = 0
        gear_ratio = 0

    gear_ratio = sum(ratio for ratio in matrix_protogears.values())
    print("(part 2) - sum(gear ratios): ", gear_ratio)

    # calculate collisions. collision is a 1 unit grid around a symbol.
    for idx in matrix_symbols | matrix_protogears:
        for jdx in adjacency(idx, line_length):
            if ref := matrix_numbers.get(jdx):
                ref["seen"] = True

    total = 0
    for key, ref in matrix_numbers.items():
        if ref["seen"]:
            total += ref["value"]
            ref["seen"] = False
    print("(part 1) - sum(parts): ", total)
