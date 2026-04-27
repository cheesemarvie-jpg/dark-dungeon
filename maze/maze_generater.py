import random
import config

class Maze_generater:
    def __init__(self, status):
        self.status = status
        self.map = self.generate_maze()
        self.set_coodinates()
        
    def generate_maze(self):#参考: https://af-e.net/python-maze/#rtoc-17
         # 迷路の初期化
         size = self.status.get_level() + 2
         width = size
         height = size
         maze = [[1] * (width * 2 + 1) for _ in range(height * 2 + 1)]
         edges = []
         
         # エッジの作成
         for y in range(height):
             for x in range(width):
                 if x < width - 1:
                     edges.append(((x, y), (x + 1, y)))  # 右のセル
                 if y < height - 1:
                     edges.append(((x, y), (x, y + 1)))  # 下のセル
         random.shuffle(edges)  # エッジをランダムにシャッフル

         # グループの初期化
         parent = {}
         for y in range(height):
             for x in range(width):
                 parent[(x, y)] = (x, y)

         def find(node):
             if parent[node] != node:
                 parent[node] = find(parent[node])
             return parent[node]

         def union(node1, node2):
             root1 = find(node1)
             root2 = find(node2)
             if root1 != root2:
                 parent[root2] = root1

         # エッジを処理
         for edge in edges:
             cell1, cell2 = edge
             if find(cell1) != find(cell2):
                 maze[cell1[1] * 2 + 1][cell1[0] * 2 + 1] = 0
                 maze[cell2[1] * 2 + 1][cell2[0] * 2 + 1] = 0
                 maze[(cell1[1] + cell2[1]) + 1][(cell1[0] + cell2[0]) + 1] = 0
                 union(cell1, cell2)
         
         return maze

    def set_coodinates(self):
        reached = []
        leaf = []
        def search(x, y):
            reached.append((x, y))
            stacked = True
            for d in config.DIRECT:
                if not (x + d[0], y + d[1]) in reached and self.map[y + d[1]][x + d[0]] == 0:
                    search(x + d[0], y + d[1])
                    stacked = False
            if stacked:
                leaf.append((x, y))
        search(1, 1)
    
        if len(leaf) < 3:#葉の数が少なければ再生成
            #print("regenerate")
            self.map = self.generate_maze()
            self.set_coodinates()
        else:
            [(self.px, self.py), (self.gx, self.gy), (self.cx, self.cy)] = random.sample(leaf, 3)   

    def get_maze(self):
        return self.map
    def get_coordinates(self):
        return (self.px, self.py, self.gx, self.gy, self.cx, self.cy)             
