"""
K-Nearest Neighbors (KNN) Algorithm - Simple Example
=====================================================
Dataset: Classify fruits based on weight (grams) and sweetness (1-10)
Classes: Apple, Orange, Grape
"""

import math
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from collections import Counter


# ─────────────────────────────────────────────
# 1. TRAINING DATA
# ─────────────────────────────────────────────
# Each entry: [weight_grams, sweetness_score, label]
training_data = [
    [170, 6, "Apple"],
    [185, 7, "Apple"],
    [160, 5, "Apple"],
    [175, 6, "Apple"],
    [190, 8, "Apple"],

    [130, 8, "Orange"],
    [145, 9, "Orange"],
    [120, 7, "Orange"],
    [140, 8, "Orange"],
    [155, 9, "Orange"],

    [5,   9, "Grape"],
    [6,   10, "Grape"],
    [4,   8,  "Grape"],
    [7,   9,  "Grape"],
    [5,   10, "Grape"],
]

# ─────────────────────────────────────────────
# 2. EUCLIDEAN DISTANCE
# ─────────────────────────────────────────────
def euclidean_distance(point1, point2):
    """Calculate straight-line distance between two points."""
    return math.sqrt(
        (point1[0] - point2[0]) ** 2 +
        (point1[1] - point2[1]) ** 2
    )


# ─────────────────────────────────────────────
# 3. KNN PREDICT FUNCTION
# ─────────────────────────────────────────────
def knn_predict(training_data, test_point, k=3):
    """
    Predict the class of a test point using KNN.

    Steps:
      1. Compute distance from test point to every training point
      2. Sort by distance, pick the K closest
      3. Majority vote → predicted class
    """
    distances = []
    for row in training_data:
        features = row[:2]       # weight, sweetness
        label    = row[2]        # class
        dist     = euclidean_distance(test_point, features)
        distances.append((dist, label))

    # Sort by distance (closest first)
    distances.sort(key=lambda x: x[0])

    # Pick K nearest neighbors
    k_neighbors = distances[:k]

    print(f"\n  Test point : weight={test_point[0]}g, sweetness={test_point[1]}")
    print(f"  K={k} nearest neighbors:")
    for i, (dist, label) in enumerate(k_neighbors, 1):
        print(f"    {i}. {label:6s}  (distance = {dist:.2f})")

    # Majority vote
    labels = [label for _, label in k_neighbors]
    vote   = Counter(labels)
    prediction = vote.most_common(1)[0][0]

    print(f"  Vote count : {dict(vote)}")
    print(f"  Prediction : ✅ {prediction}")
    return prediction


# ─────────────────────────────────────────────
# 4. RUN PREDICTIONS
# ─────────────────────────────────────────────
print("=" * 50)
print("  KNN Fruit Classifier (k=3)")
print("=" * 50)

test_cases = [
    ([180, 7], "Apple"),     # heavy + medium sweet
    ([135, 8], "Orange"),    # medium weight + sweet
    ([5,   9], "Grape"),     # very light + very sweet
    ([100, 6], "?"),         # unknown - let KNN decide
]

predictions = []
for test_point, actual in test_cases:
    pred = knn_predict(training_data, test_point, k=3)
    predictions.append((test_point, pred))
    if actual != "?":
        result = "✓ Correct" if pred == actual else "✗ Wrong"
        print(f"  Actual: {actual} → {result}")

print("\n" + "=" * 50)


# ─────────────────────────────────────────────
# 5. MATPLOTLIB VISUALIZATION
# ─────────────────────────────────────────────
COLOR_MAP = {"Apple": "#378ADD", "Orange": "#D85A30", "Grape": "#639922"}

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle("KNN Fruit Classifier", fontsize=15, fontweight="bold", y=1.01)

# --- Plot 1: Training data + test points ---
ax1 = axes[0]
ax1.set_title("Training Data & Test Points", fontsize=12)

for row in training_data:
    w, s, label = row
    ax1.scatter(w, s, color=COLOR_MAP[label], s=80, edgecolors="white",
                linewidths=0.8, zorder=3)

# Plot test points as stars
test_colors  = ["#378ADD", "#D85A30", "#639922", "#888888"]
test_labels  = ["Test: Apple?", "Test: Orange?", "Test: Grape?", "Test: Unknown"]

for i, (tp, pred) in enumerate(predictions):
    ax1.scatter(tp[0], tp[1], marker="*", s=280,
                color=COLOR_MAP.get(pred, "#888888"),
                edgecolors="black", linewidths=0.8, zorder=5)
    ax1.annotate(f"→ {pred}", (tp[0], tp[1]),
                 textcoords="offset points", xytext=(8, 4),
                 fontsize=8, color="black")

ax1.set_xlabel("Weight (grams)", fontsize=10)
ax1.set_ylabel("Sweetness (1-10)", fontsize=10)
ax1.grid(True, alpha=0.25)

legend_patches = [mpatches.Patch(color=c, label=l) for l, c in COLOR_MAP.items()]
legend_patches.append(mpatches.Patch(color="white", label="★ = Test point"))
ax1.legend(handles=legend_patches, fontsize=9)


# --- Plot 2: Decision boundary (grid sweep) ---
ax2 = axes[1]
ax2.set_title("Decision Boundary (K=3)", fontsize=12)

# Sweep a grid and classify every point
w_range = range(0, 210, 4)
s_range = [s / 10 for s in range(10, 105, 4)]   # 1.0 → 10.5

for w in w_range:
    for s in s_range:
        pred = knn_predict(training_data, [w, s], k=3)
        ax2.scatter(w, s, color=COLOR_MAP[pred], alpha=0.18, s=18, zorder=1)

# Overlay actual training points
for row in training_data:
    w, s, label = row
    ax2.scatter(w, s, color=COLOR_MAP[label], s=80, edgecolors="white",
                linewidths=0.8, zorder=3)

ax2.set_xlabel("Weight (grams)", fontsize=10)
ax2.set_ylabel("Sweetness (1-10)", fontsize=10)
ax2.grid(True, alpha=0.25)
ax2.legend(handles=legend_patches[:3], fontsize=9)

plt.tight_layout()
plt.savefig("/mnt/user-data/outputs/knn_plot.png", dpi=130, bbox_inches="tight")
print("\n  Plot saved → knn_plot.png")
plt.show()
