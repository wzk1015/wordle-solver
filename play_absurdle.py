from solver import possible_words, to_emoji, process_result
from vocabulary import v as vocab


def get_result_new_ans(attempt, yellows, greens, blacks):
    result = ["-"] * 5
    color = 'YGB'
    max_num_words = 0
    max_result = None
    max_words = None
    for i in range(243):
        result = color[(i+1-i%81-i%27-i%9-i%3)//81] + color[(i%81-i%27-i%9-i%3)//27] + \
            color[(i%27-i%9-i%3)//9] + color[(i%9-i%3)//3] + color[i%3]
        ny, ng, nb = yellows.copy(), greens.copy(), blacks.copy()
        process_result(result, attempt, ny, ng, nb)
        words = possible_words(ny, ng, nb)
        if max_num_words < len(words):
            max_num_words = len(words)
            max_result = result
            max_words = words
    # print(max_result, max_num_words)
    return max_result, max_words
    

def play_absurdle():
    yellows, greens, blacks = [], [], set()
    cur_words = vocab
    while True:
        attempt = input("your guess: ").lower()
        if attempt == "quit":
            if len(cur_words) > 10:
                print("answer:", ", ".join(cur_words[:10]), f"... and {len(cur_words)-10} more")
            else:
                print("answer:", ", ".join(cur_words))
            return
        
        if len(attempt) != 5 or not attempt.isalpha() or attempt not in vocab:
            print("invalid word")
            continue
        
        result, cur_words = get_result_new_ans(attempt, yellows, greens, blacks)
        print(to_emoji(result), end=". ")
        
        if result == "GGGGG":
            print("congratulations!")
            return
        process_result(result, attempt, yellows, greens, blacks) 


if __name__ == "__main__":
    play_absurdle()