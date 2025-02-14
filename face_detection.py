#!/usr/bin/python3

# Import libraries
import cv2
from config.frame_drawing import FrameDrawing
from config.frame_editing import FrameEditing
import os


# This is just a class to find the width and height of the frame
class FindValues:
    # Get frame width and height
    @staticmethod
    def get_frame_width_height(frame):
        # Return width and height
        return frame.shape[1], frame.shape[0]


# This is the class that contain the face detection algorithm
class FaceDetection:
    # Face detection ~ Detect human face
    @staticmethod
    def face_detection(frame, face_cascade, scale_factor, min_neighbors, line_thickness):
        """
            cascade.detectMultiScale(frame, scaleFactor, minNeighbors, minSize=Optional, maxSize=Optional)

                frame: have to be a gray frame bc most of the model are train with gray frame

                scaleFactor: parameter specifying how much the image size is reduced at each image scale.
                            1.05 is a good possible value for this, which means you use a small step for resizing, i.e. reduce size by 5%, you increase the chance of a matching size with the model for detection is found.
                            (We have to scale the image bc the model has a fixed size defined during training)

                minNeighbors: parameter specifying how many neighbors each candidate rectangle should have to retain it.
                            This parameter will affect the quality of the detected faces.
                            Higher value results in less detections but with higher quality. 3~6 is a good value for it.
                            (This is the quality for detecting faces)

                minSize: minimum possible object size. Objects smaller than that are ignored.
                        This parameter determine how small size you want to detect. Usually, [30, 30] is a good start for face detection.
                        (Optional ~ This is the min size we want to detect a face in a frame)

                maxSize: maximum possible object size. Objects bigger than this are ignored.
                        This parameter determine how big size you want to detect.
                        Usually, you don't need to set it manually, the default value assumes you want to detect without an upper limit on the size of the face
                        (Optional ~ This is the max size we want to detect a face in a frame)
        """

        # Get frame width and height
        width, height = FindValues.get_frame_width_height(frame)  # Get video width and height

        # Convert original frame to gray
        gray = FrameEditing.convert_frame_to_gray(frame)

        # Get location of the faces in term of position
        faces = face_cascade.detectMultiScale(gray, scale_factor, min_neighbors, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)  # Return a rectangle (x_pos, y_pos, width, height)

        # Detect faces
        for (x, y, w, h) in faces:
            # Draw rectangle in the face
            FrameDrawing.draw_rect(frame, (x, y), (x+w, y+h), (255, 53, 18), line_thickness)  # Rect for the face

            # Print feedback
            print(f'Coordinate: {(x, y)} - Size: {(w, h)}')

            # Draw the coordinates and the size of the rectangle into the screen
            FrameDrawing.draw_text(frame, 'Coordinate: {} - Size: {}'.format((x, y), (w, h)), (width // 25, height // 10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 1)


# This is the Main Class ~ This class will show you the Video Frame with the live face detection
class LiveFaceDetection:
    def __init__(self):
        # Live face detection
        self.live_face_detection()

    # Load and show video frame
    @classmethod
    def live_face_detection(cls):
        """
            color ~ RGB, BGR, HSV:
                RGB: (red, green, blue)
                BGR: (blue, green, red)
                HSV: hue saturation and lightness/brightness

            frame ~ [row, column, channels]:
                row: height of the image
                column: width of the image
                channels: color space of the image in each pixel (blue, green, red) ~ BGR
        """

        # Video capture using WebCam
        cap = cv2.VideoCapture(0)

        # print a feedback
        print('Camera On')

        # Load face detection classifier ~ I put this here because I didn't want to load it everytime I run the FaceDetection class
        # Load face detection classifier ~ Path to face & eye cascade
        face_cascade = cv2.CascadeClassifier(os.path.dirname(__file__) +
            "/haarcascade_frontalface_default.xml")  # Pre-trained model

        while True:

            # Original frame ~ Video frame from camera
            ret, frame = cap.read()  # Return value (true or false) if the capture work, video frame

            # Edited Frames
            small_frame = FrameEditing.scale_frame(frame, 0.5, 0.5)  # Make original frame smaller by half
            # Please uncomment one or both of this if you want to use it
            hsv_frame = FrameEditing.convert_frame_to_hsv(small_frame)  # Convert BGR color into HSV color
            gray_frame = FrameEditing.convert_frame_to_gray(small_frame)  # Convert BGR color into Gray scale color

            # Get video width and height ~ Please uncomment this if you want to see fur frame in one
            width, height = FindValues.get_frame_width_height(frame)

            # Show certain colors that you want ~ Please uncomment this if you want to see only the skin color in the frame
            skin_color = FrameEditing.show_skin_color(small_frame, hsv_frame, [0, 58, 30], [33, 255, 255])

            # Face & Eye detection
            FaceDetection.face_detection(small_frame, face_cascade, scale_factor=1.2, min_neighbors=5, line_thickness=2)

            # Combine frame ~ Please uncomment one of this if you want to see two or fur frame in one
            two_frame_combined = FrameEditing.combine_two_frame(small_frame, skin_color)  # Show two frame next to each other horizontally
            # four_frame_combine = FrameEditing.combine_four_frame(frame, width, height, small_frame, hsv_frame, skin_color, gray_frame)

            # Load video frame ~ Please put here the frame that you will like to see
            cv2.imshow('Video Frame', small_frame)

            # Wait 1 millisecond second until q key is press
            # Get a frame every 1 millisecond
            if cv2.waitKey(1) == ord('q'):
                print('Camera Off')
                break

        # Close windows
        cap.release()  # Realise the webcam
        cv2.destroyAllWindows()  # Destroy all the windows


if __name__ == '__main__':
    # Face detecton - Webcam test
    face_detection = LiveFaceDetection()
