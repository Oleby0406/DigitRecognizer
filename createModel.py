from keras.datasets import mnist
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import Dropout
from keras.layers import MaxPooling2D
from keras.layers import Dense
from keras.layers import Flatten
from keras.optimizers import Adam
from keras.optimizers.schedules import ExponentialDecay
from keras import callbacks

def load_dataset():
	(trainX, trainY), (valX, valY) = mnist.load_data()
	trainX = trainX.reshape((trainX.shape[0], 28, 28, 1))
	valX = valX.reshape((valX.shape[0], 28, 28, 1))
	trainY = to_categorical(trainY)
	valY = to_categorical(valY)
	return trainX, trainY, valX, valY

def prep_pixels(train, test):
	train_norm = train.astype('float32')
	test_norm = test.astype('float32')
	train_norm = train_norm / 255.0
	test_norm = test_norm / 255.0
	return train_norm, test_norm

def define_model():
	lr_schedule = ExponentialDecay(
    initial_learning_rate=0.0001,
    decay_steps=10000,
    decay_rate=0.96,
    staircase=True)

	model = Sequential()
	model.add(Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_uniform', input_shape=(28, 28, 1)))
	model.add(MaxPooling2D((2, 2)))

	model.add(Conv2D(64, (3, 3), activation='relu', kernel_initializer='he_uniform'))
	model.add(Conv2D(64, (3, 3), activation='relu', kernel_initializer='he_uniform'))
	model.add(MaxPooling2D((2, 2)))

	model.add(Flatten())
	model.add(Dense(128, activation='relu', kernel_initializer='he_uniform'))
	model.add(Dropout(0.5))
	model.add(Dense(10, activation='softmax'))

	opt = Adam(learning_rate = lr_schedule)
	model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])

	return model

def run_test_harness():
	trainX, trainY, valX, valY = load_dataset()
	trainX, valX = prep_pixels(trainX, valX)
	model = define_model()

	earlystopping = callbacks.EarlyStopping(monitor = "val_loss",
                                        patience = 3,
                                        mode = 'min',
                                        restore_best_weights = True,
                                        start_from_epoch = 3)
	
	model.fit(trainX, trainY, epochs=20, validation_data = [valX, valY], callbacks = [earlystopping], verbose=1)
	model.save('final_model')

run_test_harness()