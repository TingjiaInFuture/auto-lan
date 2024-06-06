def nfa_to_dfa(nfa, initial_state):
    initial_state = set([initial_state])
    dfa = {str(initial_state): {}}
    unmarked = [initial_state]

    while unmarked:
        T = unmarked.pop()
        for _input in nfa[0].keys():
            U = set()
            for state in T:
                if state in nfa and _input in nfa[state]:
                    U = U.union(nfa[state][_input])
            U = frozenset(U)
            if str(U) not in dfa.keys() and U:
                dfa[str(U)] = {}
                unmarked.append(U)
            if U:
                dfa[str(T)][_input] = str(U)

    return dfa

def tuple_to_dict(nfa_tuple):
    Q, Σ, δ = nfa_tuple
    nfa_dict = {}
    for state in Q:
        nfa_dict[state] = {}
        for symbol in Σ:
            if (state, symbol) in δ:
                nfa_dict[state][symbol] = δ[state, symbol]
    return nfa_dict

def dict_to_tuple(dfa_dict):
    Q = set(frozenset(eval(q)) for q in dfa_dict.keys())  # 先将集合转换为frozenset
    Σ = set(next(iter(dfa_dict.values())).keys())
    δ = {}
    for state, transitions in dfa_dict.items():
        for symbol, next_state in transitions.items():
            δ[frozenset(eval(state)), symbol] = frozenset(eval(next_state))  # 将集合转换为frozenset
    return Q, Σ, δ

def main():
    # 从命令行接收五元组
    Q = set(eval(input("请输入状态集Q(例如:{0, 1, 2}):")))
    Σ = set(eval(input("请输入字母表Σ(例如:{'a', 'b'}):")))
    δ = eval(input("请输入转移函数δ(例如:{(0, 'a'): {0, 1}, (0, 'b'): {0}, (1, 'a'): {2}, (1, 'b'): {2}, (2, 'a'): {2}, (2, 'b'): {2}}):"))
    q0 = int(input("请输入初始状态q0(例如:0):"))
    F = set(eval(input("请输入接受状态集F(例如:{2}):")))

    # 将五元组转换为字典形式的NFA
    nfa = tuple_to_dict((Q, Σ, δ))
    print("NFA:")
    print(nfa)


    # 将NFA转换为DFA
    dfa = nfa_to_dfa(nfa, q0)
    print("DFA:")
    print(dfa)

    # DFA 的终止状态集合初始化为空
    dF = set()

    # 遍历 DFA 的每个状态
    for state in dfa:
        # 将状态从字符串转换回集合
        state_set = eval(state)
        # 如果该状态集合与 NFA 的终止状态集合有交集
        if state_set & F:
            # 那么这个状态就是 DFA 的一个终止状态
            dF.add(frozenset(state_set))


    # 将字典形式的DFA转换回五元组形式
    dfa_tuple = dict_to_tuple(dfa)
    print("DFA(五元组形式）:")
    print((dfa_tuple[0], dfa_tuple[1], dfa_tuple[2], {q0}, dF))


if __name__ == "__main__":
    main()
