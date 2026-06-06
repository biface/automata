The Chomsky-Schützenberger Hierarchy
====================================

The Chomsky-Schützenberger hierarchy is a framework in formal language theory that classifies languages, as sets of
string, based on the type of formal grammars that generate them. This framework was introduced
by `Noam Chomsky <https://en.wikipedia.org/wiki/Noam_Chomsky>`_ in 1956 and is fundamental in understanding
the computational complexity of language processing. This framework consists of four levels.

Type 0 - Unrestricted Grammars
------------------------------

These are the most general and powerful grammars in the Chomsky hierarchy. They are capable of describing any class of
**recursively enumerable** languages, meaning languages whose membership can be verified by a *Turing machine*, but
where this process may never terminate if the word is not part of the language.

.. Note::
    In 1936, Alan Turing described a model of the “ideal machine” to which he gave his name. A Turing machine is an
    abstract model of the operation of mechanical computing devices, such as a computer and its memory.

    Alan Turing wanted to give a precise definition to the concept of algorithm or “mechanical procedure” in order to
    address the *Decision problem* posed by David Hilbert. This model is still widely used in theoretical computer
    science, in particular to solve problems of algorithmic complexity and computability.

    Originally, the concept of the Turing machine, invented before the computer, was supposed to represent a virtual
    person executing a well-defined procedure, changing the contents of the squares of an infinite array, by choosing
    these contents from a finite set of symbols.

    Other models have been proposed, all of which are equivalent to the Turing machine. Church demonstrated in his
    thesis that these models are as general as possible.

Definition
^^^^^^^^^^

A Type-0 grammar is a formal grammar :math:`G = (N,\ \Sigma,\ P,\ S)` where :

    * :math:`N` is the set of non-terminals
    * :math:`\Sigma` is an alphabet
    * :math:`P` is a set of production rules such as :math:`P = \{ \alpha \to \beta \}`

        * :math:`\alpha,\ \beta \in (N \cup \Sigma)^*`
        * :math:`\alpha \neq  \varepsilon`

Example
^^^^^^^

A Type-0 grammar that describes the language of palindromes (words that read the same forward and backward) can be
expressed by rules that progressively build complexity of the construction of the word.

Type 1 - Context-Sensitive Grammars
-----------------------------------

Context-sensitive languages are recognized by linear bounded Turing machines. Production rules ensures the left handed
side (:math:`\alpha`) is no longer than right-hand side (:math:`\beta`).

Definition
^^^^^^^^^^

A Type-1 grammar is a formal grammar :math:`G = (N,\ \Sigma,\ P,\ S)` where :

    * :math:`N = \{A\}` is the set of non-terminals
    * :math:`\Sigma` is an alphabet
    * :math:`P` is a set of production rules such as :math:`P = \{ \alpha A \beta \to \alpha \gamma \beta \}`

        * :math:`\alpha,\ \beta,\ \gamma \in (N \cup \Sigma)^*`
        * :math:`\mid \gamma \mid \geq 1`

Example
^^^^^^^

    * :math:`\Sigma = \{a,\ b,\ c\}`
    * :math:`N =\{B,\ C,\ H,\ S\}` is the set of non-terminals
    * :math:`P` is the set of production rules as follows :

        1. :math:`S \to aSBC`
        2. :math:`S \to aBC`
        3. :math:`CB \to HB`
        4. :math:`HB \to HC`
        5. :math:`HC \to BC`
        6. :math:`aB \to ab`
        7. :math:`bB \to bb`
        8. :math:`bC \to bc`
        9. :math:`cC \to cc`

    * :math:`G = (N,\ \Sigma,\ P,\ S)` is the context-sensitive grammar.

It produces :math:`L = \{a^n b^n c^n \mid n \geq 1 \}` a context-sensitive language.

Type 2 - Context-Free Grammars
------------------------------

Context-free grammar produced languages where non-terminals generate a string independent of its context. These
languages are recognized by **pushdown automata** (automata with stack that allows for storage of information)
and are used in programming languages especially with arithmetic expressions.

Definition
^^^^^^^^^^

A Type-2 grammar is a formal grammar :math:`G = (N,\ \Sigma,\ P,\ S)` where :

    * :math:`N = \{A\}` is the set of non-terminals
    * :math:`\Sigma` is an alphabet
    * :math:`P` is a set of production rules such as :math:`P = \{A \to \alpha \}`

        * :math:`\alpha \in (N \cup \Sigma)^*`

