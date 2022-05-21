#!/bin/python3
# -*- coding: utf-8 -*-
from prettytable import PrettyTable
class CFG(object):
    def __init__(self,nonterminal_symbol_set,terminal_symbol_set,productions,start_symbol):
        '''
        List nonterminal
        List terminal
        List[HashMap] productions
        char start
        '''
        self.nonterminal_symbol_set = nonterminal_symbol_set
        self.terminal_symbol_set = terminal_symbol_set
        self.productions = productions
        self.start_symbol = start_symbol
        
    def str2productions(str):
        productions = {}
        str = str.strip()
        lines = str.split("\n")
        for line in lines:
            if line != '':
                split_line = line.split("->")
                left = split_line[0].strip()
                right = split_line[1].strip()
                if left in productions:
                    productions[left].add(right)
                else:
                    productions[left] = set()
                    productions[left].add(right)
        return productions

    def __repr__(self):
        return f'nonterminal: {self.nonterminal_symbol_set}\nterminal: {self.terminal_symbol_set}\nproductions: {self.productions}\nstart: {self.start_symbol}'

    def get_production_expression(self,nonterminal_symbol):
        if nonterminal_symbol in self.terminal_symbol_set:
            raise ValueError("class CFG: get_production_expression's argv must to be nonterminal_symbol_set!")
        if self.productions.__contains__(nonterminal_symbol):
            return self.productions[nonterminal_symbol]
        else:
            return None

    def get_production_expression_right(self,nonterminal_symbol):
        expression_right = self.get_production_expression(nonterminal_symbol)
        if expression_right == None:
            raise ValueError("class CFG: get_production_expression_right cause \"None\" error")
        else:
            return expression_right

    def is_nonterminal(self,symbol):
        return symbol in self.nonterminal_symbol_set

    def is_terminal(self,symbol):
        return symbol in self.terminal_symbol_set
    
    def get_terminal_symbol_set(self):
        return self.terminal_symbol_set
    
    def get_nonterminal_symbol_set(self):
        return self.nonterminal_symbol_set
    
    def get_start_symbol(self):
        return self.start_symbol

    def get_all_production_expression_left(self):
        return self.productions.keys()
    def is_start_symbol(self,symbol):
        return self.start_symbol == symbol
    def get_all_production_expression_right(self):
        return self.values()
    def is_empty(self,symbol):
        if symbol == '' or symbol == 'ε':
            return True
        else:
            return False
    def find_production_from_right_by_symbol(self,symbol):
        # 搜索产生式右侧是否有symbol
        result = {}
        for left in self.productions:
            right_list = set()
            for right in self.productions[left]:
                if symbol in right:
                    right_list.add(right)
            if len(right_list) > 0:
                result[left] = right_list
        return result

    def is_nonterminal_symbol_contains_empty(self,symbol):
        if symbol not in self.nonterminal_symbol_set:
            return False
        else:
            if symbol in self.productions:
                right_list = self.productions[symbol]
                for right in right_list:
                    if right == "" or right == "ε":
                        return True
            else:
                return False

    def get_first_set(self):
        '''
1.如果X是终结符，则FIRST(X) = {X}.
2.如果X是非终结符 ，且有产生式 X → a… 则把a加入到FIRST集合中.
若 X → ε也是其中一条产生式，则把ε也加入到FIRST集合中.
3.如果X是非终结符，且 X → Y… 是一条产生式，其中Y是非终结符，那么则把FIRST(Y) - {ε}（即FIRST集合去除ε）加入到FIRST(X)中.
更复杂些的，对于产生式 X → Y1 Y2…Yi-1 Yi…Yk ，其中Y1，…，Yi-1都是非终结符:
    i.对于任意的j，满足 1 <= j <= i-1 ，且FIRST(Yj)都含有ε，则把
FIRST(Yi) \ {ε} 加入到FIRST(X)中.
    ii.对于任意的p，满足 1 <= p <= k ，且FIRST(Yp)都含有ε，则把
ε加入到FIRST(X)中.

连续执行以上三条规则直到集合大小不发生变化为止，其中原则1和原则2只需一次循环即可得到结果
        '''
        first_set = {}
        first_size = -1

        # 定义 获取first大小的函数
        def get_first_set_size():
            size = 0
            for left,right_set in first_set.items():
                size += len(right_set)
            return size

        # 初始化每一个first集
        for nonterminal_symbol in self.nonterminal_symbol_set:
            first_set[nonterminal_symbol] = set()


        # 规则1
        for terminal_symbol in self.terminal_symbol_set:
            first_set[terminal_symbol] = { terminal_symbol }

        # 原则2，注意规则1只需要for循环跑一次就可以知道所有的结果，所以无需放入while循环中
        # 若A -> aB，即先求出简单的first集，且求出来的first集不完整
        for left,right_list in self.productions.items():
            result = set()
            for right in right_list:
                if len(right) == 0 or right[0] == "ε":
                    result.add("ε")
                elif right[0] in self.terminal_symbol_set:
                    result.add(right[0])
            first_set[left] = first_set[left].union(result)
        # 规则2 和 规则3，即右部左侧都是非终结符
        # 如果集合大小没有变化，则停止循环
        while first_size != get_first_set_size():
            first_size = get_first_set_size()
            for left,right_list in self.productions.items():
                for right in right_list:
                    if len(right) == 0:
                        continue
                    for c in right:
                        # 规则3的i情况
                        if c in self.nonterminal_symbol_set and "ε" in first_set[c]:
                            # first(c)存在空串，则先把first(c)加入到first[left]中，然后接着继续向下扫描
                            first_set[left] = first_set[left].union(first_set[c])
                            first_set[left].remove("ε")
                            continue
                        elif c in self.nonterminal_symbol_set and "ε" not in first_set[c]:
                            # first(c)不存在空串，则直接把first(c)加入到first[left]，由于本身first(c)不存在空串，所以无需remove空串
                            first_set[left] = first_set[left].union(first_set[c])
                            break
                        elif c in self.terminal_symbol_set:
                            # 如果c是终结符就直接ok了
                            first_set[left].add(c)
                            break
                    
                    # 规则3的ii情况，若右部都是非终结符且这些非终结符都含有空串
                    all_have_empty = True
                    for c in right:
                        if c not in self.nonterminal_symbol_set or "ε" not in first_set[c]:
                            all_have_empty = False
                            break
                    if all_have_empty:
                        first_set[left].add("ε")
        return first_set

    def get_follow_set(self):
        '''
求follow(B)，规则如下
(1)对文法的开始符号 S，置 $ 于FOLOOW（S）中；
(2)若A->aBb 是一个规则，则把FIRST(b)-{ε}加到FOLLOW(B)中；
(3)
    i情况:若A->aB 是一个规则，
    ii情况:A->aBb 是一个规则，而 b=>ε，即ε∈FIRST(b)
    [则把FOLLOW(A)加至FOLLOW(B)中]
(4)反复使用上面的规则，直到每个非终结符的FOLLOW集 不再增大为止。
        '''
        first_set = self.get_first_set()
        follow_set = {}
        follow_set_size = -1
        
        def get_follow_size():
            size = 0
            for left,right_set in follow_set.items():
                size += len(right_set)
            return size
        # 初始化follow_set:
        for nonterminal_symbol in self.nonterminal_symbol_set:
            follow_set[nonterminal_symbol] = set()

        while follow_set_size != get_follow_size():
            follow_set_size = get_follow_size()
            for nonterminal_symbol in self.nonterminal_symbol_set:
                if nonterminal_symbol == self.get_start_symbol():
                    # 规则1
                    follow_set[nonterminal_symbol].add("$")
                for left,right_list in self.productions.items():
                    for right in right_list:
                        if nonterminal_symbol not in right:
                            continue
                        for i in range(len(right)):
                            if right[i] != nonterminal_symbol:
                                continue
                            if i < len(right) - 1:
                                # 规则2
                                next_symbol_position = i + 1
                                new_set = first_set[right[next_symbol_position]].copy()
                                if "ε" in new_set:
                                    new_set.remove("ε")
                                follow_set[nonterminal_symbol] = follow_set[nonterminal_symbol].union(new_set)
                            if i == len(right) - 1:
                                # 规则3 i情况
                                follow_set[nonterminal_symbol] = follow_set[nonterminal_symbol].union(follow_set[left])
                            if i < len(right) - 1 and self.is_nonterminal_symbol_contains_empty(right[i+1]):
                                # 规则3 ii情况
                                follow_set[nonterminal_symbol] = follow_set[nonterminal_symbol].union(follow_set[left])
        return follow_set

    def get_production_right_first_set(self,right):
        if right == "ε" or len(right) == 0:
            return {"ε"}
        elif right[0] in self.terminal_symbol_set:
            return {right[0]}
        elif right[0] in self.nonterminal_symbol_set:
            first_set = self.get_first_set()
            tmp_set = set()
            idx = 0
            while idx < len(right):
                symbol = right[idx]
                if "ε" not in first_set[symbol]:
                    tmp_set = tmp_set.union(first_set[symbol])
                    return tmp_set
                else:
                    tmp_set = tmp_set.union(first_set[symbol])
                    tmp_set.discard("ε")
                    tmp_set.discard("")
                    idx += 1
            return tmp_set.union("ε")
        return {"ε"}

    def get_select_set(self):
        follow_set = self.get_follow_set()
        select_set = {}
        for left in self.productions:
            for right in self.productions[left]:
                right_first_set = self.get_production_right_first_set(right)
                if 'ε' in right_first_set:
                    right_first_set.discard('ε')
                    select_set[(left,right)] = follow_set[left].union(right_first_set)
                else:
                    select_set[(left,right)] = right_first_set
        return select_set

    def get_symbol_from_point_backward(self,item):
        right = item[1]
        point_pos = right.find("·")
        if point_pos >= len(right)-1:
            return ""
        else:
            now_symbol = right[point_pos+1:point_pos+2]
            return now_symbol

    def get_point_next_right(self,item):
        left,right = item
        point_pos = right.find("·")
        symbol = self.get_symbol_from_point_backward(item)
        
        if point_pos >= len(right) - 1 or symbol == '':
            return right
        else:
            return right.replace("·" + symbol,symbol + "·")

    def get_closure_from_symbol(self,symbol):
        looked = [symbol]
        tmp_stack = [symbol]
        closure = set()
        #DFS
        while len(tmp_stack) != 0:
            choose_symbol = tmp_stack.pop()
            for right in self.productions[choose_symbol]:
                if self.is_nonterminal(right[0]) and right[0] not in looked:
                    tmp_stack.append(right[0])
                    looked.append(right[0])
                else:
                    continue
        for choose_symbol in looked:
            for right in self.productions[choose_symbol]:

                closure.add((choose_symbol,"·" + right))
        return closure

    def get_analyses(self):
        def get_now_symbol_set(item_set):
            symbol_set = set()
            for item in item_set:
                symbol = self.get_symbol_from_point_backward(item)
                if symbol != '':
                    symbol_set.add(symbol)
            return symbol_set

        def spawn_new_items_from_item(item_set):
            symbol_set = get_now_symbol_set(item_set)
            return_items = []
            for symbol in symbol_set:
                new_item = set()
                for item in item_set:
                    left,right = item
                    symbol_from_point_backward = self.get_symbol_from_point_backward(item)
                    if symbol_from_point_backward == symbol:
                        new_right = self.get_point_next_right(item)
                        new_item.add((left,new_right))
                        new_symbol_from_point_backward = self.get_symbol_from_point_backward((left,new_right))
                        if new_right != '' and self.is_nonterminal(new_symbol_from_point_backward):
                            for production in self.get_closure_from_symbol(new_symbol_from_point_backward):
                                new_item.add(production)
                    else:
                        continue
                if len(new_item) == 0:
                    continue
                return_items.append((new_item,symbol))
            return return_items
        
        start_item_set = set()
        link_list = {}

        for left,right_list in self.productions.items():
            for right in right_list:
                start_item_set.add((left,'·' + right))
        item_set_list = []
        item_set_list.append(start_item_set)
        item_set_list_size = -1
        while len(item_set_list) != item_set_list_size:
            item_set_list_size = len(item_set_list)
            tmp_item_set_list = item_set_list.copy()
            for item in tmp_item_set_list:
                for new_item,symbol in spawn_new_items_from_item(item):
                    if new_item not in item_set_list:
                        item_set_list.append(new_item)
                    if item_set_list.index(item) not in link_list:
                        link_list[item_set_list.index(item)] = set()
                    link_list[item_set_list.index(item)].add((item_set_list.index(new_item),symbol))
        return (item_set_list,link_list)

    def is_shift_action(self,item_set):
        for left,right in item_set:
            if right[-1] == '·':
                return False
        return True

    def has_reduce_production(self,item_set):
        for left,right in item_set:
            if right[-1] == '·' and left != self.start_symbol:
                return True
        return False

    def is_accept_action(self,item_set):
        for left,right in item_set:
            if left == self.start_symbol and right[-1] == '·':
                return True
        return False

    def get_production_turples(self):
        return_data = []
        for left,right_list in self.productions.items():
            for right in right_list:
                return_data.append((left,right))
        return return_data

    def get_action_and_goto_table(self):
        production_turples = self.get_production_turples()
        item_set_list,link_list = self.get_analyses()
        follow_set = self.get_follow_set()
        goto_table = {}
        action_table = {}
        print(f"link_list: {link_list}")
        for src in link_list:
            for (des,symbol) in link_list[src]:
                if self.is_nonterminal(symbol):
                    goto_table[(src,symbol)] = des

        for terminal_symbol in self.terminal_symbol_set.union("$"):
            for state_idx in range(len(item_set_list)):
                if state_idx in link_list and terminal_symbol != "$":
                    for (des,symbol) in link_list[state_idx]:
                        if symbol == terminal_symbol:
                            if (state_idx,symbol) in action_table:
                                print("s存在冲突!")
                            action_table[(state_idx,symbol)] = f's{des}'

        for terminal_symbol in self.terminal_symbol_set.union("$"):
            for state_idx in range(len(item_set_list)):
                if self.has_reduce_production(item_set_list[state_idx]):
                    if (state_idx,terminal_symbol) in action_table:
                        print("r存在冲突!",f"已有:{action_table[(state_idx,terminal_symbol)]}\t\t",(state_idx,terminal_symbol,item_set_list[state_idx]))
                        continue
                    item_set = item_set_list[state_idx]
                    for left,right in item_set:
                        if right[-1] == '·' and left != self.start_symbol:
                            turple = (left,right.replace("·",""))
                            action_table[(state_idx,terminal_symbol)] = f'r{production_turples.index(turple)}'

        for terminal_symbol in self.terminal_symbol_set.union("$"):
            for state_idx in range(len(item_set_list)):
                if self.is_accept_action(item_set_list[state_idx]):
                    if (state_idx,terminal_symbol) in action_table:
                        print("r存在冲突!",f"已有:{action_table[(state_idx,terminal_symbol)]}\t\t",(state_idx,terminal_symbol,item_set_list[state_idx]))
                    action_table[(state_idx,terminal_symbol)] = '$'
        return (production_turples,goto_table,action_table,item_set_list,link_list)

    def dump_goto_action_table(self,argv):
        (production_turples,goto_table,action_table,item_set_list) = argv
        idx = 0
        print(f"item_set_list: {item_set_list}")
        for item_set in item_set_list:
            print(f"{idx}. {item_set}")
            idx += 1
        idx = 0
        for left,right in production_turples:
            print(f"{idx}. {left} -> {right}")
            idx += 1
        tb = PrettyTable()
        field_names = ['state']
        terminal_symbol_list = ["$"]
        nonterminal_symbol_list = []
        for terminal_symbol in self.terminal_symbol_set:
            terminal_symbol_list.append(terminal_symbol)
            

        for nonterminal_symbol in self.nonterminal_symbol_set:
            if nonterminal_symbol != self.start_symbol:
                nonterminal_symbol_list.append(nonterminal_symbol)
        
        terminal_symbol_list = sorted(terminal_symbol_list)
        nonterminal_symbol_list = sorted(nonterminal_symbol_list)

        for terminal_symbol in terminal_symbol_list:
            field_names.append(terminal_symbol)
        for nonterminal_symbol in nonterminal_symbol_list:
            field_names.append(nonterminal_symbol)

        tb.field_names = field_names
        for idx in range(len(item_set_list)):
            row = [idx]
            for terminal_symbol in terminal_symbol_list:
                if (idx,terminal_symbol) in action_table:
                    row.append(action_table[(idx,terminal_symbol)])
                else:
                    row.append("")
            for nonterminal_symbol in nonterminal_symbol_list:
                if (idx,nonterminal_symbol) in goto_table:
                    row.append(goto_table[(idx,nonterminal_symbol)])
                else:
                    row.append("")
            tb.add_row(row)
        print(tb)
        return tb

    def check(self,str):
        def get_next_symbol(s):
            if len(s) > 0:
                next_char = s[0]
                remain_str = s[1:]
            else:
                next_char = '$'
                remain_str = ''
            return (next_char,remain_str)
        production_turples,goto_table,action_table,item_set_list,link_list = self.get_action_and_goto_table()
        self.dump_goto_action_table((production_turples,goto_table,action_table,item_set_list))
        symbol_stack = '$'
        state_stack = [0]
        input_str = str+'$'
        print(f"goto_table: {goto_table}")
        print(f"action_table: {action_table}")
        data = ''
        while True:
            now_state = state_stack[len(state_stack) - 1]
            symbol,input_str = get_next_symbol(input_str)
            if (now_state,symbol) in action_table and action_table[(now_state,symbol)][0] == 's':
                symbol_stack += symbol
                state_idx = int(action_table[(now_state,symbol)][1:],10)
                state_stack.append(state_idx)
                #print(f"移进{state_idx}")
            elif (now_state,symbol) in action_table and action_table[(now_state,symbol)][0] == 'r':
                #print(f"规约 {action_table[(now_state,symbol)]}")
                production_idx = int(action_table[(now_state,symbol)][1:],10)
                production = production_turples[production_idx]
                left,right = production
                symbol_stack = symbol_stack[:len(symbol_stack) - len(right)]
                symbol_stack += left
                for i in range(len(right)):
                    state_stack.pop()
                now_state = state_stack[len(state_stack) - 1]
                state_stack.append(goto_table[(now_state,left)])
                input_str = symbol + input_str
            elif symbol == "$" and  (now_state,symbol) in action_table and action_table[(now_state,symbol)][0] == '$':
                print("success!")
                return True
            else:
                print(f"state_stack: {state_stack}")
                print(f"symbol_stack: {symbol_stack}")
                print("failed!")
                return False
            #print(f"state_stack: {state_stack}")
            print(f"symbol_stack: {symbol_stack}")
            #print(f"symbol: {symbol}")
            #print(f"input: {input_str}\n\n")

        
    def get_lr(self,tokens):
        def get_next_symbol(s):
            if len(s) > 0:
                next_char = s[0]
                remain_str = s[1:]
            else:
                next_char = '$'
                remain_str = ''
            return (next_char,remain_str)
        str = self.t2s(tokens)
        production_turples,goto_table,action_table,item_set_list,link_list = self.get_action_and_goto_table()
        self.dump_goto_action_table((production_turples,goto_table,action_table,item_set_list))
        symbol_stack = '$'
        state_stack = [0]
        input_str = str + '$'
        print(f"goto_table: {goto_table}")
        print(f"action_table: {action_table}")
        while True:
            now_state = state_stack[len(state_stack) - 1]
            symbol,input_str = get_next_symbol(input_str)
            print((now_state,symbol) in action_table)
            if (now_state,symbol) in action_table and action_table[(now_state,symbol)][0] == 's':
                symbol_stack += symbol

                state_idx = int(action_table[(now_state,symbol)][1:],10)
                state_stack.append(state_idx)

                print(f"移进{state_idx}")
            elif (now_state,symbol) in action_table and action_table[(now_state,symbol)][0] == 'r':
                print(f"规约 {action_table[(now_state,symbol)]}")
                production_idx = int(action_table[(now_state,symbol)][1:],10)
                production = production_turples[production_idx]
                left,right = production
                symbol_stack = symbol_stack[:len(symbol_stack) - len(right)]
                symbol_stack += left

                
                #token_stack.append(tmp_tokens.pop(0))

                for i in range(len(right)):
                    state_stack.pop()
                
                now_state = state_stack[len(state_stack) - 1]
                state_stack.append(goto_table[(now_state,left)])
                input_str = symbol + input_str
            elif symbol == "$" and  (now_state,symbol) in action_table and action_table[(now_state,symbol)][0] == '$':
                print("success!")
                return True
            else:
                print("failed!")
                return False
            #print(f"state_stack: {state_stack}")
            print(f"symbol_stack: {symbol_stack}")
            #print(f"symbol: {symbol}")
            #print(f"input: {input_str}\n\n")

    # token to grammer stream
    def t2s(self,tokens):
        grammer_stream = ''
        for item in tokens:
            if item.type == "KEYWORD":
                if item.value == "func":
                    grammer_stream += "f"
                else:
                    grammer_stream += "k"
            elif item.type == 'IDENTIFIER':
                grammer_stream += "i"
            elif item.type == 'POSTFIX_OPERATORS':
                grammer_stream += item.value
            elif item.type == "MISC_OPERATORS":
                grammer_stream += item.value
            elif item.type == 'LEFT_BRACE' or item.type == 'RIGHT_BRACE':
                grammer_stream += item.value
            elif item.type == 'STRING':
                grammer_stream += 's'
            elif item.type == 'END_MARK':
                grammer_stream += ';'
            elif item.type == "INT":
                grammer_stream += 'n'
            elif item.value == '+':
                grammer_stream += "+"
            elif item.value == '-':
                grammer_stream += "-"
            elif item.value == '*':
                grammer_stream += "*"
            elif item.value == '/':
                grammer_stream += "/"
            elif item.value == '=':
                grammer_stream += "="
            elif item.value == '%':
                grammer_stream += "%"
        return grammer_stream





