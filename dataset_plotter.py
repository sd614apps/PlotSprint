import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def read_dataset(file, file_type):
    if file_type == 'csv':
        dataset = pd.read_csv(file)
    elif file_type == 'tsv':
        dataset = pd.read_csv(file, sep='\t')
    elif file_type == 'xlsx':
        dataset = pd.read_excel(file)
    else:
        raise ValueError("Unsupported file type")
    
    columns = dataset.columns.tolist()
    return dataset, columns

def plot_dataset(dataset, plot_type, plot_folder, x_column, y_column, aggregate_function):
    sns.set(style="whitegrid")
    fig, ax = plt.subplots()

    if aggregate_function != 'none':
        if aggregate_function == 'sum':
            dataset = dataset.groupby(x_column)[y_column].sum().reset_index()
        elif aggregate_function == 'mean':
            dataset = dataset.groupby(x_column)[y_column].mean().reset_index()
        elif aggregate_function == 'count':
            dataset = dataset.groupby(x_column)[y_column].count().reset_index()
        else:
            raise ValueError("Unsupported aggregate function")

    if plot_type == 'line':
        sns.lineplot(data=dataset, x=x_column, y=y_column, ax=ax)
    elif plot_type == 'bar':
        sns.barplot(data=dataset, x=x_column, y=y_column, ax=ax)
    elif plot_type == 'scatter':
        sns.scatterplot(data=dataset, x=x_column, y=y_column, ax=ax)
    else:
        raise ValueError("Unsupported plot type")

    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, fontsize=8)  # Rotate xtick labels and adjust font size

    plot_filename = f"{plot_type}_{x_column}_{y_column}_{aggregate_function}.png"
    plot_filepath = os.path.join(plot_folder, plot_filename)
    fig.savefig(plot_filepath)
    plt.close(fig)

    return plot_filename

if __name__ == "__main__":
    file_path = input("Enter the path to your dataset: ")
    file_type = input("Enter the file type (csv, excel, json): ")
    plot_type = input("Enter the plot type (line, scatter, bar, hist): ")
    x_column = input("Enter the x-axis column name: ")
    y_column = input("Enter the y-axis column name: ")

    data = read_dataset(file_path, file_type)
    plot_dataset(data, plot_type, x_column, y_column)
