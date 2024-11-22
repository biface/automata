The Chomsky-Schützenberger Hierarchy
------------------------------------

The Chomsky-Schützenberger hierarchy is a framework in formal language theory that classifies languages, as sets of
string, based on the type of formal grammars that generate them. This framework was introduced by Noam Chomsky in 1956
and is fundamental in understanding the computational complexity of language processing. This framework consists of
four levels.

Type 0 - Unrestricted Grammars
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

These grammars generate **recursively enumerable languages**, the most general class of languages. These languages are
recognized by a Turing machine. There a no restrictions on production rules.

**Formalization**

    * :math:`\alpha \to \beta`
    * :math:`\alpha,\ \beta \in \Sigma^*`
    * :math:`\alpha \neq \varepsilon`

Where :

    * :math:`\Sigma` is an alphabet
    * :math:`\alpha,\ \beta` are terminals or non-terminals


.. Note::
    In 1936, Alan Turing described a model of the “ideal machine” to which he gave his name. A Turing machine is an
    abstract model of the operation of mechanical computing devices, such as a computer and its memory.

    Alan Turing wanted to give a precise definition to the concept of algorithm or “mechanical procedure”.
    This model is still widely used in theoretical computer science, in particular to solve problems of algorithmic
    complexity and computability.

    Originally, the concept of the Turing machine, invented before the computer, was supposed to represent a virtual
    person executing a well-defined procedure, changing the contents of the squares of an infinite array, by choosing
    these contents from a finite set of symbols.

    Other models have been proposed, all of which are equivalent to the Turing machine. Church demonstrated in his
    thesis that these models are as general as possible.

Type 1 - Context-Sensitive Grammars
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Context-sensitive languages are recognized by linear bounded Turing machines. Production rules ensures the left handed
side (:math:`\alpha`) is no longer than right-hand side (:math:`\beta`).

**Formalization**

    * :math:`\alpha A \beta \to \alpha \gamma \beta`

where:

    * :math:`A \in N`
    * :math:`\alpha,\ \beta,\ \gamma \in (N \cup \Sigma)^*`
    * :math:`\mid \gamma \mid \geq 1`

Example

    * :math:`\Sigma = \{a,\ b,\ c\}`
    * Grammar

        1. :math:`S \to aSBC`
        2. :math:`S \to aBC`
        3. :math:`CB \to HB`
        4. :math:`HB \to HC`
        5. :math:`HC \to BC`
        6. :math:`aB \to ab`
        7. :math:`bB \to bb`
        8. :math:`bC \to bc`
        9. :math:`cC \to cc`

    Result : :math:`\{a^n b^n c^n \mid n \geq 1 \}`


Type 2 - Context-Free Grammars
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Formalization**

Type 3 - Regular Grammars
^^^^^^^^^^^^^^^^^^^^^^^^^

**Formalization**


This work led to a distinction being made between functions that are theoretically computable and those that are not, even theoretically. (A function is said to be computable if it can be calculated by the Turing machine in finite time (number of operations).

A finite-state automaton is an abstract machine made up of states and transitions. This machine is designed to process
words supplied as input: the automaton moves from state to state, according to the transitions, on reading each letter
of the input. The automaton is said to be “finite” because it has a finite number of distinct states: it therefore only
has a bounded memory, irrespective of the size of the data on which calculations are performed.

Finite-state automata provide a particularly simple tool for constructing algorithms. They are also found in the study
of formal languages, in compilers and also in the search for regular expressions in texts.They are used in process
modeling, control, communication protocols, program verification and computability theory.
