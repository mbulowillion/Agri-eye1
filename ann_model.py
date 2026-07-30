import math
import random
import numpy as np
import cv2


DEFAULT_CLASSES = [
    "Healthy Leaf", "Maize Streak Virus", "Cassava Mosaic Disease",
    "Early Blight", "Fall Armyworm Damage",
]


class AnnModel:
    def __init__(self, input_dim=96, hidden_dim=32, output_dim=5, classes=None):
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.output_dim = output_dim
        self.classes = classes or DEFAULT_CLASSES

        rng = random.Random(42)
        scale1 = math.sqrt(2.0 / input_dim)
        scale2 = math.sqrt(1.0 / hidden_dim)
        self.w1 = [[rng.random() * scale1 for _ in range(hidden_dim)] for _ in range(input_dim)]
        self.b1 = [0.0] * hidden_dim
        self.w2 = [[rng.random() * scale2 for _ in range(output_dim)] for _ in range(hidden_dim)]
        self.b2 = [0.0] * output_dim

    def extract_features(self, image):
        if isinstance(image, str):
            img = cv2.imread(image, cv2.IMREAD_COLOR)
            if img is None:
                raise FileNotFoundError(f"Cannot read: {image}")
        else:
            img = image

        resized = cv2.resize(img, (128, 128))
        r_hist = cv2.calcHist([resized], [2], None, [32], [0, 256]).flatten()
        g_hist = cv2.calcHist([resized], [1], None, [32], [0, 256]).flatten()
        b_hist = cv2.calcHist([resized], [0], None, [32], [0, 256]).flatten()

        feat = np.concatenate([r_hist, g_hist, b_hist]).astype(np.float32)
        norm = np.linalg.norm(feat)
        if norm > 0:
            feat /= norm
        return feat.tolist()

    def forward(self, X):
        z1 = [self.b1[j] + sum(self.w1[i][j] * X[i] for i in range(self.input_dim))
              for j in range(self.hidden_dim)]
        a1 = [max(0.0, v) for v in z1]

        z2 = [self.b2[j] + sum(self.w2[i][j] * a1[i] for i in range(self.hidden_dim))
              for j in range(self.output_dim)]
        max_z = max(z2)
        exp_z = [math.exp(v - max_z) for v in z2]
        sum_exp = sum(exp_z)
        return [v / sum_exp for v in exp_z]

    def predict(self, image):
        X = self.extract_features(image)
        probs = self.forward(X)
        pred_idx = max(range(len(probs)), key=lambda i: probs[i])
        conf = round(probs[pred_idx] * 100, 1)
        class_probs = {self.classes[i]: round(probs[i] * 100, 1) for i in range(len(self.classes))}
        return {"condition": self.classes[pred_idx], "confidence": conf, "class_probabilities": class_probs}

    def train_epoch(self, samples, lr=0.05):
        m = len(samples)
        if m == 0:
            return 0.0, 0.0
        total_loss = 0.0
        correct = 0

        for x, label_idx in samples:
            target = [0.0] * self.output_dim
            target[label_idx] = 1.0

            z1 = [self.b1[j] + sum(self.w1[i][j] * x[i] for i in range(self.input_dim))
                  for j in range(self.hidden_dim)]
            a1 = [max(0.0, v) for v in z1]
            z2 = [self.b2[j] + sum(self.w2[i][j] * a1[i] for i in range(self.hidden_dim))
                  for j in range(self.output_dim)]
            max_z = max(z2)
            exp_z = [math.exp(v - max_z) for v in z2]
            sum_exp = sum(exp_z)
            a2 = [v / sum_exp for v in exp_z]

            total_loss += -math.log(max(a2[label_idx], 1e-12))
            if max(range(len(a2)), key=lambda i: a2[i]) == label_idx:
                correct += 1

            dz2 = [a2[j] - target[j] for j in range(self.output_dim)]
            for i in range(self.hidden_dim):
                for j in range(self.output_dim):
                    self.w2[i][j] -= lr * a1[i] * dz2[j] / m
            for j in range(self.output_dim):
                self.b2[j] -= lr * dz2[j] / m

            da1 = [sum(self.w2[i][j] * dz2[j] for j in range(self.output_dim)) / m
                   for i in range(self.hidden_dim)]
            dz1 = [da1[i] * (1.0 if z1[i] > 0 else 0.0) for i in range(self.hidden_dim)]
            for i in range(self.input_dim):
                for j in range(self.hidden_dim):
                    self.w1[i][j] -= lr * x[i] * dz1[j]
            for j in range(self.hidden_dim):
                self.b1[j] -= lr * dz1[j]

        return round(total_loss / m, 2), round(correct / m * 100, 2)

    def train(self, dataset, epochs=250, lr=0.05, on_epoch=None):
        for ep in range(1, epochs + 1):
            loss, acc = self.train_epoch(dataset, lr)
            if ep % 10 == 0 or ep == 1:
                if on_epoch:
                    on_epoch(ep, loss, acc)


def generate_synthetic_dataset(ann, count=140):
    return [([random.random() for _ in range(96)], random.randint(0, 4)) for _ in range(count)]
