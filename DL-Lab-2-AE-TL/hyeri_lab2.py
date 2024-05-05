# -*- coding: utf-8 -*-
"""hyeri_lab2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1u7D82PuaO_FdmBOIDeuNyYL8mUxqx2bt
"""

# Import necessary libraries

import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from keras.utils import plot_model
from sklearn.metrics import confusion_matrix
import seaborn as sns

"""### a. Get the Data:

1. Import and Load the dataset
"""

# Load the Fashion MNIST dataset
(x_train, y_train), (x_test, y_test) = keras.datasets.fashion_mnist.load_data()

# Check the shape of dataset
print(x_train.shape)

# Dictionaries to store the fashion_mnist datasets
unsupervised_hyeri = {}
supervised_hyeri = {}

# Split data into unsupervised and supervised sets
unsupervised_hyeri['images'] = x_train[:60000]
supervised_hyeri['images'] = x_test[:10000]
supervised_hyeri['labels'] = y_test[:10000]

# Check the lengths of the unsupervised and supervised sets
print(f"The length of unsupervised sets: {len(unsupervised_hyeri['images'])}")
print(f"The length of supervised sets: {len(supervised_hyeri['images'])}")

"""### b. Data Pre-processing:

1. Normalization:
"""

# Normalize pixel values to 0-1 range
unsupervised_hyeri['images'] = unsupervised_hyeri['images'] / 255.0
supervised_hyeri['images'] = supervised_hyeri['images'] / 255.0

"""2. One-hot Encoding:"""

# Convert labels to one-hot encoded format
supervised_hyeri['labels'] = tf.keras.utils.to_categorical(supervised_hyeri['labels'], num_classes=10)

# Print out the shape of each dataset
print("The shape of the datasets\n")
print("unsupervised_images:", unsupervised_hyeri['images'].shape)
print("supervised_images:", supervised_hyeri['images'].shape)
print("supervised_labels:", supervised_hyeri['labels'].shape)

"""### c. Data Preparation (Training, Validation, Testing):

1. Split the Unsupervised Dataset:
"""

# Random seed based on last two digits of student ID
random_seed = 60

# Split unsupervised data into training and validation sets
X_train_unsupervised, X_val_unsupervised = train_test_split(unsupervised_hyeri['images'],
                                                            test_size=0.05,
                                                            random_state=random_seed)

# Use astype function to keep the original shape of dataset
X_train_unsupervised_reshaped = X_train_unsupervised.astype(np.float32).reshape(-1, 28 * 28)
X_val_unsupervised_reshaped = X_val_unsupervised.astype(np.float32).reshape(-1, 28 * 28)

# Store in DataFrames
unsupervised_train_hyeri = pd.DataFrame(X_train_unsupervised_reshaped)
unsupervised_val_hyeri = pd.DataFrame(X_val_unsupervised_reshaped)

print("Original dataset for unsupervised: ", X_train_unsupervised.shape)
print("Reshaped dataset for unsupervised: ", X_train_unsupervised_reshaped.shape)

"""Supervised Random Discard:"""

# Discard 7,000 random samples from supervised data
supervised_hyeri['images'], _, supervised_hyeri['labels'], _ = train_test_split(supervised_hyeri['images'],
                                                                                supervised_hyeri['labels'],
                                                                                test_size=0.7,
                                                                                shuffle=True,
                                                                                random_state=random_seed)

"""Supervised Split:"""

# Split remaining supervised data into training, validation, and testing sets
X_train_hyeri, X_test_hyeri, y_train_hyeri, y_test_hyeri = train_test_split(supervised_hyeri['images'], supervised_hyeri['labels'], test_size=0.2, random_state=random_seed)
X_train_hyeri, X_val_hyeri, y_train_hyeri, y_val_hyeri = train_test_split(X_train_hyeri, y_train_hyeri, test_size = 0.25, random_state=random_seed)

# Print out the shapes
print("unsupervised_train:", unsupervised_train_hyeri.shape)
print("unsupervised_val:", unsupervised_val_hyeri.shape)
print("x_train:", X_train_hyeri.shape)
print("x_val:", X_val_hyeri.shape)
print("x_test:", X_test_hyeri.shape)
print("y_train:", y_train_hyeri.shape)
print("y_val:", y_val_hyeri.shape)
print("y_test:", y_test_hyeri.shape)

"""### d. Build, Train, and Validate a Baseline CNN Model:

Building the Model:
"""

