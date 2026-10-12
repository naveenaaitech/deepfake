import cv2


def extract_frames(video_path, max_frames=20):
    """
    Extract up to max_frames evenly spaced frames
    from a video.
    """
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise ValueError("Unable to open the uploaded video.")

    try:
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        if total_frames <= 0:
            raise ValueError("Video contains no readable frames.")

        frame_count = min(total_frames, max_frames)
        frames = []

        for i in range(frame_count):
            frame_index = int(
                i * total_frames / frame_count
            )

            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
            success, frame = cap.read()

            if success and frame is not None:
                frames.append(frame)

        if not frames:
            raise ValueError("Could not extract video frames.")

        return frames

    finally:
        cap.release()