import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Time series data
time = np.arange(0, 100, 1)

# Simulate realistic CPU and Memory metrics with values not less than 10
np.random.seed(42)  # for reproducibility

# Cluster 1: Low initial load, stays low
cpu_cluster1 = np.clip(np.random.normal(30, 5, 100), 10, 85)
memory_cluster1 = np.clip(np.random.normal(30, 5, 100), 10, 85)

# Cluster 2: Gradual increase until time mark 40, then decreases, then increases again, not exceeding 80
def logistic_growth(x, L=70, k=0.1, x0=20):
    return L / (1 + np.exp(-k * (x - x0)))

initial_growth = logistic_growth(time)
cpu_cluster2 = np.concatenate((initial_growth[:80], np.linspace(initial_growth[79], 10, 20)))
memory_cluster2 = np.concatenate((initial_growth[:80], np.linspace(initial_growth[79], 10, 20)))

# Add some noise to make it more realistic
cpu_cluster2 += np.random.normal(0, 2, 100)
memory_cluster2 += np.random.normal(0, 2, 100)

# Ensure values are not less than 10 and not more than 80
cpu_cluster2 = np.clip(cpu_cluster2, 10, 80)
memory_cluster2 = np.clip(memory_cluster2, 10, 80)

# Cluster 3: Low load until time mark 40, then increases
cpu_cluster3 = np.where(time < 40, np.random.normal(20, 5, 100), np.random.normal(60, 10, 100))
memory_cluster3 = np.where(time < 40, np.random.normal(20, 5, 100), np.random.normal(60, 10, 100))

# Ensure values are not less than 10 and not more than 85
cpu_cluster3 = np.clip(cpu_cluster3, 10, 85)
memory_cluster3 = np.clip(memory_cluster3, 10, 85)

# Create a DataFrame
df = pd.DataFrame({
    'Time': time,
    'CPU Cluster 1': cpu_cluster1,
    'CPU Cluster 2': cpu_cluster2,
    'CPU Cluster 3': cpu_cluster3,
    'Memory Cluster 1': memory_cluster1,
    'Memory Cluster 2': memory_cluster2,
    'Memory Cluster 3': memory_cluster3
})

# Plotting the data
plt.figure(figsize=(14, 7))

# CPU Usage Plot
plt.subplot(2, 1, 1)
plt.plot(df['Time'], df['CPU Cluster 1'], label='CPU Cluster 1', color='r')
plt.plot(df['Time'], df['CPU Cluster 2'], label='CPU Cluster 2', color='g')
plt.plot(df['Time'], df['CPU Cluster 3'], label='CPU Cluster 3', color='b')
plt.title('CPU Usage Over Time')
plt.xlabel('Time')
plt.ylabel('CPU Usage')
plt.legend()

# Memory Usage Plot
plt.subplot(2, 1, 2)
plt.plot(df['Time'], df['Memory Cluster 1'], label='Memory Cluster 1', color='r')
plt.plot(df['Time'], df['Memory Cluster 2'], label='Memory Cluster 2', color='g')
plt.plot(df['Time'], df['Memory Cluster 3'], label='Memory Cluster 3', color='b')
plt.title('Memory Usage Over Time')
plt.xlabel('Time')
plt.ylabel('Memory Usage')
plt.legend()

plt.tight_layout()
plt.show()
