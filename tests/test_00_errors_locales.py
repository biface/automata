import pytest
from fsm_tools.utils.json import generate_json_message, seek_json_message, get_json_message


# Test : seek_message avec accès réel au fichier
@pytest.mark.parametrize("msg_id, domain, lang, expected", [
    ("4101", "automata", "en-US", "Read the symbols of the alphabet of a finite automaton."),
    ("4505", "automata", "en-US", "A state is inaccessible from the initial state."),
    ("1203", "automata", "fr-FR", "Supprimer une transition d'une machine de Turing."),
    ("3102", "automata", "de-DE", "Füge ein Symbol zum Alphabet eines Kellerautomaten hinzu."),
    ("1506", "automata", "it-IT", "È stato rilevato un ciclo infinito durante l'esecuzione."),
    ("add", "errors", "sv-SV", "Misslyckades med att lägga till objektet:"),
])
def test_seek_message_real_file(msg_id, domain, lang, expected):
    result = seek_json_message(msg_id, domain, lang)
    assert result == expected

# Test : seek_message with raised exceptions

@pytest.mark.parametrize("msg_id, domain, lang, exception_expected", [
    ("4110", "automata", "en-US", KeyError),
    ("nope", "automaton", "en-US", FileNotFoundError),
    ("1506", "automata", "fr-YT", KeyError),
])
def test_seek_message_with_exception(msg_id, domain, lang, exception_expected):
    with pytest.raises(exception_expected):
        seek_json_message(msg_id, domain, lang)

# Test : generate_message avec accès réel au fichier
@pytest.mark.parametrize("grammar, component, action, lang, expected_msg", [
    ("Regular", "alphabet", "read", "en-US", "Read the symbols of the alphabet of a finite automaton."),
    ("Context-Free", "states", "remove", "en-US", "Remove a state from a pushdown automaton."),
    ("Context-Sensitive", "grammar", "add", "en-US", "Add a grammar rule to a context-sensitive automaton."),
    ("Context-Sensitive", "grammar", "remove", "ga-IE", "Bain rialáil gramadaí as uathoibriú éighníomhach."),
    ("Recursively Enumerable", "transitions", "modify", "es-ES", "Modificar una transición en una máquina de Turing.")
])
def test_generate_message_real_file(grammar, component, action, lang, expected_msg):
    result = generate_json_message(grammar, component, action, lang)
    assert expected_msg in result


# Test : get_message avec accès réel au fichier
@pytest.mark.parametrize("msg_id, lang, expected", [
    ("4101", "en-US", "Read the symbols of the alphabet of a finite automaton."),
    ("4505", "en-US", "A state is inaccessible from the initial state."),
    ("3102", "de-DE", "Füge ein Symbol zum Alphabet eines Kellerautomaten hinzu."),
    ("1605", "sv-SV", "Validera en Turingmaskin.")

])
def test_get_message_real_file(msg_id, lang, expected):
    result = get_json_message(msg_id, lang)
    assert result == expected


# Test : Edge cases avec accès réel au fichier
@pytest.mark.parametrize("grammar, component, action, expected_exception", [
    ("Unknown", "alphabet", "read", KeyError),
    ("Regular", "unknown_component", "add", KeyError),
    ("Regular", "alphabet", "unknown_action", KeyError)
])
def test_generate_message_invalid_inputs_real_file(grammar, component, action, expected_exception):
    with pytest.raises(expected_exception):
        generate_json_message(grammar, component, action)
