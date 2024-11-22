The Kleene Star (Kleene closure)
--------------------------------

The *Kleene Star* (named after `Stephen Cole Kleene <https://en.wikipedia.org/wiki/Stephen_Cole_Kleene>`_) is a mathematical
operator used in formal language theory and theoretical computer science. It applies to sets of strings and describes
arbitrary repetitions (*including no repetition*) of those strings.

Definition
^^^^^^^^^^

Given :math:`A` an alphabet or a language, the Kleene star, denoted :math:`A^*`, is defined as the set of all strings
that can be formed by concatenated zero or more strings from :math:`A`

.. math::

    A^* = \bigcup_{n=0}^{\infty} A_n

Where :

    * :math:`A^0 = \{\varepsilon\}`
    * :math:`A^n,\ n \geq 1` is the set of strings formed by concatenated :math:`n` elements of :math:`A`

Properties
^^^^^^^^^^

The Kleene star is a fundamental construct used to describe regular language in regular expressions.

    1. By definition, the Kleene star always includes the empty string :math:`\varepsilon`, even if :math:`A`
    2. If :math:`A = \{a,\ b\}`, then :math:`A^* = \{\varepsilon,\ a,\ b,\ aa,\ ab,\ ba,\ bb,\ aaa,\ aab,\ aba,...\}`

Differences with :math:`+` operator
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The Kleene plus operator (:math:`A⁺`) is similar sur the kleene star, but it excludes the possibility of no repetitions.

.. math::
    A⁺ = A^* \setminus \{\varepsilon\} = \bigcup_{n=1}^{\infty} A_n