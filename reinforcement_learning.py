import sys; args = sys.argv[1:]
import math


def _next_digits(s, i):
    r = ""
    while i < len(s) and s[i].isdigit():
        r += s[i]; i += 1
    return r, i


def _bit(c, p, v): return c[:p] + v + c[p+1:]
def _adj(x, n): return x if x >= 0 else n + x
def _disc(x, g): return x * g if g >= 0.5 else x - g


def _native(g):
    w = g["width"]; n = g["size"]
    if w == 0 or g["type"] == "N":
        for i in range(n):
            g[i] = ("0000", [], False)
        return g, {}
    h = n // w
    nat = {}
    for i in range(n):
        r, c = divmod(i, w)
        b = ["0", "0", "0", "0"]; nb = []; st = set()
        if r > 0: b[0] = "1"; nb.append(i-w); st.add(i-w)
        if r < h-1: b[1] = "1"; nb.append(i+w); st.add(i+w)
        if c < w-1: b[2] = "1"; nb.append(i+1); st.add(i+1)
        if c > 0: b[3] = "1"; nb.append(i-1); st.add(i-1)
        code = "".join(b)
        g[i] = (code, nb, False)
        nat[i] = (code, st)
    return g, nat


def _add(g, a, b):
    if b in g[a][1]:
        return
    c = g[a][0]; w = g["width"]
    if b == a-w: c = _bit(c, 0, "1")
    elif b == a+w: c = _bit(c, 1, "1")
    elif b == a+1: c = _bit(c, 2, "1")
    elif b == a-1: c = _bit(c, 3, "1")
    g[a] = (c, g[a][1] + [b], False)


def _rem(g, a, b):
    if b not in g[a][1]:
        return
    c = g[a][0]; w = g["width"]
    if b == a-w: c = _bit(c, 0, "0")
    elif b == a+w: c = _bit(c, 1, "0")
    elif b == a+1: c = _bit(c, 2, "0")
    elif b == a-1: c = _bit(c, 3, "0")
    nb = list(g[a][1]); nb.remove(b)
    g[a] = (c, nb, False)
    g.pop(f"({a},{b})r", None)


def _toggle(g, a, b):
    if b in g[a][1]:
        _rem(g, a, b); _rem(g, b, a)
    else:
        _add(g, a, b); _add(g, b, a)


def _safe_idx(seg, n): return None if seg == "" else _adj(int(seg), n)


def _find(spec, g):
    n = g["size"]; w = g["width"]; out = []
    for tok in spec.split(","):
        if ":" in tok:
            p = tok.split(":")
            a = _safe_idx(p[0], n); b = _safe_idx(p[1], n)
            st = int(p[2]) if len(p) > 2 and p[2] != "" else None
            out.extend(g["allVert"][a:b:st])
        elif "#" in tok:
            if tok == "#": continue
            if tok.startswith("#"):
                if tok[1:] == "": continue
                end = _adj(int(tok[1:]), n); er, ec = divmod(end, w)
                for r in range(er+1):
                    for c in range(ec+1): out.append(r*w + c)
            elif tok.endswith("#"):
                if tok[:-1] == "": continue
                start = _adj(int(tok[:-1]), n)
                sr, sc = divmod(start, w)
                er, ec = divmod(n-1, w)
                for r in range(sr, er+1):
                    for c in range(sc, ec+1): out.append(r*w + c)
            else:
                a_s, b_s = tok.split("#")
                if a_s == "" or b_s == "": continue
                a = _adj(int(a_s), n); b = _adj(int(b_s), n)
                sr, sc = divmod(a, w); er, ec = divmod(b, w)
                for r in range(sr, er+1):
                    for c in range(sc, ec+1): out.append(r*w + c)
        elif tok != "":
            out.append(_adj(int(tok), n))
    return out


def _parse_vs(tok, g):
    allow = set(":#,-0123456789"); i = 1; spec = ""
    while i < len(tok) and tok[i] in allow:
        spec += tok[i]; i += 1
    sel = set(_find(spec, g))
    if "R" in tok:
        j = tok.rfind("R") + 1; d = ""
        while j < len(tok) and tok[j].isdigit():
            d += tok[j]; j += 1
        rval = int(d) if d else g["rwd"]
        for v in sel:
            g[f"{v}r"] = rval
    if "B" not in tok:
        return
    w = g["width"]; n = g["size"]
    for v in sel:
        for nb in (v-w, v+w, v-1, v+1):
            if nb < 0 or nb >= n:
                continue
            if abs(nb - v) == 1 and v//w != nb//w:
                continue
            if (v in sel) ^ (nb in sel):
                _toggle(g, v, nb)


