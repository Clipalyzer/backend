from .read_dir import read_dir
from .cleanup_classes import cleanup_classes
import os
import math
import json
import cv2
from .frame_positions import sub_list_from_frame_position
import numpy as np
from threading import Thread

def grab_detailed_images_from_video(number_of_learn_images_per_thread):

    number_of_classes = cleanup_classes()
    number_of_threads = os.cpu_count()
    number_of_threads_per_class = math.floor(number_of_threads/number_of_classes)
    number_of_total_images = number_of_threads_per_class * number_of_learn_images_per_thread * number_of_classes

    # Videos von den einzelnen Klassen/number_of_threads_per_class

    threads = []

    video_cache = {}
    with open("data\\all_images.json", 'r') as file:
        video_cache = json.loads(file.read().replace('\n', ''))

    # print(video_cache)
    dir = read_dir("data\\all_images\\")
    for classId in dir:
        dir_name = "data\\all_images\\{}".format(classId)
        subdir = read_dir(dir_name)
        number_of_images = math.ceil(len(subdir)/number_of_threads_per_class)
        i = 0
        while i < number_of_threads_per_class:
            thread_images = subdir[number_of_images*i:number_of_images*i + number_of_images]
            thread_videos = []
            for image in thread_images:
                thread_videos.append(video_cache[image])
            threads.append({
                "videos": thread_videos,
                "classId": classId,
                "images_per_video": math.ceil(number_of_learn_images_per_thread / len(thread_videos)),
                "thread": None,
                "images_per_thread": number_of_learn_images_per_thread
            })
            i = i+1

    def grab_detailed_images_from_video_thread(threadId):
        videoId = 0
        print("[{}] Wanted images/video: {}".format(threadId,threads[threadId]["images_per_video"]))
        while videoId < len(threads[threadId]["videos"]):
            print("[{}] videoId: {}".format(threadId,videoId))
            frameOffset = 0
            video = threads[threadId]["videos"][videoId]
            vidcap = cv2.VideoCapture(video)
            frame_count = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
            success,image = vidcap.read()
            found_maps = 0
            while success:
                cropped_image = sub_list_from_frame_position(image,"map")

                number_of_gray_pix = np.sum(cropped_image==126)
                if number_of_gray_pix > 10_000:
                    current_id = ((threads[threadId]["images_per_thread"]*(threadId) + threads[threadId]["images_per_video"]*(videoId))+frameOffset)
                    cv2.imwrite("data\\obj\\{}\\{}.png".format(threads[threadId]["classId"],current_id), cropped_image)
                    found_maps = found_maps + 1

                frameOffset = frameOffset + 1
                vidcap.set(cv2.CAP_PROP_POS_FRAMES,(frame_count/threads[threadId]["images_per_video"]*frameOffset))
                success,image = vidcap.read()
            # print("Found images/video: {} - Need: {}".format(found_maps,threads[threadId]["images_per_video"]-found_maps))

            frameOffset = frameOffset - 1

            vidcap.set(cv2.CAP_PROP_POS_FRAMES,((frame_count/2)/threads[threadId]["images_per_video"]*1))
            success,image = vidcap.read()
            while success:
                cropped_image = sub_list_from_frame_position(image,"map")

                number_of_gray_pix = np.sum(cropped_image==126)
                if number_of_gray_pix > 10_000:
                    current_id = ((threads[threadId]["images_per_video"]*(threadId)*(videoId))+frameOffset)
                    cv2.imwrite("data\\obj\\{}\\{}.png".format(threads[threadId]["classId"],current_id), cropped_image)
                    found_maps = found_maps + 1

                frameOffset = frameOffset + 1
                vidcap.set(cv2.CAP_PROP_POS_FRAMES,((frame_count/2)/threads[threadId]["images_per_video"]*(frameOffset - found_maps)))
                success,image = vidcap.read()
                if found_maps >= threads[threadId]["images_per_video"]:
                    success = False
            videoId = videoId + 1
        print("[{}] done".format(threadId))

    threadId = 0
    while threadId < number_of_threads:
        # threads[threadId]["thread"] = grab_detailed_images_from_video_thread
        t = Thread(target=grab_detailed_images_from_video_thread, args=[threadId])
        t.start()
        threads[threadId]["thread"] = t
        threadId = threadId + 1
