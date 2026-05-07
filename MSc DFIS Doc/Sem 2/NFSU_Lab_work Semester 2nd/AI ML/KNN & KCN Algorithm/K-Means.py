# -------------------------------
# K-Means Algorithm 
# -------------------------------

# Dataset (Marks only for clustering)
marks_data = [85, 40, 75, 30, 90]

# Number of clusters
k = 2

# Step 1: Initialize centroids manually
centroids = [40, 85]  # Starting centroids

def assign_clusters(data, centroids):
    clusters = [[] for _ in range(len(centroids))]

    for point in data:
        distances = []
        for c in centroids:
            distances.append((point - c) * (point - c))

        # Find nearest centroid
        min_index = distances.index(min(distances))
        clusters[min_index].append(point)

    return clusters

def update_centroids(clusters):
    new_centroids = []
    for cluster in clusters:
        if len(cluster) == 0:
            new_centroids.append(0)
        else:
            new_centroids.append(sum(cluster) / len(cluster))
    return new_centroids


# Run K-Means for few iterations
for i in range(5):
    clusters = assign_clusters(marks_data, centroids)
    centroids = update_centroids(clusters)

# Display Results
print("Final Centroids:", centroids)
print("Clusters:", clusters)
