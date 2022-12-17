class TextAnalyzer:
    _MAX_CHUNK_LENGTH = 4
    _MOST_POPULAR_NUMBER = 10

    def __init__(self):
        self._chunk_list = [''] * self._MAX_CHUNK_LENGTH
        self._results = dict()
        self._chunk_length = 0
        self._start_index = 0

    def process_line(self, line):
        for c in line:
            self._process_character(c)

    def _process_character(self, c):
        if c.isspace():
            self._chunk_length = 0
            self._start_index = 0
        else:
            if self._chunk_length == 4:
                self._chunk_list[self._start_index] = c
                self._start_index = (self._start_index + 1) % self._MAX_CHUNK_LENGTH
                self._save_chunk()
            else:
                self._chunk_list[self._chunk_length] = c
                self._chunk_length += 1
                if self._chunk_length == 4:
                    self._save_chunk()

    def _save_chunk(self):
        chunk_string = self._current_chunk_string()
        if chunk_string in self._results:
            self._results[chunk_string] += 1
        else:
            self._results[chunk_string] = 1

    def _current_chunk_string(self):
        chunk_list_in_order = self._chunk_list[self._start_index:]
        chunk_list_in_order.extend(self._chunk_list[:self._start_index])
        return "".join(chunk_list_in_order)

    @property
    def top_chunks(self):
        sorted_chunks = sorted(filter(lambda item: item[1] > 1, self._results.items()),
                               key=lambda item: item[1], reverse=True)
        if len(sorted_chunks) > self._MOST_POPULAR_NUMBER:
            return sorted_chunks[:self._MOST_POPULAR_NUMBER]
        return sorted_chunks

    @property
    def chunk_set(self):
        return set(self._results.keys())
