import cv2

# Path to the AVI video file
video_path = "screen_recording.avi"

# Open the video file
video = cv2.VideoCapture(video_path)

# Check if the video file opened successfully
if not video.isOpened():
    print(f"Error: Could not open video {video_path}")
    exit()

# Loop through the video frames
while video.isOpened():
    # Read each frame
    ret, frame = video.read()
    
    # If the frame was not successfully read, break the loop (end of video)
    if not ret:
        print("End of video.")
        break
    
    # Display the frame in a window
    cv2.imshow('AVI Video Player', frame)
    
    # Exit the video when 'q' key is pressed
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

# Release the video capture object and close all windows
video.release()
cv2.destroyAllWindows()