def _modify(g, edges, op, val, flag):
    for a, b in edges:
        pres = (b in g[a][1])
        if op == "~":
            if pres:
                _rem(g, a, b); _rem(g, b, a)
            else:
                _add(g, a, b); _add(g, b, a)
        elif op in {"+", "*"}:
            if not pres:
                _add(g, a, b); _add(g, b, a)
        elif op == "!":
            if pres:
                _rem(g, a, b); _rem(g, b, a)
        elif op == "@":
            if not pres:
                continue
        if flag:
            g[f"({a},{b})r"] = val
            g[f"({b},{a})r"] = val


def _readtok(s, i, allow):
    r = ""
    while i < len(s) and s[i] in allow:
        r += s[i]; i += 1
    return r, i


def _parse_e(tok, g):
    mods = {"!", "+", "*", "~", "@"}
    op = "~"; p = 1
    if tok[1] in mods:
        op = tok[1]; p = 2
    seg1, pos = _readtok(tok, p, ":,#-0123456789")
    v1 = _find(seg1, g)
    edges = []
    if pos < len(tok) and tok[pos] in {"=", "~"}:
        seg2, _ = _readtok(tok, pos+1, ":,#-0123456789")
        v2 = _find(seg2, g)
        for a, b in zip(v1, v2):
            edges.append((b, a))
    else:
        dirs = ""; i = pos
        while i < len(tok) and tok[i] in "NSEW":
            dirs += tok[i]; i += 1
        w = g["width"]; n = g["size"]
        for d in dirs:
            for v in v1:
                nb = None
                if d == "N": nb = v - w
                elif d == "S": nb = v + w
                elif d == "E": nb = v + 1 if v//w == (v+1)//w else None
                elif d == "W": nb = v - 1 if v//w == (v-1)//w else None
                if nb is not None and 0 <= nb < n:
                    edges.append((v, nb))
    uniq = []; seen = set()
    for e in edges:
        if e not in seen:
            seen.add(e); uniq.append(e)
    edges = uniq
    flag = False; rval = g["rwd"]
    if "R" in tok:
        flag = True
        j = tok.rfind("R") + 1; d = ""
        while j < len(tok) and tok[j].isdigit():
            d += tok[j]; j += 1
        if d:
            rval = int(d)
    _modify(g, edges, op, rval, flag)


def grfParse(argv):
    t = argv[0]; extra = argv[1:]; g = {}
    g["type"] = t[1] if len(t) > 1 and t[1].isalpha() else "G"
    k = 0
    while k < len(t) and not t[k].isdigit():
        k += 1
    g["size"] = int(_next_digits(t, k)[0])
    g["rwd"] = int(_next_digits(t, t.find("R")+1)[0] or 12) if "R" in t else 12
    if g["type"] == "G":
        if "W" in t:
            g["width"] = int(_next_digits(t, t.find("W")+1)[0])
        else:
            s = g["size"]; w = int(math.sqrt(s))
            while w and s % w:
                w -= 1
            g["width"] = s // w
    else:
        g["width"] = 0
    g["allVert"] = list(range(g["size"]))
    g, nat = _native(g); g["ogNat"] = nat
    for tok in extra:
        if tok.startswith("V"):
            _parse_vs(tok, g)
        elif tok.startswith("E"):
            _parse_e(tok, g)
    return g


def grfSize(g): return g["size"]


def grfGProps(g, v=None):
    d = {"rwd": g["rwd"]}
    if g["type"] == "G":
        d["width"] = g["width"]
    return d


def grfVProps(g, v):
    k = f"{v if v >= 0 else g['size'] + v}r"
    return {"rwd": g[k]} if k in g else {}


def grfEProps(g, a, b):
    k = f"({a},{b})r"
    return {"rwd": g[k]} if k in g else {}


def grfNbrs(g, v=None):
    return [g[i][1] for i in g["allVert"]] if v is None else set(g[v][1])


_cmap = {
    "0000": ".", "0001": "W", "0010": "E", "0011": "-",
    "0100": "S", "0101": "7", "0110": "r", "0111": "v",
    "1000": "N", "1001": "J", "1010": "L", "1011": "^",
    "1100": "|", "1101": "<", "1110": ">", "1111": "+"
}


def grfStrEdges(g):
    if g["type"] == "N" or g["width"] == 0:
        return ""
    body = "".join(_cmap[g[i][0]] for i in range(g["size"]))
    jumps = {(v, n) for v in g["allVert"]
             for n in g[v][1] if n not in g["ogNat"][v][1]}
    if not jumps:
        return body
    seen = set(); out = []
    for a, b in jumps:
        if (b, a) in jumps and (min(a, b), max(a, b)) not in seen:
            out.append(f"{min(a, b)}={max(a, b)}")
            seen.add((min(a, b), max(a, b)))
        elif (b, a) not in jumps:
            out.append(f"{a}~{b}")
    return body + "\nJumps: " + ";".join(out)


