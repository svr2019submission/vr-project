#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import csv

import pandas as pd

"""
    Given a csv file, compute 
"""
def compute_metrics(afile, repo_filter = None):

    results = []

    repo = pd.read_csv(afile,sep=',')
    
    #check wheter should filter the data_frame or not
    if repo_filter:
        repo_filter = pd.read_csv(repo_filter, sep=',')

        #need to filter the repo according to filter_file
        repo = repo[repo['Type'].isin(repo_filter['Type'])]
    
    class_names = list(repo['Type'])

    #get general information of each repositorie
    num_classes = repo['Type'].count()
    lines_code = repo['LOC'].sum()

    try:
    	repo.drop('LCOM', axis=1, inplace=True)
    except Exception as e:
    	print("Error file: {}".format(afile))    
    
    #sum of all values of each column
    new_df = repo.sum()

    #get the name of the columns
    columns = list(repo.columns.values)

    try:
        columns.remove('Type') #name isn't important
    except:
        print("E: Can't do operation in: {}".format(afile))

    #get the total of each column and place inside a index of a list
    for c in columns:
        r =  new_df[c]
        results = results + [r]

    #return a list with the total of each column, num_classes, lines_code 
    return results, class_names, num_classes, lines_code


"""
    Given a directory, compute metrics for all valid csv files
"""
def compute_all_metrics(repo_filter = None):
    
    #will store the final results
    results = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    classes, class_names, loc, total_classes, total_loc, all_class_names = 0, [], 0, 0, 0, []

    
    for root, dirs, files in os.walk(".", topdown=False):
        for csv_file in files:
            
            if ".csv" not in csv_file:
                continue

            #comput sum value for all columns
            result = []

            #check wheter filter the csv_file or not
            if repo_filter:
                result, class_names, classes, loc = compute_metrics(csv_file, repo_filter) #Non-VR
            else:
                result, class_names, classes, loc = compute_metrics(csv_file) #VR
            
            #sum up the results
            total_loc += loc
            total_classes += classes
            all_class_names = all_class_names + class_names
    
            #sum the values of all files in results
            for i in range(len(result)):
                results[i] += result[i]
    
    #return the results
    return results, total_loc, total_classes, all_class_names
    

if __name__ == '__main__':

	#choices
    print "1 - Run on VR projects"
    print "2 - Run on Non-VR projects"

    #read the option
    switch = int(raw_input("Chose a target: "))

    #execute according to the option
    if switch not in [1, 2]:
        print "W: Invalid option!"

    base_dir = os.getcwd()

    repositories_vr_path      = "./results/full_results/metrics/vr"
    repositories_non_vr_path  = "./results/full_results/metrics/non-vr"

    #csv file used was filter
    non_vr_tested_classes = base_dir + "/results/sampled_results/non_vr_tested_classes.csv"

    all_class_names = []

    #change to the targeted path.: VR analize all classes. Non-VR analize only tested classes
    if(switch == 1):    
        os.chdir(repositories_vr_path)

        #run comput all metrics for a given dir
        results, total_loc, total_classes, all_class_names = compute_all_metrics()
    
    else:
        
        os.chdir(repositories_non_vr_path)

        #run comput all metrics for a given dir
        results, total_loc, total_classes, all_class_names = compute_all_metrics(repo_filter= non_vr_tested_classes)


    #print the results properly

    #name of the columns
    columns = ['NOF','NOM','NOP','NOPF','NOPM','LOC','WMC','NC','DIT','LCOM','Fan-Out', 'Fan-In']

    #print the values
    for column, value in zip(columns, results):
        print("{}: {}".format(column, value))

    #other information
    print('Lines of code: ', total_loc)    
    print('Number of classes: ', total_classes)