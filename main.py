
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--input")
parser.add_argument("--corpus")
args = parser.parse_args()


def chunk_list_to_string(chunk_list, start_index):
    chunk_list_in_order = chunk_list[start_index:]
    chunk_list_in_order.extend(chunk_list[:start_index])
    return "".join(chunk_list_in_order)


MAX_CHUNK_LENGTH = 4
results = dict()
chunk_length = 0
start_index = 0
chunk_list = [''] * MAX_CHUNK_LENGTH
with open(args.input) as file:
    for line in file:
        for c in line:  # \n is space!
            if c.isspace():
                chunk_length = 0
                start_index = 0
            else:
                if chunk_length == 4:
                    chunk_list[start_index] = c
                    start_index = (start_index + 1) % MAX_CHUNK_LENGTH
                    chunk_string = chunk_list_to_string(chunk_list, start_index)
                    if chunk_string in results:
                        results[chunk_string] += 1
                    else:
                        results[chunk_string] = 1
                else:
                    chunk_list[(start_index + chunk_length) % MAX_CHUNK_LENGTH] = c
                    chunk_length += 1
                    if chunk_length == 4:
                        chunk_string = chunk_list_to_string(chunk_list, start_index)
                        if chunk_string in results:
                            results[chunk_string] += 1
                        else:
                            results[chunk_string] = 1
keys = list(results.keys())
for key in keys:
    if results[key] < 2:
        del results[key]
print(results)