# Set model name and image size
image_size = (28, 28, 1)  # Assuming grayscale images

# Create the model architecture
cnn_v1_model_hyeri = tf.keras.Sequential([
    layers.Conv2D(16, (3, 3), activation='relu', padding='same', strides=2, input_shape=image_size),
    layers.Conv2D(8, (3, 3), activation='relu', padding='same', strides=2),
    layers.Flatten(),
    layers.Dense(100, activation='relu'),
    layers.Dense(10, activation='softmax')
])

"""Compiling the Model:"""

# Compile the model
cnn_v1_model_hyeri.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

"""Model Summary and Diagram:"""

# Print model summary
cnn_v1_model_hyeri.summary()

# Draw the diagram for the summary
plot_model(cnn_v1_model_hyeri, show_shapes=True, show_layer_names=True)

"""Training and Validation:"""

# Train and validate the model
cnn_v1_history_hyeri = cnn_v1_model_hyeri.fit(X_train_hyeri,
                                              y_train_hyeri,
                                              epochs=10,
                                              batch_size=256,
                                              validation_data=(X_val_hyeri, y_val_hyeri))

"""### e. Test and Analyze the Baseline Model:

Plot Training vs. Validation Accuracy:
"""

# Plot accuracy
plt.plot(cnn_v1_history_hyeri.history['accuracy'], label='Training Accuracy')
plt.plot(cnn_v1_history_hyeri.history['val_accuracy'], label='Validation Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.title('Training vs. Validation Accuracy')
plt.legend()
plt.show()

"""Evaluate on Test Set:"""

# Evaluate on test set
test_loss, test_acc = cnn_v1_model_hyeri.evaluate(X_test_hyeri, y_test_hyeri, verbose=2)
print('\nTest accuracy:', test_acc)

"""Create Predictions:"""

# Create predictions
cnn_predictions_hyeri = cnn_v1_model_hyeri.predict(X_test_hyeri)

"""Plot Confusion Matrix:"""

# Create confusion matrix
cm_v1 = confusion_matrix(y_test_hyeri.argmax(axis=1), cnn_predictions_hyeri.argmax(axis=1))

# Plot using seaborn
sns.heatmap(cm_v1, annot=True, fmt='d')
plt.xlabel('Predicted')
plt.ylabel('True')
plt.title('CNN Confusion Matrix')
plt.show()

"""### f. Add random noise to unsupervised dataset:"""

# Define noise factor and random seed
noise_factor = 0.2
random_seed = 60

# Add noise to training and validation data
x_train_noisy_hyeri = X_train_unsupervised + tf.random.normal(shape=X_train_unsupervised.shape, mean=0.0, stddev=noise_factor, seed=random_seed)
x_val_noisy_hyeri = X_val_unsupervised + tf.random.normal(shape=X_val_unsupervised.shape, mean=0.0, stddev=noise_factor, seed=random_seed)

# Clip values to range 0-1
x_train_noisy_hyeri = tf.clip_by_value(x_train_noisy_hyeri, clip_value_min=0.0, clip_value_max=1.0)
x_val_noisy_hyeri = tf.clip_by_value(x_val_noisy_hyeri, clip_value_min=0.0, clip_value_max=1.0)

# Plot first 10 images from noisy validation set
plt.figure(figsize=(10, 5))
for i in range(10):
    plt.subplot(2, 5, i + 1)
    plt.imshow(x_val_noisy_hyeri[i], cmap='gray')
    plt.axis('off')
plt.show()

"""### g. Build and pretrain Autoencoder:"""

# Define input layer based on image size
inputs_hyeri = layers.Input(shape=(28, 28, 1))

# Encoder section
e_hyeri = []

e_hyeri.append(layers.Conv2D(16, (3, 3), activation='relu', padding='same', strides=2)(inputs_hyeri))
e_hyeri.append(layers.Conv2D(8, (3, 3), activation='relu', padding='same', strides=2)(e_hyeri[0]))


# Decoder section
d_hyeri = []

d_hyeri.append(layers.Conv2DTranspose(8, (3, 3), activation='relu', padding='same', strides=2)(e_hyeri[1]))
d_hyeri.append(layers.Conv2DTranspose(16, (3, 3), activation='relu', padding='same', strides=2)(d_hyeri[0]))
d_hyeri.append(layers.Conv2D(1, (3, 3), activation='sigmoid', padding='same')(d_hyeri[1]))

# Autoencoder model
autoencoder_hyeri = models.Model(inputs=inputs_hyeri, outputs=d_hyeri[-1])

# Compile autoencoder
autoencoder_hyeri.compile(optimizer='adam', loss='mse')

# Print summary
autoencoder_hyeri.summary()

# Draw the diagram for the summary
plot_model(autoencoder_hyeri, show_shapes=True, show_layer_names=True)

# Train autoencoder
autoencoder_history_hyeri = autoencoder_hyeri.fit(x_train_noisy_hyeri,
                                                  X_train_unsupervised,
                                                  epochs=10,
                                                  batch_size=256,
                                                  shuffle=True,
                                                  validation_data=(x_val_noisy_hyeri, X_val_unsupervised))

# Predict on validation set
autoencoder_predictions_hyeri = autoencoder_hyeri.predict(X_val_unsupervised)

# Plot first 10 predicted images
plt.figure(figsize=(10, 5))
for i in range(10):
    plt.subplot(2, 5, i + 1)
    plt.imshow(autoencoder_predictions_hyeri[i][:, :, 0], cmap='gray')  # Remove last dimension for grayscale
    plt.axis('off')
plt.show()

"""### h. Build and perform transfer learning on a CNN with the Autoencoder:

"""

# Extract encoder section from Autoencoder
encoder_section_hyeri = tf.keras.Model(inputs=inputs_hyeri, outputs=d_hyeri[-1])

# Build CNN model for transfer learning
cnn_v2_hyeri = tf.keras.Sequential([
    encoder_section_hyeri,
    layers.Flatten(),
    layers.Dense(100, activation='relu'),
    layers.Dense(10, activation='softmax')
])

# Compile CNN
cnn_v2_hyeri.compile(optimizer='adam',
                     loss='categorical_crossentropy',
                     metrics=['accuracy'])

# Print summary
cnn_v2_hyeri.summary()

# Draw the diagram for the summary
plot_model(cnn_v2_hyeri, show_shapes=True, show_layer_names=True)

# fit the model to our train and val supervised dataset
cnn_v2_history_hyeri = cnn_v2_hyeri.fit(X_train_hyeri,
                                        y_train_hyeri,
                                        epochs=10,
                                        batch_size=256,
                                        validation_data=(X_val_hyeri, y_val_hyeri))

# Plot Training Vs Validation Accuracy for the pretrained CNN model
plt.plot(cnn_v2_history_hyeri.history['accuracy'], label='Training Accuracy')
plt.plot(cnn_v2_history_hyeri.history['val_accuracy'], label='Validation Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.title('Training Vs Validation Accuracy of Pretrained CNN Model')
plt.legend()
plt.show()

# Evaluate the pretrained CNN model on test dataset
test_loss_pretrained, test_accuracy_pretrained = cnn_v2_hyeri.evaluate(X_test_hyeri, y_test_hyeri)
print(f"Test Accuracy (Pretrained Model): {test_accuracy_pretrained}")

# Make predictions on test dataset using pretrained CNN model
cnn_predictions_pretrained_hyeri = cnn_v2_hyeri.predict(X_test_hyeri)

# Confusion matrix for pretrained CNN model
cm_pretrained = confusion_matrix(
    np.argmax(y_test_hyeri, axis=1),
    np.argmax(cnn_predictions_pretrained_hyeri, axis=1))
plt.figure(figsize=(8, 6))
sns.heatmap(cm_pretrained, annot=True, fmt='g', cmap='Blues', xticklabels=range(10), yticklabels=range(10))
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.title('Confusion Matrix - Pretrained CNN Model')
plt.show()

"""### j. Compare the performance of the baseline CNN model to the pretrained model in your report

"""

# Plot Validation Accuracy for Baseline vs Pretrained model
plt.plot(cnn_v1_history_hyeri.history['val_accuracy'], label='Baseline Model')
plt.plot(cnn_v2_history_hyeri.history['val_accuracy'], label='Pretrained Model')
plt.xlabel('Epochs')
plt.ylabel('Validation Accuracy')
plt.title('Validation Accuracy - Baseline vs Pretrained CNN Model')
plt.legend()
plt.show()

# Compare and analyze test accuracy for Baseline vs Pretrained model
print(f"Test Accuracy (Baseline Model): {test_acc}")
print(f"Test Accuracy (Pretrained Model): {test_accuracy_pretrained}")