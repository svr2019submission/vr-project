#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd

from statsmodels.graphics.gofplots import qqplot
from matplotlib import pyplot

from scipy import stats

"""
    Normalisty test to a serie of args
"""
def normality_test(*args):

    print "I : Testing the normality of the data"
    print "H0: Sample looks Gaussian (Normal distributed)"
    print "H1: Sample does not look Gaussian (Don't follow a normal distribution)"

    for arg in args:

        stat, p = stats.shapiro(arg)

        print('Statistics=%.3f, p=%.5f' % (stat, p))
        
        # interpret
        alpha = 0.05
        if p > alpha:
            print('fail to reject H0')
        else:
            print('reject H0')


"""
    Mann-Whitney test
"""
def mann_whitney_test(*args):

    print "I : Applying Mann-Whitney test to compare if the distributions of two populations are shifted"
    print "H0: The distribution of the variable in question is identical (in the population) in the two groups"
    print "H1: The distribution of the variable isn't identical in the two groups"

    #arg is a tuple of list data
    for arg in args:

        #convert both to an array like format
        array1 = np.array(arg[0])
        array2 = np.array(arg[1])

        #comput wilcoxcon between array1 x array2
        stat, p = stats.mannwhitneyu(array1, array2)

        print('Statistics=%.3f, p=%.5f' % (stat, p))
        
        # interpret
        alpha = 0.05
        if p < alpha:
            print('The distributions in the two groups aren\'t the same (reject H0)')
        else:
            print('the distributions in the two groups are the same (fail to reject H0)')



def qq_plot(data):

    #convert data (python list) to a numpy array
    data = np.array(data)

    #plot the data
    qqplot(data, line='s')
    pyplot.show()

if __name__ == "__main__":

    #smells results

    arch_non_vr_smells = [1, 6, 2, 24, 12, 8, 11]
    arch_vr_smells     = [29, 212, 3, 366, 201, 84, 78]


    implem_vr_smells     = [1812,684,9,150,583,2117,6841,11947,25264,931,35]
    implem_non_vr_smells = [9,14,1,5,9,13,12,40,36,17,5]


    design_vr_smells     = [245,991,3149,6,0,8101,2469,4,627,1171,18,209,1,389,15,483,3741,6987,64]
    design_non_vr_smells = [8,46,45,4,1,13,11,16,9,44,2,2,2,9,2,7,17,23,5]

    #normality test for each data sample
    normality_test(arch_non_vr_smells, arch_vr_smells, implem_non_vr_smells, implem_vr_smells, design_non_vr_smells, design_vr_smells)

    #mann whitney test 
    mann_whitney_test((arch_non_vr_smells, arch_vr_smells), (implem_non_vr_smells, implem_vr_smells), (design_non_vr_smells, design_vr_smells))