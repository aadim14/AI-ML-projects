import sys; args=sys.argv[1:]
import time

start_time = time.time()

def do_seeds(b, s, w):
    p = list(s)
    d = p[0].upper()
    r = 0
    c = 0
    i = 1
    while i < len(p) and p[i].isdigit():
        r = r * 10 + int(p[i])
        i += 1
    if i < len(p) and p[i] == 'x':
        i += 1
    while i < len(p) and p[i].isdigit():
        c = c * 10 + int(p[i])
        i += 1
    x = p[i:] if i < len(p) else ['#']
    L = list(b)
    n = len(L)
    if d == 'H':
        for o, ch in enumerate(x):
            idx = r * w + (c + o)
            if 0 <= idx < n:
                L[idx] = ch
    else:
        for o, ch in enumerate(x):
            idx = (r + o) * w + c
            if 0 <= idx < n:
                L[idx] = ch
    return ''.join(L)

def rot(pos, h, w):
    r, c = divmod(pos, w)
    return (h - 1 - r) * w + (w - 1 - c)

def check_em(board, h, w):
    L = list(board)
    for i in range(h * w):
        s = rot(i, h, w)
        if L[i] == '#' or L[s] == '#':
            L[i] = '#'
            L[s] = '#'
    return ''.join(L)

def get_neighbors(r, c, H, W):
    res = []
    if r > 0:
        res.append((r - 1, c))
    if r < H - 1:
        res.append((r + 1, c))
    if c > 0:
        res.append((r, c - 1))
    if c < W - 1:
        res.append((r, c + 1))
    return res

def connected(board, H, W, fill=False):
    n = H * W
    L = list(board)
    s = None
    for i, ch in enumerate(L):
        if ch != '#':
            s = i
            break
    if s is None:
        return board if fill else True
    st = [s]
    seen = set()
    while st:
        u = st.pop()
        if u in seen:
            continue
        seen.add(u)
        rr, cc = divmod(u, W)
        for(nx, ny) in get_neighbors(rr, cc, H, W):
            idx = nx * W + ny
            if L[idx] != '#' and idx not in seen:
                st.append(idx)
    if fill:
        for i in range(n):
            if L[i] != '#' and i not in seen:
                L[i] = '#'
        return ''.join(L)
    for i in range(n):
        if L[i] != '#' and i not in seen:
            return False
    return True

def over3(b, H, W, fin=False):
    for r in range(H):
        for c in range(W):
            if b[r * W + c] == '#':
                continue
            sc = c
            while sc > 0 and b[r * W + sc - 1] != '#':
                sc -= 1
            ec = c
            while ec < W - 1 and b[r * W + ec + 1] != '#':
                ec += 1
            if (ec - sc + 1) < 3:
                if fin:
                    return False, 'H', r * W + c
                return False
            sr = r
            while sr > 0 and b[(sr - 1) * W + c] != '#':
                sr -= 1
            er = r
            while er < H - 1 and b[(er + 1) * W + c] != '#':
                er += 1
            if (er - sr + 1) < 3:
                if fin:
                    return False, 'V', r * W + c
                return False
    if fin:
        return True, None, None
    return True

def boardlegal(b, H, W):
    if not over3(b, H, W):
        return False
    if not connected(b, H, W):
        return False
    return True

def fixIt(b, H, W):
    L = list(b)
    while True:
        ok, d, pos = over3(''.join(L), H, W, True)
        if ok:
            break
        r, c = divmod(pos, W)
        if d == 'H':
            lc = c
            while lc > 0 and L[r * W + lc - 1] != '#':
                lc -= 1
            rc = c
            while rc < W - 1 and L[r * W + rc + 1] != '#':
                rc += 1
            for cc in range(lc, rc + 1):
                L[r * W + cc] = '#'
        else:
            ur = r
            while ur > 0 and L[(ur - 1) * W + c] != '#':
                ur -= 1
            dr = r
            while dr < H - 1 and L[(dr + 1) * W + c] != '#':
                dr += 1
            for rr in range(ur, dr + 1):
                L[rr * W + c] = '#'
    F = ''.join(L)
    if not connected(F, H, W):
        F = connected(F, H, W, True)
    return F

