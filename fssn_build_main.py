# About OCSSN
# OCSSN - Open Closed state-sum network with tqft foundation, its topological deep learning type model, the main test - "remesh invariance test"
# Stage: Proof Of Concept

import torch
import torchvision.transforms as T
import opt_einsum
from collections import defaultdict
import random    
from collections import Counter
import sys

device = torch.device("cuda" if torch.cuda.is_available() else "cpu") # gpu as main for training, because cpu is slow :)
#sys.stdout = open("log_run_23.txt", "w", encoding="utf-8", buffering=1) # just convenient feature for run's logging

def set_seed(seed):
    random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    try:
        torch.use_deterministic_algorithms(True)
    except RuntimeError:
        pass # some CUDA ops may not have a deterministic kernel on this torch/gpu combo

main_seed = 33

seed_r = 10 # seed range
K = 200 # amount of classes
tr = 50 # epochs amount
C_cls = 2
d = 5


# Torus generator ; m,n is a size of torus, Example: torus(3,3)
def torus(m,n):
    # vid used for generation torus mesh consisting of triangles, it works like that: 
    def vid(r,c):
        return (r % m) * n + (c % n)
    tris = [] # a list where we will write down the triangles that we get by dividing a square into two triangles
    for r in range(m):
        for c in range(n):
            # its all a the boundaries of a square (its points) through 2 points of which we divide into triangles
            v00 = vid(r,c)
            v01 = vid(r, c+1)
            v10 = vid(r+1,c)
            v11 = vid(r+1, c+1)
            # make a 2 triangles in our list (tris)
            tris.append((v00, v01, v10))
            tris.append((v01, v11, v10))
    return tris

# pick fugire (list) and calculate type of surface g by Eulers Characteristic: x = V - E + F = 2 - 2g (for find g we just need to change it a bit: "g = 2 - (V - E + F) / 2")
# V = unique vertices, E = unique edges, F = number of faces, g = surface genus
def g(tris):
    F = len(tris) # In example of octahedron: F=8
    vert = set() # set() guarantees no duplicates
    for (a,b,c) in tris: # calculate V
        vert.add(a)
        vert.add(b)
        vert.add(c)
    V = len(vert) # In example of octahedron: V=6 
    edges = set()
    for (a,b,c) in tris: # calculate E
        # if 2 triangles share one edge ; Example. Upper: 1-2 & Lower: 2-1 ; They will be written in edges as (1,2) 
        edges.add(tuple(sorted((a,b)))) # About python base: tuple() is list ensures that it cannot be modified after creation ; sorted(()) sorts values ​​in ascending order
        edges.add(tuple(sorted((b,c))))
        edges.add(tuple(sorted((a,c))))
    E = len(edges) # In example of octahedron: E=12
    g = (2 - (V-E+F)) // 2 # Pick our values: 6 - 12 + 8 = 2 ==> 2 - 2 = 0 // 2 ==> g = 0 
    return g
 
# vertex normalization
def relabel(tris):
    map = {}
    n_tris = []
    for a,b,c in tris:
        for v in (a,b,c):
            if v not in map:
                map[v] = len(map)
        n_tris.append((map[a], map[b], map[c]))
    return n_tris
# Pachner move 2/2, imagine a quadrilateral with points ABCD, where A lies opposite B, C opposite D, it has a diagonal AB, the Pachner move is 2/2 diagonal from AB to CD
def p_2_2(tris):
    # we need to construct a mapping : edge -> list of tris containing it
    ett = defaultdict(list) # edge to tris
    for idx, (a,b,c) in enumerate(tris): # first triangle: (0, (0,1,2)) ; second triangle: (1, (0,2,3))
        # for each triangle, we iterate over its three edges for ensure that the edges (a,b) and (b,a) are considered the same
        for edge in [tuple(sorted((a,b))), tuple(sorted((b,c))), tuple(sorted((a,c)))]:
            ett[edge].append(idx) # add the index of the current triangle to the list of triangles that own this edge
    exist=set(ett.keys()) # set of all exist edges ; it is necessary to check whether a new diagonal already exists
    # choose an edge that has exactly two tris
    inter=[e for e, tris in ett.items() if len(tris) == 2] # A move 2/2 can only be done on an edge that is adjacent to exactly two triangles
    random.shuffle(inter)
    #edge=random.choice(inter) # choose random
    for edge in inter:
        t1_idx,t2_idx=ett[edge]
        a,b = edge # a,b = end of this edge
        t1 = tris[t1_idx]
        t2 = tris[t2_idx]
        c = [v for v in t1 if v != a and v != b]
        d = [v for v in t2 if v != a and v != b]
        if not c or not d: # empty check
            continue
        c,d = c[0], d[0]
        new_edge=tuple(sorted((c,d)))
        if c==d or new_edge in exist:
            continue
        new_triangles = [t for i, t in enumerate(tris) if i != t1_idx and i != t2_idx] # all triangles except those with indices 0 and 1 will be empty []
        new_triangles.append((a,c,d))
        new_triangles.append((c,b,d))
        return new_triangles
    return tris
