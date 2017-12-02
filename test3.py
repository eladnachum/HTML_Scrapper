from collections import defaultdict
inputt = "1 1000\n2 1000\n3 3000"
scores = defaultdict(list)
first_line = True
for line in inputt:
    if first_line:
        lines_num = int(line)
        first_line = False
    else:
        item = line.split()
        scores[item[0]].append(item[1])
for k, v in scores:
    avg_scores[k] = mean(v)
print avg_scores

for k, v in scores:
    avg_scores[k] = mean(v)
print avg_scores