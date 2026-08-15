This document can be helpful in understanding the [Open-Closed State-sum Network](https://github.com/kaifczxc-lab/OCSSN)

Author: [siritoriyowai](https://github.com/kaifczxc-lab)

The connection between the code and the mathematics can be found in the main README document, specifically in [Section 1.1](https://github.com/kaifczxc-lab/OCSSN/tree/SiritoriProjects#section-11--a-complete-analysis-of-each-variable-) & [Section 2](https://github.com/kaifczxc-lab/OCSSN/tree/SiritoriProjects#section-2--description-of-every-function-)

This is not complete educational material. It contains the author's notes and strict definitions from sources, some statements may require independent verification. However, if the reader wants to gain a deeper understanding of the topic, they should study the sources that the author referenced throughout this document

You can find the meaning of the highlighted words and definitions in the reference section at the end of this document. Each such definition will be marked (1)–(10) and you can find it in the reference book using the same number.

## Table of contents

- [Section 0.1: Simplicial Complex](https://github.com/kaifczxc-lab/OCSSN/blob/SiritoriProjects/OCSSN-Maths-Introduction.md#section-01--simplicial-complex-)
- [Section 0.2: Piecewise Linear Manifolds](https://github.com/kaifczxc-lab/OCSSN/blob/SiritoriProjects/OCSSN-Maths-Introduction.md#section-02--piecewise-linear-manifolds-)
- [Section 0.3: Euler's Characteristics](https://github.com/kaifczxc-lab/OCSSN/blob/SiritoriProjects/OCSSN-Maths-Introduction.md#section-03--eulers-characteristics-)
- [Section 1: Manifolds Triangulation](https://github.com/kaifczxc-lab/OCSSN/blob/SiritoriProjects/OCSSN-Maths-Introduction.md#section-1--manifolds-triangulation-)
    - [Section 1.1: Pachner Moves](https://github.com/kaifczxc-lab/OCSSN/blob/SiritoriProjects/OCSSN-Maths-Introduction.md#section-11--pachner-moves-)
- [Additional Section 1: Very basics of category theory](https://github.com/kaifczxc-lab/OCSSN/blob/SiritoriProjects/OCSSN-Maths-Introduction.md#additional-section-1--very-basics-of-category-theory-)
    - [Additional Section 1.1: Functors](https://github.com/kaifczxc-lab/OCSSN/blob/SiritoriProjects/OCSSN-Maths-Introduction.md#additional-section-11--functors-)
- [Section 2: Commutative Frobenius Algebras](https://github.com/kaifczxc-lab/OCSSN/blob/SiritoriProjects/OCSSN-Maths-Introduction.md#section-2--commutative-frobenius-algebras-)
    - [Section 2.1: What is a symmetrical monoidal category?](https://github.com/kaifczxc-lab/OCSSN/blob/SiritoriProjects/OCSSN-Maths-Introduction.md#section-21-what-is-a-symmetrical-monoidal-category-)
    - [Section 2.2: What is a symmetric monoidal functor $Z: 2Cob \to Vect_K$?](https://github.com/kaifczxc-lab/OCSSN/blob/SiritoriProjects/OCSSN-Maths-Introduction.md#section-22--what-is-a-symmetric-monoidal-functor-z-2cob-to-vect_k-)
    - [Section 2.3: What is a cobordisms/2Cob?](https://github.com/kaifczxc-lab/OCSSN/blob/SiritoriProjects/OCSSN-Maths-Introduction.md#section-23--what-is-a-cobordisms2cob-)
    - [Section 2.4: Categorical View on Commutative Frobenius Algebras](https://github.com/kaifczxc-lab/OCSSN/blob/SiritoriProjects/OCSSN-Maths-Introduction.md#section-24--categorical-view-on-commutative-frobenius-algebras-)
- [Section 3: Reference Section](https://github.com/kaifczxc-lab/OCSSN/blob/SiritoriProjects/OCSSN-Maths-Introduction.md#section-3--reference-section-)



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

The space must have such a triangulation if we are talking about PL-Manifolds, and the main factor is the affineness of the space (in which barycentric coordinates are preserved)

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

* Fact: It has been proven that if two complexes are star equivalent, then they define the same topological space

What Udo Pachner's theorem states: two closed combinatorial n-manifolds are bistellarly equivalent (connected by a finite sequence of Pachner moves and simplicial isomorphisms) if and only if they are stellarly equivalent

Formally, in a triangulation of a d-dimensional manifold, a Pachner move of type (p,q), where p + q = d + 2, removes the **star** of a (p-1)-simplex - consisting of p d-simplices whose common intersection is this (p-1)-simplex - and replaces it with the star of a (q-1)-simplex, consisting of q d-simplices. This replacement is possible only if the **link**(3) of the original (p-1)-simplex is **combinatorially isomorphic**(1) to a (q-2)-sphere, which guarantees that the star forms a combinatorial d-ball and the move preserves the PL structure of the manifold. A move of type (q,p) reverses this process, making the operations reversible

In the two-dimensional case, there exist two types of moves:: (2,2) diagonal **flip**, (1,3) and inverse (3,1). They correspond to the general scheme of bistellar equivalence, where for dimension n = 2 the moves are denoted by (p,q) with p + q = n + 2 = 4

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

Let X denote the category of topological spaces and G the category of groups

the map {X} -> {G} represents the transition from topology to group theory

But, what is category means?

A category consists of objects and morphisms between them, these morphisms must be composable and must preserve the structure of the objects

---

Category K

1) $Obj_K$ (objects set of category K ; class)

2) A,B (topological spaces) => A,B ∈ $Obj_K$ (We need all possible mappings between two objects, we must find all mappings that show the complete set A or B and such mappings are called morphisms)

Formally

* $∀A,B ∈ Obj_K ∃\mathrm{Hom}_K(A,B)$ (for any A,B exists set of maps between A,B)

3) Composition must be defined

* $∀f ∈ \mathrm{Hom}_K(A,B), g ∈ Hom_K(B,C) ∃h = g ∘ f ∈ Hom_K(A,C)$ (that is, we go from point A straight to C because there is the same mapping B between them)

4) id for any object in K 

* $∀A ∈ Obj_K ∃id_A ∈ \mathrm{Hom}_K(A,A)$

5) mappings must be associative

* $f_1 ∘ (f_2 ∘ f_3) = (f_1 ∘ f_2) ∘ f_3$

6) Multiplication on id - nothing change

* id ∘ f = f ∘ id = f

---

*How does it work on specific categories?*

**Topological spaces**

Let $K_1$ = category of topological spaces ($\mathrm{Obj}_{K_1}$ the class of all topological spaces)

$\mathrm{Hom}_{K_1}$ - all possible continuous maps

composition is defined as usual function composition

identity map as usual identity map

associativity holds right away


**Groups**

Let $K_2$ = category of groups ($\mathrm{Obj}_{K_2}$ set of all possible groups)

$\mathrm{Hom}_{K_2}$ = set of homomorphisms between groups

composition of homomorphisms

identity is the usual identity map

associativity holds

the identity law also holds

---

## Additional Section 1.1 | Functors |

Let A, B be some categories, what is a mapping (functor) between $A \to B$ and what should it include

This mapping should translate objects of category A into objects of category B

$F: A \to B$

1) $∀X ∈ Ob_A \to F(X) ∈ Ob_B$

2) 

$$
(f \in \mathrm{Hom}_A(A,B): A \to B) \to (F(f) \in \mathrm{Hom}_{B}(F(A),F(B)): F(A) \to F(B))
$$

Axioms

3) $F(id_X) = id_F(X)$

4.1) $F(f ∘ g) = F(f) ∘ F(g)$

4.2) $F(f ∘ g) = F(g) ∘ F(f)$

Such mappings that include three conditions (1,2,3) are called functors, and if 4.1) exists, then it is a covariant functor, and if 4.2) it is a contravariant functor

---

**Quick reference**

Category K contains

Objects $Ob_A$

$∀A,B ∈ Ob_A ∃Hom_A(A,B)$

$∀f ∈ Hom_A(A,B), g ∈ Hom_A(B,C) ∃h = g ⋅ f ∈ Hom_A(A,C)$

$f ∈ Hom_A: A \to B$

$g ∈ Hom_A: B \to C $

$h = g ∘ f ∈ Hom_C(A, C)$

functor is:

1. $∀X ∈ Ob_A \to F(X) ∈ Ob_B$

2.

$$
(f \in \mathrm{Hom}_A(A,B): A \to B) \to (F(f) \in \mathrm{Hom}_{B}(F(A),F(B)): F(A) \to F(B))
$$

3. $F(id_A) = id_F(A)$

If we satisfy these conditions, then this is a functor, next come the formulas for defining a covariant functor or contravariant functor

$F(f ∘ g) = F(f) ∘ F(g)$ covariant functor

$F(f ∘ g) = F(g) ∘ F(f)$ contravariant functor

---

# Section 2 | Commutative Frobenius Algebras |

Source: ["Frobenius Algebras and 2D Topological Quantum Field Theories" By Joachim Kock](https://math.mit.edu/~hrm/palestine/koch-frobenius-algebras.pdf)

Chapter 2 Frobenius algebras. Page 78

The explanation in this document will be based on the categorical view, we will not consider explanations using linear algebra

---

## Section 2.1 |What is a symmetrical monoidal category? |

It is a category C equipped with:

* A bifunctor $⊗: C \times C \to C$, called the tensor product.

* A unit object $I ∈ Ob(C)$

* Three natural isomorphisms, expressing the fact that the tensor product operation
    
    * associative: there exists a natural isomorphism $$\alpha$$ (the associator)
    
    $$\alpha_{A,B,C}: (A ⊗ B) ⊗ C \to A ⊗ (B ⊗ C)$$

    * unital: exist two natural isomorphisms $$\lambda$$ and $$\rho$$, $$\lambda_A: I ⊗ A \to A$$

(There are also some additional conditions, more information can be found [here](https://en.wikipedia.org/wiki/Monoidal_category) or on page 138 of the [source](https://math.mit.edu/~hrm/palestine/koch-frobenius-algebras.pdf))

Thus, all this is defined as the triple $$(C, ⊗, I)$$

A monoid in a monoidal category is an object A ∈ Ob(C) equipped with two morphisms:

* Multiplication $$u: A ⊗ A \to A$$

* Unit $$n: I \to A$$

Now that we have the concept of a monoidal category, we can move on to the concept of a monoidal functor

## Section 2.2 | What is a symmetric monoidal functor $$Z: 2Cob \to Vect_K$$? |

A functor is a set of rules for translating elements from one object to another

$∀A ∈ Obj_2Cob \to F(A) ∈ Obj_Vect_K$

The functor also translates morphisms, in this case

In 2Cob, objects are closed oriented (n-1)-manifolds (for 2Cob, these are simply circles), the morphisms are a operations with these circles (pairs of pants, cylinder)

In $Vect_K$, objects are vector spaces (more often over a field of complex numbers), and morphisms are linear maps

What does the functor do in this situation? It assigns a vector space to each object, and tensor products to the morphisms of 2Cob

What does monoidal mean?, comes from the word monoid, which means it's logical to imagine that it places objects next to each other (a side-by-side union of elements). In the 2Cob category, this is a disjoint union ⊔, $$S^1 ⊔ S^1$$, in the $Vect_K$ category, this will be a tensor product $$V ⊗ V$$

It looks like this: $$Z(S^1 ⊔ S^1) = Z(S^1) ⊗ Z(S^1) = V ⊗ V$$

What does "symmetric" mean here? It allows one to twist the expression, say, from $$A ⊔ B \to B ⊔ A$$ ; or $$u ⊗ w \to w ⊗ u$$


## Section 2.3 | What is a cobordisms/2Cob? |

Cobordisms: objects are closed oriented (n-1)-manifolds, a map from Σ to Σ' is a oriented n-manifold M, where the enter boundary is Σ and exit boundary is Σ' (like a ways in segment I = [0,1]) 
    
(Cobordism M defined with accurate to diffeomorphism, motionless on the edge)
    
Monoidal category: ($$2Cob, ⊔, ∅$$)

A toy example: cylinder Σ x I over closed manifold Σ, say, circle. This is cobordism from one copy to another.

In general case, 2D TQFT and Commutative Frobenius Algebras are one and the same, this is an officially proven fact

Theorem. There is an equivalence of categories 

2TQFT ≃ cFA

given by sending a TQFT to its value on the circle (the unique closed connected 1-manifold)

(From the book) The idea of the proof is this: let A be the image of the circle, under a TQFT A. Now A sends each of the generators of 2Cob to a linear map between tensor powers of A, just as tabulated above. The relations which hold in 2Cob are preserved by A (since A by definition is a monoidal functor) and in its target category Vect they translate into the axioms for a commutative Frobenius algebra

## Section 2.4 | Categorical View on Commutative Frobenius Algebras |

(explanations will be supplemented)

It is more convenient for the author to construct an explanation from a categorical point of view

In current explanation i will use define's from this sources

* [1] [ncatlab.org/Frobenius+Algebras](https://ncatlab.org/nlab/show/Frobenius+algebra)

* [2] [Wikipedia: Frobenius Algebras](https://en.wikipedia.org/wiki/Frobenius_algebra)

* [3] [Joachim Kock: Frobenius Algebras and 2D Topological Quantum Field Theories](https://math.mit.edu/~hrm/palestine/koch-frobenius-algebras.pdf)

If the reader is having difficulty understanding the topic of the conversation and its purpose, the author recommends watching this short video:

[Wannes Malfait: TQFT's and Frobenius Algebras (#SoME3)](https://youtu.be/CSwsD6hAqvE?si=RniJXxjiCIyiAIIe)

There are two main types of Frobenius algebra:

* symmetric

* commutative

For what we need frobenius algebras?

Recently, it has been seen that they play an important role in the algebraic treatment and axiomatic foundation of topological quantum field theory. A commutative Frobenius algebra determines uniquely (up to isomorphism) a (1+1)-dimensional TQFT. More precisely, the category of commutative Frobenius K-algebras is equivalent to the category of symmetric strong monoidal functors from 2-Cob (the category of 2-dimensional cobordisms between 1-dimensional manifolds) to $$Vect_K$$ (the category of vector spaces over K)

(The following words will be taken from [[1]](https://ncatlab.org/nlab/show/Frobenius+algebra))

**Definition 2.1. (see. [1])** A *Frobenius algebra* in a monoidal category(10) $(\mathcal{C}, \otimes, \mathbb{1})$ (for instance, $\mathbf{Vect}$ with the usual tensor product of vector spaces) consists of:

* An object $A$;
* The following morphisms:
  * **(unit)** $\eta \colon \mathbb{1} \to A$,
  * **(counit)** $\varepsilon \colon A \to \mathbb{1}$,
  * **(multiplication)** $\mu \colon A \otimes A \to A$,
  * **(comultiplication)** $\delta \colon A \to A \otimes A$,

such that:

1. $(A, \mu, \eta)$ is a monoid (an associative algebra when $\mathcal{C} = \mathbf{Vect}$);
2. $(A, \delta, \varepsilon)$ is a comonoid (a coassociative coalgebra when $\mathcal{C} = \mathbf{Vect}$);
3. The **Frobenius laws** hold:
   $$(\mathrm{id}_A \otimes \mu) \circ (\delta \otimes \mathrm{id}_A) = \delta \circ \mu = (\mu \otimes \mathrm{id}_A) \circ (\mathrm{id}_A \otimes \delta)$$


Pairing definition (see. [3] *2.1.9 Pairings of vector spaces*): A bilinear pairing – or just a pairing – of two vector spaces $V$ and $W$ is, by definition, a linear map $\beta \colon V \otimes W \to k$. 

When we want to write what it does on elements, it is convenient to write:

$$
\begin{aligned}
\beta \colon V \otimes W &\longrightarrow k \\
v \otimes w &\mapsto \langle v \mid w \rangle
\end{aligned}
$$

Nondegenerate pairing definition (see. [3] *2.1.10 Nondegenerate pairings*): 

A pairing $\beta \colon V \otimes W \to k$ is called **nondegenerate in the variable $V$** if there exists a linear map $\gamma \colon k \to W \otimes V$, called a *copairing*, such that the following composite is equal to the identity map of $V$:

$$
V \cong V \otimes k \xrightarrow{\mathrm{id}_V \otimes \gamma} V \otimes (W \otimes V) \cong (V \otimes W) \otimes V \xrightarrow{\beta \otimes \mathrm{id}_V} k \otimes V \cong V
$$

Similarly, $\beta$ is called **nondegenerate in the variable $W$** if there exists a copairing $\gamma \colon k \to W \otimes V$, such that the following composite is equal to the identity map of $W$:

$$
W \cong k \otimes W \xrightarrow{\gamma \otimes \mathrm{id}_W} (W \otimes V) \otimes W \cong W \otimes (V \otimes W) \xrightarrow{\mathrm{id}_W \otimes \beta} W \otimes k \cong W
$$

These two notions are provisory (but convenient for [3] Lemma 2.1.12); the important notion is this: the pairing $\beta \colon V \otimes W \to k$ is simply called **nondegenerate** if it is simultaneously nondegenerate in $V$ and in $W$.


### Commutative Frobenius algebras

We can define ‘commutative’ Frobenius algebras in any symmetric monoidal category. Namely, a Frobenius algebra is commutative if its associated monoid is commutative, or equivalently, if its associated comonoid is cocommutative.

# Section 3 | Reference Section |

This includes everything that does not belong to the topic of discussion but is used in the main definitions

(1) **combinatorially isomorphic objects** - that is, the same number of vertices, edges, triangles and other simplices, and they are connected to each other in the exact same way

(2) "simplicial complex **homeomorphic** to a manifold" - that is, the mapping of the simplicial complex to the manifold will be continuous, inversely continuous, bijective

(3) **Link** - imagine a triangulated space (manifold), you are standing at a point, around you are 6 triangles (you can imagine it as the center of a pizza cut into 6 slices), all edges that touch your point, this is called the star of a vertex, and the link is those edges and vertices that do not touch your point (continuing the pizza metaphor - the crusts of the pizza and the ends of these crusts are exactly the link) and in general the link looks like a sphere or if we are in two-dimensional space a circle (further developing the metaphor, if you eat this pizza without eating the crusts you get a circle out of them, assuming each crust stays in its original place), that is, if the link is not an n-dimensional sphere then the space is not a manifold

(4) **dual (n-k)-ball** - in topology two objects are called dual if their dimensions add up to the dimension of the whole space (k + (n-k) = n)

(5) **group**:

source: author's notes

1) a group must consist of some set (say G)

2) there must be a binary operation (multiplication "*" ; addition "+"), a binary operation is one that takes two elements and gives a third

3) identity element e for a specific operation

4) for each element x, there must exist an inverse element $x^-1$ such that $x * x^-1 = e$

5) associativity: (xy)z = x(yz) = xyz 

(6) **abelian group** - if commutativity a * b = b * a holds then the group is abelian, if not then the group is non-abelian

(7) **homomorphism**:

source: author's notes

Let us have two groups
(G, "*")
(G',"0") 
And let us have a mapping $f: G \to G'$ ; a,b ∈ G 
A homomorphism is what satisfies this condition
f(a * b) = f(a) 0 f(b) ; a => f(a) , b => f(b)

(8) **linearity**/**linear map** - for a mapping (function) f(x) to be called linear, it must strictly follow two rules

1) f(x + y) = f(x) + f(y)

2) f(c * x) = c * f(x) | c = just a number

(9) **contravariant functor** - Category Theory section, "Functors" subsection last line

(10) **Monoid in a monoidal category**: this is A ∈ Ob(C), equipped with two morphisms:

* Multiplication $$u: A ⊗ A \to A$$

* Identity $$n: I \to A$$
