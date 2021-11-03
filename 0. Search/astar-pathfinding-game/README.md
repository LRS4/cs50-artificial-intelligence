# A* Pathfinding Algorithm Game

A game to visualise the A* search pathfinding algorithm.

[A\* search](https://youtu.be/D5aJNFWsWew?t=3916) is a search algorithm that expands node with lowest value of the "cost to reach node" g(*n*) plus the "estimated goal cost" *h(n)*. In other words, *g(n)* is the number of steps you had to take to get to the node you're at and the h(*n*) is the ['Manhatten distance'](https://xlinux.nist.gov/dads/HTML/manhattanDistance.html) heuristic estimate of how far a node is away from the goal.

An A* search is like a breadth-first seach, except that in each iteration, instead of expanding the cell with the shortest path from the origin, we expand the cell with the lowest overall estimated path length -- this is the distance so far, plus a heuristic (rule-of-thumb) estimate of the remaining distance. This can be expressed as *f(n) = g(n) + h(n)*

As long as the heuristic is consistent, an A* graph-search will find the shortest path. This can be somewhat more efficient than breadth-first-search as we typically don't have to visit nearly as many cells. Intuitively, an A* search has an approximate sense of direction, and uses this sense to guide it towards the target.

![A* search process](https://res.cloudinary.com/dayqxxsip/image/upload/v1628157180/App%20Images/Blog%20Images/Article%20Images/CS50%20AI%20Review/astar-search_zrqazw.gif "A* search process")

## Prerequisites

You need to install the pygame package before using this game.

```
pip install pygame
```

## Playing the game

```
python3 game.py
```

## Controls

* First click marks the starting square
* Second click marks the goal square
* Any clicks after that marks barriers
* Right click clears squares
* Space starts the A* search algorithm
* Press 'c' key to clear the screen and start again

## References

* [Tutorial](https://www.youtube.com/watch?v=JtiK0DOeI4A)
* [Example](https://leetcode.com/problems/shortest-path-in-binary-matrix/discuss/313347/A*-search-in-Python)