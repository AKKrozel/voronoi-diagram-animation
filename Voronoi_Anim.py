import numpy as np
import multiprocessing
import os
import cv2
import time
from save_voronoi_frame import save_voronoi_frame

# Global constants
PIXEL_DIMENSION = 1080
NUM_POINTS = 6
CIRCLE_RADIUS = 3.0
FRAME_RATE = 60
INIT_P = -5.0
FINAL_P = 100.0
SLOW_INCREMENT = 0.005
FAST_INCREMENT = 0.025
RAPID_INCREMENT = 0.5
SLOW_PAST_P = 0.0
FAST_PAST_P = 2.5
RAPID_PAST_P = 6.0
IMAGE_FOLDER = 'voronoi_images'
DPI = 100

os.makedirs(IMAGE_FOLDER, exist_ok=True)

def generate_points_and_colors(num_points, pixel_dim):
    points = np.array([[np.random.uniform(1.5*CIRCLE_RADIUS, pixel_dim-(1.5*CIRCLE_RADIUS)), np.random.uniform(1.5*CIRCLE_RADIUS, pixel_dim-(1.5*CIRCLE_RADIUS))] for _ in range(num_points)])
    colors = np.array([[np.random.uniform(0, 255), np.random.uniform(0, 255), np.random.uniform(0, 255)] for _ in range(num_points)])
    return points, colors

def create_images(image_folder, points, colors, pixel_dim, init_p, final_p, increment, frame_rate):
    p_values = []
    p = init_p
    while p < final_p:
        if np.abs(p)<10e-10:
            p -= increment / 2.0

        p_values.append(p)

        if p > SLOW_PAST_P:
            increment = SLOW_INCREMENT
        if p > FAST_PAST_P:
            increment = FAST_INCREMENT
        if p > RAPID_PAST_P:
            increment = RAPID_INCREMENT
        p += increment

    args = [(i, image_folder, points, colors, pixel_dim, p, CIRCLE_RADIUS, DPI) for i, p in enumerate(p_values)]
    
    with multiprocessing.Pool() as pool:
        pool.starmap(save_voronoi_frame, args)

def create_video(image_folder, video_name, fps):
    image_files = sorted([f for f in os.listdir(image_folder) if f.endswith('.png')])
    sample_image = cv2.imread(os.path.join(image_folder, image_files[0]))
    height, width, _ = sample_image.shape

    video_writer = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'DIVX'), fps, (width, height))

    for file in image_files:
        image_path = os.path.join(image_folder, file)
        frame = cv2.imread(image_path)
        video_writer.write(frame)

    video_writer.release()

if __name__ == "__main__":
    points, colors = generate_points_and_colors(NUM_POINTS, PIXEL_DIMENSION)

    create_images(IMAGE_FOLDER, points, colors, PIXEL_DIMENSION, INIT_P, FINAL_P, FAST_INCREMENT, FRAME_RATE)

    video_name = 'voronoi_animation.mp4'
    create_video(IMAGE_FOLDER, video_name, FRAME_RATE)
