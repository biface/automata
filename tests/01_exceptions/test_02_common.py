"""
Tests for fsm_tools.utils.common — generate_code() and id_code().

generate_code()'s own KeyError branches are never exercised through the normal
exception hierarchy: AutomatonException.__init__ validates grammar/component/
action itself (raising ValueError) *before* ever calling generate_code(), so
these branches are only reachable by calling the function directly.

id_code() is not called anywhere in the codebase today, but is kept as a
public utility (a generic weighted-sum code, unlike generate_code()'s fixed
10000/100/1 weights) — tested on its own merits, independent of current usage.
"""

import pytest

from fsm_tools.utils.common import generate_code, id_code


class TestGenerateCode:

    def test_valid_inputs(self):
        assert generate_code("Regular", "alphabet", "read") == "40101"

    def test_unknown_grammar_raises_key_error(self):
        with pytest.raises(KeyError, match="Unknown grammar name"):
            generate_code("Unknown", "alphabet", "read")

    def test_unknown_component_raises_key_error(self):
        with pytest.raises(KeyError, match="Unknown component name"):
            generate_code("Regular", "unknown_component", "read")

    def test_unknown_action_raises_key_error(self):
        with pytest.raises(KeyError, match="Unknown action name"):
            generate_code("Regular", "alphabet", "unknown_action")

    def test_alias_resolves_to_same_code_as_its_primary_axis(self):
        """ "states" and "blank" are pure usage-vocabulary aliases (#79) —
        they must produce the exact same code as their primary axis."""
        assert generate_code("Regular", "states", "read") == generate_code(
            "Regular", "non_terminals", "read"
        )
        assert generate_code("Regular", "blank", "read") == generate_code(
            "Regular", "alphabet", "read"
        )


class TestIdCode:

    def test_weighted_sum(self):
        assert id_code([10000, 100, 1], [4, 1, 1]) == "40101"

    def test_empty_lists(self):
        assert id_code([], []) == "0"

    def test_mismatched_lengths_truncate_to_shortest(self):
        """zip() silently stops at the shortest iterable — documented here
        so a future caller doesn't discover it by surprise."""
        assert id_code([1, 2, 3], [10, 10]) == "30"
