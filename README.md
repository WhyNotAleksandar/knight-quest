## Knight Quest: A Geometric Heuristic Approach to Knight Pathfinding
**Licence**: MIT License _(Free to use, modify, and distribute)_ 

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15860239.svg)](https://doi.org/10.5281/zenodo.15860239)

**Knight Quest** is a geometry-inspired solution to the knight’s shortest path problem. This method models the knight’s movements as base vectors in the complex plane,
specifically using the canonical vectors **_( 2, 1 )_** and **_( 1, 2 )_** represented as **_u = 2 + i_** and **_v = 1 + 2i_**. These vectors are then rotated and mirrored 
according to the signed distance vector between the starting point **_( A )_** and the destination **_( B )_**, allowing for a modular decomposition of the knight's path. 
The solution operates by transforming the pathfinding problem into one of rotational alignment and mirrored symmetry, with strategic reference point **_( R )_** used to 
identify optimal paths across different directional regions. By analyzing the periodic structure of knight moves—especially across diagonals like **_y = x_** and lines 
**_y = x/2_** the algorithm uses the repeating alternation in movement patterns to reduce the problem to a combination of sequence evaluation and rotation-based projection. 

## 📘 Documentation
The full mathematical derivation and evaluation model is available in: [knight-quest.pdf](paper/knight-quest.pdf)
This document details the geometric formulation, modular reasoning and evaluation function.

## 🚀 Example of Usage
**Development**: Includes comparison and testing against BFS
```
cd code/development 
python main.py --num_cases 500 --max_coord 250 --seed 100 --log file
python main.py --help
```
**Release**: Base knight quest algorithm stripped of testing.
```
cd code/production 
python main.py --start '0,0' --end '100,100'
python main.py --help
```

## 📂 Project Structure
```
knight-quest/
    code/
        development/
            logic/
                kq.py
                bfs.py
            model/
                point.py
                sequence.py
            tests/
                output/
                    log.txt
                case.py
                reporter.py
                statistics.py
                tester.py
            main.py
        release/
            logic/
                kq.py
            model/
                point.py
                sequence.py
            main.py
    paper/
        figures/
            figure-1.png
            figure-2.png
        knight-quest.pdf
        knight-quest.tex
```

## 🧾 Summary of test results:
Detailed test log: [log.txt](code/development/tests/output/log.txt)
```
Tested over the range: (-500, 500)
Seed: 42
Total test runs: 1000
Failed tests: 0
Total fallback moves used: 0

Average KQ path time:   0.00478579s
Average BFS path time: 26.76225433s
Average feval time:     0.00000585s

Average KQ speedup:        4616.54x
Average feval speedup:  4781206.19x
```
