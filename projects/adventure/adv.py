from room import Room
from player import Player
from world import World

import random
from ast import literal_eval


class Queue():
    def __init__(self):
        self.queue = []

    def enqueue(self, value):
        self.queue.append(value)

    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop()
        else:
            return None

    def size(self):
        return len(self.queue)


# Load world
world = World()

# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "projects/adventure/maps/test_line.txt"
# map_file = "projects/adventure/maps/test_cross.txt"
# map_file = "projects/adventure/maps/test_loop.txt"
# map_file = "projects/adventure/maps/test_loop_fork.txt"
# map_file = "projects/adventure/maps/main_maze.txt"
map_file = "projects/adventure/maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

visited = set()

room_maps = {
    0: {'n': '?', 's': '?', 'e': '?', 'w': '?'}
}

def reverse_dir(dir):
    if dir == "n":
        return "s"
    elif dir == "s":
        return "n"
    elif dir == "w":
        return "e"
    else:
        return "w"


def across_map(dir):
    directions = {}

    from_id = player.current_room.id
    from_dir = reverse_dir(dir)

    room_id = player.current_room.get_room_in_direction(dir).id
    room_maps[from_id][dir] = room_id

    player.travel(dir)
    traversal_path.append(dir)

    if room_id not in room_maps:
        for exit in player.current_room.get_exits():
            reverse = reverse_dir(exit)
            exit_id = player.current_room.get_room_in_direction(exit).id

            if exit_id not in room_maps:
                directions[exit] = "?"
            elif exit is from_dir:
                directions[exit] = from_id
            elif room_maps[exit_id][reverse] == "?":

                print(f"""Player's current room:
                {player.current_room.id}, you came from: {from_id} to
                the {reverse}, your exit is {exit_id} to the {reverse}
                with id: {player.current_room.id}""")

                room_maps[exit_id][reverse] = room_id
        room_maps[room_id] = directions


def find_nearest_room(to_id):
    queue = Queue()
    path = []
    queue.enqueue([(to_id, None)])
    visited_rooms = set()

    while queue.size() > 0:
        path = queue.dequeue()
        room = path[-1]

        for dir, rm in room_maps[room[0]].items():
            if rm not in visited_rooms:
                room_path = list(path)
                room_path.append((rm, dir))
                visited_rooms.add(rm)

                queue.enqueue(room_path)
                if rm == "?":
                    room_path.pop(0)
                    path_to_room = [rm[1] for rm in room_path]
                    return path_to_room
    return None


stack = list()
stack.append("n")
while len(room_graph) > len(room_maps):
    dir = stack.pop()
    next = player.current_room.get_room_in_direction(dir)

    exits = player.current_room.get_exits()
    if next:
        stack.append(dir)
        across_map(dir)

        print(f"I'm in room {player.current_room.id}. I came from the {reverse_dir(dir)}")
    elif len(stack) == 0:
        for exit in exits:
            to_next_dir = find_nearest_room(player.current_room.id)
            for i, to_room in enumerate(to_next_dir):
                across_map(to_room)
                if i == len(to_next_dir) - 1:
                    stack.append(to_room)

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")

#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#    cmds = input("-> ").lower().split(" ")
#    if cmds[0] in ["n", "s", "e", "w"]:
#        player.travel(cmds[0], True)
#   elif cmds[0] == "q":
#       break
#   else:
#       print("I did not understand that command.")