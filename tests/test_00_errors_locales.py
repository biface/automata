import pytest
from fsm_tools.utils.json import localized_messages, \
    load_message, seek_message, format_message, get_message, generate_message


# Test : load_messages

@pytest.mark.parametrize("domain, lang, key", [
    ("automata", "de-DE", "3102"),
    ("automata", "sv-SV", "1203"),
    ("automata", "en-US", ""),
    ("errors", "en-US", "1102"),
])
def test_load_real_file(domain, lang, key):
    load_message(domain)
    assert lang in localized_messages[domain].keys()
    if len(key) > 0:
        assert key in localized_messages[domain][lang].keys()


# Test : load_message with exception

def test_load_with_exception():
    with pytest.raises(FileNotFoundError, match="The JSON file for domain 'fallback' was not found."):
        load_message("fallback")


@pytest.mark.parametrize("msg_id, domain, lang, expected", [
    ("4101", "automata", "en-US", "Read the symbols of the alphabet of a finite automaton."),
    ("4505", "automata", "en-US", "A state is inaccessible from the initial state."),
    ("1203", "automata", "fr-FR", "Supprimer une transition d'une machine de Turing."),
    ("3102", "automata", "de-DE", "Füge ein Symbol zum Alphabet eines Kellerautomaten hinzu."),
    ("1506", "automata", "it-IT", "È stato rilevato un ciclo infinito durante l'esecuzione."),
    ("4605", "errors", "sv-SV", "Den ändliga automaten är ogiltig: {reason}."),
])
def test_seek_messages(msg_id, domain, lang, expected):
    result = seek_message(msg_id, domain, lang)
    assert result == expected


@pytest.mark.parametrize("msg_id, domain, lang, exception_expected, exception_msg", [
    ("4110", "automata", "en-US", KeyError, "The message with ID '4110' was not found for language 'en-US'."),
    ("nope", "errors", "de-DE", KeyError, "The message with ID 'nope' was not found for language 'de-DE'."),
    ("1215", "automata", "fr-FR", KeyError, "The message with ID '1215' was not found for language 'fr-FR'."),
])
def test_seek_message_with_exception(msg_id, domain, lang, exception_expected, exception_msg):
    with pytest.raises(exception_expected, match=exception_msg):
        seek_message(msg_id, domain, lang)


# Test : format messages
@pytest.mark.parametrize("template, symbols, excepted_result", [
    ("The start state '{symbol}' is not a valid non-terminal.", {'symbol': "N"},
     "The start state 'N' is not a valid non-terminal."),
    ("L'état d'acceptation '{symbol}' n'est pas un non-terminal valide.", {'symbol': "U"},
     "L'état d'acceptation 'U' n'est pas un non-terminal valide."),
    ("Ní féidir an riail '{lhs}' -> '{rhs}' a scriosadh mar níl sí ann sa ghramadaí.", {'lhs': "U", 'rhs': "N"},
     "Ní féidir an riail 'U' -> 'N' a scriosadh mar níl sí ann sa ghramadaí.")
])
def test_format_message(template, symbols, excepted_result):
    result = format_message(template, **symbols)
    assert result == excepted_result


def test_format_message_with_exception():
    template = "The start state '{symbol}' is not a valid non-terminal."
    symbols = {"rule": "N"}
    with pytest.raises(ValueError, match="The parameter 'symbol' is missing for formatting the message."):
        format_message(template, **symbols)


