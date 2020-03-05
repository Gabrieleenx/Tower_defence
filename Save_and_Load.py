
def search(word):
    with open('Save_and_Load.txt', 'r') as f:
        for num, line in enumerate(f, 1):
            if word in line:
                return num


def read_name(line):
    with open('Save_and_Load.txt', 'r') as f:
        name_line = f.readlines()
        name = name_line[line-1].split("name =", 1)
        return name[1]


def read_data(line):
    with open('Save_and_Load.txt', 'r') as f:
        name_line = f.readlines()
        type_ = name_line[line-1].split("data_type = ", 1)
        rotate_ = name_line[line].split("data_rotation = ", 1)

        return type_[1], rotate_[1]


def write_name(line, name):
    with open('Save_and_Load.txt', 'r') as f:
        name_line = f.readlines()
        name_line[line - 1] = 'name = ' + name + '\n'
    with open('Save_and_Load.txt', 'w') as f:
        f.writelines(name_line)

def write_data(line, type, rotation):
    with open('Save_and_Load.txt', 'r') as f:
        data_line = f.readlines()
        data_line[line +1] = 'data_type = ' + type + '\n'
        data_line[line+2] = 'data_rotation = ' + rotation + '\n'
    with open('Save_and_Load.txt', 'w') as f:
        f.writelines(data_line)

