import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--input")
parser.add_argument("--corpus")
args = parser.parse_args()


def chunk_list_to_string(chunk_list, start_index):
    chunk_list_in_order = chunk_list[start_index:]
    chunk_list_in_order.extend(chunk_list[:start_index])
    return "".join(chunk_list_in_order)


def analyze_file(filename):
    MAX_CHUNK_LENGTH = 4
    results = dict()
    chunk_length = 0
    start_index = 0
    chunk_list = [''] * MAX_CHUNK_LENGTH
    with open(filename) as file:
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
    return results


def get_non_unique_set(results):
    non_unique_set = set()
    for key, value in results.items():
        if value >= 2:
            non_unique_set.add(key)
    return non_unique_set

input_results = analyze_file(args.input)
input_set = get_non_unique_set(input_results)
corpus_results = analyze_file(args.corpus)
corpus_set = get_non_unique_set(corpus_results)
print(input_results)
print(input_set)
print(corpus_results)
print(corpus_set)
print(input_set & corpus_set)

