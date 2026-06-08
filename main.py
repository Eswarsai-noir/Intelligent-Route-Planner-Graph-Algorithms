import heapq
from collections import defaultdict, deque
import os

# Optional Visualization
try:
    import networkx as nx
    import matplotlib.pyplot as plt
    VISUALIZATION_AVAILABLE = True
except ImportError:
    VISUALIZATION_AVAILABLE = False


class Graph:
    def __init__(self):
        self.graph = defaultdict(list)

    # ---------------------------
    # Add Road
    # ---------------------------
    def add_edge(self, u, v, weight):
        self.graph[u].append((v, weight))
        self.graph[v].append((u, weight))

    # ---------------------------
    # Display Graph
    # ---------------------------
    def display_graph(self):
        print("\n===== ADJACENCY LIST =====")

        for node in sorted(self.graph.keys()):
            print(f"{node} -> {self.graph[node]}")

    # ---------------------------
    # BFS
    # ---------------------------
    def bfs(self, start):

        if start not in self.graph:
            print("Invalid Location!")
            return []

        visited = set()
        queue = deque([start])
        order = []

        while queue:
            node = queue.popleft()

            if node not in visited:
                visited.add(node)
                order.append(node)

                for neighbor, _ in self.graph[node]:
                    if neighbor not in visited:
                        queue.append(neighbor)

        return order

    # ---------------------------
    # DFS
    # ---------------------------
    def dfs(self, start):

        if start not in self.graph:
            print("Invalid Location!")
            return []

        visited = set()
        stack = [start]
        order = []

        while stack:
            node = stack.pop()

            if node not in visited:
                visited.add(node)
                order.append(node)

                for neighbor, _ in reversed(self.graph[node]):
                    if neighbor not in visited:
                        stack.append(neighbor)

        return order

    # ---------------------------
    # Dijkstra
    # ---------------------------
    def dijkstra(self, start, end):

        if start not in self.graph:
            print(f"\nLocation '{start}' does not exist.")
            return None, None

        if end not in self.graph:
            print(f"\nLocation '{end}' does not exist.")
            return None, None

        distances = {
            node: float('inf')
            for node in self.graph
        }

        previous = {
            node: None
            for node in self.graph
        }

        distances[start] = 0

        pq = [(0, start)]

        while pq:

            current_distance, current_node = heapq.heappop(pq)

            if current_distance > distances[current_node]:
                continue

            for neighbor, weight in self.graph[current_node]:

                distance = current_distance + weight

                if distance < distances[neighbor]:

                    distances[neighbor] = distance
                    previous[neighbor] = current_node

                    heapq.heappush(
                        pq,
                        (distance, neighbor)
                    )

        if distances[end] == float('inf'):
            print("\nNo path available.")
            return None, None

        path = []
        current = end

        while current is not None:
            path.append(current)
            current = previous[current]

        path.reverse()

        return path, distances[end]

    # ---------------------------
    # Visualization
    # ---------------------------
    def visualize(self):

        if not VISUALIZATION_AVAILABLE:
            print("\nVisualization libraries not installed.")
            print("Install:")
            print("pip install networkx matplotlib")
            return

        G = nx.Graph()

        for node in self.graph:
            for neighbor, weight in self.graph[node]:
                G.add_edge(node, neighbor, weight=weight)

        pos = nx.spring_layout(G, seed=42)

        nx.draw(
            G,
            pos,
            with_labels=True,
            node_size=2500
        )

        labels = nx.get_edge_attributes(
            G,
            'weight'
        )

        nx.draw_networkx_edge_labels(
            G,
            pos,
            edge_labels=labels
        )

        plt.title("Intelligent Route Planner")
        plt.show()


# ==================================
# Sample City Map
# ==================================

def create_sample_city():

    g = Graph()

    roads = [

        ("A", "B", 4),
        ("A", "D", 2),

        ("B", "C", 5),
        ("B", "E", 10),

        ("D", "E", 3),

        ("E", "F", 4),

        ("C", "F", 11)

    ]

    for u, v, w in roads:
        g.add_edge(u, v, w)

    return g


# ==================================
# Save Report
# ==================================

def save_report(path, distance):

    os.makedirs("outputs", exist_ok=True)

    with open(
            "outputs/route_report.txt",
            "w",
            encoding="utf-8"
    ) as file:

        file.write("INTELLIGENT ROUTE PLANNER REPORT\n")
        file.write("=" * 40 + "\n\n")

        file.write(
            "Shortest Route:\n"
        )

        file.write(
            " -> ".join(path)
        )

        file.write("\n\n")

        file.write(
            f"Total Distance: {distance} km\n"
        )

    print(
        "\nReport saved to outputs/route_report.txt"
    )


# ==================================
# Main Menu
# ==================================

def main():

    graph = create_sample_city()

    while True:

        print("\n")
        print("=" * 40)
        print(" INTELLIGENT ROUTE PLANNER ")
        print("=" * 40)

        print("1. Show Graph")
        print("2. BFS Traversal")
        print("3. DFS Traversal")
        print("4. Find Shortest Route")
        print("5. Visualize Graph")
        print("6. Exit")

        choice = input("\nEnter Choice: ").strip()

        # -------------------
        # Show Graph
        # -------------------
        if choice == "1":

            graph.display_graph()

        # -------------------
        # BFS
        # -------------------
        elif choice == "2":

            print("\nLocations:")
            print(", ".join(sorted(graph.graph.keys())))

            start = input(
                "\nStart Location: "
            ).strip().upper()

            result = graph.bfs(start)

            if result:
                print(
                    "\nBFS Traversal:"
                )
                print(
                    " -> ".join(result)
                )

        # -------------------
        # DFS
        # -------------------
        elif choice == "3":

            print("\nLocations:")
            print(", ".join(sorted(graph.graph.keys())))

            start = input(
                "\nStart Location: "
            ).strip().upper()

            result = graph.dfs(start)

            if result:
                print(
                    "\nDFS Traversal:"
                )
                print(
                    " -> ".join(result)
                )

        # -------------------
        # Shortest Path
        # -------------------
        elif choice == "4":

            print("\nAvailable Locations:")
            print(
                ", ".join(
                    sorted(graph.graph.keys())
                )
            )

            source = input(
                "\nSource: "
            ).strip().upper()

            destination = input(
                "Destination: "
            ).strip().upper()

            path, distance = graph.dijkstra(
                source,
                destination
            )

            if path is not None:

                print("\n===== ROUTE SUMMARY =====")

                print(
                    "\nOptimized Route:"
                )

                print(
                    " -> ".join(path)
                )

                print(
                    f"\nTotal Distance: {distance} km"
                )

                save_report(
                    path,
                    distance
                )

        # -------------------
        # Visualization
        # -------------------
        elif choice == "5":

            graph.visualize()

        # -------------------
        # Exit
        # -------------------
        elif choice == "6":

            print(
                "\nThank you for using Intelligent Route Planner!"
            )

            break

        else:

            print(
                "\nInvalid Choice. Try Again."
            )


if __name__ == "__main__":
    main()