# Pachner's move 1/3, from 1 triangle => 3 triangle
def p_1_3(tris):
    index = random.randrange(len(tris)) # pick rangom triangle index from tris list
    a,b,c = tris[index] # We go to our tris list by a random index (select a triangle) and lay out its three vertices
    n_v = max(max(t) for t in tris) + 1 # make new vertex, +1 guaranteed unique ID
    n_triangles = [t for i, t in enumerate(tris) if i != index] # remove 1 triangle
    n_triangles += [(a,b, n_v), (b,c, n_v), (a,c,n_v)] # make 3 new triangles, its looks like 3d triangle (tetrahedron)
    return n_triangles
# Pachner's move 3/1, from 3 triangle => 1 triangle
def p_3_1(tris):
    e_count = Counter()
    # We run through all the triangles of the mesh and split it into 3 edges using a tuple (sorted) and count how many times each edge occurs
    for (a,b,c) in tris:
        for e in [tuple(sorted((a,b))), tuple(sorted((b,c))), tuple(sorted((a,c)))]:
            e_count[e] += 1
    vert_tris = defaultdict(list) # defaultdict automatically assigns a default value to a key that does not exist
    # we take a mesh and output pairs of the form (triangle index, triangle vertices)
    # the loop takes each vertex of the triangle and writes the triangle's index to its private list
    for i, (a,b,c) in enumerate(tris):
        for v in (a,b,c):
            vert_tris[v].append(i)
    for v, incident in vert_tris.items():
        if len(incident) != 3: # if vertice = 3 then continue
            continue
        others = []
        for i in incident:
            a,b,c = tris[i]
            for u in (a,b,c):
                if u != v and u not in others:
                    others.append(u)
        if len(others) != 3:
            continue
        o0,o1,o2 = others
        # all 3 outer edges must be interior (shared with exactly 1 other tri each, no, theyre outer boundary of the patch)
        new_tri = (o0, o1, o2)
        new_edge = tuple(sorted((o0,o1)))
        # make sure outer triangle doesn't already exist
        existing_edges = set(tuple(sorted((a,b))) for a,b,c in tris 
                            for a,b in [(a,b),(b,c),(a,c)])
        # check none of the outer edges closes to itself
        if tuple(sorted((o0,o1))) in existing_edges and tuple(sorted((o1,o2))) in existing_edges and tuple(sorted((o0,o2))) in existing_edges: 
            pass
        new_triangles = [t for i, t in enumerate(tris) if i not in incident]
        new_triangles.append(new_tri)
        return new_triangles
    return None


# chain is the one of the most important slice of dataset generation ; about p_13=0.3 (this is a chance, 30%) and this to for p_31
# in foundation of this function we have Markov chain algorithm: P(X_n+1 = x_n+1 | X_n = x_n, X_n-1 = x_n-1, ... , X_0 = x_0) = P(X_n+1 = x_n+1 | X_n = x_n), This algorithm models transitions from one state to another
def chain(base, label, k, p_13=0.3, p_31=0.3, tag="unknown", stats=None):
    out = []
    current = base
    e_g = g(current)
    st = None
    if stats is not None:
        st = stats.setdefault(tag, {"moves": Counter(), "mesh_min": None, "mesh_max": None, "mesh_final": None})
        moves = st["moves"]
    else:
        moves = Counter()
    for _ in range(k):
        r = random.random()
        if r < p_13:  # Pachner move 1/3
            move = "1-3"
            figure = p_1_3(current)
        elif r < p_13 + p_31:  # Pachner move 3/1
            move = "3-1"
            figure = p_3_1(current)
            if figure is None:  # no valid vertex for 3-1, fall back to 2-2
                move = "3-1_fallback_2-2"
                figure = p_2_2(current)
        else: # Pachner move 2/2
            move = "2-2"
            figure = p_2_2(current)
        is_noop = figure is current
        if figure is not None and g(figure) == e_g:  # g correctness check
            if is_noop:
                moves[f"{move}_noop"] += 1
            else:
                moves[f"{move}_accept"] += 1
                current = figure
        else:
            moves[f"{move}_reject"] += 1
        out.append((current, label))
        if st is not None:
            n = len(current)
            st["mesh_min"] = n if st["mesh_min"] is None else min(st["mesh_min"], n)
            st["mesh_max"] = n if st["mesh_max"] is None else max(st["mesh_max"], n)
    if st is not None:
        st["mesh_final"] = len(current)

    return out
