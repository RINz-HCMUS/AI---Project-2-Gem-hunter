<a name="br1"></a> 

University of Science - VNUHCM

Faculty of Information Technology

PROJECT REPORT

Topic: Gem hunter

Course: Artiﬁcial Intelligence

Student:

Lecturer:

Ho Minh Dang - 22127050

Vo Hung Khoa - 22127202

Nguyen Binh Minh - 2217266

Vo Huu Tuan - 22127439

Le Ngoc Thanh

Nguyen Ngoc Thao

Nguyen Hai Dang

Nguyen Tran Duy Minh



<a name="br2"></a> 

University of Science - VNUHCM

Artiﬁcial Intelligence

PROJECT REPORT

Contents

[1](#br4)[ ](#br4)[Information](#br4)

3

[1.1](#br4)[ ](#br4)[Member](#br4)[ ](#br4)[Information](#br4)[ ](#br4). . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

3

3

3

[1.2](#br4)[ ](#br4)[Project](#br4)[ ](#br4)[Information](#br4)[ ](#br4). . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

[1.3](#br4)[ ](#br4)[Checklist](#br4)[ ](#br4). . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

[2](#br5)[ ](#br5)[Running](#br5)[ ](#br5)[Instruction](#br5)

4

[3](#br6)[ ](#br6)[Logical](#br6)[ ](#br6)[principles](#br6)[ ](#br6)[for](#br6)[ ](#br6)[generating](#br6)[ ](#br6)[CNFs](#br6)

5

5

6

6

[3.1](#br6)[ ](#br6)[Example](#br6)[ ](#br6)[case](#br6)[ ](#br6). . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

[3.2](#br7)[ ](#br7)[2-trap](#br7)[ ](#br7)[CNF](#br7)[ ](#br7). . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

[3.3](#br7)[ ](#br7)[k-trap](#br7)[ ](#br7)[CNF](#br7)[ ](#br7). . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

[4](#br8)[ ](#br8)[Brute-force](#br8)[ ](#br8)[algorithm](#br8)

7

7

7

8

[4.1](#br8)[ ](#br8)[Initial](#br8)[ ](#br8)[idea](#br8)[ ](#br8). . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

[4.2](#br8)[ ](#br8)[Better](#br8)[ ](#br8)[ideas](#br8)[ ](#br8)[to](#br8)[ ](#br8)[implement](#br8)[ ](#br8). . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

[4.3](#br9)[ ](#br9)[Pros](#br9)[ ](#br9)[and](#br9)[ ](#br9)[Cons](#br9)[ ](#br9). . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

[5](#br10)[ ](#br10)[Backtracking](#br10)[ ](#br10)[algorithm:](#br10)[ ](#br10)[DPLL](#br10)

9

9

9

9

[5.1](#br10)[ ](#br10)[Function](#br10)[ ](#br10). . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

[5.1.1](#br10)[ ](#br10)[unit](#br10)[ ](#br10)[propagate](#br10)[ ](#br10)[function](#br10)[ ](#br10). . . . . . . . . . . . . . . . . . . . . . . . . . . . .

[5.1.2](#br10)[ ](#br10)[DPLL](#br10)[ ](#br10). . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

[5.2](#br11)[ ](#br11)[Pros](#br11)[ ](#br11)[and](#br11)[ ](#br11)[Cons](#br11)[ ](#br11). . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 10

[6](#br13)[ ](#br13)[Optimal](#br13)[ ](#br13)[Algorithm](#br13)[ ](#br13)12

[6.1](#br13)[ ](#br13)[Introduction](#br13)[ ](#br13). . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 12

[6.2](#br13)[ ](#br13)[Function](#br13)[ ](#br13)[overview](#br13)[ ](#br13). . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 12

[6.2.1](#br13)[ ](#br13)[Input](#br13)[ ](#br13)[Grid](#br13)[ ](#br13)[Preparation](#br13)[ ](#br13). . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 12

[6.2.2](#br14)[ ](#br14)[CNF](#br14)[ ](#br14)[Clause](#br14)[ ](#br14)[Generation](#br14)[ ](#br14). . . . . . . . . . . . . . . . . . . . . . . . . . . . . 13

[6.2.3](#br14)[ ](#br14)[SAT](#br14)[ ](#br14)[Solving](#br14)[ ](#br14)[with](#br14)[ ](#br14)[Heuristic](#br14)[ ](#br14). . . . . . . . . . . . . . . . . . . . . . . . . . . 13

[6.2.4](#br14)[ ](#br14)[Solution](#br14)[ ](#br14)[Processing](#br14)[ ](#br14). . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 13

[6.2.5](#br14)[ ](#br14)[Ouput](#br14)[ ](#br14). . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 13

1



<a name="br3"></a> 

University of Science - VNUHCM

Artiﬁcial Intelligence

PROJECT REPORT

[6.3](#br16)[ ](#br16)[Pros](#br16)[ ](#br16)[and](#br16)[ ](#br16)[Cons](#br16)[ ](#br16). . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 15

[6.3.1](#br16)[ ](#br16)[Pros](#br16)[ ](#br16). . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 15

[6.3.2](#br16)[ ](#br16)[Cons](#br16)[ ](#br16). . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 15

[6.4](#br16)[ ](#br16)[Conclusion](#br16)[ ](#br16). . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 15

[7](#br18)[ ](#br18)[Running](#br18)[ ](#br18)[Time](#br18)[ ](#br18)[Comparison](#br18)

17

[7.1](#br18)[ ](#br18)[Level](#br18)[ ](#br18)[1](#br18)[ ](#br18). . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 17

[7.2](#br18)[ ](#br18)[Level](#br18)[ ](#br18)[2](#br18)[ ](#br18). . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 17

[7.3](#br18)[ ](#br18)[Level](#br18)[ ](#br18)[3](#br18)[ ](#br18). . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 17

[7.4](#br19)[ ](#br19)[Level](#br19)[ ](#br19)[4](#br19)[ ](#br19). . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 18

[7.5](#br19)[ ](#br19)[Level](#br19)[ ](#br19)[5](#br19)[ ](#br19). . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 18

[8](#br20)[ ](#br20)[Additonal](#br20)[ ](#br20)[Information](#br20)

[Reference](#br21)

19

20

2



<a name="br4"></a> 

University of Science - VNUHCM

Artiﬁcial Intelligence

PROJECT REPORT

1 Information

1\.1 Member Information

No. ID

Name

22127050 Ho Minh Dang

Note

1

2

3

4

22127202 Vo Hung Khoa Leader

22127266 Nguyen Binh Minh

22127439 Vo Huu Tuan

Table 1: Student Information

1\.2 Project Information

Name project Gem Hunter

Environment Python 3.10.11

Graphic library Tkinter + PIL

IDE VScode

Table 2: Project information table

1\.3 Checklist

No. Speciﬁcations Scores

Member Progress (%)

1

2

3

4

5

6

7

8

Logical principles for generating CNFs.

Dang & Minh

Dang

Dang

Khoa

Tuan

Minh

Tuan

All members

100%

100%

100%

100%

100%

100%

100%

100%

Generate CNFs automatically

Solve CNF using Pysat library

Implement an optimal algorithm without a library

Brute-force algorithm

Backtracking algorithm

Generate map

Report

Table 3: Checklist table

3



<a name="br5"></a> 

University of Science - VNUHCM

Artiﬁcial Intelligence

PROJECT REPORT

2 Running Instruction

Prerequisites:

• Python installed.

• Pysat library installed.

This is a guide on how to run the project ”Gem Hunter” from source code.

1\. First locate the ”GUI.py” ﬁle in the ”Source/Source code” folder

2\. Then open the ﬁle in Visual Studio code. On the upper right corner of the Visual Studio

Code editor choose the down arrow symbol next to the Play symbol

Figure 1: Button

3\. Choose ”Run Python File” to execute the program.

4\. (Alternative) Open the ”Source code” folder in the terminal and run the command ”py

GUI.py” to execute the program.

5\. Proceed to watch the demo video in order to use the program.

4



<a name="br6"></a> 

University of Science - VNUHCM

Artiﬁcial Intelligence

PROJECT REPORT

3 Logical principles for generating CNFs

3\.1 Example case

In order to create a CNF formula, we need to take a closer look in to a case.

Example case:

X1 = Trap X2 = Trap X3

X8

X7

Number = 2 X4

X6 X5

Table 4: 2 traps

Let X1, X2 are traps, the other Xi is anything but trap. To make this case true the CNF must be:

(X1 ∧ X2) ⇔ (¬X3 ∧ ¬X4 ∧ . . . ∧ ¬X8)

This CNF means that if X1 and X2 are “Trap” then the others are not and vice versa.

But as you can see, turning this logic into code is not easy. Therefore we need to reformulate the

logic above into something much easier to code:

≡ [(X1 ∧ X2) ⇒ (¬X3 ∧ ¬X4 ∧ . . . ∧ ¬X8)] ∧ [(¬X3 ∧ ¬X4 ∧ . . . ∧ ¬X8) ⇒ (X1 ∧ X2)]

≡ [¬(X1 ∧ X2) ∨ (¬X3 ∧ ¬X4 ∧ . . . ∧ ¬X8)] ∧ [(X3 ∨ X4 ∨ . . . ∨ X8) ∨ (X1 ∧ X2)]

≡ [(¬X1 ∨ ¬X2) ∨ (¬X3 ∧ ¬X4 ∧ . . . ∧ ¬X8)] ∧ [(X3 ∨ X4 ∨ . . . ∨ X8) ∨ (X1 ∧ X2)]

≡ [(¬X1 ∨ ¬X2 ∨ ¬X3) ∧ (¬X1 ∨ ¬X2 ∨ ¬X4) ∧ . . . ∧ (¬X1 ∨ ¬X2 ∨ ¬X8)]

∧ [(X1 ∨ X3 ∨ X4 ∨ X5 ∨ . . . ∨ X8) ∧ (X2 ∨ X3 ∨ X4 ∨ X5 ∨ . . . ∨ X8)]

Let explain each part:

• (¬X1 ∨ ¬X2 ∨ ¬Xi): with i from 3 to 8, this clause only false if there are more than 3 traps.

• (Xy ∨ X3 ∨ X4 ∨ X5 ∨ . . . ∨ X8): with y from 1 to 2, the clause only false if there are no trap

at all

We have successfully turn the original CNF into multiple small clauses.

In the above example case, there are 2 traps at the precise location 1, 2. What happens if we know

only the amount of traps but not the location?

5



<a name="br7"></a> 

University of Science - VNUHCM

Artiﬁcial Intelligence

PROJECT REPORT

3\.2 2-trap CNF

To generate CNF for unknown number of trap location, we call the ﬁrst part is L and the second

part is U:

CNF = L ∧ U.

• L = (¬Xa ∨ ¬Xb ∨ ¬Xc); the number of possible combinations of 3 variables Xa, Xb, Xc

ꢀ ꢁ

8

3

from a set of 8 variables is

• U = (Xa∨Xb∨Xc∨Xd∨Xe∨Xf ∨Xg); the number of possible combinations of 7 variables

ꢀ ꢁ

8

7

Xa, Xb, Xc, Xd, Xe, Xf, Xg from a set of 8 variables is

We have successfully generalized a 2-trap CNF. But how to make 3-trap CNF, 4-trap CNF?

3\.3 k-trap CNF

Formulate the general k-trap CNF logic:

CNF(k, n) = L(k + 1) ∧ U(n − k + 1)

Let CNF(k, n) with k is the number of traps in n surrounding cells.

• L(k+ 1): (k+1)-combination of n cells taken from {Xa, . . . , Xn} to create (¬Xx∨. . .∨¬Xy)

• U(n − k + 1): (n − k + 1)-combination of n cells taken from {Xa, . . . , Xn} to create (Xx ∨

. . . ∨ Xy)

6



<a name="br8"></a> 

University of Science - VNUHCM

Artiﬁcial Intelligence

PROJECT REPORT

4 Brute-force algorithm

4\.1 Initial idea

Initially, the brute-force algorithm is based on the state of each unknown-cell (cells marked with

” ”): Each unknown-cell can either be a trap or a gem, meaning each unknown-cell has 2 states.

Therefore, we need to check all possible states of the N ∗ N cells in the map to ﬁnd the solution!

According to this calculation, in the worst-case, we have to consider all 2<sup>N2</sup> states. This is a huge

problem because, for N = 10, the total number of states is 2<sup>100</sup> ≈ 1.26 \*10<sup>30</sup>, an enormous number!

It is a very large number, not to mention the case of N = 20, it is 2<sup>400</sup>≈ 2.5 \* 10<sup>120</sup> states. Surely,

this poses a signiﬁcant challenge for a computer!

4\.2 Better ideas to implement

Therefore, the new idea for the brute-force algorithm is to consider the number of unexplored cells

based on the number-cells (cells with integer values). The idea is as follows:

• The unknown-cell with the highest number of number-cells around will be marked as a trap.

• Decrease the value of the number-cells by 1 if there is a neighboring cell marked as a trap.

• If there is a number cell with a value of 0, the unexplored cell near it will be marked as a gem.

With the simple idea above, the algorithm will work as follows:

1\. Iterate through all cells in the map:

(a) If the cell is unknown: Perform step 2

(b) Otherwise, skip

2\. Check the neighboring cells of the current cell:

(a) If there is a number-cell with a value of 0: Mark the current cell as a gem and move to

the next cell

(b) Otherwise, increase the count of number-cells of the current cell by 1

7



<a name="br9"></a> 

University of Science - VNUHCM

Artiﬁcial Intelligence

PROJECT REPORT

3\. After iterating through all cells, the cell with the highest number of neighboring number-cells

will be marked as a trap, and the value of all neighboring number-cells will be decreased by

1\.

4\. Repeat the process until there are no unknown-cells left.

With the above operating method, the complexity of the algorithm is signiﬁcantly reduced! We

only need to traverse the map based on the number of unexplored cells (less than N \* N cells), each

cell needs to check 8 neighboring cells and decrease the value of the neighboring number-cells after

each iteration. Therefore, the worst-case will have a complexity of O(N) = N ∗ N ∗ (N ∗ N ∗ 8 + 8).

With N = 20, O(20) = 1, 280, 032, 000 = 1, 28 ∗ 10<sup>10</sup>, faster than the initial idea by nearly 10<sup>110</sup>

times!

4\.3 Pros and Cons

Pros:

• Simple idea: easy to understand and implement.

• Completeness: It is guaranteed to ﬁnd a satisfying assignment if one exists.

Cons:

• Worst-case Time Complexity: The algorithm can become prohibitively slow for maps with

large sizes.

• Memory Eﬃciency: The algorithm consumes a lot of memory space for memorization when

iterating over unknown-cells

8



<a name="br10"></a> 

University of Science - VNUHCM

Artiﬁcial Intelligence

PROJECT REPORT

5 Backtracking algorithm: DPLL

Davis–Putnam–Logemann–Loveland (DPLL) algorithm is a complete, backtracking-based search

algorithm for deciding the satisﬁability of propositional logic formulae in conjunctive normal form,

i.e. for solving the CNF-SAT problem.

5\.1 Function

5\.1.1 unit propagate function

The purpose of the unit propagate function is to simplify the given CNF (Conjunctive Normal

Form) formula by identifying and propagating unit clauses.

A unit clause is a clause that contains only one unassigned literal.

5\.1.2 DPLL

This is an step by step illustration of how DPLL - iterative version works.

1\. Initialization: Initialize a stack with the initial CNF formula and an empty set of variable

assignments. Start with an empty stack.

2\. Main Loop: While the stack is not empty, repeat the following steps:

3\. Unit Propagation: Pop a formula and assignments from the top of the stack. Perform unit

propagation on the formula with the current assignments.

4\. Conﬂict Check: If there are any empty clauses (indicating a conﬂict), skip to the next iteration

of the loop.

5\. Satisﬁability Check: If the formula becomes empty after unit propagation (all clauses are

satisﬁed), return True along with the satisfying assignment.

6\. Variable Selection: If there are unassigned literals remaining, choose a literal (non-deterministically

in this implementation).

7\. Branching: Create two new branches by assigning the chosen literal to True and False, re-

spectively.

9



<a name="br11"></a> 

University of Science - VNUHCM

Artiﬁcial Intelligence

PROJECT REPORT

8\. Push Branches onto Stack: Push these two new branches (modiﬁed formulas and assignments)

onto the stack.

9\. Termination: If the loop terminates without ﬁnding a satisfying assignment, return False.

10\. Backtracking: Backtracking is implicitly handled by the stack. If a branch fails (returns

False), the algorithm simply continues with the next branch on the stack.

5\.2 Pros and Cons

Pros:

• Completeness: It is guaranteed to ﬁnd a satisfying assignment if one exists.

• Eﬃciency in Practice: While the worst-case time complexity of DPLL is exponential. Vari-

ous optimizations, such as unit propagation, pure literal elimination, and eﬃcient branching

strategies, can signiﬁcantly improve performance.

• Memory Eﬃciency: The iterative version of DPLL can be memory-eﬃcient, as it avoids the

overhead of recursive function calls by using a stack to maintain state.

Cons:

• Exponential Worst-case Time Complexity: The algorithm can become prohibitively slow for

very large or complex CNF formulas.

• Limited Performance Guarantees: While DPLL is complete, it does not provide any perfor-

mance guarantees in terms of runtime.

• Diﬃculty with Hard Instances: There are certain classes of SAT instances known as ”hard”

instances for which DPLL may struggle to ﬁnd a solution within a reasonable amount of time.

• Example for a hard instance:

– In level 4, the map 20x20 has an interesting layout that makes the DPLL algorithm runs

extremely slower that other algorithm, even the brute force algorithm.

10



<a name="br12"></a> 

University of Science - VNUHCM

Artiﬁcial Intelligence

PROJECT REPORT

Figure 2: 20x20 map

– The DPLL algorithm performed much worse than any other algorithm because the con-

stantly back tracking to ﬁnd the satisﬁed condition.

Figure 3: DPLL runtime compare to other

11



<a name="br13"></a> 

University of Science - VNUHCM

Artiﬁcial Intelligence

PROJECT REPORT

6 Optimal Algorithm

To solve this problem, we have chosen a basic backtracking technique to assign variables and

eliminate invalid assignments. To make the variable assignment more eﬃcient, we additionally

use the Jeroslow-Wang (JW) heuristic function to achieve that.

6\.1 Introduction

The Jeroslow-Wang (JW) heuristic is used to prioritize variable assignment during the solving

process of the Boolean Satisﬁability Problem (SAT). It assesses the importance of each variable

based on its frequency of occurrence in positive literals across the Conjunctive Normal Form (CNF)

clauses. The JW score of a variable is calculated by summing the exponential of the negative length

of each clause containing the variable. Variables with higher JW scores are given priority during

variable selection, as they are more likely to contribute signiﬁcantly to ﬁnding a valid assignment,

thus enhancing the eﬃciency of the SAT-solving algorithm.

6\.2 Function overview

6\.2.1 Input Grid Preparation

• The algorithm takes the input grid representing the Minesweeper game and its size.

Figure 4: Structure of an input ﬁle

12



<a name="br14"></a> 

University of Science - VNUHCM

Artiﬁcial Intelligence

PROJECT REPORT

6\.2.2 CNF Clause Generation

• For each cell in the grid, the algorithm generates CNF (Conjunctive Normal Form) clauses

based on the Minesweeper rules.

• It identiﬁes neighboring cells and generates clauses to satisfy the numeric clues provided in

the grid.

6\.2.3 S AT Solving with Heuristic

• The algorithm attempts to solve the SAT (Boolean Satisﬁability Problem) generated from the

CNF clauses.

• It employs backtracking along with the Jeroslow-Wang (JW) heuristic to eﬃciently explore

the solution space.

• Backtracking involves recursively assigning truth values to variables and backtracking when

a contradiction is encountered.

• The JW heuristic guides variable selection, prioritizing variables with higher Jeroslow-Wang

scores.

6\.2.4 Solution Processing

• If a satisfying assignment is found, the algorithm processes the assignment to generate the

solution grid.

• It maps the assignment to the cells of the original grid, marking mines (’T’) or safe cells (’G’)

accordingly.

• If no satisfying assignment is found, the algorithm concludes that no solution exists.

6\.2.5 Ouput

• The algorithm returns the solution grid if a solution is found.

• If no solution is found, it indicates the absence of a valid solution.

13



<a name="br15"></a> 

University of Science - VNUHCM

Artiﬁcial Intelligence

PROJECT REPORT

Figure 5: Display result

Figure 6: The output is also saved in a ﬁle in folder ”output”

14



<a name="br16"></a> 

University of Science - VNUHCM

Artiﬁcial Intelligence

PROJECT REPORT

6\.3 Pros and Cons

6\.3.1 Pros

• Easy Implementation: The algorithm utilizes basic backtracking and simple heuristics like

JW, making it easy to implement and understand.

• Problem-solving Capability: The algorithm can solve the Minesweeper problem by ﬁnding a

solution that satisﬁes the Boolean constraints described.

• Flexibility: Other heuristic functions can be modiﬁed or added to improve the algorithm’s

performance.

6\.3.2 Cons

• Suboptimal Performance: Using basic backtracking and JW heuristics may result in subopti-

mal performance, especially when solving large or complex problems.

• Incomplete Search Capability: Due to the use of backtracking, the algorithm may fail to ﬁnd

a solution within a reasonable time for large-sized problems.

• Potential for Inﬁnite Loops: In some cases, the algorithm may run into inﬁnite loops if it

cannot ﬁnd a solution or eliminate invalid situations.

6\.4 Conclusion

• The algorithm sequentially performs grid preparation, CNF clause generation, SAT solving

with backtracking and heuristic, solution processing, and output generation.

• By combining backtracking with the JW heuristic, the algorithm eﬃciently solves the Minesweeper

game, providing accurate solutions when possible.

• Generally, due to its use of basic backtracking, this algorithm may be less optimized compared

to commonly used algorithms like DPLL or libraries like Pysat. Therefore, its processing time

might vary, especially in some scenarios.

15



<a name="br17"></a> 

University of Science - VNUHCM

Artiﬁcial Intelligence

PROJECT REPORT

No.

1

2

3

4

Map name

Pysat Optimal Backtracking Brute force

Map with size 5 5 00:00:002 00:00:001 00:00:000 00:00:001

Map with size 9 9 00:00:002 00:00:006 00:00:001 00:00:004

Map with size 11 11 00:00:003 00:00:011 00:00:004 00:00:011

Map with size 20 20 00:00:005 00:00:059 00:02:796 00:00:030

Map with size 25 25 00:00:012 00:00:210 00:00:060 00:00:240

5

Table 5: The processing time statistics of the 4 algorithms

16



<a name="br18"></a> 

University of Science - VNUHCM

Artiﬁcial Intelligence

PROJECT REPORT

7 Running Time Comparison

7\.1 Level 1

Figure 7: Level 1 Running Time

Observation: Because of the small size of this level(5x5), every algorithm running time is extremely

low.

7\.2 Level 2

The size of the map is 9x9.

Figure 8: Level 2 Running Time

Observation: Even though it is called the ”Optimal Algorithm”, this algorithm is not fully developed

to the ﬁnest of its level. Other algorithms work just ﬁne.

7\.3 Level 3

The map size is 11X11.

Figure 9: Level 3 Running Time

17



<a name="br19"></a> 

University of Science - VNUHCM

Artiﬁcial Intelligence

PROJECT REPORT

Observation: As the map grows in size, the time it takes to solve the puzzle increases rapidly. In

this level 3 map, the more information given (numbered cell) the quicker the backtracking algorithm

runs.

7\.4 Level 4

The map size is 20x20.

Figure 10: Level 4 Running Time

Observation: As you can see, the map size is 20x20, which is really big. But the amount of numbered

cells is very little. Because of the little information, the backtracking algorithm takes a ton of time

to run. Therefore the higher the numbered cell/unknown cell ratio, the faster the DPLL algorithm.

7\.5 Level 5

The map size is 25x25.

Figure 11: Level 5 Running Time

Observation: In the end, the Pysat library is the fastest algorithm. The ”Optimal Algorithm” our

group proposes is not really good enough but it has room to improve. The backtracking algorithm

works well as there are ton of information. Brute force is indeed the slowest one.

18



<a name="br20"></a> 

University of Science - VNUHCM

Artiﬁcial Intelligence

PROJECT REPORT

8 Additonal Information

You can review the source code and online video by clicking on the link below.

• [Video](https://studenthcmusedu-my.sharepoint.com/:v:/g/personal/22127202_student_hcmus_edu_vn/ET_f_nfGOINPtyqVZBaY7FoBt4LwgG7JeDL96k_G0wDlIA?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJPbmVEcml2ZUZvckJ1c2luZXNzIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXciLCJyZWZlcnJhbFZpZXciOiJNeUZpbGVzTGlua0NvcHkifX0&e=hcY4B7)

• [Source](https://github.com/RINz-HCMUS/AI---Project-2-Gem-hunter/tree/Khoa)

19



<a name="br21"></a> 

University of Science - VNUHCM

Artiﬁcial Intelligence

PROJECT REPORT

Reference

1\. [tkinter](https://docs.python.org/3/library/tkinter.html)[ ](https://docs.python.org/3/library/tkinter.html)[—](https://docs.python.org/3/library/tkinter.html)[ ](https://docs.python.org/3/library/tkinter.html)[Python](https://docs.python.org/3/library/tkinter.html)[ ](https://docs.python.org/3/library/tkinter.html)[interface](https://docs.python.org/3/library/tkinter.html)[ ](https://docs.python.org/3/library/tkinter.html)[to](https://docs.python.org/3/library/tkinter.html)[ ](https://docs.python.org/3/library/tkinter.html)[Tcl/Tk](https://docs.python.org/3/library/tkinter.html)

2\. [DPLL](https://www.cs.ox.ac.uk/people/james.worrell/lecture06.pdf)[ ](https://www.cs.ox.ac.uk/people/james.worrell/lecture06.pdf)[algorithm](https://www.cs.ox.ac.uk/people/james.worrell/lecture06.pdf)

3\. [Phase](https://arxiv.org/pdf/1106.1372#:~:text=The%20basic%20idea%20of%20Jeroslow-Wang%20heuristic%20is%20to,of%20clauses%20containing%20that%20variable%20and%20its%20size.)[ ](https://arxiv.org/pdf/1106.1372#:~:text=The%20basic%20idea%20of%20Jeroslow-Wang%20heuristic%20is%20to,of%20clauses%20containing%20that%20variable%20and%20its%20size.)[Selection](https://arxiv.org/pdf/1106.1372#:~:text=The%20basic%20idea%20of%20Jeroslow-Wang%20heuristic%20is%20to,of%20clauses%20containing%20that%20variable%20and%20its%20size.)[ ](https://arxiv.org/pdf/1106.1372#:~:text=The%20basic%20idea%20of%20Jeroslow-Wang%20heuristic%20is%20to,of%20clauses%20containing%20that%20variable%20and%20its%20size.)[Heuristics](https://arxiv.org/pdf/1106.1372#:~:text=The%20basic%20idea%20of%20Jeroslow-Wang%20heuristic%20is%20to,of%20clauses%20containing%20that%20variable%20and%20its%20size.)[ ](https://arxiv.org/pdf/1106.1372#:~:text=The%20basic%20idea%20of%20Jeroslow-Wang%20heuristic%20is%20to,of%20clauses%20containing%20that%20variable%20and%20its%20size.)[for](https://arxiv.org/pdf/1106.1372#:~:text=The%20basic%20idea%20of%20Jeroslow-Wang%20heuristic%20is%20to,of%20clauses%20containing%20that%20variable%20and%20its%20size.)[ ](https://arxiv.org/pdf/1106.1372#:~:text=The%20basic%20idea%20of%20Jeroslow-Wang%20heuristic%20is%20to,of%20clauses%20containing%20that%20variable%20and%20its%20size.)[Satisﬁability](https://arxiv.org/pdf/1106.1372#:~:text=The%20basic%20idea%20of%20Jeroslow-Wang%20heuristic%20is%20to,of%20clauses%20containing%20that%20variable%20and%20its%20size.)[ ](https://arxiv.org/pdf/1106.1372#:~:text=The%20basic%20idea%20of%20Jeroslow-Wang%20heuristic%20is%20to,of%20clauses%20containing%20that%20variable%20and%20its%20size.)[Solvers](https://arxiv.org/pdf/1106.1372#:~:text=The%20basic%20idea%20of%20Jeroslow-Wang%20heuristic%20is%20to,of%20clauses%20containing%20that%20variable%20and%20its%20size.)[ ](https://arxiv.org/pdf/1106.1372#:~:text=The%20basic%20idea%20of%20Jeroslow-Wang%20heuristic%20is%20to,of%20clauses%20containing%20that%20variable%20and%20its%20size.)[-](https://arxiv.org/pdf/1106.1372#:~:text=The%20basic%20idea%20of%20Jeroslow-Wang%20heuristic%20is%20to,of%20clauses%20containing%20that%20variable%20and%20its%20size.)[ ](https://arxiv.org/pdf/1106.1372#:~:text=The%20basic%20idea%20of%20Jeroslow-Wang%20heuristic%20is%20to,of%20clauses%20containing%20that%20variable%20and%20its%20size.)[Jingchao](https://arxiv.org/pdf/1106.1372#:~:text=The%20basic%20idea%20of%20Jeroslow-Wang%20heuristic%20is%20to,of%20clauses%20containing%20that%20variable%20and%20its%20size.)[ ](https://arxiv.org/pdf/1106.1372#:~:text=The%20basic%20idea%20of%20Jeroslow-Wang%20heuristic%20is%20to,of%20clauses%20containing%20that%20variable%20and%20its%20size.)[Chen](https://arxiv.org/pdf/1106.1372#:~:text=The%20basic%20idea%20of%20Jeroslow-Wang%20heuristic%20is%20to,of%20clauses%20containing%20that%20variable%20and%20its%20size.)

20

