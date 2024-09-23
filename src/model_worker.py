import os
import cv2
from PIL import Image
import numpy as np

import tensorflow as tf
print(tf.__version__)
from tensorflow.keras import layers

from alibi_detect.od import OutlierVAE
# from alibi_detect.utils.visualize import plot_instance_score, plot_feature_outlier_image
from alibi_detect.utils.saving import save_detector, load_detector

class Model:
    def __init__(self):
        pass

    def define_encoder(self):
        self.encoding_dim = 1024  #Dimension of the bottleneck encoder vector.
        #Define encoder
        self.encoder_net = tf.keras.Sequential(
        [
            layers.InputLayer(input_shape=(64, 64, 3)),
            layers.Conv2D(64, 4, strides=2, padding='same', activation=tf.nn.relu),
            layers.Conv2D(128, 4, strides=2, padding='same', activation=tf.nn.relu),
            layers.Conv2D(512, 4, strides=2, padding='same', activation=tf.nn.relu),
            layers.Flatten(),
            layers.Dense(self.encoding_dim,)
        ])
        print(self.encoder_net.summary())

    def define_decoder(self):
        self.dense_dim = [8, 8, 512] #Dimension of the last conv. output. This is used to work our way back in the decoder. 
        self.decoder_net = tf.keras.Sequential(
        [
            layers.InputLayer(input_shape=(self.encoding_dim,)),
            layers.Dense(np.prod(self.dense_dim)),
            layers.Reshape(target_shape=self.dense_dim),
            layers.Conv2DTranspose(256, 4, strides=2, padding='same', activation=tf.nn.relu),
            layers.Conv2DTranspose(64, 4, strides=2, padding='same', activation=tf.nn.relu),
            layers.Conv2DTranspose(3, 4, strides=2, padding='same', activation='sigmoid')
        ])

        print(self.decoder_net.summary())

    def define_outlier_detector(self):
        self.latent_dim = 1024  #(Same as encoding dim. )
        # initialize outlier detector
        self.od = OutlierVAE(threshold=.015,  # threshold for outlier score above which the element is flagged as an outlier.
                        score_type='mse',  # use MSE of reconstruction error for outlier detection
                        encoder_net=self.encoder_net,  # can also pass VAE model instead
                        decoder_net=self.decoder_net,  # of separate encoder and decoder
                        latent_dim=self.latent_dim,
                        samples=4)

        print("Current threshold value is: ", self.od.threshold)



class FlawDetectorTrain:
    def __init__(self, model, detector_id:int):
        # размер обрабатываемого изображения
        self.size = 64

        # храним датасет для обучения
        self.dataset = []
        self.fill_good_images_from_directory(f"./detector/{detector_id}/train/good/")

        self.detector_id = detector_id

        # делим датасет на обучающие итестовые выборки
        self.train = self.dataset[0:int(len(self.dataset))-1]
        self.test = self.dataset[int(len(self.dataset)*0.8):len(self.dataset)-1]

        # нормируем данные для дальнейшего обучения
        self.train = self.train.astype('float32') / 255.
        self.test = self.test.astype('float32') / 255.

        self.myModel = model
        self.myModel.define_encoder()
        self.myModel.define_decoder()
        self.myModel.define_outlier_detector()
        print("Конструктор FlawDetectorTrain завершил свою работу")

    def fill_good_images_from_directory(self, directory_name):
        good_images = os.listdir(directory_name)
        for i, image_name in enumerate(good_images):
            if (image_name.split('.')[-1] == 'png' or image_name.split('.')[-1] == 'jpg'):
                image = cv2.imread(directory_name + image_name)
                image = Image.fromarray(image, 'RGB')
                image = image.resize((self.size, self.size))
                self.dataset.append(np.array(image))

        self.dataset = np.array(self.dataset)

    def clear_datasets(self):
        self.dataset.clear()

    def train_model(self):
        print("training started")
        adam = tf.keras.optimizers.Adam(learning_rate=0.001)

        self.myModel.od.fit(self.train,
            optimizer=adam,
            epochs=15,
            batch_size=4,
            verbose=True)
        
        print("Current threshold value is: ", self.myModel.od.threshold)

        self.myModel.od.infer_threshold(self.test, outlier_type='instance', threshold_perc=99.0)
        print("Current threshold value is: ", self.myModel.od.threshold)

        save_detector(detector=self.myModel.od, filepath=f"./detector/{self.detector_id}/weights/")
        

class FlawDetectorPredict:
    def __init__(self, model, detector_id:int):
        # размер обрабатываемого изображения
        self.size = 64

        # храним датасет для проверки на нахождение отклонения
        self.bad_dataset=[]
        self.fill_bad_images_from_directory(f"./detector/{detector_id}/train/bad/")

        self.detector_id = detector_id

        # нормируем данные для дальнейшей проверки модели после обучения
        self.bad_dataset = self.bad_dataset.astype('float32') / 255.

        self.myModel = model
        self.myModel.define_encoder()
        self.myModel.define_decoder()
        self.myModel.define_outlier_detector()

        self.myModel.od = load_detector(f"./detector/{detector_id}/weights/", compile=False)

    def fill_bad_images_from_directory(self, directory_name):
        bad_images = os.listdir(directory_name)
        for i, image_name in enumerate(bad_images):
            if (image_name.split('.')[-1] == 'png' or image_name.split('.')[-1] == 'jpg'):
                image = cv2.imread(directory_name + image_name)
                image = Image.fromarray(image, 'RGB')
                image = image.resize((self.size, self.size))
                self.bad_dataset.append(np.array(image))

        self.bad_dataset = np.array(self.bad_dataset)

    def clear_datasets(self):
        self.bad_dataset.clear()

    def predict_model(self, index:int, threshold:float):
        self.myModel.od.threshold = threshold
        test_bad_image = self.bad_dataset[index].reshape(1, 64, 64, 3)


        test_bad_image_recon = self.myModel.od.vae(test_bad_image)
        test_bad_image_recon = test_bad_image_recon.numpy()

        test_bad_image_predict = self.myModel.od.predict(test_bad_image)
        bad_image_instance_score = test_bad_image_predict['data']['instance_score'][0]
        print("The instance score is:", bad_image_instance_score)
        print("Is this image an outlier (0 for NO and 1 for YES)?", test_bad_image_predict['data']['is_outlier'][0])
        return test_bad_image_predict['data']['is_outlier'][0]

    def predict_model_frame(self, my_frame:cv2.Mat, threshold:float):
        self.myModel.od.threshold = threshold
        # test_bad_image = self.bad_dataset[index].reshape(1, 64, 64, 3)
        image = Image.fromarray(my_frame, 'RGB')
        image = image.resize((self.size, self.size))
        image = np.array(image)
        image = image.astype('float32') / 255.
        image = image.reshape(1, 64, 64, 3)

        test_bad_image_predict = self.myModel.od.predict(image)
        bad_image_instance_score = test_bad_image_predict['data']['instance_score'][0]
        # print("The instance score is:", bad_image_instance_score)
        # print("Is this image an outlier (0 for NO and 1 for YES)?", test_bad_image_predict['data']['is_outlier'][0])
        return bad_image_instance_score