# lets pick some figures 

octahedron = [(0,1,2), (0,2,3), (0,3,4), (0,4,1),(5,2,1), (5,3,2), (5,4,3), (5,1,4),] #8 triangles list
octabipyramid = [(0,1,2), (0,2,3), (0,3,4), (0,4,5), (0,5,6), (0,6,7), (0,7,8), (0,8,1),(9,2,1), (9,3,2), (9,4,3), (9,5,4), (9,6,5), (9,7,6), (9,8,7), (9,1,8)] #16 triangles list
hexabipyramid = [(0,1,2), (0,2,3), (0,3,4), (0,4,5), (0,5,6), (0,6,1),(7,2,1), (7,3,2), (7,4,3), (7,5,4), (7,6,5), (7,1,6)] #12 triangles list
icosahedron = [(0,11,5), (0,5,1), (0,1,7), (0,7,10), (0,10,11),(1,5,9), (5,11,4), (11,10,2), (10,7,6), (7,1,8),(3,9,4), (3,4,2), (3,2,6), (3,6,8), (3,8,9),(4,9,5), (2,4,11), (6,2,10), (8,6,7), (9,8,1)] # 20 triangles, 12 edges, by euler characteristic x=12 - 30 + 20 = 2 => 2 = 2 - 2g = 2g = 0 => g=0 (sphere)

# lets put some spheres in spheres list

spheres = [icosahedron, hexabipyramid, octahedron]

sphere_names = {id(icosahedron): "icosahedron", id(hexabipyramid): "hexabipyramid", id(octahedron): "octahedron"}
last_stats = {}  # populated by the most recent dataset() call, for post-hoc inspection

def dataset_logging(stats, seed):
    print(f"dataset generation report (seed={seed})")
    for tag, st in stats.items():
        m = st["moves"]
        real_flips = m["1-3_accept"] + m["3-1_accept"] + m["2-2_accept"] + m["3-1_fallback_2-2_accept"]
        noops = m["2-2_noop"] + m["3-1_fallback_2-2_noop"]
        rejects = m["1-3_reject"] + m["3-1_reject"] + m["2-2_reject"] + m["3-1_fallback_2-2_reject"]
        total = real_flips + noops + rejects
        print(f"[{tag}] total={total} | 1-3={m['1-3_accept']} | 3-1={m['3-1_accept']} | 2-2={m['2-2_accept']} | 3-1->2-2_fallback={m['3-1_fallback_2-2_accept']} | no-op={noops} | g-mismatch={rejects} | mesh_tris=[{st['mesh_min']}..{st['mesh_max']}], final={st['mesh_final']}")
        if total:
            print(f"real_flip_rate={real_flips/total:.1%}  noop_rate={noops/total:.1%}")
    print("=" * 60)

# dataset generation
def dataset(k, n=None, seed=None, verbose=True):
    if seed is not None:
        random.seed(seed)
    if n is None:
        n = k // len(spheres)
    stats = {}
    out = []
    for b in spheres:
        tag = sphere_names.get(id(b), "sphere")
        out += chain(b, 0, n, tag=tag, stats=stats) # generation g=0 (spheres)
    out += chain(torus(3, 3), 1, k, tag="torus", stats=stats) # generation g=1 (torus)
    global last_stats
    last_stats = stats
    if verbose:
        dataset_logging(stats, seed)
    return out