def addBlocks(b, H, W, target, start=0):
    if not boardlegal(b, H, W):
        b = fixIt(b, H, W)
        if not boardlegal(b, H, W):
            return ''
    c = b.count('#')
    if c == target:
        return b
    if c > target:
        return ''
    n = H * W
    L = list(b)
    for i in range(start, n):
        if L[i] == '-':
            sym = rot(i, H, W)
            if sym < n and L[sym] == '-':
                L[i] = '#'
                L[sym] = '#'
                newb = ''.join(L)
                if boardlegal(newb, H, W):
                    r = addBlocks(newb, H, W, target, i + 1)
                    if r:
                        return r
                L[i] = '-'
                L[sym] = '-'
    return ''

def parseDimsAndGoal(a):
    h = 0
    w = 0
    g = 0
    sd = []
    dfile = None
    for x in a:
        y = x.lower()
        if '.txt' in y:
            dfile = x
        elif 'x' in y and y.replace('x', '').isdigit():
            pa = y.split('x')
            h = int(pa[0])
            w = int(pa[1])
        elif x.isdigit():
            g = int(x)
        else:
            sd.append(x)
    return h, w, g, sd, dfile

def process_seeds(b, seeds, w, h):
    for s in seeds:
        b = do_seeds(b, s, w)
        b = check_em(b, h, w)
    return b

def load_dictionary():
    try:
        lines = open(args[0]).read().splitlines()
    except:
        return set()
    S = set()
    for line in lines:
        line = line.strip()
        if len(line) >= 3 and line.isalpha():
            S.add(line.upper())
    return S

def find_word_runs(b, H, W):
    R = []
    C = []
    for r in range(H):
        c = 0
        while c < W:
            if b[r * W + c] == '#':
                c += 1
                continue
            sc = c
            while c < W and b[r * W + c] != '#':
                c += 1
            l = c - sc
            if l >= 3:
                R.append((r, sc, l))
    for c in range(W):
        r = 0
        while r < H:
            if b[r * W + c] == '#':
                r += 1
                continue
            sr = r
            while r < H and b[r * W + c] != '#':
                r += 1
            l = r - sr
            if l >= 3:
                C.append((sr, c, l))
    return R, C

def build_run_possible_words(b, H, W, runs, D, hz):
    out = []
    for (r, c, l) in runs:
        pat = []
        for i in range(l):
            rr = r if hz else (r + i)
            cc = (c + i) if hz else c
            x = b[rr * W + cc]
            if x == '-' or x == '#':
                pat.append(None)
            else:
                pat.append(x.upper())
        S = set()
        for w2 in D:
            if len(w2) != l:
                continue
            ok = True
            for i in range(l):
                if pat[i] and pat[i] != w2[i]:
                    ok = False
                    break
            if ok:
                S.add(w2)
        out.append(S)
    return out

def get_cell_runs_map(HR, VR):
    m = {}
    for i, (r, c, l) in enumerate(HR):
        for off in range(l):
            rr, cc = r, c + off
            m.setdefault((rr, cc), []).append(('H', i, off))
    for j, (r, c, l) in enumerate(VR):
        for off in range(l):
            rr, cc = r + off, c
            m.setdefault((rr, cc), []).append(('V', j, off))
    return m

def compute_cell_letter_options(b, H, W, HR, VR, HP, VP, cm):
    d = {}
    n = H * W
    for i in range(n):
        if b[i] == '#':
            continue
        r, c = divmod(i, W)
        if (r, c) not in cm:
            continue
        if b[i] not in ('-', '#'):
            d[(r, c)] = {b[i].upper()}
        else:
            L = []
            for (rt, idx, off) in cm[(r, c)]:
                if rt == 'H' and idx < len(HP):
                    cw = HP[idx]
                elif rt == 'V' and idx < len(VP):
                    cw = VP[idx]
                else:
                    cw = set()
                vals = set()
                for w2 in cw:
                    vals.add(w2[off])
                L.append(vals)
            if not L:
                d[(r, c)] = set()
            else:
                S = L[0]
                for S2 in L[1:]:
                    S = S.intersection(S2)
                d[(r, c)] = S
    return d

