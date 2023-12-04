from collections import defaultdict

with open("4.input.txt") as fp:
    total = 0
    repeats = defaultdict(int)
    for idx, line in enumerate(fp):
        _, game = line.strip().split(":")
        winners, ours = game.split("|")
        winners, ours = winners.split(" "), ours.split(" ")
        wins = len([win for win in filter(None, ours) if win in winners])

        for i in range(repeats[idx] + 1):
            for j in range(1, wins + 1):
                repeats[idx + j] += 1
    print(sum(repeats.values()) + len(repeats))