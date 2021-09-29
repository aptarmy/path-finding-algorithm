from implementation import *
from diagram_walls import DIAGRAM1_WALLS
from math import sqrt

def best_first_search(graph: Graph, start: Location, goal: Location):
    frontier = Queue()
    frontier.put(start)
    came_from: Dict[Location, Optional[Location]] = {}
    came_from[start] = None
    
    while not frontier.empty():
        current: Location = frontier.get()
        if current == goal: break;
        for next in graph.neighbors(current):
            if next not in came_from:
                frontier.put(next)
                came_from[next] = current
    return (came_from)

def dijkstra_search(graph: GridWithWeights, start: Location, goal: Location):
  frontier = PriorityQueue()
  frontier.put(start, 0)
  came_from: Dict[Location, Optional[Location]] = {}
  cost_so_far: Dict[Location, float] = {}
  came_from[start] = None
  cost_so_far[start] = 0
  while not frontier.empty():
    current: Location = frontier.get()
    if current == goal:
      break
    for next in graph.neighbors(current):
      new_cost = cost_so_far[current] + graph.cost(current, next)
      if next not in cost_so_far or new_cost < cost_so_far[next]:
        cost_so_far[next] = new_cost
        priority = new_cost
        frontier.put(next, priority)
        came_from[next] = current
  return came_from, cost_so_far

def heuristic(a: GridLocation, b: GridLocation) -> float:
    (x1, y1) = a
    (x2, y2) = b
    return sqrt((x1 - x2)**2 + (y1 - y2)**2)

def a_star_search(graph: GridWithWeights, start: Location, goal: Location):
  frontier = PriorityQueue()
  frontier.put(start, 0)
  came_from: Dict[Location, Optional[Location]] = {}
  cost_so_far: Dict[Location, float] = {}
  came_from[start] = None
  cost_so_far[start] = 0
  while not frontier.empty():
    current: Location = frontier.get()
    if current == goal:
      break
    for next in graph.neighbors(current):
      new_cost = cost_so_far[current] + graph.cost(current, next)
      if next not in cost_so_far or new_cost < cost_so_far[next]:
        cost_so_far[next] = new_cost
        priority = new_cost + heuristic(next, goal)
        frontier.put(next, priority)
        came_from[next] = current
  return came_from, cost_so_far

def reconstruct_path(came_from: Dict[Location, Location], start: Location, goal: Location) -> List[Location]:
  current: Location = goal
  path: List[Location] = []
  while current != start:
    path.append(current)
    current = came_from[current]
  path.append(start) # optional
  path.reverse() # optional
  return path

g = GridWithWeights(30, 15)
g.walls = DIAGRAM1_WALLS
start = (24, 0)
goal = (0, 0)


# (came_from) = best_first_search(g, start, goal)
# path = reconstruct_path(came_from, start, goal)
# draw_grid(g, point_to=came_from, start=start, path=path, goal=goal)

# (came_from, cost_so_far) = dijkstra_search(g, start, goal)
# path = reconstruct_path(came_from, start, goal)
# draw_grid(g, point_to=came_from, start=start, path=path, goal=goal)

(came_from, cost_so_far) = a_star_search(g, start, goal)
path = reconstruct_path(came_from, start, goal)
draw_grid(g, point_to=came_from, start=start, goal=goal)
draw_grid(g, point_to=came_from, start=start, path=path, goal=goal)
