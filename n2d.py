def epsilon_closure(nfa, state):
    """
    Computes the epsilon closure of a state in the NFA.
    """
    stack = [state]
    closure = {state}

    while stack:
        current = stack.pop()
        if 'ε' in nfa[current]:
            for next_state in nfa[current]['ε']:
                if next_state not in closure:
                    closure.add(next_state)
                    stack.append(next_state)

    return closure

def epsilon_closure_of_set(nfa, state_set):
    """
    Computes the epsilon closure of a set of states in the NFA.
    """
    closure = set()
    for state in state_set:
        closure.update(epsilon_closure(nfa, state))
    return closure

def nfa_to_dfa(nfa, start_state):
    initial_state = epsilon_closure(nfa, start_state)
    dfa = {str(frozenset(initial_state)): {}}
    unmarked = [frozenset(initial_state)]


    while unmarked:
        T = unmarked.pop()
        T_closure = epsilon_closure_of_set(nfa, T)
        for _input in set(sum((list(nfa[state].keys()) for state in T_closure if state in nfa), [])):
            if _input == 'ε':
                continue
            U = set()
            for state in T_closure:
                if state in nfa and _input in nfa[state]:
                    U.update(nfa[state][_input])
            U = frozenset(epsilon_closure_of_set(nfa, U))
            if str(U) not in dfa:
                dfa[str(U)] = {}
                unmarked.append(U)
            dfa[str(frozenset(T_closure))][_input] = str(U)
    return dfa

def tuple_to_dict(nfa_tuple):
    Q, Σ, δ, q0, F = nfa_tuple
    nfa_dict = {state: {} for state in Q}
    for (state, symbol), next_states in δ.items():
        if symbol not in nfa_dict[state]:
            nfa_dict[state][symbol] = set()
        nfa_dict[state][symbol].update(next_states)
    return nfa_dict

def dict_to_tuple(dfa_dict, nfa_final_states):
    Q = set(frozenset(eval(q)) for q in dfa_dict.keys())
    Σ = set(next(iter(dfa_dict.values())).keys())
    δ = {}
    for state, transitions in dfa_dict.items():
        for symbol, next_state in transitions.items():
           δ[frozenset(eval(state)), symbol] = frozenset(eval(next_state))
    q0 = next(iter(Q))
    F = {state for state in Q if any(nfa_final_state in state for nfa_final_state in nfa_final_states)}
    return Q, Σ, δ, q0, F

def main():
    # 从命令行接收五元组
    Q = set(eval(input("请输入状态集Q(例如:{0, 1, 2}):")))
    Σ = set(eval(input("请输入字母表Σ(例如:{'a', 'b', 'ε'}):")))
    δ = eval(input("请输入转移函数δ(例如:{(0, 'a'): {0, 1}, (0, 'ε'): {1}, (1, 'b'): {2}, (2, 'a'): {2}, (2, 'b'): {2}}):"))
    q0 = int(input("请输入初始状态q0(例如:0):"))
    F = set(eval(input("请输入接受状态集F(例如:{2}):")))

    # 将五元组转换为字典形式的NFA
    nfa = tuple_to_dict((Q, Σ, δ, q0, F))
    print("NFA:")
    print(nfa)

    # 将NFA转换为DFA
    dfa = nfa_to_dfa(nfa, q0)
    print("DFA:")
    print(dfa)

    # 将字典形式的DFA转换回五元组形式
    dfa_tuple = dict_to_tuple(dfa, F)
    print("DFA(五元组形式）:")
    print(dfa_tuple)

if __name__ == "__main__":
    main()