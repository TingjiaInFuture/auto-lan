def nfa_to_dfa(nfa):
    initial_state = set([0])
    dfa = {str(initial_state): {}}
    unmarked = [initial_state]

    while unmarked:
        T = unmarked.pop()
        for _input in nfa[0].keys():
            U = set()
            for state in T:
                if _input in nfa[state].keys():
                    U = U.union(nfa[state][_input])
            if str(U) not in dfa.keys() and U:
                dfa[str(U)] = {}
                unmarked.append(U)
            if U:
                dfa[str(T)][_input] = U

    return dfa

def main():
    nfa = {0: {'a': {0, 1}, 'b': {0}}, 1: {'a': {2}, 'b': {2}}, 2: {'a': {2}, 'b': {2}}}
    print("NFA:")
    print(nfa)
    dfa = nfa_to_dfa(nfa)
    print("DFA:")
    print(dfa)

if __name__ == "__main__":
    main()
