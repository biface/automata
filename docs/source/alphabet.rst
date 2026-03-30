Alphabet, grammar and Language
==============================

Alphabet
--------

In *Language Theory* an alphabet is a set of indivisible symbols, characters or glyphs, used to construct
strings. Strings are known as *words* or *sentenses* over an alphabet as a sequence of symbols from the alphabet

Mathematical formalization
^^^^^^^^^^^^^^^^^^^^^^^^^^

Let :math:`\Sigma = \{a_1,\ a_2,...,\ a_n\}` where :math:`\Sigma` is the **alphabet**, and each :math:`a_i` is a symbol
from the alphabet. The set :math:`\Sigma^*` represents the sets of strings that can be formed from the alphabet
:math:`\Sigma` including :math:`\varepsilon` as the empty string.

Alphabet examples
^^^^^^^^^^^^^^^^^

    * roman alphabet: :math:`\Sigma = \{a,b,c,d,e,f,...,x,y,z\}`
    * an alphabet with words: :math:`\Sigma = \{dog, cat, bird\}`
    * binary alphabet: :math:`\Sigma = \{0,1\}`


Terminals and Non-terminals
---------------------------

    * **Terminals** are symbols form the alphabet that appear in the final string of the language. They are the *basic building blocks* of the language.
    * **Non-terminals** are symbols used to form production rules in a grammar but do not appear in the final strings. They are intermediate symbols and they are used to generate other terminal or non-terminal symbols.

Mathematical formalization
^^^^^^^^^^^^^^^^^^^^^^^^^^

Let :math:`T` be the set of terminals, :math:`N` be the set of non-terminals and :math:`S` a start symbol where
:math:`S \in N`.

Terminals and Non-terminals examples
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    * Classical example
        * :math:`T =\{a,\ b\}`
        * :math:`N =\{S\}`
        * Rule:

            * :math:`S \to aSb \mid \varepsilon`
    * With words
        * A given alphabet: :math:`\Sigma = \{hello, goodbye\}`
        * Two given non-terminals: :math:`N = \{S,\ A\}`
        * Rules:

            * :math:`S \to hello\ A`
            * :math:`A \to goodbye`

        * Result: *hello goodbye*

Grammar
-------

A formal grammar is a set of production rules that define a formal language. Each rule replaces a non-terminal symbol
with sequence of terminal and non-terminal symbols.

Mathematical formalization
^^^^^^^^^^^^^^^^^^^^^^^^^^


A grammar :math:`G` is a quadruple :math:`G = (N,\ T,\ P,\ S)`

where :

    * :math:`N` is a set of non-terminals
    * :math:`T` is a set of terminals
    * :math:`P` is a set of production rules :math:`(A \to \alpha)`
    * :math:`S \in N` is the start symbol

Grammar example
^^^^^^^^^^^^^^^

Consider the grammar :math:`G =(\{S\},\ \{a,\ b\},\ \{S \to aSb,\ S \to \varepsilon\},\ S)` which generates strings of
the form :math:`a^nb^n`


Language
--------

A formal language is a set of strings formed from an alphabet, according to specified grammar rules.

Mathematical formalization
^^^^^^^^^^^^^^^^^^^^^^^^^^

Let :math:`\Sigma` an alphabet, and :math:`L \subseteq \Sigma^*` be a formal language where each string of :math:`L` is
a string of symbols formed from :math:`\Sigma`

Language example
^^^^^^^^^^^^^^^^

From the previous examples, consider :

    * :math:`\Sigma = \{a,\ b\}` an alphabet
    * :math:`G = (\{S\},\ \{a,\ b\},\ \{S \to aSb,\ S \to \varepsilon\},\ S)` a given grammar
    * :math:`L = \{a^nb^n \mid n \geq 0\}` is a **language**