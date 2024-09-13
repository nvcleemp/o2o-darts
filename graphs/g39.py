import re
import random

vs = """node [circle,fill] (39) at (99.999999,6.701743) {};
node [circle,fill] (38) at (71.644076,23.034854) {};
node [circle,fill] (37) at (74.583765,11.559970) {};
node [circle,fill] (36) at (83.042014,26.334316) {};
node [circle,fill] (35) at (60.024594,16.433337) {};
node [circle,fill] (34) at (71.575655,36.393342) {};
node [circle,fill] (33) at (0.000000,6.695767) {};
node [circle,fill] (32) at (28.367027,23.144807) {};
node [circle,fill] (31) at (25.573286,11.593314) {};
node [circle,fill] (30) at (16.978314,26.377286) {};
node [circle,fill] (29) at (40.012369,16.482146) {};
node [circle,fill] (28) at (28.472152,36.532161) {};
node [circle,fill] (27) at (50.000029,93.304233) {};
node [circle,fill] (26) at (50.075697,60.536518) {};
node [circle,fill] (25) at (58.624917,68.646558) {};
node [circle,fill] (24) at (41.541451,68.852709) {};
node [circle,fill] (23) at (61.597962,53.695805) {};
node [circle,fill] (22) at (38.570107,53.881872) {};
node [circle,fill] (21) at (50.006505,19.577422) {};
node [circle,fill] (20) at (36.165250,43.612951) {};
node [circle,fill] (19) at (63.879380,43.505215) {};
node [circle,fill] (18) at (57.066426,32.058418) {};
node [circle,fill] (17) at (60.922851,35.818503) {};
node [circle,fill] (16) at (57.525123,27.413424) {};
node [circle,fill] (15) at (56.900582,36.896267) {};
node [circle,fill] (14) at (53.069902,28.788081) {};
node [circle,fill] (13) at (43.644615,31.584904) {};
node [circle,fill] (12) at (44.307842,26.606245) {};
node [circle,fill] (11) at (39.336066,34.435159) {};
node [circle,fill] (10) at (47.950776,28.697605) {};
node [circle,fill] (9) at (43.013285,36.570090) {};
node [circle,fill] (8) at (54.378653,45.176658) {};
node [circle,fill] (7) at (45.243441,45.061915) {};
node [circle,fill] (6) at (49.772947,43.064409) {};
node [circle,fill] (5) at (54.220829,41.043553) {};
node [circle,fill] (4) at (45.365515,40.876422) {};
node [circle,fill] (3) at (51.943108,34.343161) {};
node [circle,fill] (2) at (48.294703,34.340963) {};
node [circle,fill] (1) at (49.977412,37.583119) {};""".split("\n")

es = """draw [black] (39) to (27);
draw [black] (39) to (33);
draw [black] (39) to (37);
draw [black] (39) to (36);
draw [black] (38) to (34);
draw [black] (38) to (36);
draw [black] (38) to (37);
draw [black] (38) to (35);
draw [black] (37) to (35);
draw [black] (37) to (36);
draw [black] (36) to (34);
draw [black] (35) to (21);
draw [black] (35) to (34);
draw [black] (34) to (19);
draw [black] (33) to (27);
draw [black] (33) to (30);
draw [black] (33) to (31);
draw [black] (32) to (28);
draw [black] (32) to (29);
draw [black] (32) to (31);
draw [black] (32) to (30);
draw [black] (31) to (29);
draw [black] (31) to (30);
draw [black] (30) to (28);
draw [black] (29) to (21);
draw [black] (29) to (28);
draw [black] (28) to (20);
draw [black] (27) to (24);
draw [black] (27) to (25);
draw [black] (26) to (22);
draw [black] (26) to (24);
draw [black] (26) to (25);
draw [black] (26) to (23);
draw [black] (25) to (23);
draw [black] (25) to (24);
draw [black] (24) to (22);
draw [black] (23) to (19);
draw [black] (23) to (22);
draw [black] (22) to (20);
draw [black] (21) to (12);
draw [black] (21) to (16);
draw [black] (20) to (7);
draw [black] (20) to (11);
draw [black] (19) to (8);
draw [black] (19) to (17);
draw [black] (18) to (14);
draw [black] (18) to (15);
draw [black] (18) to (17);
draw [black] (18) to (16);
draw [black] (17) to (15);
draw [black] (17) to (16);
draw [black] (16) to (14);
draw [black] (15) to (3);
draw [black] (15) to (14);
draw [black] (14) to (3);
draw [black] (13) to (9);
draw [black] (13) to (10);
draw [black] (13) to (12);
draw [black] (13) to (11);
draw [black] (12) to (10);
draw [black] (12) to (11);
draw [black] (11) to (9);
draw [black] (10) to (2);
draw [black] (10) to (9);
draw [black] (9) to (2);
draw [black] (8) to (5);
draw [black] (8) to (6);
draw [black] (8) to (7);
draw [black] (7) to (4);
draw [black] (7) to (6);
draw [black] (6) to (4);
draw [black] (6) to (5);
draw [black] (5) to (1);
draw [black] (5) to (4);
draw [black] (4) to (1);
draw [black] (3) to (1);
draw [black] (3) to (2);
draw [black] (2) to (1);""".split("\n")

vs = [re.split(r"[\(\)]", v) for v in vs]
vs = {int(v[1])-1: [float(c) for c in v[3].split(",")] for v in vs}

#print(vs)

es = [re.split(r"[\(\)]", e) for e in es]
es = [[int(e[1])-1, int(e[3])-1] for e in es]

adj = {i: [] for i in range(39)}

for e in es:
    adj[e[0]].append(e[1])
    adj[e[1]].append(e[0])

#print(es)

relabelling = [i for i in range(39)]
random.shuffle(relabelling)
reverseRelabelled = [0] * 39
for i, r in enumerate(relabelling):
    reverseRelabelled[r] = i
print(relabelling)
print(reverseRelabelled)

#relabelling = [36, 31, 15, 21, 4, 22, 1, 28, 19, 14, 10, 38, 29, 13, 3, 23, 27, 25, 5, 34, 33, 9, 8, 26, 37, 20, 6, 30, 2, 32, 11, 18, 0, 12, 24, 35, 16, 7, 17]
#reverseRelabelled = [32, 6, 28, 14, 4, 18, 26, 37, 22, 21, 10, 30, 33, 13, 9, 2, 36, 38, 31, 8, 25, 3, 5, 15, 34, 17, 23, 16, 7, 12, 27, 1, 29, 20, 19, 35, 0, 24, 11]

for p, i in enumerate(relabelling):
    print(f"{p}:[{vs[i]},{sorted([reverseRelabelled[n] for n in adj[i]])}],")