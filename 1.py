import re

digits = "padding|one|two|three|four|five|six|seven|eight|nine"
digitals = digits.split("|")
def str_to_digit(string):
    return str(digitals.index(string))

exp = re.compile(f"((\d|{digits}).*)?(\d|{digits}).*")
with open("1.input.txt") as fp:
    matches = (exp.search(line) for line in fp)
    templates = (match.expand("\\2\\3\\3") for match in matches)
    subs = (re.sub(digits, lambda m: str_to_digit(m.group(0)), item) for item in templates)
    res = sum(int(sub[:2]) for sub in subs)
    print(res)
