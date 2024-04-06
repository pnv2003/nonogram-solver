import heapq
from typing import Any, Callable
from src.problem import Problem
from src.node import Node

def DFS(problem: Problem):
    
    node = Node(problem.initial)
    frontier = [node] # stack
    reached = { problem.initial: node }
    
    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            return node
        
        for child in node.expand(problem):
            if child.state not in reached:
                reached[child.state] = child
                frontier.append(child)
                
    return None
                
def BeFS(problem: Problem, heuristic: Callable[[Node], Any]):
    
    node = Node(problem.initial, priority=heuristic)
    frontier = [node] # priority queue
    reached = { problem.initial: node }
    
    while frontier:
        node = heapq.heappop(frontier)
        if problem.goal_test(node.state):
            return node
        
        for child in node.expand(problem):
            if child.state not in reached:
                reached[child.state] = child
                heapq.heappush(frontier, child)
    
    return None
    