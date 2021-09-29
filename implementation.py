from typing import Dict, Iterator, List, Optional, Tuple, TypeVar, Protocol
import collections
import heapq

Location = TypeVar('Location')
GridLocation = Tuple[int, int]
T = TypeVar('T')

class Graph(Protocol):
  def neighbors(self, id: Location) -> List[Location]: pass

class SimpleGraph(Graph):
  def __init__(self):
    self.edges: Dict[Location, List[Location]] = {}
  def neighbors(self, id: Location) -> List[Location]:
    return self.edges[id]

class WeightedGraph(Graph):
  def cost(self, from_id: Location, to_id: Location) -> float: pass


class Queue:
  def __init__(self):
    self.elements = collections.deque()
  def empty(self) -> bool:
    return not self.elements
  def put(self, x: T):
    self.elements.append(x)
  def get(self) -> T:
    return self.elements.popleft()

class PriorityQueue:
  def __init__(self):
    self.elements: List[Tuple[float, T]] = []

  def empty(self) -> bool:
    return not self.elements

  def put(self, item: T, priority: float):
    heapq.heappush(self.elements, (priority, item))

  def get(self) -> T:
    return heapq.heappop(self.elements)[1]

class SquareGrid:
  def __init__(self, width: int, height: int):
    self.width = width
    self.height = height
    self.walls: List[GridLocation] = []
  def in_bounds(self, id: GridLocation) -> bool:
    (x, y) = id
    return 0 <= x < self.width and 0 <= y < self.height
  def passable(self, id: GridLocation) -> bool:
    return id not in self.walls
  def neighbors(self, id: GridLocation) -> Iterator[GridLocation]:
    (x, y) = id
    neighbors = [(x+1, y), (x-1, y), (x, y-1), (x, y+1), (x-1, y-1), (x+1, y+1), (x+1, y-1), (x-1, y+1)]
    if (x + y) % 2 == 0: neighbors.reverse()
    results = filter(self.in_bounds, neighbors)
    results = filter(self.passable, results)
    return results

class GridWithWeights(SquareGrid):
  def __init__(self, width: int, height: int):
    super().__init__(width, height)
    self.weights: Dict[GridLocation, float] = {}
  def cost(self, from_node: GridLocation, to_node: GridLocation) -> float:
    return self.weights.get(to_node, 1)

def draw_grid(g: SquareGrid, point_to: Dict[Location, Optional[Location]], start: Optional[Location], goal: Optional[Location], path: Optional[List[Location]]=[], cost: Optional[Dict[Location, float]]={}):
  print("drawing %d x %d grid" % (g.width, g.height))
  for y in range(g.height):
    for x in range(g.width):
      if (x, y) == start:
        print("🚢 ", end="")
        continue
      if (x, y) == goal:
        print("🏡 ", end="")
        continue
      if (x, y) in g.walls:
        print(" ■ ", end="")
        continue
      if (x, y) in path:
        print(" ● ", end="")
        continue
      if (x, y) in cost:
        print("%3.0f" % cost[(x, y)], end="")
        continue
      # if (x, y) in point_to and point_to[(x, y)] != None:
      #   (point_to_x, point_to_y) = point_to[(x, y)]
      #   if point_to[(x, y)] == (x - 1, y):
      #     print(" ← ", end="")
      #   if point_to[(x, y)] == (x + 1, y):
      #     print(" → ", end="")
      #   if point_to[(x, y)] == (x, y - 1):
      #     print(" ↑ ", end="")
      #   if point_to[(x, y)] == (x, y + 1):
      #     print(" ↓ ", end="")
      #   continue
      print(" . ", end="")
    print("")
  print("==================\n")