Example
^^^^^^^

.. Note::
    An interesting example is `Dyck Language <https://en.wikipedia.org/wiki/Dyck_language>`_ used in the parsing of
    expression that must have a correctly nested sequence of brackets. This type of automaton is used in many, many
    graphical programming editor interfaces to check the closure of parenthesis nesting.


The Dyck language is defined as :

    * :math:`\Sigma = \{(,\ ),\ [,\ ],\ \{,\ \}\}` a generalized dyck alphabet

        * Parenthesis: ( and )
        * Square brackets: [ and ]
        * Curly brackets: { and }

    * :math:`N = \{S\}` the set of non-terminals
    * :math:`P` the production rules defined as follows:

        1. :math:`S \to SS` (concatenation of balanced sequences)
        2. :math:`S \to (S)` (balanced parenthesis)
        3. :math:`S \to [S]` (balanced square brackets)
        4. :math:`S \to \{S\}` (balanced curly brackets)
        5. :math:`S \to \varepsilon` (base case of recursion)

The Dyck context-free grammar is given by :

.. math::

    G = (\{S\},\ \{(,\ ),\ [,\ ],\ \{,\ \}\},\ \{S \to SS,\ S \to (S),\ S \to [S],\ S \to \{S\},\ S \to \varepsilon \},\ S \})

Valid strings
"""""""""""""

    * :math:`\varepsilon`
    * :math:`(\ )`
    * :math:`[\ ]`
    * :math:`(\ [\ ]\ )`
    * :math:`\{\ (\ [\ ]\ )\ \}`

Invalid strings
"""""""""""""""

    * :math:`(\ [\ )`
    * :math:`(\ ]`
    * :math:`[\ (\ ]`

Parsing and derivation
""""""""""""""""""""""

Let's drive the string :math:`(\ \Box\ )`

    1. Start with S :math:`\to S`
    2. Apply rule 2 to the inner S :math:`\to (S)`
    3. Apply rule 4 to the inner S :math:`\to (\{S\})`
    4. Apply rule 3 to the inner S :math:`\to ([S])`
    5. Apply rule 5 to the innermost S : :math:`\to (\ \Box\ )`

Result : :math:`(\ \Box\ )` is valid.

Parsing with a Pushdown automaton
"""""""""""""""""""""""""""""""""

The generalize Dyck language, like all context-free language, can be parsed using a pushdown automaton (PDA). The stack
ensures that each opening bracket matches the correct closing bracket. The stack uses two operators *push* to add to
the stack and *pop* to remove from the stack, and only the last pushed element can be popped.

Parsing the string :math:`[([])]`

    ==== ============== ================ ======= =================================
    Step Automaton      Input            Command Stack
    ==== ============== ================ ======= =================================
     1   Input          :math:`[([])]`           :math:`\langle \rangle` (Empty)
     2   Read :math:`[` :math:`([])]`    push    :math:`\langle [ \rangle`
     3   Read :math:`(` :math:`[])]`     push    :math:`\langle [,\ ( \rangle`
     4   Read :math:`[` :math:`])]`      push    :math:`\langle [,\ (,\ [ \rangle`
     5   Read :math:`]` :math:`)]`       pop     :math:`\langle [,\ ( \rangle`
     6   Read :math:`)` :math:`]`        pop     :math:`\langle [ \rangle`
     7   Read :math:`]` Processed        pop     :math:`\langle \rangle` (Empty)
    ==== ============== ================ ======= =================================

Since the stack is empty at the end of the process and symbols are processed, :math:`[([])]` is a valid string.

Type 3 - Regular Grammars
-------------------------

Regular languages are the simplest and are recognized by finite state machines. These languages are the most common in
computer science, especially for pattern matching string such as regular expressions.

Definition
^^^^^^^^^^

A Type-2 grammar is a formal grammar :math:`G = (N,\ \Sigma,\ P,\ S)` where :

    * :math:`N` is the set of non-terminals
    * :math:`\Sigma` is an alphabet
    * :math:`P` is a set of production rules such as :math:`P = \{A \to \alpha B,\ A \to \alpha \}`

        * :math:`A,B \in N`
        * :math:`\alpha \in \Sigma^*`

Example
^^^^^^^

    * :math:`\Sigma = \{hello,\ goodbye\}`
    * :math:`G = (\{A\},\ \Sigma,\ \{S \to hello\ A,\ A \to goodbye\}, S)` the give grammar

It produces :math:`L = \{hello\ goodbye\}`
