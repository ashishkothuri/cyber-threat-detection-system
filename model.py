import pandas as pd
import random
import pickle
from sklearn.ensemble import RandomForestClassifier, IsolationForest

data = []

for _ in range(1000):
    length = random.randint(20, 1500)
    protocol = random.randint(0, 2)
    port = random.randint(0, 65535)

    label = 1 if length > 1000 else 0

    data.append([length, protocol, port, label])

df = pd.DataFrame(data, columns=["length", "protocol", "port", "label"])

X = df[["length", "protocol", "port"]]
y = df["label"]

# Classification model
clf = RandomForestClassifier()
clf.fit(X, y)

# Anomaly detection model
anomaly = IsolationForest(contamination=0.1)
anomaly.fit(X)

pickle.dump(clf, open("model.pkl", "wb"))
pickle.dump(anomaly, open("anomaly.pkl", "wb"))

print("Advanced models ready!")