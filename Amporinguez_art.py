import cv2
import numpy as np
import time
import random

# Create a white canvas
chart = np.ones((300, 795, 3), dtype=np.uint8) * 255

# Define bear shape using coordinates
bear = np.array([[303,219],[294,230],[272,228],[241,190],[232,188],[215,227],
                 [234,236],[225,244],[195,240],[193,194],[152,195],[151,222],
                 [164,228],[158,235],[136,233],[120,201],[104,217],[104,232],
                 [113,242],[97,246],[80,224],[98,138],[138,104],[207,100],
                 [240,93],[272,122],[280,106],[288,116],[300,115],[312,109],
                 [309,129],[325,143],[322,157],[339,174],[330,182],[315,184],
                 [273,176],[281,213],[303,219]])

# Draw bear's eye, make it red for a fierce look
eyebear = np.array([[308,147],[311,153],[315,153],[313,147],[308,147]])
cv2.polylines(chart, [bear], False, (0, 0, 255))  # Draw bear outline
cv2.polylines(chart, [eyebear], False, (255, 0, 0))  # Draw bear eye
cv2.fillPoly(chart, [bear], (0, 0, 255))  # Fill bear with red
cv2.fillPoly(chart, [eyebear], (255, 0, 0))  # Fill bear eye with red

# Define bull shape using coordinates
bull = np.array([[364,41],[370,83],[387,90],[386,93],[390,111],[376,136],
                 [387,142],[402,141],[432,130],[447,155],[462,164],[440,174],
                 [450,216],[469,220],[455,184],[493,182],[489,197],[513,239],
                 [532,239],[511,203],[530,189],[601,195],[605,209],[587,242],
                 [606,241],[608,226],[640,195],[657,216],[639,241],[660,241],
                 [672,216],[667,181],[682,156],[682,141],[668,121],[697,124],
                 [715,156],[710,182],[722,156],[707,118],[660,108],[618,106],
                 [555,85],[534,60],[502,46],[457,72],[416,71],[398,63],
                 [386,40],[391,72],[381,72],[364,41]])

# Draw bull's eye, make it red for a fierce look
eyebull = np.array([[394,110],[399,110],[400,100],[394,110]])
cv2.fillPoly(chart, [bull], color=(50, 205, 50))  # Fill bull with green
cv2.fillPoly(chart, [eyebull], color=(255, 0, 0))  # Fill bull eye with red

# Function to make shapes larger
def expand_shape(shape, buffer):
    centroid = np.mean(shape, axis=0)
    expanded_shape = []
    for point in shape:
        vector = point - centroid
        unit_vector = vector / np.linalg.norm(vector)
        expanded_point = point + unit_vector * buffer
        expanded_shape.append(expanded_point)
    return np.array(expanded_shape, dtype=np.int32)

# Function to draw random lightning
def draw_lightning(chart, num_strikes=1):
    height, width, _ = chart.shape
    for _ in range(num_strikes):
        x_start = random.randint(0, width)
        y_start = random.randint(0, height // 2)
        x_end = random.randint(x_start - 50, x_start + 50)
        y_end = height
        thickness = random.randint(2, 4)
        cv2.line(chart, (x_start, y_start), (x_end, y_end), (255, 0, 0), thickness)



# Open window to show the chart
cv2.namedWindow('Bull vs Bear')

# Loop for animation
for i in range(10000):
    chart_copy = chart.copy()  # Make a copy of the chart

    # Calculate pulsating size
    buffer = 20 + 10 * np.sin(i / 10.0)

    # Draw lightning every 10 frames
    if i % 10 == 0:
        draw_lightning(chart_copy, num_strikes=random.randint(1, 3))

    # Make the bear and bull bigger
    expanded_bear = expand_shape(bear, buffer)
    expanded_bull = expand_shape(bull, buffer)

    # Draw expanded bear and bull shapes
    cv2.polylines(chart_copy, [expanded_bear], False, (0, 0, 255), thickness=2)
    cv2.polylines(chart_copy, [expanded_bull], False, (50, 205, 50), thickness=2)

    # Random shaking effect to simulate earthquake
    if i % 10 == 0:
        shake_x = random.randint(-5, 5)
        shake_y = random.randint(-5, 5)
        M = np.float32([[1, 0, shake_x], [0, 1, shake_y]])
        chart_copy = cv2.warpAffine(chart_copy, M, (chart_copy.shape[1], chart_copy.shape[0]))

    # Show the animation
    cv2.imshow('Bull vs Bear', chart_copy)
    cv2.waitKey(50)

# Close the window when done
cv2.destroyAllWindows()