def grfStrProps(g):
    s = f"rwd: {g['rwd']}"
    if g["type"] == "G":
        s += f", width: {g['width']}"
    s += "\n"; m = {}
    for k, v in g.items():
        if isinstance(k, str) and k.endswith("r"):
            m.setdefault(v, []).append(k[:-1])
    for r, it in m.items():
        s += ", ".join(sorted(it)) + f": rwd: {r}\n"
    return s.rstrip()


def _reward(g):
    return [int(k[:-1]) for k in g
            if isinstance(k, str) and k.endswith("r") and "(" not in k]


def grfValuePolicy(g, pol, gamma):
    n = g["size"]; val = ["" for _ in range(n)]
    for v in _reward(g):
        val[v] = g[f"{v}r"]
    while True:
        delta = 0.0
        for v in g["allVert"]:
            if v in _reward(g) or not pol[v]:
                continue
            acc = []
            for nb in pol[v]:
                k = f"({v},{nb})r"
                if k in g:
                    acc.append(_disc(g[k], gamma))
                elif val[nb] != "":
                    acc.append(_disc(val[nb], gamma))
            if not acc:
                continue
            nv = sum(acc) / len(acc)
            ov = 0 if val[v] == "" else val[v]
            delta = max(delta, abs(nv - ov)); val[v] = nv
        if delta < 1e-3:
            break
    return val


def grfPolicyFromValuation(g, val, gamma=0.01):
    pol = [set() for _ in g["allVert"]]
    for v in g["allVert"]:
        if v in _reward(g):
            continue
        best = None; chs = []
        for nb in g[v][1]:
            k = f"({v},{nb})r"
            vnb = _disc(g[k], gamma) if k in g else (
                   _disc(val[nb], gamma) if val[nb] != "" else None)
            if vnb is None:
                continue
            if best is None or vnb > best:
                best = vnb; chs = [nb]
            elif vnb == best:
                chs.append(nb)
        pol[v].update(sorted(chs))
    return pol


def grfFindOptimalPolicy(g, gamma=0.01):
    pol = [set() for _ in g["allVert"]]
    for v in g["allVert"]:
        if v in _reward(g):
            continue
        pol[v] = set(g[v][1])
    while True:
        val = grfValuePolicy(g, pol, gamma)
        new = grfPolicyFromValuation(g, val, gamma)
        if all(new[i] == pol[i] for i in g["allVert"]):
            return new
        pol = new


def _pol_str(g, pol):
    if g["width"] == 0 or g["type"] == "N":
        return "".join("*" if i in _reward(g) else "." for i in range(g["size"]))
    w = g["width"]; body = ""; jumps = set()
    for v in g["allVert"]:
        if v in _reward(g):
            body += "*"; continue
        bits = ["0", "0", "0", "0"]
        for nb in pol[v]:
            if nb == v-w: bits[0] = "1"
            elif nb == v+w: bits[1] = "1"
            elif nb == v+1: bits[2] = "1"
            elif nb == v-1: bits[3] = "1"
            if nb not in g["ogNat"][v][1]:
                jumps.add((v, nb))
        body += _cmap["".join(bits)]
    if not jumps:
        return body
    seen = set(); out = []
    for a, b in jumps:
        if (b, a) in jumps and (min(a, b), max(a, b)) not in seen:
            out.append(f"{min(a, b)}={max(a, b)}"); seen.add((min(a, b), max(a, b)))
        elif (b, a) not in jumps:
            out.append(f"{a}~{b}")
    return body + "\nJumps: " + ";".join(out)


def _grid(s, w):
    if w == 0:
        print(s)
    else:
        for i in range(0, len(s), w):
            print(s[i:i + w])


def _val(g, val):
    w = g["width"]; fmt = lambda x: "      00"[-6:] if x == "" else f"      {x:.5g}"[-6:]
    if w == 0 or g["type"] == "N":
        print("".join(fmt(x) for x in val))
    else:
        for i in range(0, g["size"], w):
            print("".join(fmt(x) for x in val[i:i+w]))


def main():
    g = grfParse(args)
    print("Graph:"); _grid(grfStrEdges(g), g["width"]); print(grfStrProps(g))
    pol = grfFindOptimalPolicy(g, 0.01); val = grfValuePolicy(g, pol, 0.01)
    print("\nOptimal policy:"); _grid(_pol_str(g, pol), g["width"])
    print("\nValuation:"); _val(g, val)


if __name__ == "__main__":
    main()




# Aadi Malhotra

