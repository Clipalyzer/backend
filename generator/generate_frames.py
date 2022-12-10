import cv2


def generate_frames(file, _count, limit):
    vidcap = cv2.VideoCapture(file)
    count = _count
    vidcap.set(cv2.CAP_PROP_POS_MSEC, (count * 1000))
    success, image = vidcap.read()
    while success:
        vidcap.set(cv2.CAP_PROP_POS_MSEC, (count * 1000))
        cv2.imwrite("images\\frame%d.jpg" % count, image)  # save frame as JPEG file
        success, image = vidcap.read()
        print("Read frame on second {}: {}".format(count, success))
        count += 1
        if count >= limit:
            return
