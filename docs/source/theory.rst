Introduction to Formal Language Theory and Finite State Machines
****************************************************************

Formal language theory and finite state machines (FSMs) - or automata (FSA) - provide a foundation for understanding how
computational systems operate and how structured languages are defined and processed.

FSMs are not only theoretical models for understanding computation and languages but also extensively
used in practical applications. Their simplicity, clarity and structure make them invaluable tools for modeling
processes and controlling workflows in various domains.

FSMs provide structured way to represent states (distinct configuration of a system) and transitions between them,
driven by external inputs or events. This makes FSMs/FSA particularly effective in modeling systems where behavior
depends on sequences of events, such as industrial processes, software applications, and workflow automation.

**FSMs in Process Modeling**

Process modeling involves breaking down complex workflow into discrete, manageable steps. FSMs are ideal for this
because :

    1. **State Representation**: Each State in FSMs corresponds to a specific phase or condition of the process.
    2. **Transitions**: Events, conditions, or user actions trigger transitions between states, defining how the process evolves
    3. **Determinism**: FSMs ensure that the process follows a clear, logical path, avoiding ambiguities.

**FSMs in Workflow Control**

In Software systems, FSMs help manage workflow by dictating the flow of tasks, ensuring that the system behaves
predictably and efficiently. Application includes :

    1. **User Interface Navigation**: FSMs model how users navigate through an application, such as states for *Home screen, Settings* and *Profile*.
    2. **Workflow Automation**: FSMs control task dependencies, ensuring one task cannot begin until its prerequisites are complete.

**Advantages of FSMs in Practical Applications**

    1. **Clarity**:FSMs provide a visual and logical structure for understanding and communicating workflows.
    2. **Simplicity**: The finite nature of states ensures systems remain manageable.
    3. **Robustness**: FSMs ensure consistency, reducing errors in processes and workflows.
    4. **Versatility**: FSMs are used in diverse domains, including robotics, software engineering, industrials automation,...

This document is not intended to be a course on formal language theory and finite state machines. What follows is an
introduction and guide to key concepts, presented in a logical manner for clarity and progression. These elements will
be taken up again in advanced implementation of finite state automata. Below you can find information on :

    1. Alphabet and languages
    2. Terminals and Non-terminals
    3. The Kleene Star
    4. The Chomsky Hierarchy
    5. Finite State Machines
    6. Building an FSM from a Regular Grammar


**Detailed Chapter Content**

.. toctree::
    alphabet
    kleene
    chomsky
    fsm