import time
from threading import Lock, Thread
from typing import Optional

import cv2
import numpy as np
import supervision as sv
import yaml
from ultralytics import YOLO


def get_coco_class(yaml_file):
    with open(yaml_file, "r") as file:
        data = yaml.safe_load(file)
    return data["names"]


class Vision:
    def __init__(self, camera_id: int = 0):
        self.camera_id = camera_id
        self.current_img = None
        self.read_lock = Lock()
        self.keep_running = True
        fps = 25
        self.last_image_response = time.time()
        self.duration_between_frames = 1 / fps
        self.frame_counter = 0
        self.detector = YOLO(model="yolov8n.pt", task="detect")
        class_maps = get_coco_class(yaml_file="data/data.yaml")
        self.class_names = [class_name for key, class_name in class_maps.items()]

    def start_capturing(self) -> None:
        self.loop = Thread(target=self._loop, args=(self.camera_id,), daemon=True)
        self.loop.start()

    def stop_capturing(self) -> None:
        self.keep_running = False

    def check_camera(self) -> bool:
        return self.keep_running

    def read(self, encode=False) -> Optional[np.ndarray]:
        with self.read_lock:
            if self.current_img is not None:
                img = self.current_img.copy()
                yolo_result = self.detector([img], imgsz=224, verbose=False)[0]
                detections = sv.Detections.from_yolov8(yolo_result)
                labels = [
                    f"{self.class_names[class_id]}" for class_id in detections.class_id
                ]
                img = sv.BoxAnnotator().annotate(
                    scene=img, detections=detections, labels=labels
                )

                if encode:
                    ret, encodedImage = cv2.imencode(".jpeg", img)
                    return encodedImage
                return img
            else:
                return None

    def _loop(self, camera_id):
        cap = cv2.VideoCapture(camera_id)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        try:
            while self.keep_running:
                success, image = cap.read()

                if not success:
                    self.keep_running = False
                else:
                    time_to_wait = (
                        self.last_image_response
                        + self.duration_between_frames
                        - time.time()
                    )
                    if time_to_wait > 0:
                        time.sleep(time_to_wait)
                    self.last_image_response = time.time()
                    self.current_img = image.copy()
                    self.frame_counter += 1

                if self.frame_counter == total_frames:
                    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    self.frame_counter = 0

            cap.release()
        except:
            print("Problem with camera")
