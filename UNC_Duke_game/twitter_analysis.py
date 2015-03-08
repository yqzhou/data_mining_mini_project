import json
import time
import re
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
from pylab import yticks
import matplotlib
import scipy


locations = ["processed_Duke.txt", "processed_UNC.txt"]
summaries = []

for location in locations:
    summary = {}
    for line in  open(location, "r"):
        data = json.loads(line.rstrip())
        date =data['timestamp']
        date = re.search(r'(.)*\+0000', date)
        date = date.group(0)[:-6]
        date = time.strptime(date, "%a %b %d %H:%M:%S")
        if date.tm_mday != 8 or date.tm_hour > 5 or date.tm_hour < 1:
            continue
        timeslot = str(date.tm_hour) + ":" +  str(date.tm_min) .zfill(2)
        if timeslot in summary.keys():
            summary[timeslot]["counts"] += 1
            summary[timeslot]["hashtags"].append(data['hashtags'])
            if data['location'] != "" and data['location'] != None:
                summary[timeslot]["location"].append(data["location"])
            if data['geo'] != "Null" and data['geo'] != None:
                summary[timeslot]["geo"].append(data["geo"])
        else:
            summary[timeslot] = {"counts": 1, "hashtags": [], "location": [], "geo": []}
    summaries.append(summary)

#print summary
ax1=plt.subplot2grid((3,2), (0,0), colspan=2)
ax2= plt.subplot2grid((3,2), (1,0), colspan=2)
ax3= plt.subplot2grid((3,2), (2,0))
ax4= plt.subplot2grid((3,2), (2,1))
total_count = []
j = 0
format = {"color":['blue', 'skyblue'], "line":['--', '-']}
for summary in summaries:
    counts = {}
    hashtags = []
    for timeslot in summary.keys():
        counts[timeslot] = summary[timeslot]["counts"]
        hashtags += summary[timeslot]["hashtags"]
    #print hashtags
    total_count.append(counts)
    counter = {}
    hashtags = sum(hashtags, [])
    hash_sum = Counter(hashtags)
    hash_name = []
    hash_count = []

    for item in hash_sum.most_common(10):
        (name, count ) = item
        hash_name.append(name)
        hash_count.append(count)

    order_time = sorted(list(counts.keys()))
    #print order_time
    order_count = [counts[i] for i in order_time]
    ax1.set_title("Tweets analysis by retrieving hashtags during UNC-Duke Game Mar 7 2015")
    ax1.plot([x for x in range(len(order_time))], order_count,  linestyle = format["line"][j], color = format["color"][j])
    ax1.set_ylabel("Number of tweets")
    ax1.set_xlabel("Time(min) starts from 8pm")

    if j == 0:
        ax3.barh( [i for i in range(10)], hash_count, height=1, color = format["color"][j], align="center")
        ax3.set_yticks(range(len(hash_name)))
        ax3.set_yticklabels(hash_name)
        ax3.set_title("Top 10 Hashtags", color=format["color"][j])
        ax3.set_xlabel("# of tweets")
    else:
        ax4.barh( [i for i in range(10)], hash_count, height=1, color = format["color"][j], align="center")
        ax4.set_yticks(range(len(hash_name)))
        ax4.set_yticklabels(hash_name)
        ax4.set_title("Top 10 Hashtags", color=format["color"][j])
        ax4.set_xlabel("# of tweets")
    j += 1


diff = {}
for key in total_count[0].keys():
    if key in total_count[1]:
        diff[key] = total_count[0][key] - total_count[1][key]

diff_time = sorted(list(diff.keys()))
diff_count = [diff[i] for i in diff_time]
x = [i for i in range(len(diff_count))]
y1 = np.array(diff_count)
y2 = np.array([0 for i in range(len(diff_count))])
ax2.set_ylabel("Differences in number of tweets")
ax2.set_xlabel("Time(min) starts from 8pm")
ax2.plot(x, y1, x, y2, color="black")
ax2.fill_between(x, y1, y2, where=y1>=y2, interpolate=True, color='blue')
ax2.fill_between(x, y1, y2, where=y1<=y2, interpolate=True, color='skyblue')
ax2.axvspan(70, 113, facecolor = 'yellow', alpha = 0.2)
ax2.axvspan(130, 193, facecolor='yellow', alpha = 0.2)
ax2.axvline(x=156, linewidth=2, color='r')
ax2.annotate('D started to lead', xy=(156, 500),  xycoords='data',  xytext=(20, 20), textcoords='offset points', arrowprops=dict(arrowstyle="->"))
ax2.annotate('First Half', xy=(75, 900), xytext=(0,0), xycoords='data', textcoords='offset points')
ax2.annotate('Second Half', xy = (135, 900), xytext=(0,0), xycoords='data', textcoords='offset points')

plt.show()



