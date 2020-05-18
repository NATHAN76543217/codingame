my_map = []
for i in range(10):
    mon_test = []
    for y in range(5):
        mon_test.append(y)
    my_map.append(mon_test)

def print_map(my_map):
	for row in my_map:
		for case in row:
			print(case, end=' ')
		print('')

# print_map(my_map)