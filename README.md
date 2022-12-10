# Valorant Clipalyzer (Clip Analyzer)

The Valorant Clipalyzer will scan your `video_path` directory defined in [main.py](main.py) and create a deep learning environment for yolov5.

## Prerequisites

- Having git installed.
- Install [Tesseract](https://github.com/tesseract-ocr/tesseract)

## Usage

```
git clone --recurse-submodules https://github.com/ReDiGermany/clipalyzer.git
cd clipalyzer
pip install -r requirements.txt
cd yolov5
pip install -r requirements.txt
cd ..
```

- `git clone --recurse-submodules https://github.com/ReDiGermany/clipalyzer.git` to clone this repository to your current folder
- `pip install -r requirements.txt` to install needed dependencies
- `python main.py s1` to generate images to categorize
- `python main.py s2` to generate deep learning images by your own categorization
- `python yolov5/train.py --batch 16 --epochs 500 --data "%cd%\data.yaml" --weights yolov5s.pt --batch-size 1 --cache` to start learning (or use the [learn.bat](learn.bat))
