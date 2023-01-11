lines = []

with open("payload", "r") as f:
    for line in f:
        lines.append(line.strip())

if "Str = Str" not in lines[0]:
    with open("payload", "w") as f:
        n = 50
        for i in range(0, len(lines[0]), n):
            f.write("Str = Str + " + '"' + lines[0][i:i+n] + '"\n')
