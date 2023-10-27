"""
main.py
25. October 2023

<description>

Author:
Nilusink
"""
# import the necessary packages
from imutils.object_detection import non_max_suppression
from tools import Track, Box, Vec2
from time import time
import numpy as np
import imutils
import cv2

# initialize the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

cv2.startWindowThread()

# open webcam video stream
cap = cv2.VideoCapture(0)

# the output will be written to output.avi
out = cv2.VideoWriter(
    'output.avi',
    cv2.VideoWriter_fourcc(*'MJPG'),
    15.,
    (640, 480))


TRACKS: list[Track] = []


start = time()
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # resizing for faster detection
    # frame = cv2.resize(frame, (640, 480))
    # using a greyscale picture, also for faster detection
    image = frame
    image = imutils.resize(image, width=min(500, image.shape[1]))
    orig = image.copy()
    # detect people in the image
    (rects, weights) = hog.detectMultiScale(image, winStride=(4, 4),
                                            padding=(8, 8), scale=1.05)
    # draw the original bounding boxes
    for (x, y, w, h) in rects:
        cv2.rectangle(orig, (x, y), (x + w, y + h), (0, 0, 255), 2)
    # apply non-maxima suppression to the bounding boxes using a
    # fairly large overlap threshold to try to maintain overlapping
    # boxes that are still people
    rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
    pick = list(non_max_suppression(rects, probs=None, overlapThresh=0.65))

    if time() - start > 2:
        for track in TRACKS:
            for p in pick.copy():
                b = Box(
                    position=Vec2(p[0], p[1]),
                    size=Vec2(p[2], p[3])
                )

                if track.in_range(b):
                    print(f"updating: {track} ({b})")
                    track.update_track(b)
                    pick.remove(p)

                else:
                    track.update_track()

        for p in pick:
            TRACKS.append(Track(Box(
                position=Vec2(p[0], p[1]),
                size=Vec2(p[2], p[3])
            )))

            print(f"new track: {TRACKS[-1]}")

        # draw bounding boxes
        for track in TRACKS.copy():
            for i in range(len(track.position_history) - 1):
                cv2.line(
                    image,
                    (int(track.position_history[i].x), int(track.position_history[i].y)),
                    (int(track.position_history[i+1].x), int(track.position_history[i+1].y)),
                    (0, 0, 255 * (10 - min(len(track.position_history) - i, 10))),
                    3
                )

            # print(track)
            match track.track_type:
                case -1:
                    TRACKS.remove(track)
                    continue

                case 0:
                    cv2.rectangle(
                        image,
                        track.last_box.position.xy,
                        track.last_box.size.xy,
                        (255, 0, 0),
                        2
                    )

                case 1:
                    cv2.rectangle(
                        image,
                        track.last_box.position.xy,
                        track.last_box.size.xy,
                        (0, 255, 0),
                        2
                    )

    # show some information on the number of bounding boxes
    # show the output images
    cv2.imshow("Before NMS", orig)
    cv2.imshow("After NMS", image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
# and release the output
out.release()
# finally, close the window
cv2.destroyAllWindows()
cv2.waitKey(1)
