The Kleene Star (Kleene closure)
********************************

The *Kleene Star* (named after `Stephen Cole Kleene <https://en.wikipedia.org/wiki/Stephen_Cole_Kleene>`_) is a mathematical
operator used in formal language theory and theoretical computer science. It applies to sets of strings and describes
arbitrary repetitions (*including no repetition*) of those strings.

.. note::
    In set theory, If :math:`\Sigma` is a set equipped with one or several methods for producing elements from other
    elements of :math:`\Phi`. A subset :math:`\Phi` of :math:`\Sigma` is said to be **closed** under these methods when
    all input are in :math:`\Phi` and all possible result elements are also in :math:`\Phi`.

    As you will see from this definition the Kleene star is also a closure.

Formal Definition
=================

Given :math:`\Sigma` be an alphabet, and :math:`L \subseteq \Sigma^*` be a language (a set of strings formed from
:math:`\Sigma`). The Kleene star of :math:`L`, denoted :math:`L^*`, is defined as follows:

.. math::

    L^* = \bigcup_{n=0}^{\infty} L^n

Where :

    * :math:`L^0 = \{\varepsilon\}`, the empty string
    * :math:`L^n,\ n \geq 1` is the set of strings formed by concatenated :math:`n` elements of :math:`A`

Kleene closure
==============

The kleene star is a **closure** because it includes all strings formed by repeated concatenation of words from a given
language, as well a the empty string.

    * :math:`L^0 = \{\varepsilon\}` the empty string
    * :math:`L^1 = L` the set of words from :math:`L`
    * :math:`L^2` is the set all strings of length 2 by concatenating to words from :math:`L`
    * and so on for the powers :math:`L^n, n \geq 0`

Example
=======

Classical example
-----------------

The Kleene star is a fundamental construct used to describe regular language in regular expressions.

    1. By definition, the Kleene star always includes the empty string :math:`\varepsilon`, even if :math:`A`
    2. If :math:`A = \{a,\ b\}`, then :math:`A^* = \{\varepsilon,\ a,\ b,\ aa,\ ab,\ ba,\ bb,\ aaa,\ aab,\ aba,...\}`

Binary alphabet
---------------

Let us consider the binary alphabet :math:`\Sigma = \{0,\ 1\}`

The Kleene star of this alphabet, denoted :math:`\Sigma^*`, is the set of all possible strings of 0 and 1, including the
empty string :

.. math::
    \Sigma^* = \{\varepsilon,\ 0,\ 1,\ 00,\ 01,\ 10,\ 11,\ 000,\ 001,\ 010,\ 011,\ 100,\ 101,\ 111,\ ...\}

Differences with :math:`+` operator
===================================

The Kleene plus operator (:math:`A⁺`) is similar sur the kleene star, but it excludes the possibility of no repetitions.

.. math::
    A⁺ = A^* \setminus \{\varepsilon\} = \bigcup_{n=1}^{\infty} A_n \\
    or \\
    A^* = A⁺ \cup \{\varepsilon\}