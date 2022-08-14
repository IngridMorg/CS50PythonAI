import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """

    # TODO - finish shortest_path
    #print("source: ",source)
    #print("target: ", target)

    #following maze.py's structure
    #number of nodes we have explored
    nodesExplored = 0

    #initialise the frontier using the source we have been given
    start = Node(state= source, parent=None, action= None)
    frontier = StackFrontier()
    #add the start/source node to the frontier
    frontier.add(start)
    #print(start.state)
    #form the neihbours
    neighbours = neighbors_for_person(source)
    #we now need to loop to find a solution
    explored = {}
    explored = set(explored)
    while True:
        if frontier.empty():
            raise Exception("no solution")

        #we need to choose a node from the frontier
        node = frontier.remove()
        #print("current node: ", node.state)
        nodesExplored += 1

        #check that the node is the goal
        if (node.state == target):
            #we have a solution
            solution = []

            #if this isnt the first node then we need to trace back up to generate the path
            if node.parent == None:
                print("two values are same")
            while node.parent is not None:

                solution.append((node.action,node.state))
                node = node.parent
            solution.reverse()
            #print("solution: ", solution)
            return solution

        #we have now explored the node
        #print("explored before: ",explored)
        explored.add(node.state)
        #print("explored after: ",explored)
        neighbours = neighbors_for_person(node.state)
        #we now need to add the neighbours to the frontier
        for film, player in neighbours:
            if(player != source):
                #if the new player isnt the source then we can consider adding it to the frontier
                if player == target:
                    print("target found")
                    newNode = Node(state=player, parent=node, action=film)
                    # we have a solution
                    solution = []

                    # if this isnt the first node then we need to trace back up to generate the path
                    if newNode.parent == None:
                        print("two values are same")
                    while newNode.parent is not None:
                        solution.append((newNode.action, newNode.state))
                        newNode = newNode.parent
                    solution.reverse()
                    # print("solution: ", solution)
                    return solution
                elif not(frontier.contains_state(player)) and player not in explored:
                    newNode = Node(state = player, parent= node, action=film)
                    frontier.add(newNode)
        #input("end?")
                #print(film)
                #child = Node(state = player, parent= node, action = film)
                #frontier.add(child)



def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