class Parser(object):
    def __init__(self):
        code = '''
G -> S
S -> fi():k{E}S
S -> fi():k{E}
S -> fi():k{}S
S -> fi():k{}
E -> i;
E -> i=T;
E -> i=T;E
E -> i(A);E
E -> i(A);
E -> i();
E -> i();E
T -> (F)
T -> (F+F)
T -> F+F
T -> (F-F)
T -> F-F
T -> (F*F)
T -> F*F
T -> (F/F)
T -> T/T
T -> F
F -> n
F -> i
A -> A,A
A -> i
A -> n
A -> s
        '''
        productions = CFG.str2productions(code)
        print(productions)
        nonterminal_symbol_set = {"G","S","A",'E',"T","F","C"}
        terminal_symbol_set = {'f','k',":","t","{","}","=","i","(",")","+",";",'i',"-","*","/",",","n","s"}
        start_symbol = "G"
        cfg = CFG(nonterminal_symbol_set,terminal_symbol_set,productions,start_symbol)
        self.cfg = cfg
        self.glibc_function_set = {'puts':'i8*',"printf":'i8*, ...','write':'i32,i8*,i32','read':'i32,i8*,i32','open':"i8*,i32"}

    def get_grammer_stream(self):
        return self.grammer_stream

    # token to grammer stream
    def t2s(tokens):
        grammer_stream = ''
        for item in tokens:
            if item.type == "KEYWORD":
                if item.value == "func":
                    grammer_stream += "f"
                else:
                    grammer_stream += "k"
            elif item.type == 'IDENTIFIER':
                grammer_stream += "i"
            elif item.type == 'POSTFIX_OPERATORS':
                grammer_stream += item.value
            elif item.type == "MISC_OPERATORS":
                grammer_stream += item.value
            elif item.type == 'LEFT_BRACE' or item.type == 'RIGHT_BRACE':
                grammer_stream += item.value
            elif item.type == 'STRING':
                grammer_stream += 's'
            elif item.type == 'END_MARK':
                grammer_stream += ';'
            elif item.type == "INT":
                grammer_stream += 'n'
            elif item.value == '+':
                grammer_stream += "+"
            elif item.value == '-':
                grammer_stream += "-"
            elif item.value == '*':
                grammer_stream += "*"
            elif item.value == '/':
                grammer_stream += "/"
            elif item.value == '=':
                grammer_stream += "="
            elif item.value == '%':
                grammer_stream += "%"
        return grammer_stream

    def check_grammer(self,tokens):
        stream = self.t2s(tokens)

    def get_lr(self,tokens):
        STATUS_FUNC_ENTER = 1
        STATUS_FUNC_ENTER_LEFT = 2
        STATUS_FUNC_ENTER_RIGHT = 3
        STATUS_FUNC_OUT   = 3

        lr_code = ''
        status = STATUS_FUNC_OUT
        str_table = {}
        declare_funcion_list = set()
        variable_dict = {}
        function_num = 0
        while len(tokens) > 0:
            token = tokens.pop(0)
            function_name = ''
            return_type = 'i32'
            function_argv = []
            
            if token.value == "func" and token.type == 'KEYWORD':
                
                status = STATUS_FUNC_ENTER
                token = tokens.pop(0)
                if token.type == 'IDENTIFIER':
                    function_name = token.value
                
                token = tokens.pop(0)
                
                if token.type == "POSTFIX_OPERATORS" and token.value == "(":
                    token = tokens.pop(0)
                    
                    while (token.type == "POSTFIX_OPERATORS" and token.value == ")") == False:
                        if token.value == ',' or (token.value == "POSTFIX_OPERATORS" and token.type == ")"):
                            continue
                        else:
                            function_argv.append(token.value)
                        token = tokens.pop(0)
                token = tokens.pop(0)
                
                if token.value == ':' and token.type == 'MISC_OPERATORS':
                    pass
                token = tokens.pop(0)
                if (token.value == "int" and token.type == "KEYWORD") or (token.value == "void" and token.type == "KEYWORD"):
                    return_type = 'i32'


                lr_code += f"define {return_type} @{function_name}() #{function_num} "
                function_num += 1
                token = tokens.pop(0)
                
                if token.type == 'LEFT_BRACE' and status == STATUS_FUNC_ENTER and token.value == '{':
                    
                    lr_code += "{\n"
                    status = STATUS_FUNC_ENTER_LEFT


                    token = tokens.pop(0)
                    variable_idx = 1
                    while token.value != "}" and token.type != "RIGHT_BRACE":
                        
                        tmp_name = ''
                        if token.type == 'IDENTIFIER':
                            tmp_name = token.value
                            if tmp_name in self.glibc_function_set:
                                declare_funcion_list.add(f"declare i32 @{tmp_name}({self.glibc_function_set[tmp_name]}) #1")
                        token = tokens.pop(0)
                        #说明这里是函数调用
                        if token.type == 'POSTFIX_OPERATORS':
                            call_argv = []
                            tmp_variable_dict = {}
                            while (token.type == "POSTFIX_OPERATORS" and token.value == ")") == False:
                                token = tokens.pop(0)
                                if token.value == ',' or (token.type == "POSTFIX_OPERATORS" and token.value == ")"):
                                    continue
                                else:
                                    call_argv.append(token)
                            for argv_idx in range(len(call_argv)):
                                argv = call_argv[argv_idx]
                                if argv.type == "IDENTIFIER":
                                    tmp_variable_dict[variable_dict[argv.value]] = f"%{variable_idx}"
                                    lr_code += f'    %{variable_idx} = load i64, i64* {variable_dict[argv.value]}, align 8' + "\n"
                                    variable_idx += 1
                            if tmp_name in self.glibc_function_set and self.glibc_function_set[tmp_name].find("...") != -1:
                                lr_code += f'    call i32 ({self.glibc_function_set[tmp_name]}) @{tmp_name}('
                            else:
                                lr_code += f'    call i32 @{tmp_name}('
                            variable_idx += 1
                            for argv_idx in range(len(call_argv)):
                                argv = call_argv[argv_idx]
                                if argv.type == "STRING":
                                    new_str = argv.value[:-1] + '\\00"'
                                    str_table[f".str.{len(str_table)}"] = f'private unnamed_addr constant [{len(argv.value)-1} x i8] c{new_str}, align 1'
                                    lr_code += f"i8* getelementptr inbounds ([{len(argv.value)-1} x i8], [{len(argv.value)-1} x i8]* @.str.{len(str_table)-1}, i64 0, i64 0)"
                                if argv.type == "INT":
                                    lr_code += f"i64 {argv.value}"
                                if argv.type == "IDENTIFIER":
                                    
                                    lr_code += f"i64 {tmp_variable_dict[variable_dict[argv.value]]}"
                                    
                                if len(call_argv) -1 != argv_idx:
                                    lr_code += ','
                            lr_code += ')\n'
                        elif token.type == "ASSIGNMENT_OPERATORS": #说明这里是赋值
                            next_token = tokens.pop(0)
                            follow_token = tokens.pop(0)
                            if follow_token.value == ";":
                                if tmp_name not in variable_dict:
                                    lr_code += f"    %{variable_idx} = alloca i64, align 8" + "\n"
                                    variable_dict[tmp_name] = f"%{variable_idx}"
                                    variable_idx += 1
                                
                                if next_token.type == "IDENTIFIER" and next_token.value in variable_dict:
                                    lr_code += f'    store i64 %{variable_dict[next_token.value]}, i64* %{variable_idx-1}, align 8' + "\n"
                                    continue
                                    
                                elif next_token.type == "INT":
                                    lr_code += f'    store i64 {next_token.value}, i64* %{variable_idx-1}, align 8' + "\n"
                                    continue
                                else:
                                    print("failed!")
                                    print(f"at: {next_token.value}{follow_token.value}")
                                    exit(0)
                            operation_dict = {"+":"add","-":"sub","*":"mul","/":"sdiv"}
                            if follow_token.value in operation_dict:
                                operation_symbol = follow_token.value

                                follow_token = tokens.pop(0)

                                if next_token.type == "IDENTIFIER":
                                    lr_code += f'    %{variable_idx} = load i64, i64* {variable_dict[next_token.value]}, align 8' + "\n"
                                    variable_idx += 1
                                elif next_token.type == "INT":
                                    lr_code += f"    %{variable_idx} = add nsw i64 0, {next_token.value}" + '\n'
                                    variable_idx += 1
                                else:
                                    print("failed!")
                                    print(f"at: {next_token.value}{follow_token.value}")
                                if follow_token.type == "IDENTIFIER":
                                    lr_code += f'    %{variable_idx} = load i64, i64* {variable_dict[follow_token.value]}, align 8' + "\n"
                                    variable_idx += 1
                                elif follow_token.type == "INT":
                                    lr_code += f"    %{variable_idx} = add nsw i64 0, {follow_token.value}" + '\n'
                                    variable_idx += 1
                                else:
                                    print("failed!")
                                    print(f"at: {next_token.value}{follow_token.value}")
                                if operation_symbol != "/":
                                    lr_code += f'    %{variable_idx} = {operation_dict[operation_symbol]} nsw i64  %{variable_idx-2}, %{variable_idx-1}' + "\n"
                                    variable_idx += 1
                                else:
                                    lr_code += f'    %{variable_idx} = sdiv i64  %{variable_idx-2}, %{variable_idx-1}' + "\n"
                                    variable_idx += 1
                                lr_code += f'    store i64 %{variable_idx-1}, i64* {variable_dict[tmp_name]}, align 8' + "\n"


                            # todo
                    lr_code += "\n    ret i32 0\n}\n\n"
        for str_name,str_value in str_table.items():
            lr_code = f"@{str_name} = {str_value}\n" + lr_code
        for declare_funcion in declare_funcion_list:
            lr_code += f"{declare_funcion}\n\n"
        print(lr_code)
        return lr_code
    def check(self,programmer_code):

        return self.cfg.check(programmer_code)
    def get_ir_headers(self,filename):
        lr_code_header = ''
        lr_code_header += f"; ModuleID = '{filename}'" + "\n"
        lr_code_header += f'source_filename = "{filename}"' + "\n"
        lr_code_header += 'target datalayout = "e-m:o-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"' + "\n"
        return lr_code_header
def main():

    code = '''
    G -> S
    S -> A
    S -> i=A
    A -> (A)
    A -> (A+A)
    A -> A+A
    A -> i
    '''
    
    productions = CFG.str2productions(code)
    print(productions)
    '''
    productions = CFG.str2productions(code)
    print(productions)
    nonterminal_symbol_set = {"G","S","E"}
    terminal_symbol_set = {'i',"+"}
    start_symbol = "G"
    cfg = CFG(nonterminal_symbol_set,terminal_symbol_set,productions,start_symbol)
    production_turples,goto_table,action_table,item_set_list,link_list = cfg.get_action_and_goto_table()
    cfg.check("i+ii")
    '''
if __name__ == "__main__":
    main()


