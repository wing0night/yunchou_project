import heapq

def dijkstra(graph, start):
    queue = [(0, start)]
    visited = set()
    shortest_distances = {node: (float('inf'), '') for node in graph}
    shortest_distances[start] = (0, start)
    paths = {start: [start]}

    while queue:
        (dist, current_node) = heapq.heappop(queue)
        if current_node not in visited:
            visited.add(current_node)
            for neighbour, distance in graph[current_node].items():
                old_distance, _ = shortest_distances[neighbour]
                new_distance = dist + distance
                if new_distance < old_distance:
                    shortest_distances[neighbour] = (new_distance, current_node)
                    paths[neighbour] = paths[current_node] + [neighbour]
                    heapq.heappush(queue, (new_distance, neighbour))

    return shortest_distances, paths


if __name__ == '__main__':
    graph = {
        'A': {'B': 1, 'C': 4, 'D': 7, 'E': 3},
        'B': {'A': 1, 'C': 2, 'D': 5, 'F': 12},
        'C': {'A': 4, 'B': 2, 'D': 1, 'G': 5},
        'D': {'A': 7, 'B': 5, 'C': 1, 'H': 4},
        'E': {'A': 3, 'F': 7, 'I': 4},
        'F': {'B': 12, 'E': 7, 'G': 3, 'J': 4},
        'G': {'C': 5, 'F': 3, 'H': 6, 'K': 3},
        'H': {'D': 4, 'G': 6, 'L': 7},
        'I': {'E': 4, 'J': 1, 'M': 5},
        'J': {'F': 4, 'I': 1, 'K': 2, 'N': 6},
        'K': {'G': 3, 'J': 2, 'L': 6, 'O': 7},
        'L': {'H': 7, 'K': 6, 'P': 8},
        'M': {'I': 5, 'N': 4, 'Q': 9},
        'N': {'J': 6, 'M': 4, 'O': 2, 'R': 7},
        'O': {'K': 7, 'N': 2, 'P': 3, 'S': 6},
        'P': {'L': 8, 'O': 3, 'T': 5},
        'Q': {'M': 9, 'R': 4, 'U': 10},
        'R': {'N': 7, 'Q': 4, 'S': 3, 'V': 6},
        'S': {'O': 6, 'R': 3, 'T': 4, 'W': 7},
        'T': {'P': 5, 'S': 4, 'X': 6},
        'U': {'Q': 10, 'V': 5, 'Y': 11},
        'V': {'R': 6, 'U': 5, 'W': 4, 'Z': 7},
        'W': {'S': 7, 'V': 4, 'X': 3, 'Z': 6},
        'X': {'T': 6, 'W': 3},
        'Y': {'U': 11, 'Z': 8},
        'Z': {'V': 7, 'W': 6, 'Y': 8}
    }

    shortest_distances, paths = dijkstra(graph, 'A')
    for node, (distance, _) in shortest_distances.items():
        print(f"Path to {node}: {' -> '.join(paths[node])}, Distance: {distance}")