# Test : Get messages with id from automata
@pytest.mark.parametrize("lang, msg_id, excepted_msg", [
    ("de-DE", "4101", "Lese Symbole aus dem Alphabet eines endlichen Automaten."),
    ("de-DE", "4102", "Füge ein Symbol zum Alphabet eines endlichen Automaten hinzu."),
    ("de-DE", "4304", "Ändere einen Zustand in einem endlichen Automaten."),
    ("de-DE", "4202", "Füge einen Übergang zu einem endlichen Automaten hinzu."),
    ("de-DE", "4203", "Entferne einen Übergang aus einem endlichen Automaten."),
    ("de-DE", "4204", "Ändere einen Übergang in einem endlichen Automaten."),
    ("de-DE", "4605", "Validiere einen endlichen Automaten."),
    ("de-DE", "3101", "Lese Symbole aus dem Alphabet eines Kellerautomaten."),
    ("de-DE", "3102", "Füge ein Symbol zum Alphabet eines Kellerautomaten hinzu."),
    ("de-DE", "3103", "Entferne ein Symbol aus dem Alphabet eines Kellerautomaten."),
    ("de-DE", "3502", "Füge ein Symbol zum Stapel eines Kellerautomaten hinzu."),
    ("de-DE", "3503", "Entferne ein Symbol vom Stapel eines Kellerautomaten."),
    ("de-DE", "3303", "Entferne einen Zustand aus einem Kellerautomaten."),
    ("de-DE", "3304", "Ändere einen Zustand in einem Kellerautomaten."),
    ("de-DE", "3202", "Füge einen Übergang zu einem Kellerautomaten hinzu."),
    ("de-DE", "3203", "Entferne einen Übergang aus einem Kellerautomaten."),
    ("de-DE", "3204", "Ändere einen Übergang in einem Kellerautomaten."),
    ("de-DE", "3605", "Validiere einen Kellerautomaten."),
    ("de-DE", "2302", "Füge einen Zustand zu einem kontextsensitiven Automaten hinzu."),
    ("de-DE", "2303", "Entferne einen Zustand aus einem kontextsensitiven Automaten."),
    ("de-DE", "2304", "Ändere einen Zustand in einem kontextsensitiven Automaten."),
    ("de-DE", "2202", "Füge einen Übergang zu einem kontextsensitiven Automaten hinzu."),
    ("de-DE", "2203", "Entferne einen Übergang aus einem kontextsensitiven Automaten."),
    ("de-DE", "2204", "Ändere einen Übergang in einem kontextsensitiven Automaten."),
    ("de-DE", "2605", "Validiere einen kontextsensitiven Automaten."),
    ("de-DE", "1103", "Entferne ein Symbol aus dem Alphabet einer Turingmaschine."),
    ("de-DE", "1202", "Füge einen Übergang zu einer Turingmaschine hinzu."),
    ("de-DE", "1203", "Entferne einen Übergang aus einer Turingmaschine."),
    ("de-DE", "1204", "Ändere einen Übergang in einer Turingmaschine."),
    ("de-DE", "1605", "Validiere eine Turingmaschine."),
    ("de-DE", "1606", "Konnte die Turingmaschine nicht validieren."),
    ("de-DE", "1506", "Unendliche Schleife während der Ausführung entdeckt."),
    ("de-DE", "1503", "Die Turingmaschine versuchte, auf einen unzulässigen Bereich des Bandes zuzugreifen."),
    ("en-GB", "4503", "A conflicting transition exists in the automaton."),
    ("en-GB", "3101", "Read the symbols of the alphabet of a pushdown automaton."),
    ("en-GB", "3102", "Add a symbol to the alphabet of a pushdown automaton."),
    ("en-GB", "3103", "Remove a symbol from the alphabet of a pushdown automaton."),
    ("en-GB", "3502", "Add a symbol to the stack of a pushdown automaton."),
    ("en-GB", "2102", "Add a symbol to the alphabet of a context-sensitive automaton."),
    ("en-GB", "2103", "Remove a symbol from the alphabet of a context-sensitive automaton."),
    ("en-GB", "2402", "Add a grammar rule to a context-sensitive automaton."),
    ("en-GB", "2403", "Remove a grammar rule from a context-sensitive automaton."),
    ("en-GB", "2406", "The added grammar rule is malformed."),
    ("en-GB", "2606", "Failed to validate the context-sensitive automaton."),
    ("en-GB", "1101", "Read the symbols of the alphabet of a Turing machine."),
    ("en-US", "3103", "Remove a symbol from the alphabet of a pushdown automaton."),
    ("en-US", "3502", "Add a symbol to the stack of a pushdown automaton."),
    ("en-US", "3503", "Remove a symbol from the stack of a pushdown automaton."),
    ("en-US", "3519", "Attempted to remove a symbol from an empty stack."),
    ("en-US", "3505", "Stack capacity exceeded."),
    ("en-US", "3302", "Add a state to a pushdown automaton."),
    ("en-US", "3303", "Remove a state from a pushdown automaton."),
    ("en-US", "3304", "Modify a state in a pushdown automaton."),
    ("en-US", "2204", "Modify a transition in a context-sensitive automaton."),
    ("en-US", "2605", "Validate a context-sensitive automaton."),
    ("en-US", "2606", "Failed to validate the context-sensitive automaton."),
    ("en-US", "1101", "Read the symbols of the alphabet of a Turing machine."),
    ("en-US", "1102", "Add a symbol to the alphabet of a Turing machine."),
    ("en-US", "1103", "Remove a symbol from the alphabet of a Turing machine."),
    ("en-US", "1202", "Add a transition to a Turing machine."),
    ("en-US", "1203", "Remove a transition from a Turing machine."),
    ("en-US", "1204", "Modify a transition in a Turing machine."),
    ("en-US", "1605", "Validate a Turing machine."),
    ("en-US", "1606", "Validation of the Turing machine failed."),
    ("en-US", "1506", "An infinite loop was detected during execution."),
    ("en-US", "1503", "The Turing machine attempted to access an unauthorized tape section."),
    ("es-ES", "4102", "Agregar un símbolo al alfabeto de un autómata finito."),
    ("es-ES", "3304", "Modificar un estado en un autómata de pila."),
    ("es-ES", "3202", "Agregar una transición a un autómata de pila."),
    ("es-ES", "3203", "Eliminar una transición de un autómata de pila."),
    ("es-ES", "3204", "Modificar una transición en un autómata de pila."),
    ("es-ES", "3605", "Validar un autómata de pila."),
    ("es-ES", "3606", "No se pudo validar el autómata de pila."),
    ("es-ES", "2101", "Leer los símbolos del alfabeto de un autómata sensible al contexto."),
    ("es-ES", "2102", "Agregar un símbolo al alfabeto de un autómata sensible al contexto."),
    ("es-ES", "2103", "Eliminar un símbolo del alfabeto de un autómata sensible al contexto."),
    ("es-ES", "2402", "Agregar una regla gramatical a un autómata sensible al contexto."),
    ("es-ES", "2403", "Eliminar una regla gramatical de un autómata sensible al contexto."),
    ("es-ES", "2406", "La regla gramatical agregada está mal formada."),
    ("es-ES", "2302", "Agregar un estado a un autómata sensible al contexto."),
    ("es-ES", "2303", "Eliminar un estado de un autómata sensible al contexto."),
    ("es-ES", "2304", "Modificar un estado en un autómata sensible al contexto."),
    ("es-ES", "2202", "Agregar una transición a un autómata sensible al contexto."),
    ("fr-FR", "3101", "Lire les symboles de l'alphabet d'un automate à pile."),
    ("fr-FR", "3102", "Ajouter un symbole à l'alphabet d'un automate à pile."),
    ("fr-FR", "3103", "Supprimer un symbole de l'alphabet d'un automate à pile."),
    ("fr-FR", "3502", "Ajouter un symbole à la pile d'un automate à pile."),
    ("fr-FR", "3503", "Supprimer un symbole de la pile d'un automate à pile."),
    ("fr-FR", "3519", "Tentative de retirer un symbole d'une pile vide."),
    ("fr-FR", "2606", "Échec de la validation de l'automate contextuel."),
    ("fr-FR", "1101", "Lire les symboles de l'alphabet d'une machine de Turing."),
    ("fr-FR", "1102", "Ajouter un symbole à l'alphabet d'une machine de Turing."),
    ("fr-FR", "1103", "Supprimer un symbole de l'alphabet d'une machine de Turing."),
    ("fr-FR", "1202", "Ajouter une transition à une machine de Turing."),
    ("fr-FR", "1203", "Supprimer une transition d'une machine de Turing."),
    ("fr-FR", "1204", "Modifier une transition dans une machine de Turing."),
    ("fr-FR", "1605", "Valider une machine de Turing."),
    ("fr-FR", "1606", "La validation de la machine de Turing a échoué."),
    ("fr-FR", "1506", "Une boucle infinie a été détectée lors de l'exécution."),
    ("fr-FR", "1503", "La machine de Turing tente d'accéder à une zone de bande non autorisée."),
    ("ga-IE", "4101", "Léamh na siombailí ón aibítir i uathoibriú críochnaithe."),
    ("ga-IE", "3304", "Athraigh stát i uathoibriú stóca."),
    ("ga-IE", "3202", "Cuir trádstón le uathoibriú stóca."),
    ("ga-IE", "3203", "Bain trádstón as uathoibriú stóca."),
    ("ga-IE", "3204", "Athraigh trádstón i uathoibriú stóca."),
    ("ga-IE", "3605", "Bailíochtú uathoibriú stóca."),
    ("ga-IE", "3606", "Ní féidir uathoibriú stóca a bhailíochtú."),
    ("ga-IE", "2101", "Léamh na siombailí ón aibítir i uathoibriú éighníomhach."),
    ("ga-IE", "2102", "Cuir siombail le aibítir uathoibriú éighníomhach."),
    ("it-IT", "2403", "Rimuovere una regola grammaticale da un automa sensibile al contesto."),
    ("it-IT", "2406", "La regola grammaticale aggiunta è malformata."),
    ("it-IT", "2302", "Aggiungere uno stato a un automa sensibile al contesto."),
    ("it-IT", "2303", "Rimuovere uno stato da un automa sensibile al contesto."),
    ("it-IT", "2304", "Modificare uno stato in un automa sensibile al contesto."),
    ("it-IT", "2202", "Aggiungere una transizione a un automa sensibile al contesto."),
    ("it-IT", "2203", "Rimuovere una transizione da un automa sensibile al contesto."),
    ("it-IT", "2204", "Modificare una transizione in un automa sensibile al contesto."),
    ("sv-SV", "4605", "Validera en ändlig automat."),
    ("sv-SV", "4606", "Kunde inte validera den ändliga automaten."),
    ("sv-SV", "4506", "Duplicerat tillstånd finns redan i automaten."),
    ("sv-SV", "4505", "Tillståndet är inte tillgängligt från starttillståndet."),
    ("sv-SV", "4503", "Konfliktande övergång finns i automaten."),
    ("sv-SV", "3101", "Läsa symbolerna från alfabetet för en stackautomat."),
    ("sv-SV", "3102", "Lägg till en symbol till alfabetet för en stackautomat."),
    ("sv-SV", "3103", "Ta bort en symbol från alfabetet för en stackautomat."),
    ("sv-SV", "3502", "Lägg till en symbol på stacken för en stackautomat."),
    ("sv-SV", "3503", "Ta bort en symbol från stacken för en stackautomat."),
    ("sv-SV", "3519", "Försök att ta bort symbol från en tom stack."),
    ("sv-SV", "3505", "Stacken överskrider kapaciteten."),
    ("sv-SV", "3302", "Lägg till ett tillstånd i en stackautomat."),
    ("sv-SV", "3303", "Ta bort ett tillstånd från en stackautomat."),
    ("sv-SV", "3304", "Ändra ett tillstånd i en stackautomat."),
    ("sv-SV", "3202", "Lägg till en övergång i en stackautomat."),
    ("sv-SV", "3203", "Ta bort en övergång från en stackautomat."),
    ("sv-SV", "3204", "Ändra en övergång i en stackautomat."),
    ("sv-SV", "3605", "Validera en stackautomat."),
    ("sv-SV", "3606", "Kunde inte validera stackautomaten."),
    ("sv-SV", "2101", "Läsa symbolerna från alfabetet för en kontextkänslig automat."),
    ("sv-SV", "2102", "Lägg till en symbol till alfabetet för en kontextkänslig automat."),
    ("sv-SV", "2103", "Ta bort en symbol från alfabetet för en kontextkänslig automat."),
    ("sv-SV", "2402", "Lägg till en grammatisk regel för en kontextkänslig automat."),
    ("sv-SV", "2403", "Ta bort en grammatisk regel från en kontextkänslig automat.")
])
def test_get_automata_message_id(lang, msg_id, excepted_msg):
    result = get_message(msg_id, "automata", lang)
    assert result == excepted_msg