# Conceptually, this is a rather confusing function in the entire code (it transforms mesh geometry into a combinatorial tensor network), so I will add a more extensive amount of explanation here, I tried to make it as clear as I could
def graph(triangles):
    slot = {} # dictionary who will contain unique ID for every port
    # sid() is function for generation a lot of unique ID's, t = triangle number, e = this triangle edge
    # if this both are first time here then we give to it an ordinal number equal to the current length of the dictionary (len(slot), like 0,1,2,3,4,5...
    # this gives us the condition that if two triangles share one edge, they will store a unique port ID for it
    def sid(t,e):
        if (t,e) not in slot:
            slot[(t,e)] = len(slot)
        return slot[(t,e)]
    v_p = [] # vertices ports, list of 3 triangles ID's 
    e_slots = {} # here we will store the connection of vertices
    # on numbered triangles, we sort their 3 edges, all this needed for make edge (2,1) and edge (1,2) similar
    for t, (a,b,c) in enumerate(triangles):
        eab = tuple(sorted((a,b)))
        ebc = tuple(sorted((b,c)))
        eac = tuple(sorted((a,c)))
        s0,s1,s2 = sid(t,eab), sid(t, ebc), sid(t, eac) # generation 3 unique port ID's for current triangle t
        v_p.append((s0,s1,s2)) # add this 3 ports in v_p and we gonna know that fact the triangle t are manage indexes s0,s1,s2
        # If edge eab is internal, then e_slots[eab] will contain two ID's: the port from the first triangle and the port from the second triangle
        e_slots.setdefault(eab,[]).append(s0)
        e_slots.setdefault(ebc,[]).append(s1)
        e_slots.setdefault(eac,[]).append(s2) 
    g_edges, open_ports = [], []
    for s in e_slots.values():
        if len(s) == 2: # 2 ports of different triangles
            g_edges.append((s[0], s[1]))
        else: # if we have more or less than 2 ports
            open_ports += s # we just send it into free lists
    return v_p, g_edges, open_ports

# Conceptually, this function computes the topological invariant of our mesh using the values ​​returned by the graph() function
# to put it in more detail, the purpose of this function is to compress the entire huge curve of hundreds of triangles into one single vector of a fixed size d
def state_sum(C, b_inv, v_p, g_edges, open_ports=()): # pass values ​​from graph() and C (c3) and b_inv
    ops = [] # main list for opt_einsum, here we gonna add all arguments
    for (a,b,c) in v_p:
        ops += [C, (a,b,c)] # for every unique port ID we compare the index
    for (x,y) in g_edges:
        ops += [b_inv, (x,y)]
    ops += [tuple(open_ports)]
    return opt_einsum.contract(*ops, optimize="greedy") # opt_einsum its better version of basic einsum, it searches the best way to sum huge values

# Convert our tris in naturally for baseline models format (right now for Graph Network)
def converter_for_gnn(tris):
    tris = relabel(tris)
    num_nodes = max(max(t) for t in tris) + 1 # we got 3 (because we got (2,3) and choose max value) and + 1 = 4
    A = torch.zeros((num_nodes, num_nodes)) # 4 x 4 zeros matrice
    for (u,v,w) in tris:
        A[u,v]=A[v,u]=1.0; A[v,w]=A[w,v]=1.0; A[u,w]=A[w,u]=1.0 # matrix symmetry
    s = A.sum() # sum of all elements in A, sum of every row (check result upper)
    degree = (A.sum(dim=1, keepdim=True) / (s + 1e-8))
    L = torch.cat([degree, torch.ones(num_nodes, 1)], dim=1)
    return A / (s + 1e-8), L
    
# Convert our tris in naturally for baseline models format #2 (right now for Tensor Network)
def converter_for_tnn(tris, N=64):
    tris = relabel(tris)
    A = torch.zeros((N, N))
    for (u, v, w) in tris:
        A[u,v]=A[v,u]=1.0; A[v,w]=A[w,v]=1.0; A[u,w]=A[w,u]=1.0

    deg = A.sum(dim=1)
    deg2 = torch.where(deg > 0, deg.pow(-0.5), torch.zeros_like(deg)) 
    D = torch.diag(deg2)
    A_norm = D @ A @ D
    return A_norm # return balanced and normalized adjacency matrix

# After all, next part with training and model initialization wont be descriptive that much

