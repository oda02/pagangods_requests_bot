new_lines = ''
for x in range(1,2000):
    new_lines += 'kukakur{}@monkos.ru ***REMOVED***.\n'.format(x)

with open('./accs.txt', 'w') as F:
    F.writelines(new_lines)