import sys;args=sys.argv[1:]
import math
import random,time

HLLIM=11
memo={}
VERBOSE=False
opening_book={}

def to_2d(s,w):
    return [list(s[i:i+w]) for i in range(0,len(s),w)]
def to_string(g):
    return ''.join(''.join(r) for r in g)
def r90(g):
    h=len(g)
    w=len(g[0])
    return [[g[h-1-r][c] for r in range(h)] for c in range(w)]
def r180(g):
    return r90(r90(g))
def r270(g):
    return r90(r180(g))
def fh(g):
    return g[::-1]
def fv(g):
    return [r[::-1] for r in g]
def dmain(g):
    return list(map(list,zip(*g)))
def danti(g):
    h=len(g)
    w=len(g[0])
    return [[g[h-1-r][w-1-c] for r in range(h)] for c in range(w)]

def rotate64(board_str):
    w=8
    h=8
    new_board=['']*(w*h)
    for r in range(h):
        for c in range(w):
            i=c*h+(h-1-r)
            new_board[i]=board_str[r*w+c]
    return ''.join(new_board)

def flip_horizontal64(board_str):
    w=8
    h=8
    res=''
    for r in range(h):
        row=board_str[r*w:(r+1)*w]
        res+=row[::-1]
    return res

def all_transformations_64(board_str):
    s=set()
    cur=board_str
    for _ in range(2):
        s.add(cur)
        fh=flip_horizontal64(cur)
        s.add(fh)
        cur=rotate64(cur)
    return s

def canonical64(board_str):
    al=all_transformations_64(board_str)
    return min(al)

def make_board(args=None):
    if args and len(args[0])==64:
        board1d=args[0].lower()
    else:
        board1d='.'*27+'ox......xo'+'.'*27
    board2d=[]
    for i in range(0,len(board1d),8):
        board2d.append(list(board1d[i:i+8]))
    return board2d

def parse_move(move):
    if move.isdigit():
        return divmod(int(move),8)
    elif len(move)==2 and move[0].isalpha() and move[1].isdigit():
        row=int(move[1])-1
        col=ord(move[0].lower())-ord('a')
        if 0<=row<8 and 0<=col<8:
            return (row,col)
    return None

def clone_board(board2d):
    return [r[:] for r in board2d]

def clear_uppercase(board2d):
    for r in range(8):
        for c in range(8):
            if board2d[r][c] in ('X','O'):
                board2d[r][c]=board2d[r][c].lower()

def disc_difference(board2d,token):
    opp='o' if token=='x' else 'x'
    score=0
    for row in board2d:
        score += row.count(token)+row.count(token.upper())
        score -= row.count(opp)+row.count(opp.upper())
    return score

