# -*- coding: utf-8 -*-
"""hyeri_lab4

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1MP1uQ54MZb8nwAUdVZam2y81AR4r0M_t
"""

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Reshape, Conv2D, Conv2DTranspose, BatchNormalization, LeakyReLU, Dropout, Flatten
from tensorflow.keras.losses import BinaryCrossentropy
from tensorflow.keras.optimizers import Adam
from keras.utils import plot_model
import time

"""### a. Get a data"""

# Load the Fashion MNIST dataset
(ds1_hyeri_images, ds1_hyeri_labels), (ds2_hyeri_images, ds2_hyeri_labels) = tf.keras.datasets.fashion_mnist.load_data()

"""### b. Pre-processing"""

# Normalize pixel values to range between -1 and 1
max_pixel_value = max(ds1_hyeri_images.max(), ds2_hyeri_images.max())
scaling_factor = max_pixel_value / 2 # Calculate the scaling factor

ds1_hyeri_images = (ds1_hyeri_images / scaling_factor) - 1.0
ds2_hyeri_images = (ds2_hyeri_images / scaling_factor) - 1.0

# Store the datasets into dictionaries
ds1_hyeri = {'images': ds1_hyeri_images, 'labels': ds1_hyeri_labels}
ds2_hyeri = {'images': ds2_hyeri_images, 'labels': ds2_hyeri_labels}

# Display the shape of the images datasets
print("Shape of ds1_hyeri['images']: ", ds1_hyeri_images.shape)
print("Shape of ds2_hyeri['images']: ", ds2_hyeri_images.shape)

# Concatenate the datasets
dataset_hyeri = np.concatenate((ds1_hyeri_images, ds2_hyeri_images), axis=0)

# Display the shape of the concatenated dataset
print("Shape of dataset_hyeri: ", dataset_hyeri.shape)

# Plot the first 12 images from the dataset
plt.figure(figsize=(8, 8))
for i in range(12):
    plt.subplot(4, 3, i+1)
    plt.imshow(dataset_hyeri[i], cmap='gray')
    plt.axis('off')
plt.show()

# Create TensorFlow Dataset and batch it
train_dataset_hyeri = tf.data.Dataset.from_tensor_slices(dataset_hyeri)
train_dataset_hyeri = train_dataset_hyeri.shuffle(7000).batch(256)

"""### c. Build the Generator Model of the GAN"""

# Define the generator model
generator_model_hyeri = Sequential([
    Dense(7*7*256, use_bias=False, input_shape=(100,)),
    BatchNormalization(),
    LeakyReLU(),
    Reshape((7, 7, 256)),
    Conv2DTranspose(128, (5, 5), strides=(1, 1), padding='same', use_bias=False),
    BatchNormalization(),
    LeakyReLU(),
    Conv2DTranspose(64, (5, 5), strides=(2, 2), padding='same', use_bias=False),
    BatchNormalization(),
    LeakyReLU(),
    Conv2DTranspose(1, (5, 5), strides=(2, 2), padding='same', use_bias=False, activation='tanh')
])

# Display the summary of the generator model
generator_model_hyeri.summary()

# Draw the diagram for the summary
plot_model(generator_model_hyeri, show_shapes=True, show_layer_names=True)

"""### d. Sample untrained generator"""

# Generate a sample vector
sample_vector = tf.random.normal([1, 100])

# Generate an image from the untrained generator
generated_image = generator_model_hyeri(sample_vector, training=False)

# Plot the generated image
plt.imshow(generated_image[0, :, :, 0], cmap='gray')
plt.axis('off')
plt.show()

"""### e. Build the Discriminator Model of the GAN"""

# Define the discriminator model
discriminator_model_hyeri = Sequential([
    Conv2D(64, (5, 5), strides=(2, 2), padding='same', input_shape=[28, 28, 1]),
    LeakyReLU(),
    Dropout(0.3),
    Conv2D(128, (5, 5), strides=(2, 2), padding='same'),
    LeakyReLU(),
    Dropout(0.3),
    Conv2DTranspose(64, (5, 5), strides=(2, 2), padding='same'),
    BatchNormalization(),
    LeakyReLU(),
    Flatten(),
    Dense(1)
])

# Display the summary of the discriminator model
discriminator_model_hyeri.summary()

# Draw the diagram for the summary
plot_model(discriminator_model_hyeri, show_shapes=True, show_layer_names=True)

"""### f. Implement Training"""

# Define loss function
cross_entropy_hyeri = BinaryCrossentropy(from_logits=True)

# Define optimizers
generator_optimizer_hyeri = Adam(1e-4)
discriminator_optimizer_hyeri = Adam(1e-4)

# Define training step function
@tf.function
def train_step(images):
    noise = tf.random.normal([256, 100])

    with tf.GradientTape() as gen_tape, tf.GradientTape() as disc_tape:
        generated_images = generator_model_hyeri(noise, training=True)

        real_output = discriminator_model_hyeri(images, training=True)
        fake_output = discriminator_model_hyeri(generated_images, training=True)

        gen_loss = cross_entropy_hyeri(tf.ones_like(fake_output), fake_output)
        real_loss = cross_entropy_hyeri(tf.ones_like(real_output), real_output)
        fake_loss = cross_entropy_hyeri(tf.zeros_like(fake_output), fake_output)
        disc_loss = real_loss + fake_loss
    gradients_of_generator = gen_tape.gradient(gen_loss, generator_model_hyeri.trainable_variables)
    gradients_of_discriminator = disc_tape.gradient(disc_loss, discriminator_model_hyeri.trainable_variables)
    generator_optimizer_hyeri.apply_gradients(zip(gradients_of_generator, generator_model_hyeri.trainable_variables))
    discriminator_optimizer_hyeri.apply_gradients(zip(gradients_of_discriminator, discriminator_model_hyeri.trainable_variables))

"""### g. Train the model in batches with 10 epochs"""

# Train the models
num_epochs = 10
for epoch in range(num_epochs):
    start_time = time.time()
    for images_batch in train_dataset_hyeri:
        train_step(images_batch)
    epoch_time = time.time() - start_time
    print(f"Epoch {epoch + 1} took {epoch_time:.2f} seconds")

# Calculate and display how long it would take to train the same model using 70,000 training samples on 100 epochs
total_samples = 70000
total_epochs = 100
estimated_total_time = (total_samples / 256) * total_epochs * epoch_time
print(f"Estimated total training time for 70,000 samples on 100 epochs: {estimated_total_time:.2f} seconds")

# Generate 16 sample vectors
sample_vectors = tf.random.normal([16, 100])

# Generate images from generator_model_firstname
generated_images = generator_model_hyeri(sample_vectors, training=False)

# Denormalize the pixel values
generated_images = 127.5 * generated_images + 127.5

# Plot generated images
plt.figure(figsize=(8, 8))
for i in range(16):
    plt.subplot(4, 4, i + 1)
    plt.imshow(generated_images[i, :, :, 0], cmap='gray')
    plt.axis('off')
plt.show()