import heapq
from typing import Any, Callable
from src.debug import dump
from src.problem import Problem
from src.node import Node

def DFS(problem: Problem, trace=False) -> tuple[Node, dict]:
    
    node = Node(problem.initial)
    frontier = [node] # stack
    reached = { problem.initial: node }
    if trace:
        trace_lst = []
    
    while frontier:
        node = frontier.pop()
        if node.state.prune:
            frontier = list(filter(
                lambda item: not (item.parent == node.parent and item.state.prune),
                frontier
            ))
        
        if trace:
            trace_lst.append(node)
        if problem.goal_test(node.state):
            if trace:
                return node, trace_lst
            return node
        
        for child in node.expand(problem):
            
            if child.state not in reached:
                reached[child.state] = child
                frontier.append(child)
    if trace:
        return None, trace_lst
    return None
                
def BeFS(problem: Problem, heuristic: Callable[[Node], Any], trace=False):
    
    node = Node(problem.initial, priority=heuristic)
    frontier = [node] # priority queue
    reached = { problem.initial: node }
    if trace:
        trace_lst = []
    
    while frontier:
        node = heapq.heappop(frontier)
        if node.state.prune:
            frontier = list(filter(
                lambda item: not (item.parent == node.parent and item.state.prune),
                frontier
            ))
                        
        if trace:
            trace_lst.append(node)
        if problem.goal_test(node.state):
            if trace:
                return node, trace_lst
            return node
        
        for child in node.expand(problem):
            if child.state not in reached:
                reached[child.state] = child
                heapq.heappush(frontier, child)
    
    if trace:
        return None, trace_lst
    return None
    