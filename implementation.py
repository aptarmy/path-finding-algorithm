from typing import Dict, Iterator, List, Optional, Tuple, TypeVar, Protocol
import collections
import heapq
from matplotlib import image, pyplot
from numpy import asarray, array, uint8, append
from PIL import Image

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

class ImgGridWithWeights(GridWithWeights):
  def __init__(self):
    self.width = None
    self.height = None
    self.walls: List[GridLocation] = []
    self.weights: Dict[GridLocation, float] = {}
    self.segmented_img_array: List[List[List[int, int, int]]] = []
    self.colorful_img_array: List[List[List[int, int, int]]] = []
  def loadImg(self, segmented_img: str, colorful_img: str):
    img = image.imread(segmented_img)
    self.segmented_img_array = asarray(img)
    img = image.imread(colorful_img)
    self.colorful_img_array = asarray(img)
    print(img.dtype)
    print(img.shape)
    # pyplot.imshow(img)
    # pyplot.show()

    self.width = img.shape[1]
    self.height = img.shape[0]
    for y in range(img.shape[0]):
      for x in range(img.shape[1]):
        pixel = self.segmented_img_array[y][x]
        if ((int(pixel[0]) + int(pixel[1]) + int(pixel[2])) / 3 <= 200):
          self.walls.append((x, y))

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

def draw_img(g: SquareGrid, start: Optional[Location], goal: Optional[Location], path: Optional[List[Location]]=[], cost: Optional[Dict[Location, float]]={}, point_to: Dict[Location, Optional[Location]]={}):
  # check type
  # print("segmented_img_array: %s" % type(g.segmented_img_array))
  # print("segmented_img_array[0]: %s" % type(g.segmented_img_array[0]))
  # print("segmented_img_array[0][0]: %s" % type(g.segmented_img_array[0][0]))
  # print("segmented_img_array[0][0][0]: %s" % type(g.segmented_img_array[0][0][0]))

  # clone segmented_img_array from SquareGrid
  colorful_img_array = []
  for y in range(len(g.colorful_img_array)):
    colorful_img_array.append([])
    for x in range(len(g.colorful_img_array[0])):
      colorful_img_array[y].append(array([ g.colorful_img_array[y][x][0], g.colorful_img_array[y][x][1], g.colorful_img_array[y][x][2] ]))
    colorful_img_array[y] = array(colorful_img_array[y])
  colorful_img_array = array(colorful_img_array)
  for point in path:
    (x, y) = point
    colorful_img_array[y][x] = array([uint8(0), uint8(255), uint8(0)])
  # highlight start/goal
  colorful_img_array[start[1]][start[0]] = array([255, 0, 0])
  colorful_img_array[start[1]+1][start[0]] = array([255, 0, 0])
  colorful_img_array[start[1]-1][start[0]] = array([255, 0, 0])
  colorful_img_array[start[1]][start[0]+1] = array([255, 0, 0])
  colorful_img_array[start[1]][start[0]-1] = array([255, 0, 0])
  colorful_img_array[goal[1]][goal[0]] = array([0, 0, 255])
  colorful_img_array[goal[1]+1][goal[0]] = array([0, 0, 255])
  colorful_img_array[goal[1]-1][goal[0]] = array([0, 0, 255])
  colorful_img_array[goal[1]][goal[0]+1] = array([0, 0, 255])
  colorful_img_array[goal[1]][goal[0]-1] = array([0, 0, 255])
  img = Image.fromarray(colorful_img_array)
  pyplot.imshow(img)
  pyplot.show()