def is_filled(b):
    return '-' not in b

def choose_cell_with_fewest_options(b, W, copt, cm):
    best_cell = None
    best_options = None
    best_score = float('inf')
    
    for (rc, cc), v in copt.items():
        idx = rc * W + cc
        if b[idx] == '-':
            option_count = len(v)
            run_count = len(cm.get((rc, cc), []))
            score = option_count / max(1, run_count)
            
            if score < best_score:
                best_score = score
                best_cell = (rc, cc)
                best_options = v
    
    return best_cell, best_options

def update_run_poss_after_placement(HP, VP, rt, i, o, letter):
    if rt == 'H':
        tmp = set()
        for w2 in HP[i]:
            if w2[o] == letter:
                tmp.add(w2)
        HP[i] = tmp
    else:
        tmp = set()
        for w2 in VP[i]:
            if w2[o] == letter:
                tmp.add(w2)
        VP[i] = tmp

def remove_used_words(HP, VP, U):
    for i in range(len(HP)):
        HP[i] = HP[i].difference(U)
    for i in range(len(VP)):
        VP[i] = VP[i].difference(U)

def get_run_string(b, H, W, r, c, l, hz):
    s = ''
    for i in range(l):
        rr = r if hz else (r + i)
        cc = (c + i) if hz else c
        s += b[rr * W + cc].upper()
    return s

def identify_completed_runs(b, H, W, HR, VR, HP, VP, U):
    for i, (r, c, l) in enumerate(HR):
        ok = True
        for off in range(l):
            if b[r * W + c + off] == '-':
                ok = False
                break
        if ok:
            s = get_run_string(b, H, W, r, c, l, True)
            S = [ww for ww in HP[i] if ww == s]
            if len(S) == 1 and S[0] not in U:
                U.add(S[0])
    for i, (r, c, l) in enumerate(VR):
        ok = True
        for off in range(l):
            if b[(r + off) * W + c] == '-':
                ok = False
                break
        if ok:
            s = get_run_string(b, H, W, r, c, l, False)
            S = [ww for ww in VP[i] if ww == s]
            if len(S) == 1 and S[0] not in U:
                U.add(S[0])

def get_letter_frequencies(dictionary):
    freq = {}
    for word in dictionary:
        for letter in word:
            freq[letter] = freq.get(letter, 0) + 1
    return freq

def backtrack_fill(b, H, W, HR, VR, HP, VP, cm, U, letter_freq, dp=0, max_depth=9999999, time_limit=9.5):
    if time.time() - start_time > time_limit:
        return None
    
    if dp > max_depth:
        return None
        
    if is_filled(b):
        return b
        
    remove_used_words(HP, VP, U)
    o = compute_cell_letter_options(b, H, W, HR, VR, HP, VP, cm)
    
    for(k, v) in o.items():
        if len(v) == 0:
            return None
    
    (rc, cc), let = choose_cell_with_fewest_options(b, W, o, cm)
    
    if (rc, cc) is None:
        if is_filled(b):
            return b
        return None
        
    i = rc * W + cc
    oc = b[i]
    L = list(b)
    
    sorted_letters = sorted(let, key=lambda x: (-letter_freq.get(x, 0)))
    
    for x in sorted_letters:
        if time.time() - start_time > time_limit:
            return None
            
        L[i] = x
        nb = ''.join(L)
        
        ohp = [set(xx) for xx in HP]
        ovp = [set(xx) for xx in VP]
        ou = set(U)
        
        if (rc, cc) in cm:
            for(rt, ind, off) in cm[(rc, cc)]:
                update_run_poss_after_placement(HP, VP, rt, ind, off, x)
        
        identify_completed_runs(nb, H, W, HR, VR, HP, VP, U)
        
        r = backtrack_fill(nb, H, W, HR, VR, HP, VP, cm, U, letter_freq, dp + 1, max_depth, time_limit)
        if r:
            return r
            
        L[i] = oc
        HP = [set(xx) for xx in ohp]
        VP = [set(xx) for xx in ovp]
        U = set(ou)
        
    return None

