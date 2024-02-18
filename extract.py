import os
import cv2
import pandas as pd

def extract_frames(CFG):
    """
    Extract frames from a video and save them as images.

    Args:
        CFG: A configuration object containing parameters for frame extraction.

    Returns:
        None
    """
    # Generate the video name for the folder
    vid_name = os.path.splitext(os.path.basename(CFG.video_path))[0]
    save_path = os.path.join(CFG.save_path, vid_name)

    # Create the video folders if it doesn't exist
    os.makedirs(save_path, exist_ok=True)

    # Capture the frames
    vidcap = cv2.VideoCapture(CFG.video_path)

    # Get the fps of the video
    fps = int(vidcap.get(cv2.CAP_PROP_FPS))

    success, image = vidcap.read()
    count = 0

    while success:
        # Save the frames based on the frame rate
        if count % fps == 0:
            timestamp = count / fps
            frame_filename = f"{timestamp:.2f}.jpg"
            frame_path = os.path.join(save_path, frame_filename)
            cv2.imwrite(frame_path, image)  # Save frame as JPEG file

            if CFG.verbose:
                print(f"{timestamp}: Read a new frame")

        success, image = vidcap.read()
        count += 1

    print(f"Frames saved at {save_path}")
