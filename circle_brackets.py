import cv2
import numpy as np
import sys, os

# Colors (B, G, R)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def create_blank(width, height, color=(0, 0, 0)):
    """Create new image(numpy array) filled with certain color in BGR"""
    image = np.zeros((height, width, 3), np.uint8)
    # Fill image with color
    image[:] = color

    return image


def draw_half_circle_rounded(image, startAngle, endAngle):
    height, width = image.shape[0:2]
    # Ellipse parameters
    radius1 = 200
    radius2 = 250
    center = (width / 2, height/2 )
    axes = (radius1, radius2)
    angle = 0
    startAngle = startAngle
    endAngle = endAngle
    thickness = 10
    # http://docs.opencv.org/modules/core/doc/drawing_functions.html#ellipse
    cv2.ellipse(image, center, axes, angle, startAngle, endAngle, (0, 0, 255), thickness)


# Create new blank 300x150 white image
imageFile = sys.argv[1]
image = cv2.imread(imageFile)
draw_half_circle_rounded(image, 135, 225)
draw_half_circle_rounded(image, -45, 45)
cv2.imwrite('output/half_circle_droplet.jpg', image)


height, width = 733, 824
image2 = create_blank(width, height, color=WHITE)
draw_half_circle_rounded(image2, 135, 225)
draw_half_circle_rounded(image2, -45, 45)
cv2.imwrite('output/half_circle_blank.jpg', image2)