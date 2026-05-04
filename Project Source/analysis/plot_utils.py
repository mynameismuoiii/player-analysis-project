import matplotlib.pyplot as plt


def save_plot(x, y, xlabel, ylabel, title, path):
    plt.figure()
    plt.plot(x, y)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.savefig(path)
    plt.close()