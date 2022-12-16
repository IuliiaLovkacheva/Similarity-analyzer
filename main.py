import argparse
from text_analyzer import TextAnalyzer

parser = argparse.ArgumentParser()
parser.add_argument("--input")
parser.add_argument("--corpus")
args = parser.parse_args()

try:
    input_file_chunk_set = None
    with open(args.input) as input_file:
        input_text_analyzer = TextAnalyzer()
        for line in input_file:
            input_text_analyzer.process_line(line)
        input_file_chunk_set = input_text_analyzer.chunk_set

    text_number = 1
    corpus_text_data = []
    with open(args.corpus) as corpus_file:
        corpus_text_analyzer = TextAnalyzer()
        for line in corpus_file:
            if line.startswith("-") and line.rstrip() == "-":
                top_chunks = corpus_text_analyzer.top_chunks
                text_results = f"[{text_number}] "
                text_results += ','.join(map(lambda chunk_data: f"{chunk_data[0]} ({chunk_data[1]} entries)", top_chunks))
                print(text_results)
                corpus_text_data.append(set(chunk for chunk, frequency in top_chunks))
                text_number += 1
                corpus_text_analyzer = TextAnalyzer()
            else:
                corpus_text_analyzer.process_line(line)
        top_chunks = corpus_text_analyzer.top_chunks
        text_results = f"[{text_number}] "
        text_results += ','.join(map(lambda chunk_data: f"{chunk_data[0]} ({chunk_data[1]} entries)", top_chunks))
        print(text_results)
        corpus_text_data.append(set(chunk for chunk, frequency in top_chunks))

    most_similar = []
    highest_similarity_level = 1
    print(input_file_chunk_set)
    for i in range(0, len(corpus_text_data)):
        similarity_level = len(input_file_chunk_set.intersection(corpus_text_data[i]))
        if similarity_level > highest_similarity_level:
            highest_similarity_level = similarity_level
            most_similar = [i + 1]
        elif similarity_level == highest_similarity_level:
            most_similar.append(i + 1)

    print(f"[{', '.join(map(str, most_similar))}]")
except IOError as e:
    print(f"Couldn't open file {e.filename}")
