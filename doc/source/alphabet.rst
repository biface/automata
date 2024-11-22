Alphabet, grammar and Language
------------------------------

Alphabet
^^^^^^^^

In *Language Theory* an alphabet is a set of indivisible symbols, characters or glyphs, used to construct
strings. Strings are known as *words* or *sentenses* over an alphabet as a sequence of symbols from the alphabet

**Alphabet examples**

    * roman alphabet: :math:`\Sigma = \{a,b,c,d,e,f,...,x,y,z\}`
    * a two words alphabet: :math:`\Sigma = \{hello, goodbye\}`
    * binary alphabet: :math:`\Sigma = \{0,1\}`

Usually :math:`\varepsilon` represents the empty string.

Grammar
^^^^^^^

Language
^^^^^^^^

Terminals and Non-terminals
---------------------------

Terminals are the final symbols of a language (e.g, letters or words in an defined alphabet) and Non-terminals are
intermediate symbols used in grammars to used to defined how strings are generated. Rules describe how non-terminals are
replaced by terminals or other non-terminals

**Terminals and Non-terminals examples**

    * A given alphabet: :math:`\Sigma = \{hello, goodbye\}`
    * Two given non-terminals: :math:`S, A`
    * Rules:

        * :math:`S \to hello\ A`
        * :math:`A \to goodbye`

    * Result: *hello goodbye*
