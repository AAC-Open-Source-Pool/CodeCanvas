import cv2
import numpy as np
import matplotlib.pyplot as plt

def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 50, 150)
    return edged

def angle_between(p1, p2, p3):
    """Calculate angle between 3 points (p2 is vertex)."""
    a = np.array(p1) - np.array(p2)
    b = np.array(p3) - np.array(p2)
    cosine_angle = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-10)
    angle = np.arccos(np.clip(cosine_angle, -1.0, 1.0))
    return np.degrees(angle)

def is_diamond(contour):
    approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
    if len(approx) == 4:
        angles = []
        for i in range(4):
            p1 = approx[i][0]
            p2 = approx[(i+1) % 4][0]
            p3 = approx[(i+2) % 4][0]
            ang = angle_between(p1, p2, p3)
            angles.append(ang)
        # Diamonds have roughly equal angles close to 60-120 degrees
        if all(40 < angle < 140 for angle in angles):
            return True
    return False

def is_oval(contour):
    if len(contour) >= 5:
        ellipse = cv2.fitEllipse(contour)
        (center, axes, orientation) = ellipse
        major_axis, minor_axis = max(axes), min(axes)
        aspect_ratio = minor_axis / major_axis
        if 0.5 < aspect_ratio < 1.0:  # Rough oval check
            return True
    return False

def detect_flowchart_elements(preprocessed_img):
    contours, _ = cv2.findContours(preprocessed_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    detected_elements = []

    for contour in contours:
        if cv2.contourArea(contour) < 200:  # Filter very small contours
            continue

        approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
        x, y, w, h = cv2.boundingRect(approx)
        vertices = len(approx)
        shape = "unknown"

        if is_diamond(contour):
            shape = "decision"
        elif is_oval(contour):
            shape = "terminal"
        elif vertices == 4:
            aspect_ratio = float(w) / h
            if 0.9 <= aspect_ratio <= 1.1:
                shape = "process"
            else:
                shape = "io"
        elif vertices == 3:
            # Triangles are uncommon but could be start/end or subprocess
            shape = "process"
        else:
            shape = "unknown"

        detected_elements.append({
            "shape": shape,
            "contour": contour,
            "bounding_box": (x, y, w, h)
        })

    return detected_elements

def draw_detected_shapes_on_image(image, detected_elements):
    color_map = {
        "terminal": (0, 0, 255),   # Red
        "process": (0, 255, 0),    # Green
        "decision": (255, 0, 0),   # Blue
        "io": (255, 255, 0),       # Cyan
        "unknown": (128, 128, 128) # Gray
    }

    occupied_positions = []  # To reduce label overlapping

    for element in detected_elements:
        shape_type = element["shape"]
        contour = element["contour"]
        x, y, w, h = element["bounding_box"]

        # Draw contour
        cv2.drawContours(image, [contour], -1, color_map.get(shape_type, (255, 255, 255)), 2)

        # Find a label position above the box but avoid overlapping labels
        label_x = x
        label_y = y - 10
        for ox, oy in occupied_positions:
            if abs(label_x - ox) < 50 and abs(label_y - oy) < 20:
                label_y -= 20  # Shift label upwards to avoid overlap
        occupied_positions.append((label_x, label_y))

        # Draw label background for readability
        (text_w, text_h), _ = cv2.getTextSize(shape_type, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        cv2.rectangle(image, (label_x, label_y - text_h - 3), (label_x + text_w, label_y + 3), (255,255,255), -1)

        # Put text label
        cv2.putText(image, shape_type, (label_x, label_y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1)

    return image

if __name__ == "__main__":
    image_path = r"C:/Users/HPEliteBook-1040 G2/Desktop/AAC 2025/flowchart_detector/Flowchart-Detection-master/flow chart of largest of three numbers in Java.JPG"
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Image not found or path is incorrect.")

    preprocessed_img = preprocess_image(image)
    detected_elements = detect_flowchart_elements(preprocessed_img)
    output_img = draw_detected_shapes_on_image(image.copy(), detected_elements)

    cv2.imwrite("labeled_flowchart_improved.png", output_img)
    print("Labeled flowchart image saved as: labeled_flowchart_improved.png")

    plt.figure(figsize=(10, 8))
    plt.imshow(cv2.cvtColor(output_img, cv2.COLOR_BGR2RGB))
    plt.title("Detected Flowchart Elements with Clean Labels")
    plt.axis('off')
    plt.show()
