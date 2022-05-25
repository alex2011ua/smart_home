import datetime
import os

import july
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from july.helpers import get_calendar_title
from july.rcmod import update_rcparams
from july.utils import date_range, preprocess_inputs


from house.core.models import DHT_MQ, Params


def refresh():

    l = DHT_MQ.objects.order_by("-date_t_h").all()[:300]
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
    ax.set_xlabel("Date")  # Add an x-label to the axes.
    ax.set_ylabel("Temp")  # Add a y-label to the axes.
    ax.legend()  # Add a legend.
    if os.path.exists("static/test.png"):
        os.remove("static/test.png")
    else:
        print("The file does not exist")

    fig.savefig("static/test.png")
    plt.close()


def calendar_plot(
    dates,
    data,
    cmap="july",
    value_label=False,
    date_label=False,
    weeknum_label=False,
    month_label=True,
    value_format="int",
    title=True,
    ncols=2,
    figsize=None,
    **kwargs,
):

    update_rcparams(**kwargs)
    dates_clean, data_clean = preprocess_inputs(dates, data)
    # Get unique years in input dates.
    years = sorted(set([day.year for day in dates_clean]))
    # Get unique months (YYYY-MM) in input dates.
    year_months = sorted(set([day.strftime("%Y-%m") for day in dates_clean]))

    nrows = int(np.ceil(len(year_months) / ncols))
    if not figsize:
        if ncols == 6:
            figsize = (12, 0.5 + nrows * 2)
        elif ncols == 5:
            figsize = (12, 1 + nrows * 2)
        elif ncols == 4:
            figsize = (14, 2 + nrows * 2)
        elif ncols == 3:
            figsize = (10, 2 + nrows * 2)
        elif ncols == 2:
            figsize = (8, 3 + nrows * 2)

    fig, axes = plt.subplots(nrows, ncols, figsize=figsize)

    for i, year_month in enumerate(year_months):
        month = [day for day in dates_clean if day.strftime("%Y-%m") == year_month]
        vals = [
            val for day, val in zip(dates_clean, data_clean) if day.strftime("%Y-%m") == year_month
        ]
        july.month_plot(
            month,  # type: ignore
            vals,
            cmap=cmap,
            date_label=date_label,
            weeknum_label=weeknum_label,
            month_label=month_label,
            value_label=value_label,
            value_format=value_format,
            ax=axes.reshape(-1)[i],
            cal_mode=True,
        )

    for ax in axes.reshape(-1)[len(year_months) :]:
        ax.set_visible(False)

    plt.subplots_adjust(wspace=0.75, hspace=0.5)
    # if title:
    #     plt.suptitle(get_calendar_title(years), fontsize="x-large", y=1.03)

    if os.path.exists("../../static/calend.png"):
        os.remove("../../static/calend.png")
    else:
        print("The file does not exist")

    fig.savefig("static/calend.png")
    plt.close()
    return axes


def calend():
    dates = date_range("2022-05-01", "2022-09-30")
    poliv = Params.objects.filter(poliv__gt=10)
    data = [5 for _ in range(len(dates))]
    for i in poliv:
        if i.date_t_h.date() in dates:
            ind = dates.index(i.date_t_h.date())
            data[ind] = i.poliv
    today = datetime.date.today()
    ind = dates.index(today)
    data[ind] = 0

    calendar_plot(dates, data, date_label=True)


if __name__ == "__main__":
    calend()