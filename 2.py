import re
from math import prod


limits = {
    "red": 12,
    "green": 13,
    "blue": 14,
}

exp_gameid = re.compile("Game (\d+)")  # type: ignore
exp_hands = re.compile("(\d+) (red|blue|green)")  # type: ignore


def game_id(text):
    if res := exp_gameid.search(text):
        return int(res.group(1))
    raise ValueError("No game ID!")


def valid_hands(hands):
    for count, colour in hands:
        if limits[colour] < int(count):
            return False
    return True


def power_of_hands(hands):
    maxes = dict()
    for count, colour in hands:
        maxes[colour] = max(int(count), maxes.get(colour, 0))
    return prod(maxes.values())


with open("2.input.txt") as fp:
    total = 0
    powers = 0
    for line in fp:
        game, hands = line.split(":")

        g_id = game_id(game)
        hands = exp_hands.findall(hands)

        powers += power_of_hands(hands)
        if valid_hands(hands):
            total += g_id

    print(total)
    print(powers)
