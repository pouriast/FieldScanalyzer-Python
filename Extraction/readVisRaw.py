
import cv2
import numpy as np
import math


def readVisRaw(imageFile, RGBcol, RGBrow):

    #=== reading raw image from visible sensor
    A = np.fromfile(imageFile, dtype='uint8', count=-1, sep="")
    A = A.reshape([RGBcol, RGBrow])
    # img = cv2.cvtColor(A, cv2.COLOR_BAYER_GR2BGR)
    img = cv2.cvtColor(A, cv2.COLOR_BAYER_GR2RGB)

    # cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    # cv2.imshow('image', img)

    # === Rotate the image 90 degree ===
    rangle = np.deg2rad(-90)  # angle in radians
    h = RGBcol
    w = RGBrow
    # === now calculate new image width and height ===
    nw = (abs(np.sin(rangle) * h) + abs(np.cos(rangle) * w)) * 1.0
    nh = (abs(np.cos(rangle) * h) + abs(np.sin(rangle) * w)) * 1.0
    # === ask OpenCV for the rotation matrix ===
    rot_mat = cv2.getRotationMatrix2D((nw * 0.5, nh * 0.5), -90, 1.0)
    # === calculate the move from the old center to the new center combined with the rotation ===
    rot_move = np.dot(rot_mat, np.array([(nw - w) * 0.5, (nh - h) * 0.5, 0]))
    # === the move only affects the translation, so update the translation part of the transform ===
    rot_mat[0, 2] += rot_move[0]
    rot_mat[1, 2] += rot_move[1]
    image_rot = cv2.warpAffine(img, rot_mat, (int(math.ceil(nw)), int(math.ceil(nh))), flags=cv2.INTER_LANCZOS4)

    return image_rot