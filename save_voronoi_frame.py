import numpy as np
import matplotlib.pyplot as plt
import os

def minkowski_distance(x1, y1, x2, y2, p):
    return (abs(x1 - x2) ** p + abs(y1 - y2) ** p) ** (1 / p)

def save_voronoi_frame(i, image_folder, points, colors, pixel_dim, p, circle_radius, dpi):
    frame = np.zeros((pixel_dim, pixel_dim, 3), dtype=np.uint8)

    for x in range(pixel_dim):
        for y in range(pixel_dim):
            closest_distance = float('inf')
            closest_index = -1
            for k in range(len(points)):
                dist = minkowski_distance(points[k][0], points[k][1], x, y, p)
                if dist < closest_distance:
                    closest_distance = dist
                    closest_index = k
            frame[y, x] = colors[closest_index] if closest_index != -1 else [0, 0, 0]

    fig, ax = plt.subplots(figsize=(pixel_dim / dpi, pixel_dim / dpi), dpi=dpi)
    ax.imshow(frame)
    ax.axis('off')

    for point in points:
        circle = plt.Circle((point[0], point[1]), circle_radius, color='red', fill=True)
        ax.add_patch(circle)

    file_name = f'frame_{str(i).zfill(8)}.png'
    plt.savefig(os.path.join(image_folder, file_name), bbox_inches='tight', pad_inches=0, dpi=dpi)
    plt.close()
