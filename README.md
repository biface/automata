# Lecteur français

Les machines à états finis sont des machines abstraites très utiles pour la modélisation et le contrôle de processus.
Ils sont constitués d'états _stables_ et de transitions. Un automate est dit _fini_, car il possède un nombre fini
d'états. Il passe d'un état à un autre par les transitions qui ont été définies.

Dans ce module python il y a deux implémentations des machines à états finis :

* Une version allégée qui utilise simplement des dictionnaires pour enregistrer les transitions d'états.
* Une version plus avancée qui s'appuie sur des classes d'objet pour décrire le quadruplet constitutif de ce type
d'automate.

Ce module embraque aussi un développement spécifique pour transcrire ces machines à états sous forme de contextes pour
être exploités dans l'environnement de publication du framework [Django](https://docs.djangoproject.com/fr/5.1/).  

# English reader and ROW

Finite-state machines (FSM) are abstract machines that are very useful for modeling and controlling processes.
They are made up of _stable_ states and transitions. An automaton is said to be _finite_ because it has a finite number
of states. It moves from one state to another via defined transitions.

In this python module there are two implementations of finite state machines:

* A light version that simply uses dictionaries to record state transitions.
* A more advanced version that uses object classes to describe the quadruplet of this type of automaton.

This module also embraces specific development to transcribe these state machines into contexts for use in the
[Django framework's](https://docs.djangoproject.com/en/5.1/) publishing environment. 
