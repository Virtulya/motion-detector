import cv2
import os
import json

# Video Recorder Class
class VideoRecorder:
    def __init__(self, config_path):
        # Load configuration from JSON file
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.cap = cv2.VideoCapture(self.config["device_id"])
        self.fourcc = cv2.VideoWriter_fourcc(*self.config["video"]["codec"])
        self.out = None
        self.frame_count = 0
        self.folder_size = 0

    # Initialize path names to save the recorded video
    def initialize_paths(self, date_and_time):
        self.year_path = './' + date_and_time[:4] + '/'
        self.month_path = self.year_path + date_and_time[5:7] + '/'
        self.day_path = self.month_path + date_and_time[8:10] + '/'
        self.time_file_path = self.day_path + date_and_time[11:19].replace(':', '_') + self.config["video"]["extension"]

        # Create the paths if they don't exist
        if not os.path.exists(self.year_path):
            os.mkdir(self.year_path)
        if not os.path.exists(self.month_path):
            os.mkdir(self.month_path)
        if not os.path.exists(self.day_path):
            os.mkdir(self.day_path)

    # Write the frame to the video file
    def write_frame(self, frame):
        self.out.write(frame)
        self.frame_count += 1

    # Release video capture and writer resources
    def release_resources(self):
        self.cap.release()
        if self.out is not None:
            self.out.release()
        cv2.destroyAllWindows()

    # Display the frame with the current date and time
    def display_frame(self, frame, date_and_time):
        # Flip the frame horizontally
        frame = cv2.flip(frame, 1)
        # Display the current time on the frame
        frame = cv2.putText(frame, date_and_time, 
                            tuple([self.config["text"]["origin_coordinates"]["x"], self.config["text"]["origin_coordinates"]["y"]]), 
                            getattr(cv2, self.config["text"]["font"]), 
                            self.config["text"]["font_scale"],
                            tuple([self.config["text"]["color"]["r"], self.config["text"]["color"]["g"], self.config["text"]["color"]["b"]]),
                            self.config["text"]["thickness"],
                            getattr(cv2, self.config["text"]["line_type"]))
        # Display the frame
        cv2.imshow('frame', frame)
        return frame