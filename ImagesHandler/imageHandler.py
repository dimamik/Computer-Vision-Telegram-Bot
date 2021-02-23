import os

from imageai.Detection import ObjectDetection

execution_path = os.getcwd()

detector = ObjectDetection()
detector.setModelTypeAsRetinaNet()
detector.setModelPath(os.path.join(execution_path, "../resnet/resnet50_coco_best_v2.1.0.h5"))
detector.loadModel()


def detect_objects_from_image(input_path, output_path):
    detector.detectObjectsFromImage(input_image=input_path,
                                    output_image_path=output_path)
