from graphviz import Digraph

dot = Digraph()
q0 = 'Move\nStart'
q1 = 'Pawn\nMove'
q2 = 'End\nRank'
q3 = 'Check\nor\nMate'
q4 = 'Piece'
q5 = 'Piece\nfile'
q6 = 'Rank\nDisamb.'
q7 = 'Piece\nCapture'
dot.node(q0, q0)
dot.node(q1, q1)
dot.node(q2, q2, shape='doublecircle')
dot.node(q3, q3, shape='doublecircle')
dot.node(q4, q4)
dot.node(q5, q5)
dot.node(q6, q6)
dot.node(q7, q7)

dot.edge(q0, q1, label='F, $→F')
dot.edge(q1, q2, label='r, F→r\nx, F→x')
dot.edge(q2, q2, label='r, F→r\nr, x→r\nε, r→ε\nε, ε→ε')
dot.edge(q2, q3, label='#, r→#\n+, r→+')
dot.edge(q3, q3, label='ε, #→ε\nε, +→ε\nε, ε→ε')

dot.edge(q0, q4, label='P, $→P')
dot.edge(q4, q5, label='F, P→F')
dot.edge(q5, q2, label='r, P→r\nF, F→F')
dot.edge(q4, q6, label='r, P→r')
dot.edge(q5, q6, label='r, F→r')
dot.edge(q6, q2, label='F, r→F')
dot.edge(q6, q7, label='x, r→x')
dot.edge(q7, q2, label='F, x→F')

dot.render('pda_diagram', format='png')
