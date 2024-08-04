import cv2
import uuid
import drivers
from time import sleep

display = drivers.Lcd()

# Load class names
classNames = []
classFile ="/home/newgn/Desktop/Object_Detection_Files/coco.names"
with open(classFile, "rt") as f:
    classNames = f.read().rstrip("\n").split("\n")

# Load model configuration and weights
configPath = "/home/newgn/Desktop/Object_Detection_Files/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
weightsPath = "/home/newgn/Desktop/Object_Detection_Files/frozen_inference_graph.pb"
net = cv2.dnn_DetectionModel(weightsPath, configPath)
net.setInputSize(320, 320)
net.setInputScale(1.0 / 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

# Define reference line parameters
reference_line_x = 320  # Assuming a 640x480 video feed
reference_line_color = (0, 255, 0)
people_count = 0
trackers = {}

def getObjects(img, thres, nms, draw=True, objects=[]):
    global people_count, trackers
    classIds, confs, bbox = net.detect(img, confThreshold=thres, nmsThreshold=nms)
    if len(objects) == 0:
        objects = classNames
    objectInfo = []

    # Update tracker positions and states
    new_trackers = {}
    for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
        className = classNames[classId - 1]
        if className.lower() == "person":
            x, y, w, h = box
            center_x = x + w // 2

            person_id = None
            min_distance = float('inf')

            # Identify person by finding the closest existing tracker
            for tid, (px, state) in trackers.items():
                distance = (center_x - px) ** 2
                if distance < min_distance:
                    min_distance = distance
                    person_id = tid

            # Threshold distance to consider it the same person
            if min_distance > 10000 or person_id is None:
                person_id = str(uuid.uuid4())  # Correctly generate a new UUID

            # Track or update the tracker
            new_state = 'left' if center_x < reference_line_x else 'right'
            if person_id not in new_trackers:
                if person_id in trackers and trackers[person_id][1] != new_state:
                    if new_state == 'right':
                        people_count += 1
                    elif new_state == 'left':
                        people_count -= 1
                new_trackers[person_id] = (center_x, new_state)

            if draw:
                cv2.rectangle(img, box, color=(0, 255, 0), thickness=2)
                cv2.putText(img, f"{className.upper()} {confidence:.2f} ID: {person_id[:8]}", (box[0], box[1] - 10), cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 255, 0), 2)

    trackers = new_trackers

    # Draw the reference line
    cv2.line(img, (reference_line_x, 0), (reference_line_x, img.shape[0]), reference_line_color, 2)

    # Display count on the screen
    cv2.putText(img, f"Count: {people_count}", (10, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

    return img, objectInfo

if _name_ == "_main_":
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    while True:
        success, img = cap.read()
        result, objectInfo = getObjects(img, 0.45, 0.2, objects=['person'])

        # Display count on the LCD screen
        display.lcd_display_string(f"People Count: {people_count}", 1)

        cv2.imshow("Output", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()