def find_flips(board2d,row,col,token):
    opponent='o' if token=='x' else 'x'
    directions=[(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]
    flips=[]
    for dr,dc in directions:
        r=row+dr
        c=col+dc
        line=[]
        while 0<=r<8 and 0<=c<8 and board2d[r][c]==opponent:
            line.append((r,c))
            r+=dr
            c+=dc
        if 0<=r<8 and 0<=c<8 and board2d[r][c]==token:
            flips.extend(line)
    return flips

def find_possible_moves(board2d,token):
    opp='o' if token=='x' else 'x'
    moves=[]
    directions=[(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]
    for r in range(8):
        for c in range(8):
            if board2d[r][c]=='.':
                for dr,dc in directions:
                    rr=r+dr
                    cc=c+dc
                    line_opp=False
                    while 0<=rr<8 and 0<=cc<8:
                        cell=board2d[rr][cc]
                        if cell.lower()==opp:
                            line_opp=True
                            rr+=dr
                            cc+=dc
                        elif cell.lower()==token and line_opp:
                            moves.append((r,c))
                            break
                        else:
                            break
    return list(set(moves))

def make_move(board2d,token,move):
    parsed=parse_move(move)
    if not parsed:
        return None
    (r,c)=parsed
    pm=find_possible_moves(board2d,token)
    if(r,c)not in pm:
        return None
    board2d[r][c]=token.upper()
    opp='o' if token=='x' else 'x'
    directions=[(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]
    for dr,dc in directions:
        rr=r+dr
        cc=c+dc
        flips=[]
        while 0<=rr<8 and 0<=cc<8:
            cell=board2d[rr][cc]
            if cell.lower()==opp:
                flips.append((rr,cc))
            elif cell.lower()==token:
                for(fr,fc)in flips:
                    board2d[fr][fc]=token
                break
            else:
                break
            rr+=dr
            cc+=dc
    return board2d

def print_board(board2d):
    for row in board2d:
        print(" ".join(row))
    print()

def print_board_with_asterisks(board2d,token):
    poss=find_possible_moves(board2d,token)
    copyb=[r[:] for r in board2d]
    for(r,c)in poss:
        copyb[r][c]='*'
    print_board(copyb)
    return poss

def print_state(board2d,token_to_play):
    s=''.join(''.join(r)for r in board2d)
    x_count=sum(ch.lower()=='x' for ch in s)
    o_count=sum(ch.lower()=='o' for ch in s)
    print(s," ",x_count,"/",o_count)
    moves=find_possible_moves(board2d,token_to_play)
    if moves:
        positions=sorted(r*8+c for(r,c)in moves)
        print("Possible moves for",token_to_play+": "+", ".join(map(str,positions)))
    else:
        print("No possible moves")

def is_corner_move(move):
    return move in {(0,0),(0,7),(7,0),(7,7)}

def is_edges(move):
    row,col=move
    edge_positions={(0,2),(0,3),(0,4),(0,5),(7,2),(7,3),(7,4),(7,5),(2,0),(3,0),(4,0),(5,0),(2,7),(3,7),(4,7),(5,7)}
    return (row,col) in edge_positions

def get_adjacent_positions(corner):
    row,col=corner
    adj=[]
    for dr in [-1,0,1]:
        for dc in [-1,0,1]:
            if dr==0 and dc==0:
                continue
            rr=row+dr
            cc=col+dc
            if 0<=rr<8 and 0<=cc<8:
                adj.append((rr,cc))
    return adj

def quickMove(board1d,token):
    board2d=[]
    for i in range(0,len(board1d),8):
        board2d.append(list(board1d[i:i+8]))
    moves=find_possible_moves(board2d,token)
    if not moves:
        return None
    corner_moves=[m for m in moves if is_corner_move(m)]
    if corner_moves:
        sel=random.choice(corner_moves)
        return sel[0]*8+sel[1]
    opponent='o' if token=='x' else 'x'
    corners=[(0,0),(0,7),(7,0),(7,7)]
    opponent_corners=[c for c in corners if board2d[c[0]][c[1]]!=token]
    x_squares=set()
    for corner in opponent_corners:
        x_squares.update(get_adjacent_positions(corner))
    non_x_moves=[m for m in moves if m not in x_squares]
    if non_x_moves:
        move_opp_len={}
        for m in non_x_moves:
            idx=m[0]*8+m[1]
            tmp=clone_board(board2d)
            if make_move(tmp,token,str(idx))is not None:
                opp_moves=find_possible_moves(tmp,opponent)
                move_opp_len[m]=len(opp_moves)
        if move_opp_len:
            min_opp=min(move_opp_len.values())
            best_moves=[m for m,v in move_opp_len.items() if v==min_opp]
            sel=random.choice(best_moves)
            return sel[0]*8+sel[1]
        else:
            sel=random.choice(non_x_moves)
            return sel[0]*8+sel[1]
    else:
        edges_chance=[m for m in moves if is_edges(m)]
        if edges_chance:
            sel=random.choice(edges_chance)
        else:
            sel=random.choice(moves)
        return sel[0]*8+sel[1]

def alphaBetaR(board2d,token,alpha,beta):
    opponent='o' if token=='x' else 'x'
    pm=find_possible_moves(board2d,token)
    if not pm:
        oppm=find_possible_moves(board2d,opponent)
        if not oppm:
            return [disc_difference(board2d,token)]
        r=alphaBetaR(board2d,opponent,-beta,-alpha)
        return [-r[0]]+r[1:]+[-1]
    best_val=alpha
    best_line=[]
    for(r,c)in pm:
        flipped=find_flips(board2d,r,c,token)
        for(fr,fc)in flipped:
            board2d[fr][fc]=token
        orig=board2d[r][c]
        board2d[r][c]=token
        subres=alphaBetaR(board2d,opponent,-beta,-max(best_val,alpha))
        for(fr,fc)in flipped:
            board2d[fr][fc]=opponent
        board2d[r][c]=orig
        score=-subres[0]
        if score>best_val:
            best_val=score
            best_line=subres[1:]+[r*8+c]
        if best_val>=beta:
            return [best_val]
    return [best_val]+best_line

def alphaBetaTop(board2d,token):
    opponent='o' if token=='x' else 'x'
    pm=find_possible_moves(board2d,token)
    if not pm:
        oppm=find_possible_moves(board2d,opponent)
        if not oppm:
            return [disc_difference(board2d,token)]
        r=alphaBetaR(board2d,opponent,-65,65)
        return [-r[0]]+r[1:]+[-1]
    best_val=-65
    best_line=[]
    alpha,beta=-65,65
    for(r,c)in pm:
        flipped=find_flips(board2d,r,c,token)
        for(fr,fc)in flipped:
            board2d[fr][fc]=token
        original=board2d[r][c]
        board2d[r][c]=token
        result=alphaBetaR(board2d,opponent,-beta,-max(alpha,best_val))
        for(fr,fc)in flipped:
            board2d[fr][fc]=opponent
        board2d[r][c]=original
        score=-result[0]
        if score>best_val:
            best_val=score
            best_line=result[1:]+[r*8+c]
        if best_val>alpha:
            alpha=best_val
        if best_val>=beta:
            return [best_val]
    return [best_val]+best_line

def eval_board(board2d,token):
    return disc_difference(board2d,token) #?!?!?!?!?!? im not even doing anything crazy

def midgameAlphaBeta(board2d,token,depth=4,alpha=-9999,beta=9999):
    if depth==0:
        return(eval_board(board2d,token),None)
    pm=find_possible_moves(board2d,token)
    if not pm:
        oppm=find_possible_moves(board2d,'o' if token=='x' else 'x')
        if not oppm:
            return(disc_difference(board2d,token),None)
        val,mv=midgameAlphaBeta(board2d,'o' if token=='x' else 'x',depth, -beta, -alpha)
        return(-val,None)
    best_val=alpha
    best_move=None
    for(r,c)in pm:
        flipped=find_flips(board2d,r,c,token)
        orig=board2d[r][c]
        for(fr,fc)in flipped:
            board2d[fr][fc]=token
        board2d[r][c]=token
        sub_val,_=midgameAlphaBeta(board2d,'o' if token=='x' else 'x',depth-1,-beta,-max(best_val,alpha))
        for(fr,fc)in flipped:
            board2d[fr][fc]='o' if token=='x' else 'x'
        board2d[r][c]=orig
        score=-sub_val
        if score>best_val:
            best_val=score
            best_move=(r,c)
        if best_val>=beta:
            return(best_val,best_move)
    return(best_val,best_move)

def determine_turn(board2d):
    flat=[cell for row in board2d for cell in row]
    x_count=sum(ch.lower()=='x' for ch in flat)
    o_count=sum(ch.lower()=='o' for ch in flat)
    if(x_count+o_count)%2==0:
        return 'x'
    else:
        return 'o'

def get_move_count(board2d):
    flat=[cell for row in board2d for cell in row]
    return sum(ch.lower() in('x','o') for ch in flat)

def canonical_opening_move(board2d,token):
    c=get_move_count(board2d)
    b_str=''.join(''.join(r)for r in board2d)
    can=canonical64(b_str)
    return opening_book.get((token,can,c))

def understand_input(args):
    bd=make_board()
    tkn=determine_turn(bd)
    moves=[]
    argi=0
    if argi<len(args)and len(args[argi])==64:
        bd=make_board([args[argi]])
        argi+=1
        tkn=determine_turn(bd)
    if argi<len(args)and args[argi].lower()in['x','o']:
        tkn=args[argi].lower()
        argi+=1
    while argi<len(args):
        chunk=args[argi]
        argi+=1
        if chunk.startswith('HL')or chunk.lower()=='v'or chunk.startswith('P')or chunk.startswith('D'):
            continue
        i=0
        while i<len(chunk):
            if chunk[i]=='_':
                i+=1
                if i<len(chunk)and chunk[i].isdigit():
                    pair='0'+chunk[i]
                    i+=1
                else:
                    continue
            else:
                if i+1<len(chunk)and chunk[i].isdigit()and chunk[i+1].isdigit():
                    pair=chunk[i:i+2]
                    i+=2
                else:
                    if chunk[i].isdigit():
                        pair='0'+chunk[i]
                        i+=1
                    else:
                        i+=1
                        continue
            if pair=='-1':
                continue
            pm=parse_move(pair)
            if pm:
                moves.append(pm[0]*8+pm[1])
    return bd,tkn,moves

def runTournament(numGames,hole_limit=10,search_depth=4):
    total_score=0
    for i in range(numGames):
        board2d=make_board()
        current_token='x' if(i%2==0)else 'o'
        while True:
            moves_cur=find_possible_moves(board2d,current_token)
            opp='o' if current_token=='x' else 'x'
            moves_opp=find_possible_moves(board2d,opp)
            if not moves_cur and not moves_opp:
                break
            if moves_cur:
                opening_idx=canonical_opening_move(board2d,current_token)
                if opening_idx is not None:
                    make_move(board2d,current_token,str(opening_idx))
                else:
                    empty_count=sum(row.count('.')for row in board2d)
                    if empty_count<=hole_limit:
                        ab_result=alphaBetaTop(board2d,current_token)
                        if len(ab_result)>1:
                            best_move_index=ab_result[-1]
                            make_move(board2d,current_token,str(best_move_index))
                    else:
                        val,best_move=midgameAlphaBeta(board2d,current_token,depth=search_depth,alpha=-9999,beta=9999)
                        if best_move is not None:
                            move_index=best_move[0]*8+best_move[1]
                            make_move(board2d,current_token,str(move_index))
                current_token=opp
            else:
                current_token=opp
        final_str=''.join(''.join(row)for row in board2d)
        count_x=final_str.count('x')
        count_o=final_str.count('o')
        score=count_x-count_o
        total_score+=score
        print("Game",i+1,"final board: X="+str(count_x)+", O="+str(count_o)+", score="+str(score))
    avg_score=total_score/numGames if numGames else 0
    print("Average score over",numGames,"games:",str(avg_score))

def applyCommandLineMoves(board2d,token_to_play,moves):
    last_move_str=None
    for mv in moves:
        clear_uppercase(board2d)
        move_str=str(mv)
        updated=make_move(board2d,token_to_play,move_str)
        if updated:
            last_move_str=token_to_play+" plays to "+str(mv)
            token_to_play='o' if token_to_play=='x' else 'x'
        else:
            opp='o' if token_to_play=='x' else 'x'
            updated2=make_move(board2d,opp,move_str)
            if updated2:
                last_move_str=opp+" plays to "+str(mv)
                token_to_play='o' if opp=='x' else 'x'
    if last_move_str:
        print(last_move_str)
    return token_to_play

def main():
    global VERBOSE
    hole_limit=11
    tournament_mode=False
    numGames=0
    search_depth=4

    for val in args:
        if val.startswith("HL")and val[2:].isdigit():
            hole_limit=int(val[2:])
        elif val.startswith("P")and val[1:].isdigit():
            tournament_mode=True
            numGames=int(val[1:])
        elif val.startswith("D")and val[1:].isdigit():
            search_depth=int(val[1:])
        elif val.lower()=="v":
            VERBOSE=True

    if tournament_mode:
        runTournament(numGames,hole_limit=hole_limit,search_depth=search_depth)
        return

    board2d,token_to_play,moves=understand_input(args)

    opponent='o' if token_to_play=='x' else 'x'

    if not find_possible_moves(board2d,token_to_play):
        token_to_play=opponent # if no move from the person playing switch to opponent

    print_board_with_asterisks(board2d,token_to_play)
    print_state(board2d,token_to_play) #format

    opening_idx=canonical_opening_move(board2d,token_to_play)
    

    token_to_play=applyCommandLineMoves(board2d,token_to_play,moves)

    print_board_with_asterisks(board2d,token_to_play)
    print_state(board2d,token_to_play)

    board_str=''.join(''.join(row)for row in board2d)
    qpref=quickMove(board_str,token_to_play)
    if qpref is not None:
        print("My preferred move is:",qpref)

    total_empty=sum(r.count('.')for r in board2d)
    if total_empty<=hole_limit:
        ab=alphaBetaTop(board2d,token_to_play)
        score=ab[0]
        seq=ab[1:]
        print("terminal alpha-beta value is:",score)
        if len(ab)>1:
            print("terminal alpha-beta preferred move is:",ab[-1])
        else:
            print("terminal alpha-beta preferred move is: None")
    else:
        val,best_move=midgameAlphaBeta(board2d,token_to_play,depth=search_depth,alpha=-9999,beta=9999)
        if best_move:
            bm_index=best_move[0]*8+best_move[1]
            print(f"midgame alpha-beta preferred move is: {bm_index}")

if __name__=="__main__":
    main()

# Aadi Malhotra, pd 1, 2026

