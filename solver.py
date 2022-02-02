from vocabulary import v as vocab, freq


def words_like(query, excluded=()):
    assert len(query) == 5
    condition = [0, 0, 0, 0, 0]
    for i, ch in enumerate(query):
        if ch.isalpha():
            condition[i] = ch.lower()

    ans = []
    for word in vocab:
        flag = False
        for exclu in excluded:
            if exclu in word:
                flag = True
                break
        if flag:
            continue
        for i, cond in enumerate(condition):
            if cond != 0 and cond != word[i]:
                flag = True
                break
        if not flag:
            ans.append(word)
    return ans


def possible_words(yellows=(), greens=(), blacks=()):
    '''
    yellows/greens: ["Y1", "C2", ...]
    '''
    # if not yellows and not greens:
    #     raise ValueError("no requirement specified")
    g, y = greens.copy(), yellows.copy()
    for i, green in enumerate(greens):
        g[i] = (green[0].lower(), int(green[1])-1)
    for i, yellow in enumerate(yellows):
        y[i] = (yellow[0].lower(), int(yellow[1])-1)

    query = ["-"] * 5
    for ch, pos in g:
        query[pos] = ch

    possible_words = words_like(query, [b.lower() for b in blacks])
    ans = []
    for word in possible_words:
        flag = False
        for ch, pos in y:
            if ch not in word or word[pos] == ch:
                flag = True
                break
        if not flag:
            ans.append(word)
    return ans


def possible_words_simple(trials, colors):
    '''
    trials: ["OPERA", "LEMON", "EIGHT"]
    colors: ["YBYBB", "BYBYB", "YBBYY"]
    '''
    yellows = []
    greens = []
    blacks = set()
    for i, color in enumerate(colors):
        for j, ch in enumerate(color):
            if ch.upper() == "Y":
                yellows.append((trials[i][j], j+1))
            elif ch.upper() == "G":
                greens.append((trials[i][j], j+1))
            elif ch.upper() == "B":
                blacks.add(trials[i][j])
    return possible_words(yellows, greens)


def words_contains(chars):
    ans = []
    for word in vocab:
        flag = False
        for ch in chars:
            if ch not in word:
                flag = True
                break
        if not flag:
            ans.append(word)
    return ans


def string_diff(s1, s2):
    # def to_num(s):
    #     assert len(s) == 5 and s.isalpha()
    #     return (ord(s[0])-ord('a')) + (ord(s[1])-ord('a')) * 30 + (ord(s[2])-ord('a')) * 900 \
    #         + (ord(s[3])-ord('a')) * 27000 + (ord(s[4])-ord('a')) * 810000
    return list(ch for i, ch in enumerate(s1) if s2[i] != ch)


def suggestion(yellows=(), greens=(), blacks=(), show_possible=False):
    words = possible_words(yellows, greens, blacks)
    if len(words) < 20 and show_possible:
        print("possible", words)
    
    # special_case = False
    # if len(words) <= 10 and len(words) > 2:
    #     flag=False
    #     for i, word1 in enumerate(words):
    #         for j, word2 in enumerate(words[i+1:]):
    #             if len(string_diff(word1, word2)) > 1:
    #                 flag = True
    #                 break
    #         if flag:
    #             break
    #     if not flag:
    #         special_case = True
    #         # print("special case")
    
    # if special_case:
    #     diff_chars = set()
    #     for i, word1 in enumerate(words):
    #         for j, word2 in enumerate(words):
    #             diff_chars.update(string_diff(word1, word2))
                
    #     new_diff = []
    #     for ch in diff_chars:
    #         flag = False
    #         for word in words:
    #             if ch not in word:
    #                 flag = True
    #                 break
    #         if flag:
    #             new_diff.append(ch)
    #     diff_chars = new_diff
        
    #     # print(len(diff_chars), words)
    #     diff_chars = list(diff_chars)
    #     k = 5
    #     while True:
    #         words2 = words_contains(diff_chars[:k])
    #         if words2:
    #             # print(words2[0])
    #             return words2[0]
    #         k -= 1
    
    best = 0
    best_word = "NONE"
    for word in words:
        cnt = 0
        for i, ch in enumerate(word):
            cnt += freq[i][ch]
            # for j in range(5):
            #     if j != i:
            #         cnt += freq[j][ch] * 0.05
        if cnt > best:
            best = cnt
            best_word = word
    # print(best_word, best)
    return best_word         


def solver():
    yellows, greens, blacks = [], [], set()
    while True:
        suggest = suggestion(yellows, greens, blacks)
        result = input(f"try the word '{suggest}': ").upper()
        if result == "GGGGG":
            break
        for i, ch in enumerate(result):
            if ch == "G":
                greens.append(suggest[i]+str(i+1))
            elif ch == "Y":
                yellows.append(suggest[i]+str(i+1))
            elif ch == "B":
                blacks.add(suggest[i])


def get_result(gt, pred):
    ret = []
    for i, ch in enumerate(pred):
        if gt[i] == ch:
            ret.append("G")
        elif ch in gt:
            ret.append("Y")
        else:
            ret.append("B")
    return "".join(ret)


def test_solver_single(ans, silent=False):
    ans = ans.lower()
    if not silent:
        print("answer:", ans)
    yellows, greens, blacks = [], [], set()
    round = 0
    while True:
        round += 1
        suggest = suggestion(yellows, greens, blacks, show_possible=not silent)
        result = get_result(ans, suggest)
        if not silent:
            print(f"round {round}, pred '{suggest}', got {result}")
        if result == "GGGGG":
            if not silent:
                print("I win in round", round)
            return round
        for i, ch in enumerate(result):
            if ch == "G":
                greens.append(suggest[i]+str(i+1))
            elif ch == "Y":
                yellows.append(suggest[i]+str(i+1))
            elif ch == "B":
                blacks.add(suggest[i]) 


def test_solver_all():
    all_rounds = []
    for word in vocab:
        cur = test_solver_single(word, silent=True)
        print(word, cur)
        all_rounds.append(cur)
    print("average", sum(all_rounds)/len(vocab), "max", max(all_rounds))


if __name__ == '__main__':
    # test_solver_all()
    test_solver_single("leafy")
    # test_solver_single("howdy")
    # test_solver_single("jazzy")
    # test_solver_single("hover")  piper refer riper viper wider
    # print(suggestion())
    # print(suggestion(yellows=["T4", "S1"], blacks="LAE"))
    # print(suggestion(greens=["O2","S4", "T5"], yellows=["O3"], blacks="LAEB"))
    # print(suggestion(greens=["O2","S4", "T5"], yellows=["O3"], blacks="LAEBF"))
    print(possible_words(
        yellows=["L2", "E5"],
        greens=["A3", "E2", "Y5"],
        blacks=("S", "T", "M")
    ))
    print(possible_words_simple(
        trials=["slate", "mealy"],
        colors=["BYGBY", "BGGYG"]
    ))
    print(suggestion(
        yellows=["L2", "E5"],
        greens=["A3", "E2", "Y5"],
        blacks=("S", "T", "M")
    ))
    pass