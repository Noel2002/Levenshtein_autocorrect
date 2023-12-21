from autocorrector import AutoCorrector
import time
import statistics
if __name__ == "__main__":
    _instance = AutoCorrector()
    _results = []
    print("Processing  ...")
    _start = time.time()
    with open('trials.txt', 'r') as file:
        while _sentence := file.readline():
            _res = _instance.auto_correct_sentence(_sentence)
            _results.append(_res)
    _end = time.time()
    _time_used = _end - _start
    _corrections_counts = 0
    _total_sentence_length = 0
    _sentence_count = 0

    for _res in _results:
        _total_sentence_length += len(_res[0].split(" "))
        _corrections_counts += len(_res[1])
        _sentence_count += 1

    _average_sentence_length = _total_sentence_length/_sentence_count
    _average_correction_time = _time_used/_corrections_counts
    print(f'''
    Performance evaluation results:
    ==============================
    Total words processed: {_total_sentence_length} words
    Number of sentences processed: {_sentence_count} sentences
    Average words per sentence: {_average_sentence_length} words/sentence
    Number of corrections made: {_corrections_counts} correction
    Time taken: {_time_used} seconds
    Average correction time: {_average_correction_time} seconds/correction
    Average time on sentence: {_time_used/ _sentence_count} seconds/sentence
    
    ''')

