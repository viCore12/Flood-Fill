import cv2
import numpy as np

def is_door_open(frame, start_pixel, diff):
    """Processes the image with floodFill and returns True if the garage door is open, otherwise False."""
    height, width, channels = frame.shape
    mask = np.zeros((height + 2, width + 2), np.uint8)

    retval, frame, mask, rect = cv2.floodFill(frame, mask, start_pixel, (0, 255, 0), diff, diff)
    if retval > 60:
        status = False  # door closed
    else:
        status = True  # door open
    return status, frame

video_url = 'http://192.168.1.248:8554/video_feed'
cap = cv2.VideoCapture(video_url)

start_pixel = (258, 50)
diff = (7,7,5)

if not cap.isOpened():
    print("Không thể mở video stream.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Không thể đọc frame từ video.")
        break

    # Process the frame and get the door status
    status, processed_frame = is_door_open(frame, start_pixel, diff)

    # Display the door status on the frame
    status_text = "Door: Open" if status else "Door: Closed"
    cv2.putText(processed_frame, status_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                1, (0, 255, 0) if status else (0, 0, 255), 2, cv2.LINE_AA)

    cv2.imshow('Door Status', processed_frame)

    # Exit if 'q' is
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
