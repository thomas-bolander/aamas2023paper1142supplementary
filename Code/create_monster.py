from itertools import chain, combinations
import os

def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

# edges for a or b?
edges_for_a = True
if edges_for_a:
    attention_string = 'h_a'
else:
    attention_string = 'h_b'

# everything should be written to a file
# open file
f = open("nodes_and_edges.tex", "w")

# construct empty set  E, set of nodes
E = set()
# set counter to 0
i = 0
# for every subset S of {p,g}
for S in powerset({'p','g'}):
    # pick a subset Xa of S
    for Xa in powerset(S):
        # pick a subset Xb of S
        for Xb in powerset(S):
            ## print S, Xa, Xb
            #print("S: ", list(S))
            #print("Xa:", list(Xa))
            #print("Xb: ", list(Xb))
            #print()
            # increase counter
            i += 1
            # create empty set X, a node
            X = set()
            # create coordinates for X, starting at (0,0)
            x = 0
            y = 0
            # add S to X
            X = X.union(S)
            # for each element r in Xa, add 'h_ar' to X
            for element in Xa:
                X.add('h_a'+element)
            # for each element in r in S - Xa, add '\neg h_ar' to X
            for element in set(S).difference(Xa):
                X.add('\\neg h_a'+element)
                # test whether element is p or g
                if element == 'p':
                    y -= 2
                elif element == 'g':
                    y -= 1
            # for each element r in Xb, add 'h_br' to X
            for element in Xb:
                X.add('h_b'+element)
            # for each element r in S - Xb, add '\neg h_br' to X
            for element in set(S).difference(Xb):
                X.add('\\neg h_b'+element)
                if element == 'g':
                    x += 2
                elif element == 'p':
                    x += 1
            # if  p or g is not in X, compute coordinates differently
            if not 'p' in X or not 'g' in X:
                if 'p' in X:   
                    x = 0.5
                if 'g' in X:
                    x = 2.5
                y = -5
                if '\\neg h_ap' in X or '\\neg h_ag' in X:
                    y -= 2
                if '\\neg h_bp' in X or '\\neg h_bg' in X:
                    y -= 1
            if not 'p' in X and not 'g' in X:
                x = 2
                y = -10
            E.add((i,(x,y),frozenset(X)))
# place nodes by printing \node tikz command for each element in E
for i, (x,y), element in E:
    f.write("\\node[draw] ("+str(i)+") at ("+str(x)+","+str(y)+") {$")
    # turn element into list to be able to iterate over it
    element = list(element)
    # for each literal in element
    for literal in element[:-1]:
            f.write(literal+"\land ")
    # for last literal in element, if it exists
    if len(element) > 0:
        f.write(element[-1])
    f.write("$};\n")   
# draw edges satisfying attentiveness and inertia
# count how many edges in total
no_edges = 0
for agent in {'a','b'}:
    # set color to red if agent is a, blue if agent is b
    if agent == 'a':
        color = 'red'
    else:
        color = 'blue'
    # start of edge
    for i, (x,y), element in E:
        # end of edge
        for j, (x2,y2), element2 in E:
            # set add edge to false
            add_edge = True
            # Attentiveness and Inertia has to hold for all r in {p,g}
            for r in {'p','g'}:
                # Attentiveness:
                # h_ir in element implies that h_ir and r in element2, where i is the agent
                if 'h_'+agent+r in element and not 'h_'+agent+r in element2:
                    add_edge = False
                if 'h_'+agent+r in element and not r in element2: 
                    add_edge = False
                # Inertia:
                # h_ar not in element implies r not in element2
                if not 'h_'+agent+r in element and r in element2:
                    add_edge = False
            # draw edge is add_edge is true
            if add_edge:
                no_edges += 1
                # if not loop, draw normal edge
                if i != j:
                    f.write("\\draw[-latex,"+color+"] ("+str(i)+") to ("+str(j)+");\n")
                # if loop, draw loop
                else:
                    f.write("\\draw[-latex,"+color+"] ("+str(i)+") edge [loop above,>=latex] ();\n")
f.close()
os.system('pdflatex monster_tikz')