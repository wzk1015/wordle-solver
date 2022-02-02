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
    return list(ch for i, ch in enumerate(s1) if s2[i] != ch)


def suggestion(yellows=(), greens=(), blacks=(), show_possible=False):
    words = possible_words(yellows, greens, blacks)
    if len(words) < 20 and show_possible:
        print("possible", words)
    
    best = 0
    best_word = "NONE"
    for word in words:
        cnt = 0
        for i, ch in enumerate(word):
            cnt += freq[i][ch]
        if cnt > best:
            best = cnt
            best_word = word
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