import tkinter as tk
import random

class Mazegenerator:
    def __init__ (self, root, cols, rows):
        #variables
        self.rows = rows
        self.cols = cols
        self.root = root
        self.start_node = (0, 0)
        self.visited = {}
        #set up canvas layout
        self.canvas = tk.Canvas(root, width=800, height =600)

        self.canvas.pack()

        #defining running order
        self.reset_maze() #Initialise the maze structure
        self.dfs(self.start_node) #Run Recursive DFS / Remove walls
        self.new_maze() #create a new maze from maze matrix
        self.create_button() #Button to recreate maze

    def reset_maze(self):
        self.maze = [[{'north': True, 'east': True, 'south': True, 'west': True} for _ in range(self.cols)] for _ in range(self.rows)]
        self.visited = {self.start_node: False}

    def dfs(self, current_node):
        x, y = current_node
        self.visited[current_node] = True
        neighbors = self.get_neighbors(current_node)
        random.shuffle(neighbors)

        for neighbor in neighbors:
            if not self.visited[neighbor]:
                self.remove_wall(current_node, neighbor)
                self.dfs(neighbor)

    def get_neighbors(self,node):
        x, y = node

        neighbors = []
        if x > 0: neighbors.append((x-1, y))
        if x < self.rows - 1: neighbors.append((x+1, y))
        if y > 0: neighbors.append((x, y-1))
        if y < self.cols - 1: neighbors.append((x, y+1))

        #adding nodes to visited if not already there. set to FALSE
        for neighbor in neighbors:
            if neighbor not in self.visited:
                #appending to visited as False
                self.visited[neighbor] = False

        return neighbors

    def remove_wall(self, current, next):
        #to determine if the wall is n,e,s,w
        x1, y1 = current
        x2, y2 = next
        if x1 == x2:
            #y because its vertical
            if y1 > y2:
                #up
                self.maze[x1][y1]['north'] = False
                self.maze[x2][y2]['south'] = False
            if y1 < y2:
                #down
                self.maze[x1][y1]['south'] = False
                self.maze[x2][y2]['north'] = False
        if y1 == y2:
            #because its horizontal
            if x1 > x2:
                #left
                self.maze[x1][y1]['west'] = False
                self.maze[x2][y2]['east'] = False
            if x1 < x2:
                #right
                self.maze[x1][y1]['east'] = False
                self.maze[x2][y2]['west'] = False

    #remove start and exit
        self.maze[0][0]['north'] = False
        self.maze[self.cols-1][self.rows-1]['south'] = False


    def initialise_maze(self):
        self.canvas.delete("all")
        cell_size = 20
        #offset from the 0,0
        offset = 150

        for i in range(self.rows):
            for j in range(self.cols):

                x1 = j * cell_size + offset
                y1 = i * cell_size + offset
                x2 = x1 + cell_size
                y2 = y1 + cell_size

                # Draw east and south walls based on maze grid
                if self.maze[j][i]['north']:
                    self.canvas.create_line(x1, y1, x2, y1)
                if self.maze[j][i]['east']:
                    self.canvas.create_line(x2, y1, x2, y2)
                if self.maze[j][i]['south']:
                    self.canvas.create_line(x1, y2, x2, y2)
                if self.maze[j][i]['west']:
                    self.canvas.create_line(x1, y1, x1, y2)
    
    def new_maze(self):
        self.reset_maze()
        self.dfs(self.start_node)
        self.initialise_maze()

    def create_button(self):
        self.button = tk.Button(self.root, text="New Maze", command=self.new_maze)
        self.button.pack()

def main():
    root = tk.Tk()
    root.title("Maze Generator")
    maze_generator = Mazegenerator(root, cols=15, rows=15)
    root.mainloop()

if __name__ == "__main__":
    main()