from autocorrector import AutoCorrector

if __name__ == "__main__":
    _instance = AutoCorrector()
    _instance.print_statistics()
    print("""
    ========================
    AutoCorrect Application
    ========================
    """)
    while (line := input("Please enter sentence or type 'q' to exit:\n> ")) != "q":
        print("Processing ...", end='\r')
        _res = _instance.auto_correct_sentence(line)
        print('                           ')  # for clearing "Processing ..." from the screen
        # continue the loop when no type are found
        if len(_res[1]) == 0:
            print("No typos found by the program.")
            continue

        print("-------------------------------------- RESULTS ----------------------------------------------------\n")
        print('[Autocorrected sentence]')
        print(_res[0])

        print("\n[Automatic corrections]")
        for _correction in _res[1]:
            print(" => ".join(_correction), end=" | ")
        print()

        print("\n[Suggestions]")
        for _token, _suggestions in _res[2].items():
            print(f'* {_token}: ', [_suggestion[0] for _suggestion in _suggestions])

        print("--------------------------------------END OF RESULTS ------------------------------------------------\n")
