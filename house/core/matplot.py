import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from house.core.models import DHT_MQ
import os

def refresh():

    l = DHT_MQ.objects.order_by("-date_t_h").all()[:500]
    dat = [item.date_t_h for item in l]
    temp_strit = [item.temp_street for item in l]
    temp_tepl = [item.temp_teplica for item in l]
    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(dat, temp_strit, label="Темература на улице")
    ax.plot(dat, temp_tepl, label="Темература в теплице")
    ax.set_title("Температура")  # Add a title to the axes.
    cdf = matplotlib.dates.ConciseDateFormatter(ax.xaxis.get_major_locator())
    ax.xaxis.set_major_formatter(cdf)
    ax.grid(True)
    ax.set_xlabel('Date')  # Add an x-label to the axes.
    ax.set_ylabel('Temp')  # Add a y-label to the axes.
    ax.legend()  # Add a legend.
    if os.path.exists('static/test.png'):
        os.remove('static/test.png')
    else:
        print("The file does not exist")

    fig.savefig('static/test.png')
    plt.close()
