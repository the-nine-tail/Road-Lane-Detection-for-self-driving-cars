import cv2
import numpy as np
import math
from moviepy.editor import VideoFileClip


def region_of_interest(img, vertices):
    mask = np.zeros_like(img)
    match_mask_color = 255
    cv2.fillPoly(mask, vertices, match_mask_color)
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image


def draw_lines(img, lines, color=[255, 0, 0], thickness=3):
    if lines is None:
        return
    img = np.copy(img)

    line_img = np.zeros(
        (
        img.shape[0],
        img.shape[1],
        3
        ), dtype=np.uint8
    )

    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(line_img, (x1, y1), (x2, y2), color, thickness)

    img = cv2.addWeighted(img, 0.8, line_img, 1.0, 0.0)

    return img


def pipeline(image):
    height = image.shape[0]
    width = image.shape[1]
    region_of_interest_vertices = [(0, height), (width / 2, height / 2), (width, height)]
    kernel = np.ones((5, 5), np.uint8)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur_image = cv2.GaussianBlur(gray_image, (1, 1), 0)
    canny_image = cv2.Canny(blur_image, 100, 200)
    dilate_image = cv2.dilate(canny_image, kernel, iterations=1)

    cropped_image = region_of_interest(dilate_image, np.array([region_of_interest_vertices], np.int32))

    lines = cv2.HoughLinesP(
        cropped_image,
        rho=4,
        theta=np.pi / 180,
        threshold=140,
        lines=np.array([]),
        minLineLength=40,
        maxLineGap=20
    )

    left_line_x = []
    left_line_y = []
    right_line_x = []
    right_line_y = []
    for line in lines:
        for x1, y1, x2, y2 in line:
            slope = (y2 - y1) / (x2 - x1)
            if math.fabs(slope) >= 0.5:
                if slope <= 0:
                    left_line_x.extend([x1, x2])
                    left_line_y.extend([y1, y2])
                else:
                    right_line_x.extend([x1, x2])
                    right_line_y.extend([y1, y2])

    min_y = int(image.shape[0] * (4 / 5))
    max_y = int(image.shape[0])

    poly_left = np.poly1d(np.polyfit(
        left_line_y,
        left_line_x,
        deg=1
    ))

    left_x_start = int(poly_left(max_y))
    left_x_end = int(poly_left(min_y))

    poly_right = np.poly1d(np.polyfit(
        right_line_y,
        right_line_x,
        deg=1
    ))

    right_x_start = int(poly_right(max_y))
    right_x_end = int(poly_right(min_y))

    line_image = draw_lines(
        image,
        [[
            [left_x_start, max_y, left_x_end, min_y],
            [right_x_start, max_y, right_x_end, min_y],
        ]],
        thickness=3,
    )
    return line_image


output = 'output/input_out.mp4'
clip = VideoFileClip('input/input.mp4')
write_clip = clip.fl_image(pipeline)
write_clip.write_videofile(output, audio=False)