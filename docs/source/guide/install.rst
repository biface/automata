Installation
============

Requirements
------------

- Python 3.10 or later
- No runtime dependencies — **fsm-tools** is pure Python

From PyPI
---------

.. code-block:: console

   pip install fsm-tools

Or with `uv <https://docs.astral.sh/uv/>`_:

.. code-block:: console

   uv add fsm-tools

From GitHub
-----------

The source code is hosted at `github.com/biface/automata <https://github.com/biface/automata>`_.
Tagged releases are available on the
`releases page <https://github.com/biface/automata/releases>`_.

.. code-block:: console

   pip install git+https://github.com/biface/automata.git@v0.1.0

Development environment
-----------------------

.. code-block:: console

   git clone https://github.com/biface/automata.git
   cd automata
   uv sync

Run the test suite:

.. code-block:: console

   tox -e pre-push

.. note::

   **fsm-tools** is currently in **Pre-Alpha** status (v0.1.0).
   The public API may change between minor versions until v0.6.0 (Beta).
   See :doc:`usage` for stability guidance.

Version history
---------------

.. list-table::
   :header-rows: 1
   :widths: 15 15 70

   * - Version
     - Status
     - Highlights
   * - 0.1.0
     - Pre-Alpha
     - First PyPI release — ``PushdownAutomaton`` (Type 2)
   * - 0.0.4
     - Pre-Alpha
     - ``TuringMachine`` and ``LinearBoundedAutomaton`` complete
   * - 0.0.2
     - Planning
     - Repository setup, formal hierarchy foundation
