from solver import get_result, to_emoji
from vocabulary import v as vocab
import random


def play_wordle():
    ans = random.choice(vocab)
    while True:
        attempt = input("your guess: ").lower()
        if attempt == "quit":
            print("answer:", ans)
            return
        
        if len(attempt) != 5 or not attempt.isalpha() or attempt not in vocab:
            print("invalid word")
            continue
        
        result = get_result(ans, attempt)
        print(to_emoji(result), end=". ")
        
        if result == "GGGGG":
            print("congratulations!")
            return

if __name__ == "__main__":
    play_wordle()