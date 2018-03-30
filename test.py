import tensorflow as tf
import numpy as np
import model
import cv2

class tfPredictor():
    def __init__(self):
        self.predictor = tf.estimator.Estimator(
            model_fn=model.model, model_dir="./Model/")

    def image_process(self, imagefile):
        np_array = np.fromstring(imagefile, np.uint8)
        print(np_array)
        np_image = cv2.imdecode(np_array, cv2.IMREAD_GRAYSCALE)
        return cv2.resize(np_image, (28, 28))

    def eval_result(self, image):
        eval_data = np.reshape(self.image_process(image),[1,28,28,1]).astype(np.float32)
        #eval_data = np.zeros([1,28,28,1], dtype=np.float32)
        predict_input_fn = tf.estimator.inputs.numpy_input_fn(
             x={"x": eval_data},
             num_epochs=1,
             shuffle=False)
        eval_results = list(self.predictor.predict(input_fn=predict_input_fn))
        return eval_results

test_file = open("test.jpg",'rb')

p = tfPredictor()

print(p.eval_result(test_file.read()))
