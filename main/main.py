import os
import pathlib


irrelevant_logs_interval = 4.0

files_input = os.path.abspath("../files_input")
files_output = os.path.abspath("../files_output")

input_dirs = [pathlib.Path(files_input).joinpath(pathlib.Path(x)) for x in os.listdir(files_input)]
output_files = [pathlib.Path(files_output).joinpath(pathlib.Path(x)) for x in os.listdir(files_input)]

for thisdir in input_dirs:
    interesting_files = ["access.log", "store.log"]
    # interesting_files = ["access.log"]

    good_files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(thisdir):
        for file in f:
            if any(x in file for x in interesting_files):
                f_with_path = os.path.join(r, file)
                print(f_with_path)
                good_files.append(f_with_path)

    constructed = []

    opened_files = list(map(lambda x: open(x, "r"), good_files))
    current_lines = [x.readline().strip('\x00') for x in opened_files]

    last_index = -1
    last_timestamp = -1
    while any(x != "" for x in current_lines):
        to_append = min(filter(lambda x: x != "", current_lines))
        to_append_index = current_lines.index(to_append)
        to_append_timestamp = float(to_append.split(" ")[0])
        if last_timestamp != -1 and abs(float(to_append.split(" ")[0]) - last_timestamp) > irrelevant_logs_interval:
            constructed.append("\n")
        last_timestamp = to_append_timestamp
        if last_index != to_append_index:
            constructed.append(str(pathlib.Path(good_files[to_append_index]).relative_to(pathlib.Path(files_input))) + "\n")
        constructed.append(to_append)
        current_lines[to_append_index] = opened_files[to_append_index].readline().strip('\x00')

    result = "".join(constructed)
    output_file = str(pathlib.Path(files_output).joinpath(pathlib.Path(thisdir).parts[-1])) + ".txt"
    with open(output_file , "a") as f:
        f.write(result)

x = 0