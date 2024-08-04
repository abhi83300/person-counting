import cv2
import numpy as np
import pyautogui

def count_people_on_screen():
    # Take a screenshot
    screenshot = pyautogui.screenshot()
    
    # Convert the screenshot to a numpy array
    frame = np.array(screenshot)
    
    # Convert RGB to BGR (OpenCV uses BGR)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    
    # Load the pre-trained person detector
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    
    # Detect people in the image
    boxes, weights = hog.detectMultiScale(frame, winStride=(8,8))
    
    # Count the number of detections
    person_count = len(boxes)
    
    # Draw boxes around detected people
    for (x, y, w, h) in boxes:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
    # Display the count on the image
    cv2.putText(frame, f'People count: {person_count}', (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    # Show the result
    cv2.imshow('People Counter', frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return person_count

if __name__ == "__main__":
    count = count_people_on_screen()
    print(f"Total people detected: {count}")