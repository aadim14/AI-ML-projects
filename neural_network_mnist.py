# Aadi Malhotra
import numpy as np
import time
import matplotlib.pyplot as plt

TRAIN_IMAGES = 'train-images.idx3-ubyte'
TRAIN_LABELS = 'train-labels.idx1-ubyte'
TEST_IMAGES  = 't10k-images.idx3-ubyte'
TEST_LABELS  = 't10k-labels.idx1-ubyte'

def load_images(path):
    with open(path, 'rb') as f:
        f.read(4)  # skip magic
        n     = int.from_bytes(f.read(4), 'big')
        rows  = int.from_bytes(f.read(4), 'big')
        cols  = int.from_bytes(f.read(4), 'big')
        data  = np.frombuffer(f.read(), dtype=np.uint8)
    return data.reshape(n, rows * cols).astype(np.float32) / 255.0

def load_labels(path):
    with open(path, 'rb') as f:
        f.read(4)  
        n = int.from_bytes(f.read(4), 'big')
        labels = np.frombuffer(f.read(), dtype=np.uint8)
    return labels.astype(np.int32)

def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))

def dsigmoid(y):
    return y * (1.0 - y)

def softmax(z):
    z = z - np.max(z, axis=1, keepdims=True)
    e = np.exp(z)
    return e / np.sum(e, axis=1, keepdims=True)

# Load dataset
X_train = load_images(TRAIN_IMAGES)
Y_train = load_labels(TRAIN_LABELS)
X_test  = load_images(TEST_IMAGES)
Y_test  = load_labels(TEST_LABELS)

# One-hot encode training labels
num_classes = 10
T_train = np.eye(num_classes, dtype=np.float32)[Y_train]

# Network hyperparameters
input_size, hidden_size, output_size = 784, 128, 10
epochs, lr = 5, 0.01
n_train = X_train.shape[0]

# Initialize weights and biases
rng = np.random.default_rng(seed=42)
W1 = rng.uniform(-0.1, 0.1, size=(input_size, hidden_size)).astype(np.float32)
b1 = np.zeros((1, hidden_size), dtype=np.float32)
W2 = rng.uniform(-0.1, 0.1, size=(hidden_size, output_size)).astype(np.float32)
b2 = np.zeros((1, output_size), dtype=np.float32)

# Plotting setup
checkpoint = 5000
samples_processed = []
train_accs = []

plt.ion()
fig, ax = plt.subplots()
line, = ax.plot([], [], '-o')
ax.set_xlabel('Samples processed')
ax.set_ylabel('Training accuracy (%)')
ax.set_title('Training Accuracy Progress')
ax.set_ylim(80, 100)
ax.set_xlim(0, epochs * n_train)

# Training
start_time = time.time()
for epoch in range(1, epochs + 1):
    print(f"\nEpoch {epoch}/{epochs} — working:", end=' ', flush=True)
    epoch_start = time.time()

    for i in range(n_train):
        if (i + 1) % 1000 == 0:
            print('.', end='', flush=True)

        x = X_train[i:i+1]
        t = T_train[i:i+1]

        z1 = x @ W1 + b1
        a1 = sigmoid(z1)
        z2 = a1 @ W2 + b2
        a2 = softmax(z2)

        d2 = a2 - t
        dW2 = a1.T @ d2
        db2 = d2.sum(axis=0, keepdims=True)
        d1  = (d2 @ W2.T) * dsigmoid(a1)
        dW1 = x.T @ d1
        db1 = d1.sum(axis=0, keepdims=True)

        W2 -= lr * dW2
        b2 -= lr * db2
        W1 -= lr * dW1
        b1 -= lr * db1

        if (i + 1) % checkpoint == 0:
            A1 = sigmoid(X_train @ W1 + b1)
            A2 = softmax(A1 @ W2 + b2)
            acc = 100.0 * np.mean(np.argmax(A2, axis=1) == Y_train)
            samples = (epoch - 1) * n_train + (i + 1)
            samples_processed.append(samples)
            train_accs.append(acc)
            line.set_data(samples_processed, train_accs)
            ax.relim()
            ax.autoscale_view()
            plt.pause(0.001)

    print(f" done ({time.time() - epoch_start:.1f}s)")

print(f"\nTotal training time: {time.time() - start_time:.1f}s")
plt.ioff()
plt.show()

