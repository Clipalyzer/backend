from generate_file_system import generate_file_system
from generate_testing_images import generate_testing_images
from grab_detailed_images_from_video import grab_detailed_images_from_video
from grab_images_from_video import grab_images_from_video
from create_configs import create_configs
import pytesseract
import sys

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
video_path = "G:\Videos\Valorant"

if len(sys.argv) <= 1:
    print("Error! Start with \"python {} s1\" or \"python {} s2\"".format(sys.argv[0],sys.argv[0]))
    print("> Use \"python {} s1\" to generate categorizable images from your clips.".format(sys.argv[0]))
    print("  Videos must be inside {}".format(video_path))
    print("> Use \"python {} s2\" create learning enviroment after categorizing your clips from hand!".format(sys.argv[0]))
    sys.argv.append("")
    sys.exit()

if sys.argv[1] == "s1":
    # Step #1
    generate_file_system()
    grab_images_from_video(video_path)
    print("You may now filter your images by hand. Move them from data/all_images to obj/all_images/{map}")

if sys.argv[1] == "s2":
    # Step #2
    number_of_learn_images_per_thread = 800
    grab_detailed_images_from_video(number_of_learn_images_per_thread)

    number_of_testing_images = 300
    generate_testing_images(number_of_testing_images)

    create_configs()
