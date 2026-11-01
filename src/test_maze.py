from mazegenerator.mazegenerator import MazeGenerator

def display_maze(maze: list[list[int]]) -> None:
    for row in maze:
        for cell in row:
            print(f"{cell:2}", end=" ")
        print()

generator = MazeGenerator(
    size=(15, 15), 
    perfect=False,
    seed=False
)

# print("Maze:")
# for row in generator.maze:
#     print(row)

# print("Entry:", generator.maze_entry)
# print("Exit:", generator.maze_exit)
# print("Shortest path:", generator.shortest_path)

display_maze(generator.maze)