# Test : Generate code et get related automata messages

@pytest.mark.parametrize("lang, grammar, component, action, expected_msg", [
    ("de-DE", "Regular", "alphabet", "read", "Lese Symbole aus dem Alphabet eines endlichen Automaten."),
    ("de-DE", "Regular", "alphabet", "add", "Füge ein Symbol zum Alphabet eines endlichen Automaten hinzu."),
    ("de-DE", "Regular", "states", "modify", "Ändere einen Zustand in einem endlichen Automaten."),
    ("de-DE", "Regular", "transitions", "add", "Füge einen Übergang zu einem endlichen Automaten hinzu."),
    ("en-GB", "Regular", "stack", "remove", "A conflicting transition exists in the automaton."),
    ("en-GB", "Context-Free", "alphabet", "read", "Read the symbols of the alphabet of a pushdown automaton."),
    ("en-GB", "Context-Free", "alphabet", "add", "Add a symbol to the alphabet of a pushdown automaton."),
    ("en-US", "Context-Sensitive", "transitions", "modify", "Modify a transition in a context-sensitive automaton."),
    ("en-US", "Context-Sensitive", "validation", "validate", "Validate a context-sensitive automaton."),
    ("en-US", "Context-Sensitive", "validation", "search", "Failed to validate the context-sensitive automaton."),
    ("es-ES", "Context-Free", "states", "modify", "Modificar un estado en un autómata de pila."),
    ("es-ES", "Context-Free", "transitions", "add", "Agregar una transición a un autómata de pila."),
    ("es-ES", "Context-Free", "transitions", "remove", "Eliminar una transición de un autómata de pila."),
    ("fr-FR", "Context-Free", "alphabet", "remove", "Supprimer un symbole de l'alphabet d'un automate à pile."),
    ("fr-FR", "Context-Free", "stack", "add", "Ajouter un symbole à la pile d'un automate à pile."),
    ("fr-FR", "Context-Free", "stack", "remove", "Supprimer un symbole de la pile d'un automate à pile."),
    ("fr-FR", "Context-Free", "stack", "withdraw", "Tentative de retirer un symbole d'une pile vide."),
    ("fr-FR", "Context-Sensitive", "validation", "search", "Échec de la validation de l'automate contextuel."),
    ("fr-FR", "Recursively Enumerable", "alphabet", "read", "Lire les symboles de l'alphabet d'une machine de Turing."),
    ("fr-FR", "Recursively Enumerable", "alphabet", "add", "Ajouter un symbole à l'alphabet d'une machine de Turing."),
    ("fr-FR", "Recursively Enumerable", "alphabet", "remove",
     "Supprimer un symbole de l'alphabet d'une machine de Turing."),
])
def test_generate_message(lang, grammar, component, action, expected_msg):
    result = generate_message(grammar, component, action, "automata", lang)
    assert result == expected_msg


