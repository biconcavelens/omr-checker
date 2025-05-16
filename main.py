import cv2
import numpy as np

def preprocess_image(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  #Grayscale
    blurred = cv2.GaussianBlur(image, (5, 5), 0)  # blur to reduce noise
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)#thresholding
    return image, thresh

def find_circles(thresh):
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    detected_circles = []

    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
        area = cv2.contourArea(contour)

        #filter contours based on shape and size
        if len(approx) > 6 and 200 < area < 1500:
            (x, y), radius = cv2.minEnclosingCircle(contour)
            detected_circles.append((int(x), int(y), int(radius)))
    
    return detected_circles

def get_option(x): # x coordinate threshold for answer options (checked from input image)
    if x < 57:
        return 'A'
    elif x < 92:
        return 'B'
    elif x < 127:
        return 'C'
    elif x < 160:
        return 'D'
    else:
        return 'E'

def group_by_questions(circles):
    circles.sort(key=lambda c: c[1])  # sorting by y value
    question_groups = []
    current_group = []

    for x, y, r in circles:
        if not current_group:
            current_group.append((x, y, r))
        else:
            #checking if bubble is for previous qn
            if abs(current_group[0][1] - y) < 20:
                current_group.append((x, y, r))
            else:
                question_groups.append(current_group[:])
                current_group = [(x, y, r)]  #new qn

    if current_group:  # Add the last group
        question_groups.append(current_group)
    
    return question_groups

def detect_answers(image_path):
    image, thresh = preprocess_image(image_path)
    circles = find_circles(thresh)
    questions = group_by_questions(circles)
    answers = {}

    debug_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)  # Convert grayscale to color for visualization

    for q_num, question_bubbles in enumerate(questions, 1):
        max_fill_ratio = 0
        marked_answer = None

        print(f"Question {q_num} bubble positions: {[x for x, _, _ in question_bubbles]}")

        for (x, y, r) in question_bubbles:
            option = get_option(x)

            # Create a mask for this bubble
            mask = np.zeros_like(thresh, dtype=np.uint8)
            mask_radius = int(r * 0.7)
            cv2.circle(mask, (x, y), mask_radius, 255, -1)

            # Apply mask and count white pixels
            bubble_area = cv2.bitwise_and(thresh, thresh, mask=mask)
            white_pixel_count = np.sum(bubble_area == 255)
            
            # Calculate fill ratio
            bubble_area_estimated = np.pi * (mask_radius ** 2)
            fill_ratio = white_pixel_count / bubble_area_estimated if bubble_area_estimated > 0 else 0

            # Determine the most filled bubble
            if fill_ratio > max_fill_ratio:
                max_fill_ratio = fill_ratio
                marked_answer = option

        # Save the detected answer if it meets the threshold
        if max_fill_ratio > 0.4:
            answers[q_num] = marked_answer

    return answers

image_path = "test.jpg"

img = cv2.imread(image_path)

# Extract answers
answers = detect_answers(image_path)

# Print final answers
print("\nFinal Detected Answers:")
for q, ans in sorted(answers.items()):
    print(f"Question {q}: Marked {ans}")