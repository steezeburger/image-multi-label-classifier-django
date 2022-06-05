import os
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow.keras.layers import BatchNormalization, Conv2D, Dense, Dropout, Flatten, MaxPooling2D
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing import image
from tqdm import tqdm

IMAGE_DIR_PATH = '../django-app/app/media/images'
TRAINING_DATA_FILE_PATH = '../django-app/app/media/training_data/images_w_labels.csv'

IMAGE_SIZE = 200


def train_model():
    # read metadata to get our Y values (multiple labels)
    df = pd.read_csv(TRAINING_DATA_FILE_PATH)
    print(df.head())  # printing first five rows of the file
    print(df.columns)

    x_dataset = list()

    for i in tqdm(range(df.shape[0])):
        image_uri = f"{IMAGE_DIR_PATH}/{df['filename'][i]}"
        img = image.load_img(image_uri,
                             target_size=(IMAGE_SIZE, IMAGE_SIZE, 3))
        img = image.img_to_array(img)
        img = img / 255.
        x_dataset.append(img)

    x = np.array(x_dataset)

    # No need to convert to categorical as the dataset is already in the right format.
    y = np.array(df.drop(['filename'], axis=1))

    x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=20, test_size=0.3)

    model = Sequential()

    model.add(Conv2D(filters=16, kernel_size=(5, 5), activation="relu", input_shape=(IMAGE_SIZE, IMAGE_SIZE, 3)))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.2))

    model.add(Conv2D(filters=32, kernel_size=(5, 5), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(BatchNormalization())
    model.add(Dropout(0.2))

    model.add(Conv2D(filters=64, kernel_size=(5, 5), activation="relu"))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(BatchNormalization())
    model.add(Dropout(0.2))

    model.add(Conv2D(filters=64, kernel_size=(5, 5), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(BatchNormalization())
    model.add(Dropout(0.2))

    model.add(Flatten())
    model.add(Dense(256, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.5))
    # FIXME - figure out why this number has to be the same as number of labels
    #  and if the above values make any sense
    num_labels = df.shape[1] - 1
    model.add(Dense(num_labels, activation='sigmoid'))

    # Do not use softmax for multilabel classification
    # Softmax is useful for mutually exclusive classes, either cat or dog but not both.
    # Also, softmax outputs all add to 1. So good for multi class problems where each
    # class is given a probability and all add to 1. Highest one wins.

    # Sigmoid outputs probability. Can be used for non-mutually exclusive problems.
    # like multi label, in this example.
    # But, also good for binary mutually exclusive (cat or not cat).

    model.summary()

    # Binary cross entropy of each label. So no really a binary classification problem but
    # Calculating binary cross entropy for each label.
    model.compile(optimizer='adam',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])

    history = model.fit(x_train,
                        y_train,
                        epochs=10,
                        validation_data=(x_test, y_test),
                        batch_size=64)

    # plot the training and validation accuracy and loss at each epoch
    loss = history.history['loss']
    val_loss = history.history['val_loss']
    epochs = range(1, len(loss) + 1)
    plt.plot(epochs, loss, 'y', label='Training loss')
    plt.plot(epochs, val_loss, 'r', label='Validation loss')
    plt.title('Training and validation loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()
    plt.show()

    # acc = history.history['acc']
    # val_acc = history.history['val_acc']
    # plt.plot(epochs, acc, 'y', label='Training acc')
    # plt.plot(epochs, val_acc, 'r', label='Validation acc')
    # plt.title('Training and validation accuracy')
    # plt.xlabel('Epochs')
    # plt.ylabel('Accuracy')
    # plt.legend()
    # plt.show()

    _, acc = model.evaluate(x_test, y_test)
    print("Accuracy = ", (acc * 100.0), "%")

    #################################################
    # Validate on an image
    # img = image.load_img('movie_dataset_multilabel/images/tt4425064.jpg', target_size=(SIZE,SIZE,3))
    img = image.load_img('cgi.jpg', target_size=(IMAGE_SIZE, IMAGE_SIZE, 3))

    img = image.img_to_array(img)
    img = img / 255.
    plt.imshow(img)
    img = np.expand_dims(img, axis=0)

    classes = np.array(df.columns[2:])  # Get array of all classes
    proba = model.predict(img)  # Get probabilities for each class
    sorted_categories = np.argsort(proba[0])[:-11:-1]  # Get class names for top 10 categories

    # Print classes and corresponding probabilities
    for i in range(10):
        print("{}".format(classes[sorted_categories[i]]) + " ({:.3})".format(proba[0][sorted_categories[i]]))

    ###################################################


if __name__ == '__main__':
    # ensure the working directory is the same as the script directory
    # so that our paths are sure to work
    script_dir = Path(__file__).parent.absolute()
    os.chdir(script_dir)

    train_model()
