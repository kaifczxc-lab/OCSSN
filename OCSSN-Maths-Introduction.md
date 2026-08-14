(These are the first commits, the document is being translated here, it was not originally written in English)

This document can be helpful in understanding the [Open-Closed State-sum Network](https://github.com/kaifczxc-lab/OCSSN)

Author: [siritoriyowai](https://github.com/kaifczxc-lab)

The connection between the code and the mathematics can be found in the main README document, specifically in [Section 1.1](https://github.com/kaifczxc-lab/OCSSN/tree/SiritoriProjects#section-11--a-complete-analysis-of-each-variable-) & [Section 2](https://github.com/kaifczxc-lab/OCSSN/tree/SiritoriProjects#section-2--description-of-every-function-)

This is not complete educational material. It contains the author's notes and strict definitions from sources. However, if the reader wants to gain a deeper understanding of the topic, they should study the sources that the author referenced throughout this document

You can find the meaning of the highlighted words and definitions in the reference section at the end of this document. Each such definition will be marked (1)–(10) and you can find it in the reference book using the same number.

## Table of contents

- [Section 0.1: Simplicial Complex]()
- [Section 0.2: Piecewise Linear Manifolds]()
- [Section 0.3: Euler's Characteristics]()
- [Section 1: Manifolds Triangulation]()
  - [Section 1.1: Pachner Moves]()
- [Additional Section 1: Very basics of category theory]()
  - [Additional Section 1.1: Functors]()
- []
# Section 0.1 | Simplicial Complex |

Material from: lectures and author's notes

Let's begin with simplices:

* A zero-dimensional simplex is a point

* A one-dimensional simplex is a segment

* A two-dimensional simplex is a triangle

* A three-dimensional simplex is a tetrahedron

We can glue these objects along edges and faces on a manifold, i.e., we cannot take a triangle and glue its vertex to the middle of an edge

(here i need to put drawing of it)

The minimal geometric figure of dimension n (n-simplex) is defined by the minimal set of independent vertices - and there are always exactly n + 1 of them (to go from a point to a segment, you need to take two points, to go from a segment to a triangle, you need three segments)

To obtain an (n-1)-dimensional face of a simplex, we take all its vertices except one

For example, let n = 1. The simplex has n + 1 = 2 vertices. Its (n-1)-dimensional faces are faces of dimension 0 — two points that form the segment

## Section 0.2 | Piecewise Linear Manifolds | 

Let's move on to piecewise linear manifolds / PL-Manifolds

A linear triangulation is a partition of the figure into triangles such that each triangle is an affine image of a standard simplex

The space must have such a triangulation if we are talking about PL-Manifolds, and the main factor is the affineness of the space (in which barycentric coordinates are preserved) (ОБЯЗАТЕЛЬНО В СПРАВОЧНИКЕ ОБЪЯСНИТЬ ЧТО ТАКОЕ АФФИННОСТЬ ПРОСТРАНСТВА!!!!)

In general, the definition looks like this, suppose we have two affine spaces $$R^m and R^n$$, a subset V ⊂ $$R^m$$, and a map $$f: V \to R^n$$. Then f is piecewise linear (PL) if there exists a linear triangulation of V such that the restriction of f to each simplex is an affine map.

Then: $$f: V \to R^n$$ is piecewise linear if there exists a linear triangulation of V such that f is affine on every simplex

## Section 0.3 | Euler's Characteristics | 

It is a simple integer that describes the shape of an object as a whole, ignoring how exactly it is curved, stretched, or how many triangles (simplices) it is broken into.

If we triangulate a two-dimensional surface (for example, by gluing a torus from triangles), the formula is:

χ = V - E + F

Where:

* V (Vertices) — number of vertices (zero-dimensional simplices)

* E (Edges) — number of edges (one-dimensional simplices)

* F (Faces) — number of faces (two-dimensional simplices)

This formula is used in the code (see. [function g](https://github.com/kaifczxc-lab/OCSSN/blob/f4f1e2b658d7dd70b371074b770499652b263b47/fssn_build_main.py#L56))

---


Main material from: 

https://en.wikipedia.org/wiki/Pachner_moves (and from there you can get to the original source, the article by Udo Pachner)

# Section 1 | Manifolds Triangulation | 

A simplicial complex is combinatorial structure that contains edges, vertices, faces and simplices of higher dimensions, where each simplex define as the convex hull of a finite set of affinely independent points in some Euclidean space

These simplices are glued along faces, so that their intersection is either empty or a common face

Manifolds triangulation - its a simplicial complex, **homeomorphic**(2) to a manifold, with the additional property that the **link**(3) of each simplex in this complex is itself a triangulated sphere

In piecewise linear (PL) topology a triangulations encode PL structures on manifolds by defining a finite decomposition into simplices with affine mappings on each

Pachner moves provide a way to move between equivalent triangulations of the same manifold.

## Section 1.1 | Pachner Moves |

### Main definition

Pachner moves represent a set of local combinatorial operations defined on the simplicial triangulations of piecewise-linear (PL) manifolds, allowing one such triangulation to be transformed into another equivalent one.

These moves consist of replacing the star of a simplex with the star of the dual simplex in such a way as to preserve the structure of the manifold, and such that, in dimension n, there are n+1 such moves

OCSSN is based on the 2D case, because we have the following moves: [1-3](https://github.com/kaifczxc-lab/OCSSN/blob/f6fa2d761a5a6644ff239636f27ffd913a94342d/fssn_build_main.py#L140), [3-1](https://github.com/kaifczxc-lab/OCSSN/blob/f6fa2d761a5a6644ff239636f27ffd913a94342d/fssn_build_main.py#L148), [2-2](https://github.com/kaifczxc-lab/OCSSN/blob/f6fa2d761a5a6644ff239636f27ffd913a94342d/fssn_build_main.py#L109). Note that applying 3-1 after 1-3 to the same figure returns it to its original position

Before the main theorem let's introduce the concept of: "star equivalence (star subdivision and inverse operations)":

* Let us have a simplicial complex, a surface made of triangles, then the star subdivision is a local operation where we take a simplex and inside it we create a new vertex, connect it to all the vertices of this simplex, to imagine this, suppose we have a two-dimensional simplex, then, after applying this operation to one triangle, we obtain three triangles ; The inverse operation means that from these three triangles we return to one triangle again

* Two different triangulations (that is, two ways to split an object into simplexes) are called star equivalent if we can transform one into the other in a finite number of steps using only star subdivision and their inverse operations

* Investigation: It has been proven that if two complexes are star equivalent, then they define the same topological space

What Udo Pachner's theorem states: two closed combinatorial n-manifolds are bistellarly equivalent (connected by a finite sequence of Pachner moves and simplicial isomorphisms) if and only if they are stellarly equivalent

Formally, in a triangulation of a d-dimensional manifold, a Pachner move of type (p,q), where p + q = d + 2, removes the **star** of a (p-1)-simplex - consisting of p d-simplices whose common intersection is this (p-1)-simplex - and replaces it with the star of a (q-1)-simplex, consisting of q d-simplices. This replacement is possible only if the **link**(3) of the original (p-1)-simplex is **combinatorially isomorphic**(1) to a (q-2)-sphere, which guarantees that the star forms a combinatorial d-ball and the move preserves the PL structure of the manifold. A move of type (q,p) reverses this process, making the operations reversible

In two-dimensional exists two types of moves: (2,2) diagonal **flip**, (1,3) and inverse (3,1). They correspond to the general scheme of bistellar equivalence, where for dimension n = 2 the perestroikas are denoted by (p,q) с p + q = n + 2 = 4

A (2,2) move acts on two adjacent triangles sharing a common interior edge and forming a quadrilateral region with four boundary edges, the move replaces the diagonal, that is, imagine a rhombus, A and B are opposite, C and D are opposite, there is a diagonal between A and B, a (2,2) flip changes the diagonal from AB to CD and vice versa, and by imagining this one can see that the number of triangles does not change, reader can see what it looks like [here](https://github.com/kaifczxc-lab/OCSSN/tree/SiritoriProjects#section-6--gallery-)

(1,3) and (3,1) moves replace one triangle with three and three triangles with one, in the end the boundaries do not change and we simply add a star vertex to the middle of the triangle and draw edges to the corners, which turns one triangle into three, but the boundaries stay the same, meaning we can glue these three back into one

### Properties

Topological invariance

Pachner moves establish it, preserving the piecewise linear homeomorphism type of manifold triangulations. In particular, each individual Pachner move acts locally as a PL homeomorphism:

(The following words will just be a proof, if you do not understand it is better for you to just jump to the main result of this property)

For a bistellar move replacing the star of a k-simplex s in an n-manifold, where the link Lk(s) is combinatorially an (n-k-1)-sphere, the operation replaces s * Lk(s) with ∂s * B(s), where B(s) is a **dual (n-k)-ball**, combinatorially homeomorphic to the cone over the link

The main result, known as Pachner's theorem, states that two PL triangulations of the same closed n-manifold are connected by a finite sequence of Pachner moves if and only if they are PL homeomorphic

### Result

Why do we need this in OCSSN? The main reason is manifold classification

Pachner transformations play an important role in manifold classification, especially in low dimensions, by establishing that any two triangulations of the same piecewise linear (PL) manifold are related by a finite sequence of these local transformations


# Additional Section 1 | Very basics of category theory |

Main information material: author notes

Recommented material for initial familiarization: [Tom Leinster (2016): Basic Category Theory](https://arxiv.org/abs/1612.09375)

This section is only for repeating (we need that in future sections), the author does not set as his initial goal to fully explain the categories

---

Let X - topological category ; G - group category

{X} -> {G} 

We have moved from the category of topology to the categories of group theory

But, what is category means?

A category is a mapping that imposes a structure on its mapping, preserving this structure between two different sets of objects (even between a topology category and a group category).

---

Category K

1) Obj_K (objects set of category K ; class)

2) A,B (topological spaces) => A,B ∈ Obj_K (We need all possible mappings between two objects, we must find all mappings that show the complete set A or B and such mappings are called morphisms)

Formally

* ∀A,B ∈ Obj_K ∃Hom_K(A,B) (for any A,B exists set of maps between A,B)

3) The superposition operation need to be exist (defined)

* ∀f ∈ Hom_K(A,B), g ∈ Hom_K(B,C) ∃h = g ∘ f ∈ Hom_K(A,C) (that is, we go from point A straight to C because there is the same mapping B between them)

4) id for any object in K 

* ∀A ∈ Obj_K ∃id_A ∈ Hom_K(A,A) 

5) mappings must be associative

* f_1 ∘ (f_2 ∘ f_3) = (f_1 ∘ f_2) ∘ f_3

6) Multiplication on id - nothing change

id ∘ f = f ∘ id = f

---

*How does it work on specific categories?*

Let K_1 = category of topological spaces (Obj_K the class of all topological spaces)

Hom - all possible continuous maps 

composition is defined as usual function composition 

identity map as usual identity map 

associativity holds right away

Let K_2 = category of groups (Obj_K set of all possible groups)

Hom_K = set of homomorphisms between groups 

composition of homomorphisms 

identity is the usual identity map 

associativity holds

the identity law also holds 

---

## Additional Section 1.1 | Functors |

Let A, B be some categories, what is a mapping (functor) between A -> B and what should it include

This mapping should translate objects of category A into objects of category B

F: A -> B 

1) ∀X ∈ Ob_A -> F(X) ∈ Ob_B

2) (f ∈ Hom_A(X,Y): A -> B) -> (F(f) ∈ Hom_B(F(X), F(Y)): F(A) -> F(B))

Axioms

3) F(id_X) = id_F(X)

