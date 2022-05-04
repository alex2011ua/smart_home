import numpy as np
import matplotlib.pyplot as plt


def refresh():
    try:
        rng = np.arange(50)
        rnd = np.random.randint(0, 10, size=(3, rng.size))
        yrs = 1960 + rng

        fig, ax = plt.subplots(figsize=(5, 3))
        ax.stackplot(yrs, rng + rnd, labels=['Eastasia', 'Eurasia', 'Oceania'])
        ax.set_title('Combined debt growth over time')
        ax.legend(loc='upper left')
        ax.set_ylabel('Total debt')
        ax.set_xlim(xmin=yrs[0], xmax=yrs[-1])
        fig.tight_layout()

        fig.savefig('/static/test.png')

        print("test")
        #fig.savefig('../../static/test.png')
        plt.close()
    except(Exception) as err:
        print(err)
        print(err.text)
