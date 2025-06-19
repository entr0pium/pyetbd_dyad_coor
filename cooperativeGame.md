# Cooperative Game Rules and Logic

This document outlines the rules and step-by-step progression for a cooperative game involving a dyad of two Artificial Organisms (AOs).

## 1. Core Concepts
- **Artificial Organism (AO)**: An agent in the simulation. The game involves a dyad of two AOs, referred to as AO1 and AO2.
- **Population (POP)**: Each AO is endowed with three distinct populations of potential behaviors (bit-strings). Each POP contains 100 potential behaviors.
  - **POP1**: Used by an AO when it is the first-mover in a trial.
  - **POP2**: Used by an AO when it is the second-mover and the first-mover made a left-move.
  - **POP3**: Used by an AO when it is the second-mover and the first-mover made a right-move.
- **Dyad**: The pair of AOs (AO1 and AO2) partaking in a trial.
- **Trial**: A single iteration of the game, which consists of a two-response sequence (one from each AO). A new trial begins after the previous one concludes.

**Target Behaviors:**
- **Left-Move**: An emitted integer in the range of 471 through 511.
- **Right-Move**: An emitted integer in the range of 512 through 552.
- **Non-Target Move**: Any emitted integer outside the ranges defined above (i.e., 0-470 and 553-1023).

## 2. Trial Structure Overview
A single trial unfolds as follows, as illustrated in the flowchart (Figure 5):

1. **Coin-Toss**: A 50/50 random chance determines which AO is the first-mover. The other becomes the second-mover.
2. **First Move**: The first-mover emits behaviors from its POP1 until a target behavior (left or right) is produced.
3. **Second Move**: The second-mover responds from either its POP2 or POP3, depending on the first move.
4. **Consequence**: Based on the sequence of moves and the availability of reinforcement, the populations of both AOs are updated via selection, mating, and mutation.
5. **Conclusion**: The trial ends, and the process repeats from the coin-toss.

## 3. Detailed Step-by-Step Trial Progression
This section assumes AO2 wins the coin-toss and becomes the first-mover. The logic is identical if AO1 wins, with the roles reversed.

### 3.1. Initialization
1. **Instantiate AOs**: AO1 and AO2 are created.
2. **Populate Behaviors**: For each AO, POP1, POP2, and POP3 are each filled with 100 random bit-strings.
3. **Start Environment**: The cooperative game program, including the two independent Random Interval (RI) schedules (one for left-left sequences, one for right-right), is executed.

### 3.2. The Coin-Toss
- The program randomly selects AO2 as the first-mover, queuing it to respond from its POP1.

### 3.3. First-Mover's Turn (AO2)
1. **Emission**: AO2 emits a behavior (integer) from its POP1.
2. **Evaluation**: The emitted behavior is checked:
   - **If Non-Target (0-470 or 553-1023):**
     - The random selection function operates on AO2's POP1.
     - The population is updated via mating and mutation.
     - Repeat until a target move is made.
   - **If Left-Move (471-511):** Advance to Second-Mover Scenario A.
   - **If Right-Move (512-552):** Advance to Second-Mover Scenario B.

### 3.4. Second-Mover's Turn (AO1)
**Scenario A: First-Mover (AO2) Chose LEFT**
- AO1 responds from POP2.
  1. **Case 1**: AO1 moves LEFT (Cooperation: Left-Left)
     - Consult left-side RI component.
     - If **Reinforcement AVAILABLE**: Midpoint fitness selection on AO1's POP2 and AO2's POP1.
     - If **Reinforcement NOT AVAILABLE**: Random selection on both populations.
  2. **Case 2**: AO1 moves RIGHT (Non-cooperation: Left-Right)
     - Random selection on both populations.
  - Trial concludes and returns to coin-toss.

**Scenario B: First-Mover (AO2) Chose RIGHT**
- AO1 responds from POP3.
  1. **Case 1**: AO1 moves RIGHT (Cooperation: Right-Right)
     - Consult right-side RI component.
     - If **Reinforcement AVAILABLE**: Midpoint fitness selection on AO1's POP3 and AO2's POP1.
     - If **Reinforcement NOT AVAILABLE**: Random selection on both populations.
  2. **Case 2**: AO1 moves LEFT (Non-cooperation: Right-Left)
     - Random selection on both populations.
  - Trial concludes and returns to coin-toss.
