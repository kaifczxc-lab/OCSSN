# Open-Closed State-Sum Network

**Independent Study in Topological Deep Learning, 2D TQFT, and Topology. Work classified as Research Report**

Author: [siritoriyowai](https://github.com/kaifczxc-lab)

Current stage: **Proof-of-Concept**

This report focuses on the architectural Proof of Concept, **large-scale benchmarks will be provided in future iterations**

Note that, the author doesn't know how to name this model correctly, so the name OCSSN is a tribute to the work that **inspired this project**

---

### Important Note (August 12, 2026)

The value of the current work is unknown. The results in the version of the [code with the shortcut fix](https://github.com/kaifczxc-lab/OCSSN/blob/SiritoriProjects/fssn_build_main_with_shortcut_fix.py) degenerate into random guessing for all models. [Section 3](https://github.com/kaifczxc-lab/OCSSN/tree/SiritoriProjects#section-3--summary-) describes the results of [the version of the code without the shortcut fix](https://github.com/kaifczxc-lab/OCSSN/blob/SiritoriProjects/fssn_build_main.py). To put it more bluntly, this shortcut was found by chance using LogisticRegression from sklearn.linear_model, which makes it very difficult to say anything about it at this point. Even so, in theory, the model provides greater gains compared to others, and this remains an open question. The author will resolve and describe this open question. For now, as of 8/12/26, we are at this stage. At a minimum, I would like to say that the situation may change with possible changes to the model parameters (such as algebra in M), that is. What the author wants to say is that the work has not yet yielded an absolutely negative result. In my opinion, the "OCSSN class" can be modified in a huge number of ways, all of which have not yet been tested and have not been found

---

## Table of Contents

- [Section 0: Introduction](https://github.com/kaifczxc-lab/OCSSN/tree/SiritoriProjects#section-0--introduction-)
- [Section 1: OCSSN main construction](https://github.com/kaifczxc-lab/OCSSN/tree/SiritoriProjects#section-1--ocssn-main-construction-)
    - [Section 1.1: Analysis of each variable](https://github.com/kaifczxc-lab/OCSSN/tree/SiritoriProjects#section-11--a-complete-analysis-of-each-variable-)
- [Section 2: Description of every function](https://github.com/kaifczxc-lab/OCSSN/tree/SiritoriProjects#section-2--description-of-every-function-)
    - [Section 2.1: Torus Generation](https://github.com/kaifczxc-lab/OCSSN/tree/SiritoriProjects#section-21--torus-generation-)
    - [Section 2.2: The function that determines the genus of a surface g](https://github.com/kaifczxc-lab/OCSSN/tree/SiritoriProjects#section-22--the-function-that-determines-the-genus-of-a-surface-g-)
    - [Section 2.3: Vertex normalization](https://github.com/kaifczxc-lab/OCSSN/tree/SiritoriProjects#section-23--vertex-normalization-)
    - [Section 2.4: All Pachner moves](https://github.com/kaifczxc-lab/OCSSN/tree/SiritoriProjects#section-24--all-pachner-moves-)
    - [Section 2.5: Graphs function construction](https://github.com/kaifczxc-lab/OCSSN/tree/SiritoriProjects#section-25--graphs-function-construction-)
    - [Section 2.6: Chain](https://github.com/kaifczxc-lab/OCSSN/tree/SiritoriProjects#section-26--chain-)
    - [Section 2.7: Dataset Generation](https://github.com/kaifczxc-lab/OCSSN/tree/SiritoriProjects#section-27--dataset-generation-)
    - [Section 2.8: Converters](https://github.com/kaifczxc-lab/OCSSN/tree/SiritoriProjects#section-28--converters-)
- [Section 3: Summary](https://github.com/kaifczxc-lab/OCSSN/tree/SiritoriProjects#section-3--summary-)
- [Section 4: Limitations & Problems](https://github.com/kaifczxc-lab/OCSSN/tree/SiritoriProjects#section-4--limitations-)
- [Section 5: Future Work](https://github.com/kaifczxc-lab/OCSSN/tree/SiritoriProjects#section-5--future-work-)
- [Section 6: Gallery](https://github.com/kaifczxc-lab/OCSSN/tree/SiritoriProjects#section-6--gallery-)


# Section 0 | Introduction | 

Goals, motivations and problems of the project at the PoC stage:

* **Motivations**: 2D TQFT is equivalent to commutative Frobenius Algebras, in 2d tqft we have a precisely described state-sum model, this served as the main motivation the question of its realization in ML field (using tensor network architectures as a foundation)

* **Goals**: show alternative way to solve a single problem from the point of view of different neural network architectures

* **Problems**: the main problem is to prove invariance under remeshing, but the [limitation](https://github.com/kaifczxc-lab/OCSSN/tree/SiritoriProjects#section-4--limitations-) must be considered

---

Main subject is: Higher Mathematics (Topology. Linear Algebra. Topological Quantum Field Theory)

**References**: 

* [1] [Lauda, A. D., & Pfeiffer, H. (2006): State sum construction of two-dimensional open-closed Topological Quantum Field Theories](https://arxiv.org/abs/math/0602047)

* [2] [Fukuma, M., Hosono, S., & Kawai, H. (1994). Lattice Topological Field Theory in Two Dimensions. Commun. Math. Phys. 161, 157–176](https://arxiv.org/abs/hep-th/9212154)

**Materials for learning / Further reading**: 

* [3] [Atiyah, M. F. (1988). Topological quantum field theory. Publications Mathématiques de l'IHÉS, 68, 175-186](https://webhomes.maths.ed.ac.uk/~v1ranick/papers/atiyahtqft.pdf)

* [4] [Grokipedia: Pachner Moves](https://grokipedia.com/page/pachner_moves) (It might not be the best source, so you can also use [Wikipedia](https://en.wikipedia.org/wiki/Pachner_moves))

* [5] ["Elementary Topology. Problem Textbook" By O. Ya. Viro, O. A. Ivanov, N. Yu. Netsvetaev, V. M. Kharlamov](https://webhomes.maths.ed.ac.uk/~v1ranick/papers/viro.pdf)

* [6] [Tom Leinster (2016): Basic Category Theory](https://arxiv.org/abs/1612.09375)

Before proceeding, some clarifications should be made, the model's name contains "Open-Closed State Sum" but **not TQFT/Frobenius/Topological**, this is because the model is a partial combination of these theories, in a form suitable for a **dynamically learning algorithm**

That is: 

* The author **doesn't claim about the project is fully correct from the point of view of pure mathematics**: [General Topology](https://webhomes.maths.ed.ac.uk/~v1ranick/papers/viro.pdf), [state-sum](https://arxiv.org/abs/math/0602047), [TQFT's](https://webhomes.maths.ed.ac.uk/~v1ranick/papers/atiyahtqft.pdf)

Due to the obvious impossibility of moving strict concepts in a **dynamically learning algorithm**, in otherwise it would just be a **static algorithm**, the reader should **take this into account as obvious fact**

The state-sum function was inspired by State-sum construction of **2D open-closed TQFTs** [[1]](https://arxiv.org/abs/math/0602047)

# Section 1 | OCSSN main construction |

In code of this project we have **two** main parts

1) OCSSN class realization by **References**

```python
class OCSSN(torch.nn.Module):
    def __init__(self, d, C):
        super().__init__()
        self.d = d
        M = torch.zeros(d, d, d)
        for k in range(d):
            for i in range(d):
                M[k,i,(k-i)%d]=1.0
        self.register_buffer("M", M)
        # self.register_buffer("u", torch.ones(d)) - unit element, not in use yet
        self.G = torch.nn.Parameter(torch.randn(C, d) * 0.1)
        self.bias = torch.nn.Parameter(torch.randn(C))
        self.eps_r = torch.nn.Parameter(torch.randn(d)*0.3)
    def eps(self):
        return torch.exp(self.eps_r) #e^eps_r
    def mul(self, a, b):
        return torch.einsum("kij,i,j->k",self.M,a,b)
    def forward(self, m, return_h=False):
        eps_v = self.eps()
        beta = torch.einsum("kij, k->ij", self.M, eps_v)
        b_inv = torch.linalg.inv(beta)
        c3=torch.einsum("pij, pk->ijk", self.M, beta)
        # removes dependence on flip-history append order
        m_sorted = sorted(m, key=lambda t: tuple(sorted(t)))
        v_ports, g, open_ports = graph(m_sorted)
        if len(open_ports) == 0:
            # smallest slot-pair, deterministic for given triangulation
            idx = min(range(len(g)), key=lambda i: g[i])
            x, y = g.pop(idx)
            open_ports = [x]
        h = state_sum(c3, b_inv, v_ports, g, open_ports=tuple(open_ports[:1])) # result: vector with type (d,)
        h_norm = h/(h.norm()+1e-8)
        z = self.G @ h_norm + self.bias
        if return_h:
            return z, h, h_norm
        return z
```

2) State-sum realization by **References**

```python
def state_sum(C, b_inv, v_p, g_edges, open_ports=()): # pass values ​​from graph() and C (c3) and b_inv
    ops = [] # main list for opt_einsum, here we will add all arguments
    for (a,b,c) in v_p: # as example let take v_p = [(0,1,2),(3,4,5)]
        ops += [C, (a,b,c)] # for every unique port ID lets compare the index =>
        # => (t0,t1,t2,t3,t4,t5) => ops += [C, (0,1,2)] => C_t0,t1,t2 ; ops += [C,(3,4,5)] => C_t3,t4,t5 ; C_a,b,c for each triangle
    for (x,y) in g_edges: # g_edges=[1,5]
        ops += [b_inv, (x,y)] # b_inv = (B^-1)_t1,t5
    ops += [tuple(open_ports)] # open_ports=[0,2,3,4]
    # After all: Z_T0 = sum_t1,t2,t3,t4,t5 C_t0,t1,t2 * C_t3,t4,t5 * (B^-1)_t1,t5
    return opt_einsum.contract(*ops, optimize="greedy") # opt_einsum its just better version of basic einsum, it searches the best way to sum huge values
```

### Section 1.1 | A complete analysis of each variable |

Because OCSSN is also a kind of tensor-based model, there is a known issue arises:

* "for small dimensions, the complete classification of finite-dimensional commutative algebras over R quickly becomes modular and partially infinite, so for d ≥ 7 the list of all types is not available in finite form, but for d ≤ 6 there is a complete classification over an algebraically closed field"

* M: Its 3-tensor of cyclic group Z/d, i.e., tensor of structure constants of group algebra $\mathbb{C}[\mathbb{Z}_d]$

    * Where does it come from? It is tensor of structure constants of group algebra $\mathbb{C}[\mathbb{Z}_d]$ over a field $\mathbb{C}$ (or $\mathbb{R}$), it defines the multiplication in the basis of group elements, more information can be found [here](https://en.wikipedia.org/wiki/Structure_constants), this tensor is mentioned there as "$c_{ij}{}^{k}$"

* eps_r (counit): In 2D TQFT, any multiplication operation requires a corresponding linear functional (counit), which in this model is represented by eps_r

* eps_v (counit): We need to build **non-degenerate symmetric invariant pairing g** (=beta) because we wrap eps_r in an exponent to ensure that eps is a positive number, otherwise if eps is close to 0 or negative, beta may become singular, but this doesnt mean the torch.linalg.inv cant be singular, but it happens noticeably less frequently than if we did not apply the exponent

* Beta ([non-degenerate symmetric invariant pairing g. Lemma 2.4.](https://arxiv.org/pdf/math/0602047)): this is the tensor form of $$g = \varepsilon \circ \mu$$, it is the Frobenius bilinear form/pairing if context of 2d tqft

* B_inv: **inverse matrix** of Beta, is also needed for state-sum. inverse of $g$, see. Definition 2.3 (2) in [[3]](https://arxiv.org/abs/math/0602047)

* c3: 3-tensor obtained by contracting M with beta, it is a complex number that is needed for the state-sum

* G,h,Z: Basic readout part

* State-sum (Partition Function): The main material is drawn from [Fukuma, M., Hosono, S., & Kawai, H. (1994). Lattice Topological Field Theory in Two Dimensions. Commun. Math. Phys. 161, 157–176](https://arxiv.org/abs/hep-th/9212154)

    * First, **Definition of LTFT Section 2 / State-sum Construction** [[2]](https://arxiv.org/abs/hep-th/9212154): 
    
    "We then assign a complex value $$C_{ijk}$$ to a triangle with ordered color indices i, j, k. We here assume that $$C_{ijk}$$ is symmetric under cyclic permutations of the indices: $$C{ijk} = C_{jki} = C_{kij}$$ ; Note, however, that $$C_{ijk}$$ is not necessarily totally symmetric. Next, we glue these triangles by contracting their indices with $$g^{ij}$$ = $$g^{ji}$$. We further assume that $$g^{ij}$$ has its inverse $$g_{ij}$$ ; $g_{ik}g^{kj} = δ^{j}_{i}$ and raise or lower indices with these matrices. Thus, we have a complex-valued function of $C_{ijk}$ and $$g_{ij}$$ for each triangulation $$T_{g}$$ and we will interpret it as the partition function of our lattice model, denoting it by $$Z(T_{g})$$  For example, the partition function for the triangulation of $$\sum_{0} = S^{2}$$ is expressed as: $$Z(T_0) = g^{ii'} g^{jj'} g^{kk'} g^{ll'} g^{mm'} g^{nn'} C_{ijk}C_{k'lm}C_{m'ni'}C_{j'n'l'}$$"

    Let us compare this with the [state-sum algorithm used in OCSSN](https://github.com/kaifczxc-lab/OCSSN/blob/66d6d0037c0b25fb4c1941eda25db16e6054cf18/fssn_build_main.py#L285)

    The triangles with ordered color indices i,j,k are represented in **$$v_p$$ with indices a,b,c**. Complex number we assign too ```ops += [C, (a,b,c)]``` and we get **$$C_{a,b,c}$$** ; $$g^{ij}$$ is obtained from ```ops += [b_inv, (x,y)]``` , triangulations here are $$v_p$$ & $$g_edges$$ and the **contraction follows** [Einstein Notation](https://en.wikipedia.org/wiki/Einstein_notation)

    **Differences**: in classical FHK State-sum construction **does not have open ports** and all indices are contracted and **yielding scalar**, in OCSSN state-sum when open_ports is **not empty**, the result of **the calculation is not a scalar**, but a **vector (or tensor)**, but if open_ports empty it **yields the same scalar** as in the **original** FHK construction


# Section 2 | Description of every function |

This section does not describe the structural features of OCSSN, it is only a complete, fairly detailed description by the author of each line of code

# Section 2.1 | Torus Generation |

```python
def torus(m,n):
    # vid used for generation torus mesh consisting of triangles, it works like that: 
    # Take a flat sheet, glue its left edge to the right, you get a cylinder, and by gluing two round bases of the cylinder, we get a torus
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
```

# Section 2.2 | The function that determines the genus of a surface g |

Lets pick fugire (list) and calculate type of surface g by Eulers Characteristic: x = V - E + F = 2 - 2g (for find g we just need to change it a bit: "g = 2 - (V - E + F) / 2")

Repeat: V = unique vertices, E = unique edges, F = number of faces, g = surface genus

The value of surface genus (g) shows how many holes there are in a given figure; Example: g=0 - sphere, g=1 - torus, etc

```python
def g(tris):
    F = len(tris) # In example of octahedron: F=8
    vert = set()
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
```

# Section 2.3 | Vertex normalization |

```python
def relabel(tris):
    map = {} # table in form : {"old index": "new index"}
    n_tris = [] # new "pure" triangles list
    # we go through each triangle, at each his vertex and write out his number => 
    # => (triangle number), this needed to remove huge number difference in list, because between 1 and 50 about 48 zero's
    # Example: tris=[(10, 50, 15), (50, 100, 15)], lets pick 10, its new vertex => mapping{10: 0} ;
    # 50 = {50: 1} ; 15 = {15: 2} ; 50 = {we already have it because that, 50: 1}, 100 = {100: 3}, 15 = {15: 2}
    # result: (10,50,15) => (0,1,2) ; (50, 100, 15) => (1,3,2)
    for a,b,c in tris:
        for v in (a,b,c):
            if v not in map:
                map[v] = len(map)
        n_tris.append((map[a], map[b], map[c]))
    return n_tris
```
# Section 2.4 | All Pachner moves |

For example in all function we take tris = [(0, 1, 2),(0, 2, 3)]

```python
def p_2_2(tris):
    # we need to construct a mapping : edge -> list of tris containing it
    ett = defaultdict(list) # edge to tris
    for idx, (a,b,c) in enumerate(tris): # first triangle: (0, (0,1,2)) ; second triangle: (1, (0,2,3))
        # for each triangle, we iterate over its three edges for ensure that the edges (a,b) and (b,a) are considered the same
        # for first triangle: a,b = tuple(sorted((0,1))) => (0,1) => ett[(0,1)].append(0) => ett[(0,1)] = [0] ; b,c = (1,2) => [(1,2)] => ett[(1,2)] = [0] ; a,c = (0,2) => [(0,2)] => ett[(0,2)] = [0]
        # for second triangle: a,b = tuple(sorted((0,2))) => we already have it => ett[(0,2)] = [0,1] ; b,c = (2,3) => [(2,3)] => ett[(2,3)] => [1] ; a,c = (0, 3) => [(0,3)] => ett[(0,3)] = [1]
        for edge in [tuple(sorted((a,b))), tuple(sorted((b,c))), tuple(sorted((a,c)))]:
            ett[edge].append(idx) # add the index of the current triangle to the list of triangles that own this edge
        # ett = {(0,1): [0], (1,2): [0], (0,2): [0,1], (2,3): [1], (0,3): [1]}
    exist=set(ett.keys()) # set of all exist edges ; it is necessary to check whether a new diagonal already exists ; with our tris we will have exist={(0,1), (1,2), (0,2), (2,3), (0,3)}
    # choose an edge that has exactly two tris
    inter=[e for e, tris in ett.items() if len(tris) == 2] # A move 2/2 can only be done on an edge that is adjacent to exactly two triangles ; in our tris we have only (0,2) (because {(0,2): [0,1} ] ) => inter = [(0,2)]
    random.shuffle(inter)
    #edge=random.choice(inter) # choose random
    for edge in inter: # edge = (0,2)
        t1_idx,t2_idx=ett[edge] # t1_idx, t2_idx = 0,1
        a,b = edge # a,b = end of this edge ; a,b = 0,2
        t1 = tris[t1_idx] # t1 = (0,1,2) ; pick our triangles in tris
        t2 = tris[t2_idx] # t2 = (0,2,3)
        c = [v for v in t1 if v != a and v != b] # vertice t1 instead of a,b ; c = [v for v in (0,1,2) if v != 0 and v != 2] => [1]
        d = [v for v in t2 if v != a and v != b] # vertice t2 instead of a,b ; d = [v for v in (0,2,3) if v != 0 and v != 2] => [3]
        if not c or not d: # empty check
            continue # we dont have empty c and d because this => continue
        c,d = c[0], d[0] # c,d = 1,3
        new_edge=tuple(sorted((c,d))) # new_edge = (1,3)
        if c==d or new_edge in exist: # c dont equals d (1 == 3? False) ; new_edge in exist? ( (1,3) in {(0,1),(1,2),(0,2),(2,3),(0,3)}? False ) => continue
            continue
        new_triangles = [t for i, t in enumerate(tris) if i != t1_idx and i != t2_idx] # all triangles except those with indices 0 and 1 will be empty []
        new_triangles.append((a,c,d)) # in our example: (0,1,3)
        new_triangles.append((c,b,d)) # (1,2,3)
        return new_triangles # return [(0,1,3), (1,2,3)]
    # result: the two original triangles (0,1,2) and (0,2,3) turned into (0,1,3) and (1,2,3), the common edge (0,2) disappeared, the edge (1,3) appeared
    return tris

# Pachner's move 1/3, from 1 triangle => 3 triangle
def p_1_3(tris):
    index = random.randrange(len(tris)) # pick rangom triangle index from tris list
    a,b,c = tris[index] # We go to our tris list by a random index (select a triangle) and lay out its three vertices
    n_v = max(max(t) for t in tris) + 1 # make new vertex, +1 guaranteed unique ID
    n_triangles = [t for i, t in enumerate(tris) if i != index] # remove 1 triangle
    # Example: lets pick tris=[(0,1,2), (0,2,3), (1,3,4)], index=1
    # i=0: (0,1,2) stay (0 != 1, its true) ; i=1: (0,2,3), remove (1 != 1, false) ; i=2: (1,3,4) stay (2 != 1, its true)
    # result: n_triangles=[(0,1,2), (1,3,4)]
    n_triangles += [(a,b, n_v), (b,c, n_v), (a,c,n_v)] # make 3 new triangles, its looks like 3d triangle (tetrahedron)
    return n_triangles

# Pachner's move 3/1, from 3 triangle => 1 triangle
def p_3_1(tris):
    e_count = Counter() # edge_count ; Counter() in python counts repetitions and writes them out for each element. 
    # Example: list=[1,2,3,1,2,1,1] => list = Counter() => ({1:4, 2:2, 3:1})
    # We run through all the triangles of the mesh and split it into 3 edges using a tuple (sorted) and count how many times each edge occurs
    for (a,b,c) in tris:
        for e in [tuple(sorted((a,b))), tuple(sorted((b,c))), tuple(sorted((a,c)))]:
            e_count[e] += 1
    vert_tris = defaultdict(list) # defaultdict automatically assigns a default value to a key that does not exist
    # we take a mesh and output pairs of the form (triangle index, triangle vertices)
    # the loop takes each vertex of the triangle and writes the triangle's index to its private list
    # Example: 1st triangle = i=0: (0,1,6) , 2nd = i=1: (1,2,6) , 3rd = i=2: (0,2,5)
    # for 1st triangle: 0 => 0 -> vert_tris[0] = [0 (this is index)] ; 1 => 0 -> vert_tris[1] = [0] ; 6 => 0 -> vert_tris[6] = [0]
    # for 2nd triangle: 1 => 1 -> vert_tris[1] = [0,1] ; 2 => 1 -> vert_tris[2] = [1] ; 6 => 1 -> vert_tris[6] = [0,1]
    # for 3rd triangle: 0 => 2 -> vert_tris[0] = [0,2] ; 2 => 2 -> vert_tris[2] = [1,2] ; 5 => 2 -> vert_tris[5] = [2] 
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
```

## Section 2.5 | Graphs function construction |

graph() turns geometry into a huge system of equations, which the neural network then collapses into a single feature vector

```python
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
    e_slots = {} # here we will store the connection of vertices (let's say (1,2)) =>
    # => and the value of the list of ports claiming it, this gonna be something about "splice map"
    # on numbered triangles, we sort their 3 edges, all this needed for make edge (2,1) and edge (1,2) similar
    for t, (a,b,c) in enumerate(triangles):
        eab = tuple(sorted((a,b)))
        ebc = tuple(sorted((b,c)))
        eac = tuple(sorted((a,c)))
        s0,s1,s2 = sid(t,eab), sid(t, ebc), sid(t, eac) # generation 3 unique port ID's for current triangle t
        v_p.append((s0,s1,s2)) # add this 3 ports in v_p and we gonna know that fact the triangle t are manage indexes s0,s1,s2
        # register ports into e_slots
        # If edge eab is internal, then e_slots[eab] will contain two ID's: the port from the first triangle and the port from the second triangle
        e_slots.setdefault(eab,[]).append(s0)
        e_slots.setdefault(ebc,[]).append(s1)
        e_slots.setdefault(eac,[]).append(s2)
    # iterate over all the port lists collected on the edges
    g_edges, open_ports = [], []
    for s in e_slots.values():
        if len(s) == 2: # 2 ports of different triangles
            g_edges.append((s[0], s[1])) 
        else: # if we have more or less than 2 ports
            open_ports += s # we just send it into free lists
    return v_p, g_edges, open_ports
```

Let's take "triangles=[(10, 20, 30),(20, 40, 30)]" ; First highlight edges via function sid

1st triangle eab = sid(0, (10,20)) => 0 ; ebc = sid(0, (20,30)) => 1 ; eac = sid(0, (10,30)) => 2 ; 2nd triangle eab = sid(1, (20,40)) => 3 ; ebc = sid(1, (40,30)) => 4 ; eac = sid(0, (20, 30)) => 5

Let's give each triangle their number: for 1st triangle t=0 ; for the 2nd triangle t=1

Let's sort vertices in ascending order (loop ```for t, (a,b,c) in enumerate(triangles):```)

1st triangle: eab=(10,20) ; ebc=(20,30) ; eac=(10,30) ; 2nd triangle: eab=(20,40) ; ebc=(40, 30) ; eac=(20,30)

Lets take our edges and add them into vertex-port list (from both triangles): v_p=[ (0,1,2),(3,4,5) ]

Now, when we have full list of vertices for t=0 and t=1, we need to find repeated vertices, the algorithm does it like this: it views every edge and looks at its vertices and assigns a unique number starting from 0 if vertices are repeated, adds them to the same list, here these are 1 and 5: `e_slots[(10, 20)] = [0] ; e_slots[(20, 30)] = [1] ; e_slots[(10, 30)] = [2] ; e_slots[(20, 40)] = [3] ; e_slots[(30, 40)] = [4] ; e_slots[(20, 30)] = [1,5]`

Finally we need define glue place, obviously it is where we have more than 1 edge, if we have it then add it into g_edges and "glue" them

If not, then these will be just ordinary sides of triangles and the last step is to collect everything together and from triangles=[(10, 20, 30),(20, 40, 30)]:

```v_p = [(0,1,2),(3,4,5)] ; g_edges=[1,5] ; open_ports=[0,2,3,4]```


# Section 2.6 | Chain |

chain is the one of the most important slice of dataset generation ; about p_13=0.3 (this is a chance, 30%) and this to for p_31

in foundation of this function we have [Markov chain algorithm](https://en.wikipedia.org/wiki/Markov_chain): P(X_n+1 = x_n+1 | X_n = x_n, X_n-1 = x_n-1, ... , X_0 = x_0) = P(X_n+1 = x_n+1 | X_n = x_n), This algorithm models transitions from one state to another

```python
def chain(base, label, k, p_13 = 0.3, p_31 = 0.3):
    out = [] # create a empty list
    current = base # take graph figure base ; current figure
    e_g = g(current) # calculate g for this starting figure
    for _ in range(k):
        r = random.random() # choose number from 0.0 to 1.0
        if r < p_13: # 30% chance for Pachner move 1/3
            figure = p_1_3(current) 
        elif r < p_13 + p_31: # 30 % Pachner move 3/1
            figure = p_3_1(current)
            if figure is None:
                figure = p_2_2(current)
        else: # 40% chance for Pachner move 2/2
            figure = p_2_2(current)
        if g(figure) == e_g: # g correctness check
            current = figure
        out.append((current, label))
    return out
```

# Section 2.7 | Dataset Generation |

```python
def dataset(k, n=None): # k = total number of examples for g=0 and g=1
    if n is None: 
        n = k // len(spheres)
    out = []
    for b in spheres:
        out += chain(b, 0, n) # generation g=0 (spheres)
    out += chain(torus(3,3), 1, k) # generation g=1 (torus)
    return out # return all objects
```

# Section 2.8 | Converters |

```python
# Convert our tris in naturally for baseline models format (right now for Graph Network)
# Lets take as example tris=[(10, 50, 15), (50, 100, 15)]
def converter_for_gnn(tris):
    tris = relabel(tris) # (10,50,15) => (0,1,2) ; (50, 100, 15) => (1,3,2) (for understand how we got this numbet =>
    # => comeback to relabel func, an example on these tris there)
    num_nodes = max(max(t) for t in tris) + 1 # we got 3 (because we got (2,3) and choose max value) and + 1 = 4
    A = torch.zeros((num_nodes, num_nodes)) # 4 x 4 zeros matrice
    for (u,v,w) in tris:
        A[u,v]=A[v,u]=1.0; A[v,w]=A[w,v]=1.0; A[u,w]=A[w,u]=1.0 # matrix symmetry
        # lets visualize, A=[                     after 1st triangle              after 2nd triangle (we gonna return this)
        #       col0|col1|col2|col3               col0|col1|col2|col3             col0|col1|col2|col3  A.sum (remember this column)
        # row 0 [0.0,0.0, 0.0, 0.0],   <->  row 0 [0.0,1.0, 1.0, 0.0],  <-> row 0 [0.0,1.0, 1.0, 0.0], ==>   [2.0]                     => 2 + 3 + 3 + 2 = 10 ; s=10
        # row 1 [0.0,0.0, 0.0, 0.0],        row 1 [1.0,0.0, 1.0, 0.0],      row 1 [1.0,0.0, 1.0, 1.0], ==>   [3.0] 
        # row 2 [0.0,0.0, 0.0, 0.0],        row 2 [1.0,1.0, 0.0, 0.0],      row 2 [1.0,1.0, 0.0, 1.0], ==>   [3.0] 
        # row 3 [0.0,0.0, 0.0, 0.0]         row 3 [0.0,0.0, 0.0, 0.0]       row 3 [0.0,1.0, 1.0, 0.0]  ==>   [2.0]
        # ], pick first triangle (0,1,2), lets understand this by that A[u(row),v(column)], first var its a row, second is column
        # take it and lets complete this cycle for 1st triangle (0,1,2):  A[0(row),1(col)] = A[1,0] = 1.0 ; A[1,2] = A[2,1] = 1.0 ; A[0,2] = A[2,0] = 1.0
        # second triangle (1,3,2): A[1,3] = A[3,1] = 1.0 ; A[3,2] = A[2,3] = 1.0 ; A[1,2] = A[2,1] = 1.0 nothing change we already have it filled by 1.0
    s = A.sum() # sum of all elements in A, sum of every row (check result upper)
    degree = (A.sum(dim=1, keepdim=True) / (s + 1e-8)) # dim=1 says: sum rows and make column (dont sum it all in 1 number), =>
    # => we can see it upper, and divide it by the total sum (s), after it degree gonna looks like this [[0.2], [0.3], [0.3], [0.2]]
    L = torch.cat([degree, torch.ones(num_nodes, 1)], dim=1) # torch.ones(num_nodes,1) says: create a matrix with num_nodes rows and 1 column, in our example its 4 x 1 => [[1.0], [1.0], [1.0], [1.0]] (let this matrix be "B")
    # torch.cat do one thing, it stands for concatenate, take a list of different tensors (matrices) and glue them together to form one single =>
    # => bigger tensor (if dim=1), if dim=0 we make 1 big column by take rows from one matrix and add rows to another
    # degree + B => L = [[0.2, 1.0], [0.3,1.0], [0.3,1.0], [0.2,1.0]]
    return A / (s + 1e-8), L # A / 10 (we got matrix B), L

# Convert our tris in naturally for baseline models format #2 (right now for Tensor Network)
# Lets take as example same tris=[(10, 50, 15), (50, 100, 15)]
def converter_for_tnn(tris, N=64):
    tris = relabel(tris) # (10,50,15) => (0,1,2) ; (50, 100, 15) => (1,3,2) (for understand how we got this numbet - comeback to relabel func, an example on these tris there)
    A = torch.zeros((N, N)) # N x N filled by zeros matrice
    for (u, v, w) in tris:
        A[u,v]=A[v,u]=1.0; A[v,w]=A[w,v]=1.0; A[u,w]=A[w,u]=1.0
        # by this method what we used upper for gnn, just dont want to clutter the code, keep in mind that this is the same circuit as in converter_for_gnn
    deg = A.sum(dim=1) # same function as in converter_for_gnn ; for next line lets take deg=[2.0, 3.0, 3.0, 2.0, 0.0] - list with indexes from 0-4 (lets designate it by i_0..4)
    deg2 = torch.where(deg > 0, deg.pow(-0.5), torch.zeros_like(deg)) 
    # how it works? Lets take our deg and look at "torch.zeros_like", it means: create a new vector with size LIKE deg 
    # our deg size is 5 (5 numbers) => [0.0, 0.0, 0.0, 0.0, 0.0]
    # what means deg.pow(-0.5) - this raises every number in deg to the power of ^-0.5 ; like x^-0.5 or 1/sqrt x
    # lets calculate our deg with all this: 1/sqrt 2.0 = 0.7071 ; 1/sqrt 3.0 = 0.5774 ; 1/sqrt 0 = inf ====> [0.7071, 0.5774, 0.5774, 0.7071, inf] 
    # but we have another torch function, "torch.where", by a name of this we can factually undestand what it does =>
    # => lets construct it in another format: deg2 = torch.where(deg>0, A, B), it works like that
    # its filter checklist that goes through the list element-by-element: "If condition (deg>0) is true, grab the value from A else from B"
    # i_0 = 2 > 0 True (A) ; i_1 = 3 > 0 True (A) ; i_2 = 3 > 0 True (A) ; i_3 = 2 > 0 True (A) ; i_4 = 0 > 0 False (B)
    # Final result: [0.7071, 0.5774, 0.5774, 0.7071, 0.0 (without inf!)]
    D = torch.diag(deg2) # torch.diag takes that flat list of numbers and scatters them perfectly down the main diagonal of a blank N x N matrix
    A_norm = D @ A @ D # symmetric normalized: D^-0.5 A D^-0.5 ; scale rows and columns
    return A_norm # return balanced and normalized adjacency matrix
```

# Section 3 | Summary |

Current stage and current PoC test don't give all understanding about OCSSN's power, because of that, the results presented here should be viewed as preliminary

All results can be found [here](https://github.com/kaifczxc-lab/OCSSN/tree/SiritoriProjects/summary-tests-logs)

For analysis the author ran 4 tests with 4 different datasets

Test Description: binary classification "sphere or torus" with Udo Pachner Moves conditions, models need to correctly identify the topological type of surface (genus), despite the fact that, the triangulation was repeatedly changed by Pachner moves. The current test checks precisely topological invariance

Complexity can be classified differently, but based on the results we can say for sure:

(In the analysis, only the datasets that were used for holdout are considered)


---


### Full characteristics of datasets during testing (with reinitialization of models)

| Characteristics                      | Easy ([seed=55](https://github.com/kaifczxc-lab/OCSSN/blob/SiritoriProjects/summary-tests-logs/seed_55_model_with_reinitialization.txt))                           | Easy ([seed=34](https://github.com/kaifczxc-lab/OCSSN/blob/SiritoriProjects/summary-tests-logs/seed_34_with_reinitialization.txt))                           | Hard ([seed=53](https://github.com/kaifczxc-lab/OCSSN/blob/SiritoriProjects/summary-tests-logs/seed_53_model_with_reinitialization.txt))                        | Hard ([seed=92](https://github.com/kaifczxc-lab/OCSSN/blob/SiritoriProjects/summary-tests-logs/seed_92_model_with_reinitialization.txt))                                |
|--------------------------------------|------------------------------------------|------------------------------------------|---------------------------------------|-----------------------------------------------|
| Intersection `mesh_tris` torus/sphere| Minimal: torus 18–46, spheres 4–28       | Minimal: torus 18–48, spheres 2–22       | Strong: torus 18–58, hexa up to 44   | Very strong: hexa=34 coincides with torus      |
| Classes with `no-op`                 | Only hexa (22.7%)                        | hexa (19.7%), octa (3.0%)                | None                                  | hexa (7.6%), octa (1.5%)                      |
| Torus fallbacks `3-1→2-2`            | 21 (very many)                           | 17 (many)                                | 4 (few)                               | 11 (moderate)                                 | 
| Spheres Fallbacks                    | icosa=3, hexa=0, octa=2                  | icosa=2, hexa=2, octa=2                  | icosa=9, hexa=1, octa=0               | icosa=4, hexa=0, octa=2                       |
| Final size of spheres                | 10, 4, 22 (heterogeneous)                | 10, 2, 12 (very small vs torus)          | 20, 44, 18 (hexa huge)                | 10, 34, 22 (hexa equals torus)                |
| OCSSN Generalization (train → val)   | train ~60–70% → val ~79% (Good)          | train ~60–70% → val ~87% (Excellent)     | train ~60–70% → val ~62% (low ceiling)| train ≥80% → val ~62% (overfitting)           |

### OCSSN growth relative to other models (with reinitialization of models)

| Dataset (val seed) | Complexity | OCSSN vs TNN | OCSSN vs GNN |
|--------------------|------------|--------------|--------------|
| 53                 | Hard       | –0.50%       | +2.33%       |
| 55                 | Easy       | –3.59%       | +28.65%      |
| 34                 | Easy       | +34.42%      | +17.76%      |
| 92                 | Hard       | +12.24%      | +15.86%      |
| **Average**        |            | **+10.64%**  | **+16.15%**  |

---

### Full characteristics of datasets during testing (without reinitialization of models)

| Characteristics                      | Easy ([seed=34](https://github.com/kaifczxc-lab/OCSSN/blob/SiritoriProjects/summary-tests-logs/seed_34_without_reinitialization.txt))                           | Moderate ([seed=55](https://github.com/kaifczxc-lab/OCSSN/blob/SiritoriProjects/summary-tests-logs/seed_55_without_reinitialization.txt))                       | Hard ([seed=53](https://github.com/kaifczxc-lab/OCSSN/blob/SiritoriProjects/summary-tests-logs/seed_53_without_reinitialization.txt))                         | Hard ([seed=92](https://github.com/kaifczxc-lab/OCSSN/blob/SiritoriProjects/summary-tests-logs/seed_92_without_reinitialization.txt))                             |
|--------------------------------------|------------------------------------------|------------------------------------------|----------------------------------------|--------------------------------------------|
| Intersection `mesh_tris` torus/sphere| Minimal: torus 18–48, spheres 2–22       | Minimal: torus 18–46, spheres 4–28       | Strong: torus 18–58, hexa up to 44     | Very strong: hexa=34 coincides with torus  |
| Classes with `no-op`                 | hexa (19.7%), octa (3.0%)                | Only hexa (22.7%)                        | None                                   | hexa (7.6%), octa (1.5%)                   |
| Torus fallbacks `3-1/2-2`            | 17 (many)                                | 21 (very many)                           | 4 (few)                                | 11 (moderate)                              | 
| Spheres Fallbacks                    | icosa=2, hexa=2, octa=2                  | icosa=3, hexa=0, octa=2                  | icosa=9, hexa=1, octa=0                | icosa=4, hexa=0, octa=2                    |
| Final size of spheres                | 10, 2, 12 (very small)                   | 10, 4, 22 (heterogeneous)                | 20, 44, 18 (hexa huge)                 | 10, 34, 22 (hexa equals torus)             |
| OCSSN Generalization (train → val)   | train ~60–70% → val ~84% (Good, unstable)| train ~60–70% → val ~81% (Good, dips)    | train ~60–70% → val ~62% (low ceiling) | train ≥80% → val ~64% (overfitting)        |

### OCSSN growth relative to other models (without reinitialization of models)

| Dataset (val seed) | Complexity | OCSSN vs TNN | OCSSN vs GNN |
|--------------------|------------|--------------|--------------|
| 53                 | Hard       | –1.1%        | –1.4%        |
| 55                 | Moderate   | –4.4%        | +30.4%       |
| 34                 | Easy       | +29.0%       | +33.5%       |
| 92                 | Hard       | +6.3%        | +13.7%       |
| **Average**        |            | **+7.45%**   | **+19.05%**  |

---

The author's analytical conclusion from results are: 

* OCSSN gives a stronger result where other models **fail to generalize**, for example: seed=33 & seed=92. This confirms the **robustness of the proposed model** in the surface classification problem

# Section 4 | Limitations & Problems |

Due to the fact that the author works alone and the code has not been tested, the number of bugs and limitations is unknown, but here are the most superficial ones

* **Dispersion**: If the reader has already looked through the architecture test files with the postscript "without_reinitialization", then most likely he could notice that dispersion and std can sometimes be large

* **Current Test**: Due to the fact that the OCSSN is on PoC stage **we only have "toy" testing**. Solution: in future iterations the author will look for other types of real applied tests

* **torch.linalg.inv goes singular when calculating b_inv**: This problem was **mentioned earlier** in Section 1.1., it problem is alleviated by exponentiating eps_r, The main issue is that after a short training period (2 seeds), in half of the cases it produces an error about the number going into singularity when calculating b_inv

* **no-op**: Even when trying to fix this error, it sometimes recurs; sometimes, for some objects, the **no-op rate can reach up to 50%**. Solution: for now, the simplest fix is to restart with a different seed and monitor the statistics

* **State-sum numerical instability**: [report](https://github.com/kaifczxc-lab/OCSSN/blob/SiritoriProjects/summary-tests-logs/h_raw_norm_instability.txt) ; As we can see, raw h has a lot of problems with numerical instability, it probably can be alleviated by h_norm, but normalization **cannot repair** the problem of gradient instability. Solution: A solution may be found in future iterations

* **Non-strict topological invariance**: As was written before, the author's conclusion (see Section 3) discusses dispersion. This problem needs to be described in more detail because it is **an open question of this work**, the solution to this problem will lead us to a non-learning static algorithm, at the current PoC stage of OCSSN this problem is both critical and, at the same time, a factor for future growth. Formulation оf open question: in future iterations, the author needs to add
    
    * A mechanism that ensures **strict invariance** (i.e. maybe, closed state-sum, refusal to open ports)

    * Do a learning **stabilization and optimization**


The author will consider a solution, but also welcomes any help from interested parties. Even a small correction from a knowledgeable person would be very valuable to the author

# Section 5 | Future Work |

The author want to going deeper into Topology DL field

* Current instability problem will not be left without an attempt at a **solution**, but the author **honestly admits that he doesn't yet know exactly how to solve the problem**

* Current Research Report will be on PoC stage **not always**, more testing and more results analytics will be added

* Further development of the author's skills in next works will be in the direction **Topological Data Analysis in Topological DL**

* Further development of this idea will lead to generalization to **3D TQFT**

# Section 6 | Gallery |

If you want to see more examples with other shapes, you can do this by changing the octahedron here to any other available shape (or you can even add your own)

## Pachner 2-2 Move Visualization on Octahedron

<img width="48%" alt="before(2)" src="https://github.com/user-attachments/assets/80bdf993-19d7-4802-b60d-f88dbb3de3a5" /> <img width="48%" alt="after(1)" src="https://github.com/user-attachments/assets/c92dbecf-284f-4deb-a959-0c5877f8af82" />  


---

## Pachner 1-3 Move Visualization on Octahedron

<img width="48%" alt="before(2)" src="https://github.com/user-attachments/assets/80bdf993-19d7-4802-b60d-f88dbb3de3a5" /> <img  width="48%" alt="after(1)" src="https://github.com/user-attachments/assets/3193a312-56a9-4b23-b667-e2f2ebe88851" />

---

## Pachner 3-1 Move

We translate the figure into 1-3 (as above) and the move 3-1 returns us the same basic octahedron, there is generally no point in visualizing it here, if the reader wants to check, then everything is in the code