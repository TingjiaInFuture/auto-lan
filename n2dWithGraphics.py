# If "graphviz" is undefined:
#I. Install graphviz: https://graphviz.org/download/, download graphviz-11.0.0 (64-bit) EXE installer [sha256] (windows)
#II. Install python graphviz: pip install graphviz
from graphviz import Digraph
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

def nfa_to_dfa(nfa,q0):
    initial_state = epsilon_closure(nfa, q0)
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

def dict_to_tuple(dfa_dict):
    Q = set(frozenset(eval(q)) for q in dfa_dict.keys())
    Σ = set(next(iter(dfa_dict.values())).keys())
    δ = {}
    for state, transitions in dfa_dict.items():
        for symbol, next_state in transitions.items():
            δ[frozenset(eval(state)), symbol] = frozenset(eval(next_state))
    q0 = next(iter(Q))
    F = {state for state in Q if any(next_state in Q for next_state in dfa_dict[str(state)].values())}
    DFA2Graph(dfa_dict,q0,F)
    return Q, Σ, δ, q0, F

def DFA2Graph (dfa,q0,F):
    # 传入字典dfa
    dot = Digraph(comment='输出的DFA图示')
    # q0 = str(q0).replace("frozenset", "").replace("(", "").replace(")", "")
    # for q in F:
    #     q = str(q).replace("frozenset", "").replace("(", "").replace(")", "")
    # print(type(q0))
    # print(type(F))
    # print(type(F[0]))
    for outer_key in dfa:
        # print(type(outer_key))
        outer_key_name = outer_key.replace("frozenset", "").replace("(", "").replace(")", "")
        # dot.node(outer_key_name)
        if outer_key == str(q0):
            # 创建一个不可见的节点
            dot.node('start', shape='none')
            # 添加一个指向起始节点的边
            dot.edge('start', outer_key_name)
        if frozenset(outer_key) in F:
            # 使用双圈框住节点
            dot.node(outer_key_name, shape='doublecircle')
        else:
            # 添加外关键字节点
            dot.node(outer_key_name)
        for inner_key, inner_value in dfa[outer_key].items():
            # 添加内关键字值节点
            inner_value_name = inner_value.replace("frozenset", "").replace("(", "").replace(")", "")
            # dot.node(inner_value_name)
            # 添加边，边的标签为内关键字
            if frozenset(inner_value) in F:
                # 使用双圈框住节点
                dot.node(inner_value_name, shape='doublecircle')
            else:
                # 添加内关键字值节点
                dot.node(inner_value_name)
            dot.edge(outer_key_name, inner_value_name, label=inner_key)
    dot.render('./output/dfa_graph', view=True,cleanup=True)
    return

def NFA2Graph (nfa,q0,F):
    dot = Digraph(format='pdf')

    # 遍历外关键字
    for outer_key in nfa:
        # 添加外关键字节点
        if outer_key == q0:
            # 创建一个不可见的节点
            dot.node('start', shape='none')
            # 添加一个指向起始节点的边
            dot.edge('start', str(outer_key), shape='circle')
        if outer_key in F:
            # 使用双圈框住节点
            dot.node(str(outer_key), shape='doublecircle')
        else:
            # 添加外关键字节点
            dot.node(str(outer_key))
        # 遍历内关键字和值
        for inner_key, inner_values in nfa[outer_key].items():
            # 内关键字的值是一个集合，我们需要为集合中的每一个元素创建一个节点
            for inner_value in inner_values:
                # 检查是否在集合F中
                if inner_value in F:
                    # 使用双圈框住节点
                    dot.node(str(inner_value), shape='doublecircle')
                else:
                    # 添加内关键字值节点
                    dot.node(str(inner_value), shape='circle')
                # 添加边，边的标签为内关键字
                dot.edge(str(outer_key), str(inner_value), label=inner_key)

    # 渲染为PDF文件并保存在output文件夹
    dot.render('output/nfa_graph', view=True,cleanup=True)

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
    NFA2Graph (nfa,q0,F)

    # 将NFA转换为DFA
    dfa = nfa_to_dfa(nfa,q0)
    print("DFA:")
    print(dfa)

    # 将字典形式的DFA转换回五元组形式
    dfa_tuple = dict_to_tuple(dfa)
    print("DFA(五元组形式）:")
    print(dfa_tuple)

if __name__ == "__main__":
    main()