# Test : Get errors messages

@pytest.mark.parametrize("lang, msg_id, txt, expected_msg", [
    ("de-DE", "1102", {'symbol': "U"},
     "Das Symbol 'U' kann nicht hinzugefügt werden, da es bereits im Alphabet der Turing-Maschine existiert."),
    ("en-GB", "2303", {'symbol': "Open"},
     "Unable to remove the state 'Open' as it does not exist in the context-sensitive automaton."),
    ("en-US", "2202", {'transition': "Push"},
     "The transition 'Push' already exists in the context-sensitive automaton."),
    ("es-ES", "4203", {'transition': "sUs"},
     "No se puede eliminar la transición 'sUs' porque no existe en el autómata finito."),
    ("fr-FR", "2605", {'reason': "règles mal formées"},
     "L'automate contextuel est invalide : règles mal formées."),
    ("ga-IE", "3302", {'symbol': 'N'}, "Tá an staid 'N' cheana san aonad puinse."),
    ("it-IT", "1103", {'symbol': "*"},
     "Impossibile rimuovere il simbolo '*' perché non esiste nell'alfabeto della macchina di Turing."),
    ("sv-SV", "3519", {}, "Fel: försök att ta bort en symbol från en tom stack.")
])
def test_get_errors_message(lang, msg_id, txt, expected_msg):
    result = get_message(msg_id, "errors", lang, **txt)
    assert result == expected_msg


