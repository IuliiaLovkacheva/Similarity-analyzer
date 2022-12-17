import argparse
from text_analyzer import TextAnalyzer


def print_corpus_text_result(text_number, top_chunks):
    text_results = f"[{text_number}] "
    text_results += ','.join(
        map(lambda chunk_data: f"{chunk_data[0]} ({chunk_data[1]} entries)", top_chunks))
    print(text_results)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="The file containing the input text")
    parser.add_argument("corpus", help="The files (at least one), each of"
                                       " which contains a text from the corpus",
                        nargs='+')
    args = parser.parse_args()

    try:
        input_file_chunk_set = None
        with open(args.input) as input_file:
            input_text_analyzer = TextAnalyzer()
            for line in input_file:
                input_text_analyzer.process_line(line)
            input_file_chunk_set = input_text_analyzer.chunk_set

        corpus_text_chunks = []
        for i in range(len(args.corpus)):
            corpus_text_analyzer = TextAnalyzer()
            with open(args.corpus[i]) as corpus_file:
                for line in corpus_file:
                    corpus_text_analyzer.process_line(line)
            top_chunks = corpus_text_analyzer.top_chunks
            corpus_text_chunks.append(top_chunks)

        most_similar = []
        highest_similarity_level = 1
        print(input_file_chunk_set)
        for i in range(0, len(corpus_text_chunks)):
            print_corpus_text_result(i + 1, corpus_text_chunks[i])
            corpus_text_chunk_set = set(chunk for chunk, frequency in corpus_text_chunks[i])
            similarity_level = len(input_file_chunk_set.intersection(corpus_text_chunk_set))
            if similarity_level > highest_similarity_level:
                highest_similarity_level = similarity_level
                most_similar.clear()
                most_similar.append(i + 1)
            elif similarity_level == highest_similarity_level:
                most_similar.append(i + 1)

        print(f"[{', '.join(map(str, most_similar))}]")
    except IOError as e:
        print(f"Couldn't open file {e.filename}")
