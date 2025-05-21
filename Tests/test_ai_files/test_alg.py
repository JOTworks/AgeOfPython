import time
import os
import sys

def next_orthogonal_point(center_x, center_y, current_x, current_y, ring_width):
    dx = current_x - center_x
    dy = current_y - center_y

    # If at center, go right first
    if dx == 0 and dy == 0:
        return center_x + ring_width, center_y

    # Compute current ring distance
    distance = dx if dx != 0 else dy
    abs_dist = -distance if distance < 0 else distance

    # Advance direction in order: right → up → left → down
    if dx > 0 and dy == 0:
        return center_x, center_y + abs_dist          # right → up
    elif dy > 0 and dx == 0:
        return center_x - abs_dist, center_y          # up → left
    elif dx < 0 and dy == 0:
        return center_x, center_y - abs_dist          # left → down
    elif dy < 0 and dx == 0:
        return center_x + abs_dist + ring_width, center_y  # down → next ring right

    # Should never reach here if always orthogonal
    return center_x, center_y

def animate_spiral(center_x, center_y, steps, ring_width, delay=0.2):
    x, y = center_x, center_y
    visited = {}

    for i in range(steps):
        visited[(x, y)] = i

        # Clear screen
        print("\033[H\033[J", end="")

        # Determine bounds dynamically
        min_x = center_x - 10
        max_x = center_x + 10
        min_y = center_y - 10
        max_y = center_y + 10

        for j in range(max_y, min_y - 1, -1):
            row = ""
            for k in range(min_x, max_x + 1):
                if (k, j) == (x, y):
                    row += "** "
                elif (k, j) in visited:
                    row += f"{visited[(k, j)]%100:02d} "
                else:
                    row += " . "
            print(row)

        time.sleep(delay)
        x, y = next_orthogonal_point(center_x, center_y, x, y, ring_width)

# === Run it! ===
animate_spiral(center_x=0, center_y=0, steps=100, ring_width=2, delay=0.05)