def find_horizontal_runs_only(b, H, W):
    runs = []
    for r in range(H):
        c = 0
        while c < W:
            if b[r * W + c] == '#':
                c += 1
                continue
            sc = c
            while c < W and b[r * W + c] != '#':
                c += 1
            length = c - sc
            if length >= 3:
                runs.append((r, sc, length))
    return runs

def pattern_matches(board, H, W, r, c, l, word):
    for i in range(l):
        ch = board[r * W + (c + i)]
        if ch != '-' and ch != '#':
            if ch.upper() != word[i]:
                return False
    return True

def place_word_in_run(board, H, W, r, c, l, word):
    L = list(board)
    for i in range(l):
        L[r * W + (c + i)] = word[i]
    return ''.join(L)

def sort_runs_by_constraint(runs, board, H, W, dictionary):
    run_constraints = []
    for idx, (r, c, l) in enumerate(runs):
        possible_words = 0
        for word in dictionary:
            if len(word) == l and pattern_matches(board, H, W, r, c, l, word):
                possible_words += 1
        run_constraints.append((possible_words, idx))
    
    run_constraints.sort()
    sorted_runs = []
    for _, idx in run_constraints:
        sorted_runs.append(runs[idx])
    return sorted_runs

def fill_horizontal_only(board, H, W, runs, idx, dictionary, used, start_time, time_limit=9.8):
    if time.time() - start_time > time_limit:
        return None
        
    if idx == len(runs):
        return board
        
    (rr, cc, ll) = runs[idx]
    
    matching_words = []
    for w2 in dictionary:
        if len(w2) == ll and w2 not in used and pattern_matches(board, H, W, rr, cc, ll, w2):
            matching_words.append(w2)
    
    if not matching_words:
        return None
    
    for w2 in matching_words:
        nb = place_word_in_run(board, H, W, rr, cc, ll, w2)
        used.add(w2)
        res = fill_horizontal_only(nb, H, W, runs, idx + 1, dictionary, used, start_time, time_limit)
        if res:
            return res
        used.remove(w2)
    
    return None

def fill_partial_horizontal(board, H, W, dictionary, max_time=9.5):
    h_runs = find_horizontal_runs_only(board, H, W)
    h_runs = sort_runs_by_constraint(h_runs, board, H, W, dictionary)
    
    result = board
    used = set()
    
    for i in range(len(h_runs)):
        if time.time() - start_time > max_time:
            break
            
        r, c, l = h_runs[i]
        best_word = None
        
        for word in dictionary:
            if len(word) == l and word not in used and pattern_matches(board, H, W, r, c, l, word):
                best_word = word
                break
                
        if best_word:
            result = place_word_in_run(result, H, W, r, c, l, best_word)
            used.add(best_word)
    
    return result

def fill_greedy(board, H, W, dictionary, max_time=9.5):
    HR, VR = find_word_runs(board, H, W)
    result = board
    used = set()
    
    all_runs = []
    for i, (r, c, l) in enumerate(HR):
        all_runs.append(('H', i, r, c, l))
    for i, (r, c, l) in enumerate(VR):
        all_runs.append(('V', i, r, c, l))
    
    run_constraints = []
    for rt, idx, r, c, l in all_runs:
        possible_words = 0
        for word in dictionary:
            if len(word) == l:
                if rt == 'H' and pattern_matches(board, H, W, r, c, l, word):
                    possible_words += 1
                elif rt == 'V':
                    ok = True
                    for i in range(l):
                        ch = board[(r + i) * W + c]
                        if ch != '-' and ch != '#' and ch.upper() != word[i]:
                            ok = False
                            break
                    if ok:
                        possible_words += 1
        run_constraints.append((possible_words, rt, idx, r, c, l))
    
    run_constraints.sort()
    
    for _, rt, _, r, c, l in run_constraints:
        if time.time() - start_time > max_time:
            break
            
        if rt == 'H':
            for word in dictionary:
                if len(word) == l and word not in used and pattern_matches(result, H, W, r, c, l, word):
                    result = place_word_in_run(result, H, W, r, c, l, word)
                    used.add(word)
                    break
        else:
            for word in dictionary:
                if len(word) == l and word not in used:
                    ok = True
                    for i in range(l):
                        ch = result[(r + i) * W + c]
                        if ch != '-' and ch != '#' and ch.upper() != word[i]:
                            ok = False
                            break
                    if ok:
                        L = list(result)
                        for i in range(l):
                            L[(r + i) * W + c] = word[i]
                        result = ''.join(L)
                        used.add(word)
                        break
    
    return result

