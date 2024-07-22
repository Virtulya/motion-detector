import cv2
import os
import numpy as np
import datetime
from videoRecorder import VideoRecorder

# Motion Detection Class (child class of VideoRecorder)
class MotionDetection(VideoRecorder):
    def __init__(self, config_path):
        super().__init__(config_path)
        self.prev_frame_mean = None
        self.motion = False
    
    def detect_motion(self):
        while(self.cap.isOpened()):
            ret, frame = self.cap.read()
            date_and_time = str(datetime.datetime.now())
            frame = self.display_frame(frame, date_and_time)

            if self.prev_frame_mean is not None:
                # Check the difference between the mean of pixels of the current frame and the previous frame
                if np.abs(np.mean(frame) - self.prev_frame_mean) > self.config["detection_threshold"]:
                    print("Motion detected.\nRecording...\n")
                    self.motion = True

                # Start recording the if motion is detected
                if self.motion:
                    self.folder_size = 0
                    self.initialize_paths(date_and_time)

                    # Create the video writer object
                    if self.out is None:
                        self.out = cv2.VideoWriter(self.time_file_path, self.fourcc, self.config["video"]["fps"],
                                            tuple([self.config["video"]["frame_width"], self.config["video"]["frame_height"]]), 
                                            isColor=True)

                    # Calculate the size of the folder
                    files = os.listdir(self.day_path)
                    for file in files:
                        fp = os.path.join(self.day_path, file)
                        self.folder_size += os.path.getsize(fp)

                    # If the folder size exceeds the allocated memory percentage, delete the oldest file.
                    # Logic is to divide the percentage by 100 and multiply the max memory usage
                    # by 1000000, simplified to shorten the code and fit it in smaller windows
                    if self.folder_size >= self.config["percentage_allocated_memory"] * self.config["max_memory_usage_mb"] * 10000:
                        oldest_file = os.path.join(self.day_path, files[0])
                        self.folder_size -= os.path.getsize(oldest_file)
                        os.remove(oldest_file)

                    self.write_frame(frame)

                    # Stop recording after the specified duration
                    if self.frame_count >= self.config["recording_duration"] * self.config["video"]["fps"]:
                        self.motion = False
                        self.frame_count = 0
                        print("Recording stopped\n")
                        if self.out is not None:
                            self.out.release()
                            self.out = None

            self.prev_frame_mean = np.mean(frame)

            # Break the loop if the specified key is pressed
            if cv2.waitKey(1) & 0xFF == ord(self.config["wait_key"]):
                break

        self.release_resources()

if __name__ == "__main__":
    config_path = 'config.json'
    motion_capture = MotionDetection(config_path)
    motion_capture.detect_motion()