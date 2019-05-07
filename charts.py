#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import the pyplot library
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

#old model just to mantain documented
def old_pie_chart():
    #data-vr
    total_vr, buggy_vr = 21508, 2627 
    clean_vr = total_vr - buggy_vr
    values_vr = [clean_vr, buggy_vr]

    #data-non-vr
    total_nvr, buggy_nvr = 21568, 1921
    clean_nvr = total_nvr - buggy_nvr
    values_nvr = [clean_nvr, buggy_nvr]

    #colors = ['b', 'g', 'r', 'c', 'm', 'y']
    colors = ['b', 'r']
    labels = ['Clean Classes', 'Fault pronner classes']
    explode = (0, 0)
    plt.pie(values_vr, colors=colors, labels= values_vr,explode=explode,counterclock=False, shadow=True)
    plt.axis('equal')

    #plt.title('Classification of the analyzed instances according to ACL')

    plt.legend(labels,loc=3)
    plt.show()    


def pie_chart():

    # Pie chart
    labels = ['Clean Classes', 'Fault pronner classes']
    sizes = [87.79, 12.21]
    sizes_tested = [91.10, 8.90]

    #colors
    colors = ['#66b3ff', '#ff9999'] #,'#99ff99','#ffcc99'
    
    #explsion
    explode = (0.05,0.05)
    
    plt.pie(sizes_tested, colors = colors, autopct='%1.1f%%', startangle=90, pctdistance=0.85, explode = explode, textprops={'fontsize': 20, 'fontweight': 'bold'})
    
    #draw circle
    centre_circle = plt.Circle((0,0),0.70,fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    # Equal aspect ratio ensures that pie is drawn as a circle
    plt.axis('equal')  
    plt.tight_layout()
    #plt.legend(labels)
    plt.show()


def stacked_histogram():

    N = 4
    clean = (47.44, 150.62, 287.20, 792.66)
    fault = (6.25, 15.11, 35.31,71.5)
    
    #colors = ['b', 'g', 'r', 'c', 'm', 'y']
    colors = ['b', 'r']    
        
    ind = np.arange(N)    # the x locations for the groups
    width = 0.35       # the width of the bars: can also be len(x) sequence

    p1 = plt.bar(ind, clean, width)
    
    p2 = plt.bar(ind, fault, width, bottom=clean)


    #plt.title('Distribution of defects by size of the repositories')
    plt.ylabel('Classes')
    plt.xlabel('Grouping of repositories by number of classes')
    
    plt.xticks(ind, ('1~100', '101~200', '201~500', '500+'))
    plt.yticks(np.arange(0, 1100, 100))
    plt.legend((p1[0], p2[0]), ('Clean', 'Fault'))

    plt.show()


def correlation_chart():
    
    
    
    #grouped the average of faults by size of repos -> 0~50| 51~100| 101~150| 151~200| 201~500| 500+
    groups = ['0~50', '51~100', '101~150', '151~200', '201~500', '500+']
    data_nonvr = [3, 11.23, 14.80, 14.6, 29.90, 122.33]
    data_vr =    [5, 13.44, 12.07, 20.92, 23.80, 130.28]

    plt.plot(groups, data_vr)
    plt.plot(groups, data_nonvr)

    #labels
    plt.xlabel("Repositories grouped by number of classes")
    plt.ylabel("Average of fault-prone classes")
    
    plt.legend(('VR', 'NonVR'))

    plt.show()

if __name__ == "__main__":

    #requires python-tk

    #possible methods
    print "1 - Pichart"
    print "2 - Correlation"
    print "3 - Histogram"

    #read the option
    switch = int(raw_input("Chose a chart: "))

    #execute according to the option
    if switch not in [1,2,3,4]:
        print "W: Invalid option!"

    if switch == 1:
        pie_chart()
    if switch == 2:
        correlation_chart()
    if switch == 3:
        stacked_histogram()
    if switch == 4:
        pass
