temperatures = []
with open('lab_05.txt', 'r') as f:
    for line in f:
        temperatures.append(float(line.strip()))

max_temp = max(temperatures)
min_temp = min(temperatures)
average = sum(temperatures) / len(temperatures)
temperatures.sort()
median_index = len(temperatures)//2
median = temperatures[median_index]
print(median, max_temp, min_temp, average)
