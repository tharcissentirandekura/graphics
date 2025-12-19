from collections import deque
import random
import time
import package.picture as picture

class Grid:
    outline_color = "white"
    fill_color = "black"
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.size = None  # Will be set in grid_canvas

    def setup_canvas(self):
        picture.new_picture(self.width, self.height)

    def background(self, color):
        picture.set_fill_color(color)
        picture.draw_filled_rectangle(0, 0, self.width, self.height)

    def outline(self, color):
        picture.set_outline_color(color)

    def grid_canvas(self, size):
        self.size = size
        self.setup_canvas()
        self.background(self.fill_color)
        self.outline(self.outline_color)
        picture.grid(self.width, self.height, size)

    def draw_in_cell(self, row, col, draw_func,color="red",*args, **kwargs):
        """
        Draw using draw_func at the center of the specified grid cell.
        draw_func should be a function from picture, e.g., picture.draw_circle.
        """
        if self.size is None:
            raise ValueError("Grid size not set. Call grid_canvas(size) first.")
        x = row * self.size + self.size // self.size
        y = col * self.size + self.size // self.size
        # print((x,y))
        picture.set_fill_color(color)
        draw_func(x, y, *args, **kwargs)
        
        # picture.save_picture('./output/grid.png')

def draw_in_grid():
    picture.set_fill_color('red')
    grid = Grid(1000, 1000)
    grid.grid_canvas(40)
    # Add start and target

    return grid
def get_neighbors(x,y,max_x,max_y):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    results = []
    for dx,dy in directions:
        nx,ny = x + dx,y+dy
        if 0 <= nx < max_x and 0 <= ny < max_y:
            # valid
            results.append((nx,ny))
    return results
def bfs(source,destination,grid):
    max_row = grid.width // grid.size
    max_col = grid.height // grid.size
    q = deque()
    visited = set()
    visited.add(source)
    q.append(source)
    path = {source:None}
    res = []

    while q is not None:
        curr = q.popleft()
        x,y = curr
        grid.draw_in_cell(x,y,picture.draw_filled_square,"red",grid.size)
        picture.display()
        # time.sleep(0.2)
        if curr == destination:
            print("destination reached")
            picture.save_picture('./output/bfs_grid.png')
            current = destination
            while current is not None:
                grid.draw_in_cell(current[0],current[1],picture.draw_filled_square,"yellow",grid.size)
                res.append(current)
                current = path[current]
            res.reverse()
            grid.draw_in_cell(0,0,picture.draw_filled_square,"blue",grid.size)
            grid.draw_in_cell(5,5,picture.draw_filled_square,"green",grid.size)
            picture.save_picture('./output/bfs_grid.png')

            print("Path:",res)
            return
        neighbors = get_neighbors(x,y,max_row,max_col)
        for neighbor in neighbors:
            if neighbor not in visited:
                path[neighbor] = curr
                q.append(neighbor)
                visited.add(neighbor)
def dfs_iterative(source,destination,grid):
    max_row = grid.width // grid.size
    max_col = grid.height // grid.size
    stack = []
    visited = set()
    path = {source:None}
    res = []

    stack.append(source)
    visited.add(source)

    while stack:
        curr = stack.pop()

        x,y = curr
        grid.draw_in_cell(x, y, picture.draw_filled_square, "blue", grid.size)
        picture.display()
        # time.sleep(0.4)

        if curr == destination:
            print("destination reached (DFS)")
            current = destination
            while current is not None:
                grid.draw_in_cell(current[0], current[1], picture.draw_filled_square, "yellow", grid.size)
                res.append(current)
                current = path[current]
            res.reverse()
            grid.draw_in_cell(0,0,picture.draw_filled_square,"blue",grid.size)
            grid.draw_in_cell(5,5,picture.draw_filled_square,"green",grid.size)
            picture.save_picture('./output/dfs_iter_grid.png')
            print("DFS Path:", res)
            return 
        
        neighbors = get_neighbors(x,y,max_row,max_col)
        for neighbor in neighbors:
            if neighbor not in visited:
                path[neighbor] = curr
                stack.append(neighbor)
                visited.add(neighbor)
def dfs_recursive(curr, destination, grid, visited, path, max_row, max_col):
    if curr == destination:
        return True
    x,y = curr
    grid.draw_in_cell(x, y, picture.draw_filled_square, "blue", grid.size)
    picture.display()
    visited.add(curr)
    neighbors = get_neighbors(x, y, max_row, max_col)
    for neighbor in neighbors:
        if neighbor not in visited:
            path[neighbor] = curr
            if dfs_recursive(neighbor, destination, grid, visited, path, max_row, max_col):
                return True
    return False
def run_dfs_recursive(source,destination,grid):
    
    path = {source:None}
    max_row = grid.width // grid.size
    max_col = grid.height // grid.size
    visited = set()
    found = dfs_recursive(source, destination, grid, visited, path, max_row, max_col)

    if found:
        res = []
        curr = destination
        while curr:
            # mark on path
            grid.draw_in_cell(curr[0], curr[1], picture.draw_filled_square, "yellow", grid.size)
            res.append(curr)
            curr = path[curr]
        res.reverse()
        grid.draw_in_cell(0,0,picture.draw_filled_square,"blue",grid.size)
        grid.draw_in_cell(5,5,picture.draw_filled_square,"green",grid.size)
        picture.save_picture('./output/dfs_rec_grid.png')
        print("DFS Recursive Path:", res)
    else:
        print("No path found with DFS recursive.")
            


    
    
def step():
    grid = draw_in_grid()
    grid.draw_in_cell(0,0,picture.draw_filled_square,"yellow",grid.size)
    grid.draw_in_cell(5,5,picture.draw_filled_square,"green",grid.size)

    source = (0,0)
    destination = (5,5)
    
    bfs(source,destination,grid)
step()