# Graph network have been modified a little bit because it just needed for that type of task, main difference with basic in agg
class gnn(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.W1 = torch.nn.Parameter(torch.randn(2, 4) * 0.1)
        self.W2 = torch.nn.Parameter(torch.randn(4, 4) * 0.1)
        self.classifier = torch.nn.Linear(4, 2)
    def forward(self, a, L):
        agg1 = a @ L # in basic gnn agg looking like that agg1 = (a @ L) / degree.reshape(-1,1) ; If i remember well (its been 3-4 weeks ago) with that basic construction i had some kind of problems with prediction
        L1 = torch.nn.functional.relu(agg1 @ self.W1)
        agg2 = a @ L1
        L2 = torch.nn.functional.relu(agg2 @ self.W2)
        graph_vec = L2.mean(dim=0)
        logits = self.classifier(graph_vec)
        return logits
def prep(A):
    a = A + torch.eye(A.shape[0], device=A.device)
    return a
# there's doesnt have some kind of modify, just 1 layer + bias
class tnn(torch.nn.Module):
    def __init__(self, N=64):
        super().__init__()
        self.N = N
        self.u = torch.nn.Parameter(torch.randn(N, 2) * 0.1)
        self.v = torch.nn.Parameter(torch.randn(N, 2) * 0.1)
        self.bias = torch.nn.Parameter(torch.zeros(2))
    def forward(self, A):
        logits = torch.einsum("bij, ic, jc -> bc", A, self.u, self.v)
        return logits + self.bias

# The main model, full description in README                                                                                                                         
class OCSSN(torch.nn.Module):
    def __init__(self, d, C_cls):
        super().__init__()
        self.d = d
        M = torch.zeros(d, d, d)
        for k in range(d):
            for i in range(d):
                M[k,i,(k-i)%d]=1.0
        self.register_buffer("M", M)
        self.register_buffer("u", torch.ones(d))
        self.G = torch.nn.Parameter(torch.randn(C_cls, d) * 0.1)
        self.bias = torch.nn.Parameter(torch.randn(C_cls))
        self.eps_r = torch.nn.Parameter(torch.randn(d)*0.3)
    def eps(self):
        return torch.exp(self.eps_r)
    def mul(self, a, b):
        return torch.einsum("kij,i,j->k",self.M,a,b)
    def forward(self, m, return_h=False, step=None):
        eps_v = self.eps()
        if step is not None and step % 100 == 0:
            print(f"eps_v_check | step={step} S={eps_v.sum().item():.4f} min={eps_v.min().item():.4f} max={eps_v.max().item():.4f}")
        beta = torch.einsum("kij, k->ij", self.M, eps_v)
        b_inv = torch.linalg.inv(beta)
        c3=torch.einsum("pij, pk->ijk", self.M, beta)
        m_sorted = sorted(m, key=lambda t: tuple(sorted(t)))
        v_ports, g, open_ports = graph(m_sorted)
        if len(open_ports) == 0:
            idx = min(range(len(g)), key=lambda i: g[i])
            x, y = g.pop(idx)
            open_ports = [x]
        h = state_sum(c3, b_inv, v_ports, g, open_ports=tuple(open_ports[:1]))
        #print(f"h raw norm: {h.norm().item()}")
        h_norm = h/(h.norm()+1e-8)
        #print(f"h_norm = {h_norm.norm().item()}")
        z = self.G @ h_norm + self.bias
        if return_h:
            return z, h, h_norm
        return z
set_seed(main_seed)
data = dataset(K, seed=main_seed)
data_val = dataset(K, seed=main_seed + 1)
split = int(0.8 * len(data)) # split, do 80% of classes on training and 20% new on validation
print(f"main_seed={main_seed}")

for seed in range(main_seed, main_seed + seed_r):
    model_gnn = gnn().to(device)
    optim_gnn = torch.optim.AdamW(model_gnn.parameters(), lr=0.001)
    # OCSSN model init
    model_OCSSN = OCSSN(d, C_cls).to(device)
    optim_OCSSN = torch.optim.AdamW(model_OCSSN.parameters(), lr=0.001)
    # tnn model init
    model_tnn = tnn().to(device)
    optim_tnn = torch.optim.AdamW(model_tnn.parameters(), lr=0.001)

    print(f"seed={seed}")
    torch.manual_seed(seed)
    random.seed(seed)
    random.shuffle(data) # every seed unique datasets, easily can be removed and replaced to one similar dataset for every seed
    trainset = data[:split]
    n_sphere = sum(1 for _, lab in trainset if lab == 0)
    n_torus = len(trainset) - n_sphere
    print(f"Trainset: sphere={n_sphere}, torus={n_torus}")

    for train in range(tr):
        model_OCSSN.train()
        model_gnn.train()
        model_tnn.train()
        err_sum_OCSSN, err_sum_gnn, err_sum_tnn, correct_OCSSN, correct_gnn, correct_tnn = 0.0, 0.0, 0.0, 0, 0, 0
        step = 0
        for tris, label in trainset:
            step += 1
            if step == 1 and train == 0:
                print(f"Analysis: label={label} V={len(set(v for t in tris for v in t))} E={len(set(tuple(sorted((a,b))) for a,b,c in tris for a,b in [(a,b),(b,c),(a,c)]))} F={len(tris)}")
            y = torch.tensor([label], dtype=torch.long).to(device)

            # OCSSN training cycle 

            optim_OCSSN.zero_grad()
            pred_OCSSN = model_OCSSN(tris, step=step)
            err_OCSSN = torch.nn.functional.cross_entropy(pred_OCSSN.unsqueeze(0), y)
            err_OCSSN.backward()
            optim_OCSSN.step()
            err_sum_OCSSN += err_OCSSN.item()
            correct_OCSSN += int(pred_OCSSN.argmax().item() == label)

            # TNN training cycle

            A_tnn = converter_for_tnn(tris).to(device)
            A_tnn = A_tnn.unsqueeze(0)
            optim_tnn.zero_grad()
            pred_tnn = model_tnn(A_tnn)
            err_tnn = torch.nn.functional.cross_entropy(pred_tnn, y)
            err_tnn.backward()
            optim_tnn.step()
            err_sum_tnn += err_tnn.item()
            correct_tnn += int(pred_tnn.argmax().item() == label)

            # GNN training cycle 

            A,L = converter_for_gnn(tris)
            A = A.to(device)
            L = L.to(device)
            optim_gnn.zero_grad()
            A_hat1 = prep(A)
            pred_gnn = model_gnn(A_hat1,L)
            err_gnn = torch.nn.functional.cross_entropy(pred_gnn.unsqueeze(0),y)
            err_gnn.backward()
            optim_gnn.step()
            err_sum_gnn += err_gnn.item()
            correct_gnn += int(pred_gnn.argmax().item() == label)

        print(f"OCSSN ep={train}, loss={err_sum_OCSSN/len(trainset):.4f}, train_acc={correct_OCSSN/len(trainset):.2%}")
        print(f"GNN ep={train}, loss={err_sum_gnn/len(trainset):.4f}, train_acc={correct_gnn/len(trainset):.2%}")
        print(f"TNN ep={train}, loss={err_sum_tnn/len(trainset):.4f}, train_acc={correct_tnn/len(trainset):.2%}")
# Holdout
    model_OCSSN.eval()
    model_gnn.eval()
    model_tnn.eval()
    with torch.no_grad():
        valset = data_val
        val_n_sphere = sum(1 for _, label in valset if label == 0)
        val_n_torus = len(valset) - val_n_sphere 
        print(f"valset: sphere={val_n_sphere}, torus={val_n_torus}")
        OCSSN_correct = 0
        gnn_correct = 0
        tnn_correct = 0
        for i, (tris, label) in enumerate(valset):
            # OCSSN
            pred_OCSSN = model_OCSSN(tris).argmax().item()
            if pred_OCSSN == label:
                OCSSN_correct += 1
            # GNN
            A,L = converter_for_gnn(tris)
            A = A.to(device)
            L = L.to(device)
            A_hat = prep(A)
            pred_gnn = model_gnn(A_hat, L).argmax().item()
            if pred_gnn == label:
                gnn_correct += 1
            # TNN
            A_tnn = converter_for_tnn(tris).to(device).unsqueeze(0)
            pred_tnn = model_tnn(A_tnn).argmax().item()
            if pred_tnn == label:
                tnn_correct += 1
            print(f"OCSNN={pred_OCSSN}, GNN={pred_gnn}, TNN={pred_tnn} | True = {label}")
        # dispersion checking
        H_sph = []
        H_tor = []
        for b, (tris, label) in enumerate(valset):
            _,_, h_norm = model_OCSSN(tris, return_h=True)
            if label == 0:
                H_sph.append(h_norm)
            elif label == 1:
                H_tor.append(h_norm)
        H_s = torch.stack(H_sph, dim=0)
        H_t = torch.stack(H_tor, dim=0)

        var_s = torch.var(H_s, dim=0, unbiased=False).mean().item()
        std_s = torch.std(H_s, dim=0, unbiased=False).mean().item()

        var_t = torch.var(H_t, dim=0, unbiased=False).mean().item()
        std_t = torch.std(H_t, dim=0, unbiased=False).mean().item()
        print(f"torus dispersion: var_t={var_t:.16f}, std_t={std_t:.16f}")
        print(f"sphere dispersion: var_s={var_s:.16f}, std_s={std_s:.16f}")
        print(f"OCSSN val acc: {OCSSN_correct / len(valset) * 100:.2f}%")
        print(f"tnn val acc: {tnn_correct / len(valset) * 100:.2f}%")
        print(f"gnn val acc: {gnn_correct / len(valset) * 100:.2f}%")