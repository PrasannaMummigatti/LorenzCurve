import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def skewed_random_integers(low, high, skewness, size):
    random_values = np.random.gamma(shape=skewness, scale=1.0, size=size)
    scaled_values = (random_values - random_values.min()) / (random_values.max() - random_values.min())
    skewed_integers = np.floor(low + scaled_values * (high - low + 1)).astype(int)
    return skewed_integers

def gini_coefficient(revenues):
    revenues = np.sort(revenues)
    n = len(revenues)
    diff_sum = np.sum([np.abs(i - j) for i in revenues for j in revenues])
    return diff_sum / (2 * n * np.sum(revenues))

skewness_values = [0.1,0.15,0.2, 0.25,0.5, 1.0, 2.0, 5.0,10,20,30,40,50,60,100]  # Different skewness values
N = 25  # Number of products

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

def update(frame):
    skew = skewness_values[frame]
    np.random.seed(42)  # Ensure reproducibility
    product_revenues = skewed_random_integers(50, 5000, skew, N)
    sorted_revenues = np.sort(product_revenues)
    cumulative_revenue = np.cumsum(sorted_revenues)
    total_revenue = cumulative_revenue[-1]
    cumulative_share = cumulative_revenue / total_revenue * 100
    cumulative_products = np.linspace(0, 1, N + 1) * 100
    cumulative_share = np.insert(cumulative_share, 0, 0)
    gini = gini_coefficient(product_revenues)
    
    descending_revenues = np.sort(product_revenues)[::-1]
    cumulative_revenue_desc = np.cumsum(descending_revenues)
    cumulative_revenue_percentage = cumulative_revenue_desc / total_revenue * 100
    
    axes[0].cla()
    axes[0].plot(cumulative_products, cumulative_share, marker='o', linestyle='-', color='b', alpha=0.7, label='Lorenz Curve')
    axes[0].plot([0, 100], [0, 100], linestyle='--', color='r', label='Perfect Equality')
    axes[0].fill_between(cumulative_products, cumulative_products, cumulative_share, alpha=0.2, color='b')
    axes[0].set_title(f'Lorenz Curve \nGini Coefficient: {gini:.4f}')
    axes[0].set_xlabel('Cumulative Share of Products (%)')
    axes[0].set_ylabel('Cumulative Share of Revenue (%)')
    axes[0].set_xlim([0, 100])
    axes[0].set_ylim([0, 100])
    axes[0].legend()
    axes[0].grid(True)
    
    axes[1].cla()
    axes[1].bar(range(1, N + 1), descending_revenues, color='skyblue', edgecolor='black', label='Revenue')
    axes[1].set_xlabel('Products (Sorted by their contributon to Revenue)')
    axes[1].set_ylabel('Revenue', color='b')
    axes[1].tick_params(axis='y', labelcolor='b')
    axes[1].set_title(f'Product-wise Revenue Distribution')
    axes[1].grid(axis='y', linestyle='--', alpha=0.7)
    
    # Clear twin axis before updating
    if hasattr(axes[1], 'twin'):  
        axes[1].twin.remove()
    
    ax2 = axes[1].twinx()
    axes[1].twin = ax2  # Store reference to remove in the next frame
    ax2.plot(range(1, N + 1), cumulative_revenue_percentage, marker='o', linestyle='-', color='r', label='Cumulative Revenue (%)')
    ax2.set_ylabel('Cumulative Revenue (%)', color='r')
    ax2.tick_params(axis='y', labelcolor='r')
    
ani = animation.FuncAnimation(fig, update, frames=len(skewness_values), repeat=True, interval=2000)
plt.show()
