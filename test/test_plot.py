import os
import pandas as pd
import matplotlib.pyplot as plt
import mpld3
from mpld3 import plugins


def plot_csv(filename):
    # Load the CSV file into a DataFrame
    df = pd.read_csv(filename)

    # Extract the base name of the input file without extension
    base_name = os.path.splitext(os.path.basename(filename))[0]

    # Identify columns to plot (exclude columns with only zeros)
    columns_to_plot = [col for col in df.columns if col != 'inkomen' and df[col].any()]

    # Create a static plot using matplotlib
    plt.figure(figsize=(10, 6))
    for col in columns_to_plot:
        plt.plot(df['inkomen'], df[col], label=col.capitalize())
    plt.xlabel('Inkomen')
    plt.ylabel('Toeslag')
    plt.title('Toeslagen vs Inkomen')
    plt.legend()
    plt.grid(True)

    # Save the static plot as PNG
    png_filename = f"{base_name}_plot.png"
    plt.savefig(png_filename)
    mpld3.show()
    # plt.close()
plot_csv("toeslagen2.csv")