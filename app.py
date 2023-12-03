import streamlit as st
import cv2
import os
import numpy as np

UPLOAD_FOLDER = 'uploads'
DIFFERENCE_VIDEO_PATH = 'static/difference.mp4'

# Create the uploads folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Streamlit app
def main():
    st.title('Upload and Process Videos')

    # Upload two videos
    file1 = st.file_uploader('Upload first video (.mp4)', type=['mp4'])
    file2 = st.file_uploader('Upload second video (.mp4)', type=['mp4'])

    if file1 and file2:
        # Process the videos
        process_button = st.button('Process Videos')
        if process_button:
            process_videos(file1, file2)
            st.success('Videos processed successfully!')

            # Display the processed video
            st.video(DIFFERENCE_VIDEO_PATH, format="video/mp4")

# Process the videos and save the difference
def process_videos(file1, file2):
    video1_path = os.path.join(UPLOAD_FOLDER, file1.name)
    video2_path = os.path.join(UPLOAD_FOLDER, file2.name)

    with open(video1_path, 'wb') as f1, open(video2_path, 'wb') as f2:
        f1.write(file1.read())
        f2.write(file2.read())

    video1 = cv2.VideoCapture(video1_path)
    video2 = cv2.VideoCapture(video2_path)

    frame_width = int(video1.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video1.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # Use "mp4v" for compatibility
    out = cv2.VideoWriter(DIFFERENCE_VIDEO_PATH, fourcc, 30.0, (frame_width, frame_height))

    while True:
        success1, frame1 = video1.read()
        success2, frame2 = video2.read()

        if not success1 or not success2:
            break

        # Process frames (for example, compute absolute difference)
        difference = cv2.absdiff(frame1, frame2)

        # Display the difference in Streamlit
        st.image(difference, channels="BGR")

        # Write the difference to the output video file
        out.write(difference)

    video1.release()
    video2.release()
    out.release()

# Run the Streamlit app
if __name__ == '__main__':
    main()
