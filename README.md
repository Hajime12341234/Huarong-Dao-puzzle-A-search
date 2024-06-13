The full implementation is available in hrd.py file. 

The purpose of this project was to implement A-star search algorithm to find the optimal path to the goal state in the context of Huarong Dao puzzle. 
We coded two algorithms, DFS and A-star to make some comparison between optimal algorithm and non-optimal algotithm. 

For A-star search algotithm, we used the Manhattan distance from the goal piece to the goal region as a heuristic function. 
Its corresponding relaxed problem is that the goal piece can overlap with any other pieces on the board. 
It is not hard to see that given any configuration, the Manhattan heuristic is admissible. 
Note that if heuristic is admissible, then A-star will return an optimal solution.

We know from the theorem that A-star search is optimally efficient. For example, one such algorithm that returns an optimal solution to this kind of "search" based problem is UCS (Uniform Cost Search, aka Dijkstra algorithm). Then, A-star search expands fewer states than UCS. Note that UCS is also a special or degenerated case of A-star algorithm.

If we use some "smarter" heuristic which dominates the Manhattan heuristic, we may expand even fewer states to find an optimal solution. 

I proposed an admissibe heuristic that dominates the Manhattan heuristic in the advanced pdf document. You could take a look at it if you are interested. 






![image](https://github.com/Hajime12341234/Huarong-Dao-puzzle-A-star-search/assets/132004336/96c4b206-3d9a-4328-8a5f-61cf6d851a9d)






