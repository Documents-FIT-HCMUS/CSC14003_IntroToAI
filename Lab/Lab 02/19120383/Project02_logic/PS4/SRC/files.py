import os
from solver import *


def files_count(path):
    count = 0
    files = list(os.scandir(path))

    for file in files:
        if os.path.isfile(file):
            count += 1

    return count


def read_input_file_content(input_file):
    fi = open(input_file, 'r')
    alpha = fi.readline().strip()
    data = fi.readline()
    count = int(data)
    knowledge_base = []

    for i in range(0, count):
        data = fi.readline()
        knowledge_base.append(data.strip())

    fi.close()
    return knowledge_base, alpha


def write_to_output_file(input_file, output_file):
    knowledge_base, alpha = read_input_file_content(input_file)
    result, records = pl_resolution(knowledge_base, alpha)

    fo = open(output_file, 'w')

    for record in records:
        fo.write(f"{len(record)}\n")
        for r in record:
            fo.write(f"{r}\n")

    fo.write("YES" if result else "NO")

    fo.close()
