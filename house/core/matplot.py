import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from house.core.models import DHT_MQ
import os

def refresh():

    l = DHT_MQ.objects.order_by("-date_t_h").all()[:100]
    dat = [item.date_t_h for item in l]
    temp_strit = [item.temp_street for item in l]

    fig, ax = plt.subplots(figsize=(15, 2.5))

    data = np.cumsum(np.random.randn(len(dat)))
    print(dat)
    ax.plot(dat, temp_strit)
    cdf = matplotlib.dates.ConciseDateFormatter(ax.xaxis.get_major_locator())
    ax.xaxis.set_major_formatter(cdf)

    if os.path.exists('static/test.png'):
        os.remove('static/test.png')
    else:
        print("The file does not exist")

    fig.savefig('static/test.png')
    plt.close()
