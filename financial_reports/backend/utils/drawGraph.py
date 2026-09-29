import matplotlib.pyplot as plt


class GraphUtils:
    def __init__(self):
        self.plot_num = 0
        self.scatter_num = 0
        self.histogram_num = 0
        
    def draw_plot(self, x, y, title="Plot", xlabel="X-axis", ylabel="Y-axis", color='blue', linewidth=2, linestyle='-', grid=True, s=1, marker='o'):
        """
        Draw a simple line plot with given x and y data.
        
        Parameters:
        - x: List of x values
        - y: List of y values
        - title: Title of the plot
        - xlabel: Label for the x-axis
        - ylabel: Label for the y-axis
        """
        
        plt.figure(figsize=(10, 6))
        plt.plot(x, y, color=color, linewidth=linewidth, linestyle=linestyle, marker=marker, markersize=s)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        
        if grid:
            plt.grid(True)
        
        self.plot_num += 1
        plt.savefig(f"plot_{self.plot_num}.png")
        
        return f"plot_{self.plot_num}.png"

    def draw_scatter(self, x, y, title="Scatter Plot", xlabel="X-axis", ylabel="Y-axis", color='red', s=50, marker='o'):
        plt.figure(figsize=(10, 6))
        plt.scatter(x, y, color=color, s=s, marker=marker)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.grid(True)

        self.scatter_num += 1
        plt.savefig(f"data/scatter_{self.scatter_num}.png")

        return f"data/scatter_{self.scatter_num}.png"
    
    def draw_histogram(self, data, title="Histogram", xlabel="Value", ylabel="Frequency", bins=10, color='green'):
        plt.figure(figsize=(10, 6))
        plt.hist(data, bins=bins, color=color, edgecolor='black')
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.grid(True)

        self.histogram_num += 1
        plt.savefig(f"data/histogram_{self.histogram_num}.png")

        return f"data/histogram_{self.histogram_num}.png"