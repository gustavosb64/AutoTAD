filename = str(input())

new_filename = filename+".h"
filename += ".c"

new_file = open(new_filename, "w")
brackets_counter = 0
with open(filename, "r") as file:
    content = file.readlines()

    for line in content:
        if '{' in line:
            if brackets_counter == 0:
                line = line.replace('{', ';')
                new_file.write(line)
            brackets_counter += 1
        if '}' in line:
            brackets_counter -= 1

new_file.close()
