@echo off
set KMP_DUPLICATE_LIB_OK=TRUE
python yolov5/train.py --batch 16 --epochs 500 --data "%cd%\data.yaml" --weights yolov5s.pt --batch-size 1 --cache