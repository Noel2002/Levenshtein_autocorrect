import re


def get_trigrams(word):
    res = set()
    for i in range(0, len(word) - 2, 1):
        res.add(word[i: i + 3])
    return res


def get_padded_trigrams(word):
    word = "  " + word
    return get_trigrams(word)


def lev_distance(w1, w2):
    m = len(w1) + 1
    n = len(w2) + 1

    OPT = [[0] * n for _ in range(m)]
    for i in range(n):
        OPT[0][i] = i

    for j in range(m):
        OPT[j][0] = j

    for i in range(1,m):
        for j in range(1, n):
            cost = 0 if w1[i-1] == w2[j-1] else 1
            OPT[i][j] = min(1 + OPT[i-1][j], 1 + OPT[i][j-1], cost + OPT[i-1][j-1])
    return OPT[-1][-1]


def sort_candidates(_list):
    _res = list(_list)
    n = len(_res)

    # Traverse through all array elements
    for i in range(n):
        swapped = False

        # Last i elements are already in place
        for j in range(0, n - i - 1):

            # Traverse the array from 0 to n-i-1
            # Swap if the element found is greater
            # than the next element
            if _res[j][1] > _res[j + 1][1] or (_res[j][1] == _res[j+1][1] and (_res[j][2] < _res[j+1][2])):
                _res[j], _res[j + 1] = _res[j + 1], _res[j]
                swapped = True
        if swapped == False:
            break
    return _res


class AutoCorrector:
    def __init__(self):
        self.DICTIONARY = dict()
        self.TRIGRAMS = dict()
        count = 0

        print("Initializing Dictionary ...")
        with open("data/corpora_news.txt", "r") as file:
            while line := file.readline():
                tokens = line.rstrip().split()
                word = tokens[1].lower()

                if word in self.DICTIONARY:
                    self.DICTIONARY[word] += 1
                else:
                    self.DICTIONARY[word] = 1

                count += 1

                if count % 100000 == 0:
                    print(f'Added {count} words', end='\r')
        print(f'\n====> FINISH: {count} words added successfully!')

        print("\nCreating Trigrams index ...")
        for word in self.DICTIONARY:
            word_trigrams = get_padded_trigrams(word)

            for trigram in word_trigrams:
                if trigram in self.TRIGRAMS:
                    self.TRIGRAMS[trigram].add(word)
                else:
                    self.TRIGRAMS[trigram] = set()
                    self.TRIGRAMS[trigram].add(word)
        print(f'====> FINISH: Trigrams index created successfully!')

    def print_statistics(self):
        _values = self.DICTIONARY.values()
        _keys = self.DICTIONARY.keys()
        _max = max(_values)
        _total = sum(_values)
        _count = len(_keys)
        print(f"""
                Here are the statistics of the Dictionary index:
                =====================================================
                Total number of words from corpus: {_total}
                Number of distinct words: {_count}
                Maximum word frequency: {_max}
            """)

        count = 0
        maximum = 0
        for key, value in self.TRIGRAMS.items():
            curr_count = len(value)
            count += curr_count
            if curr_count > maximum:
                maximum = curr_count
        total = len(self.TRIGRAMS)
        average = count / total
        print(f"""
                Here are the statistics of the trigram index:
                =====================================================
                Average words per trigram: {average}
                Maximum words per trigram: {maximum}
                Total number of Trigrams: {total}
            """)

    def correct(self, _word):
        _trigrams = set()
        if len(_word) <= 4:
            _trigrams = get_padded_trigrams(_word)
        else:
            _trigrams = get_trigrams(_word)

        _res = []
        _candidates = set()
        for _trigram in _trigrams:
            if not (_trigram in self.TRIGRAMS):
                continue

            _words = self.TRIGRAMS[_trigram]
            _temp = _candidates.union(_words)
            _candidates = _temp

        # Remove the candidates that are 2 characters longer or shorter than input
        _temp = set(_candidates)
        for _candidate in _temp:
            if abs(len(_word) - len(_candidate) > 2):
                _candidates.discard(_candidate)

        for _candidate in _candidates:
            distance = lev_distance(_word, _candidate)
            _res.append((_candidate, distance, self.DICTIONARY[_candidate]))
        return _res

    def auto_correct(self, _word):
        _candidates = self.correct(_word)
        if not (_candidates and len(_candidates) > 0):
            return (_word, 0)
        _sorted_candidates = sort_candidates(_candidates)
        _choosen = _sorted_candidates[0]
        _best_distance = _choosen[1]
        _suggestions = _sorted_candidates[:5]
        return _choosen, _suggestions

    def auto_correct_sentence(self, _sentence):
        _tokens = _sentence.split(" ")
        _corrections = []
        _suggestions = dict()
        _res = []

        for _token in _tokens:
            if (_token.lower() in self.DICTIONARY) or re.match(r'\d+', _token):
                _res.append(_token)
                continue

            _token = _token.lower()
            _correction, _word_suggestions = self.auto_correct(_token)
            if not _correction:
                _res.append(_token)
                continue
            _corrections.append((_token, _correction[0]))
            _suggestions[_token] = _word_suggestions
            _res.append(_correction[0])
        return " ".join(_res), _corrections, _suggestions

