import os
import cv2
import numpy as np
import warnings

warnings.filterwarnings("ignore")

def segment(CFG):
    """
    Segment the frames of a video based on the specified time interval and save them as images.

    Args:
        CFG: A configuration object containing parameters for video processing.

    Returns:
        None
    """
    # Capture the frames
    vidcap = cv2.VideoCapture(CFG.video_path)

    # Get fps of the video
    fps = round(vidcap.get(cv2.CAP_PROP_FPS))

    # Calculate frame indices for the segment
    initial_second = np.array(CFG.start) * fps
    final_second = np.array(CFG.end) * fps

    # Generate the video name for the folder
    vid_id = os.path.splitext(os.path.basename(CFG.video_path))[0]
    save_path = os.path.join(CFG.save_path, vid_id)

    # Create the video folders if it doesn't exist
    os.makedirs(save_path, exist_ok=True)

    success, image = vidcap.read()  # Frame capture
    count = 0



    while success:
        count += 1
        # Save the frames within the indicated segment
        for st, ft in zip(initial_second, final_second):
            if st < count < ft and count % fps == 0:
                # Save frame as JPEG file
                frame_timestamp = count / fps  # Correct calculation of timestamp
                frame_filename = f"{vid_id}_{frame_timestamp:.2f}.jpg"  # Format timestamp
                frame_path = os.path.join(save_path, frame_filename)
                cv2.imwrite(frame_path, image)

                if CFG.verbose:
                    print(f"{frame_timestamp}: Read a new frame: ", success)

              
        success, image = vidcap.read()

    print(f"Frames saved at {save_path}")