def incremental_fill(board, H, W, dictionary, max_time=9.5):
    best_board = board
    best_filled = sum(1 for ch in board if ch not in ('-', '#'))
    
    HR, VR = find_word_runs(board, H, W)
    HP = build_run_possible_words(board, H, W, HR, dictionary, True)
    VP = build_run_possible_words(board, H, W, VR, dictionary, False)
    cm = get_cell_runs_map(HR, VR)
    U = set()
    letter_freq = get_letter_frequencies(dictionary)
    
    for depth_limit in [5, 10, 15, 20, 30]:
        if time.time() - start_time > max_time * 0.8:
            break
            
        sol = backtrack_fill(board, H, W, HR, VR, HP, VP, cm, U, letter_freq, 0, depth_limit, max_time * 0.8)
        if sol:
            filled = sum(1 for ch in sol if ch not in ('-', '#'))
            if filled > best_filled:
                best_board = sol
                best_filled = filled
    
    if time.time() - start_time < max_time * 0.9:
        greedy_sol = fill_greedy(board, H, W, dictionary, max_time * 0.9)
        greedy_filled = sum(1 for ch in greedy_sol if ch not in ('-', '#'))
        if greedy_filled > best_filled:
            best_board = greedy_sol
            best_filled = greedy_filled
    
    if time.time() - start_time < max_time:
        partial_sol = fill_partial_horizontal(board, H, W, dictionary, max_time)
        partial_filled = sum(1 for ch in partial_sol if ch not in ('-', '#'))
        if partial_filled > best_filled:
            best_board = partial_sol
    
    return best_board

def main():
    h, w, g, seeds, dfile = parseDimsAndGoal(args)
    b = '-' * (h * w)
    b = process_seeds(b, seeds, w, h)
    
    if g == h * w:
        b = '#' * (h * w)
    else:
        b = check_em(b, h, w)
        if not boardlegal(b, h, w):
            b = fixIt(b, h, w)
        c = b.count('#')
        if c < g:
            nb = addBlocks(b, h, w, g)
            if nb:
                b = nb
    
    dic = load_dictionary()
    board_size = h * w
    letter_freq = get_letter_frequencies(dic)
    
    sol = None
    
    if board_size < 200:
        HR, VR = find_word_runs(b, h, w)
        HP = build_run_possible_words(b, h, w, HR, dic, True)
        VP = build_run_possible_words(b, h, w, VR, dic, False)
        cm = get_cell_runs_map(HR, VR)
        U = set()
        
        for time_limit in [3.0, 5.0, 7.0, 9.0]:
            sol = backtrack_fill(b, h, w, HR, VR, HP, VP, cm, U, letter_freq, 0, 9999999, time_limit)
            if sol and is_filled(sol):
                break
    
    elif board_size < 450:
        HR, VR = find_word_runs(b, h, w)
        HP = build_run_possible_words(b, h, w, HR, dic, True)
        VP = build_run_possible_words(b, h, w, VR, dic, False)
        cm = get_cell_runs_map(HR, VR)
        U = set()
        
        sol = backtrack_fill(b, h, w, HR, VR, HP, VP, cm, U, letter_freq, 0, 30, 9.0)
        
        if not sol or not is_filled(sol):
            h_runs = find_horizontal_runs_only(b, h, w)
            h_runs = sort_runs_by_constraint(h_runs, b, h, w, dic)
            used = set()
            sol = fill_horizontal_only(b, h, w, h_runs, 0, dic, used, start_time)
    
    else:
        sol = incremental_fill(b, h, w, dic, 9.5)
    
    if not sol:
        sol = b
    
    for i in range(h):
        print(sol[i * w : (i + 1) * w])

if __name__ == '__main__':
    main()


# Aadi Malhotra, pd 1, 2026

