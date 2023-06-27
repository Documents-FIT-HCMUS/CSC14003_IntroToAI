from files import *

input_folder, output_folder = 'input', 'output'
count = files_count(input_folder)
input_files_names, output_files_names = [], []

for i in range(count):
    input_files_names.append(f"{input_folder}/input{i}.txt")
    output_files_names.append(f"{output_folder}/output{i}.txt")

for i in range(count):
    write_to_output_file(input_files_names[i], output_files_names[i])