@pytest.mark.parametrize("lang, grammar, component, action, txt, expected_msg", [
    ("de-DE", "Recursively Enumerable", "alphabet", "add", {'symbol': "U"},
     "Das Symbol 'U' kann nicht hinzugefügt werden, da es bereits im Alphabet der Turing-Maschine existiert."),
    ("en-GB", "Context-Sensitive", "states", "remove", {'symbol': "Open"},
     "Unable to remove the state 'Open' as it does not exist in the context-sensitive automaton."),
    ("en-US", "Context-Sensitive", "transitions", "add", {'transition': "Push"},
     "The transition 'Push' already exists in the context-sensitive automaton."),
    ("es-ES", "Regular", "transitions", "remove", {'transition': "sUs"},
     "No se puede eliminar la transición 'sUs' porque no existe en el autómata finito."),
    ("fr-FR", "Context-Sensitive", "validation", "validate", {'reason': "règles mal formées"},
     "L'automate contextuel est invalide : règles mal formées."),
    ("ga-IE", "Context-Free", "states", "add", {'symbol': 'N'}, "Tá an staid 'N' cheana san aonad puinse."),
    ("it-IT", "Recursively Enumerable", "alphabet", "remove", {'symbol': "*"},
     "Impossibile rimuovere il simbolo '*' perché non esiste nell'alfabeto della macchina di Turing."),
    ("sv-SV", "Context-Free", "stack", "withdraw", {}, "Fel: försök att ta bort en symbol från en tom stack.")
])
def test_generate_errors_message(lang, grammar, component, action, txt, expected_msg):
    result = generate_message(grammar, component, action, "errors", lang, **txt)
    assert result == expected_msg


@pytest.mark.parametrize("grammar, component, action, domain, lang, txt, expected_exception, expected_msg", [
    ("Regular", "state", "read", "automata", "fr-FR", {}, KeyError, "Unknown component name"),
    ("Regular", "alphabet", "withdraw", "automata", "en-US", {}, KeyError,
     "The message with ID '4119' was not found for language 'en-US'."),
    ("Regular", "states", "read", "automaton", "fr-FR", {}, FileNotFoundError,
     "The JSON file for domain 'automaton' was not found."),
    ("Regular", "validation", "validate", "errors", "sv-SV", {'symbol': "U"}, ValueError,
     "The parameter 'reason' is missing for formatting the message.")
])
def test_generate_message_with_exception(grammar, component, action, domain, lang, txt, expected_exception,
                                         expected_msg):
    with pytest.raises(expected_exception, match=expected_msg):
        generate_message(grammar, component, action, domain, lang, **txt)