4.1) F(f ∘ g) = F(f) ∘ F(g)

4.2) F(f ∘ g) = F(g) ∘ F(f)

Such mappings that include three conditions (1,2,3) are called functors, and if 4.1) exists, then it is a covariant functor, and if 4.2) it is a contravariant functor

---

**Quick reference**

Category K contains

Objects Ob_A

∀A,B ∈ Ob_A ∃Hom_A(A,B)

∀f ∈ Hom_A(A,B), g ∈ Hom_A(B,C) ∃h = g ⋅ f ∈ Hom_A(A,C)

f ∈ Hom_A: A -> B

g ∈ Hom_A: B -> C 

h ∈ Hom_A: g -> f

functor is:

1. ∀X ∈ Ob_A -> F(X) ∈ Ob_B

2. (f∈Hom_A(A,B): A -> B) -> (F(f) ∈ Hom_A_2(F(A),F(B)): F(A) -> F(B))

3. F(id_A) = id_F(A)

If we satisfy these conditions, then this is a functor, next come the formulas for defining a covariant functor or contravariant functor

F(f * g) = F(f) * F(g) covariant functor

F(f ∘ g) = F(g) ∘ F(f) contavariant functor

---

# Section M | Commutative Frobenius Algebras |

Source: ["Frobenius Algebras and 2D Topological Quantum Field Theories" By Joachim Kock](https://math.mit.edu/~hrm/palestine/koch-frobenius-algebras.pdf)

Chapter 2 Frobenius algebras. Page 78

The explanation in this document will be based on the categorical view, we will not consider explanations using linear algebra