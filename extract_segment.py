import os
import cv2
import pandas as pd
import numpy as np
import warnings

warnings.filterwarnings("ignore")


def segment(CFG):
    # Path to the folder containing the mp4 videos
    VID_PATH = CFG.video_path

    # Empty folder to save the videos: MAIN_SAVE_PATH/VIDEOS/FRAMES
    MAIN_SAVE_PATH = CFG.save_path

    # Initiate an empty dataframe to save the videos, frames and paths
    df = pd.DataFrame()
    VERBOSE = False

    # Empty lists to save the videos, frames, paths
    frames = []
    videos = []
    image_path = []

    # Capture the frames
    vidcap = cv2.VideoCapture(f"{VID_PATH}")

    # Get fps of the video
    fps = vidcap.get(cv2.CAP_PROP_FPS)

    ## filter the segment
    initial_second = np.array(CFG.start) * fps
    final_second = np.array(CFG.end) * fps

    # Generate the video name for the folder
    vid_id = VID_PATH.split("/")[-1].split(".")[0]
    save_path = f"{MAIN_SAVE_PATH}/{vid_id}"

    # Create the video folders
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    success, image = vidcap.read()  # Frame capture
    count = 0  # Initialize frame count

    while success:

        # Save the frames within the indicated segment
        for st, ft in zip(initial_second, final_second):
            if count > st and count < ft and count % fps == 0:
                print(f"Extracting frame {count} at time stamp {count/fps}")
                cv2.imwrite(
                    f"{save_path}/{vid_id}_{count}.jpg", image
                )  # save frame as JPEG file
                success, image = vidcap.read()

                if VERBOSE:
                    print(f"{count}: Read a new frame: ", success)

                frames.append(count)
                videos.append(vid_id)
                image_path.append(f"{vid_id}/{vid_id}_{count/fps}.jpg")

            success, image = vidcap.read()
            count += 1

    # Store all the saved images to csv
    df["clip_name"] = videos
    df["frames"] = frames
    df["image_path"] = image_path

    if CFG.save_csv:
        csv_path = os.path.join(
            CFG.save_path, vid_id, f"segment{CFG.start}_{CFG.end}.csv"
        )
        df.to_csv(csv_path)
