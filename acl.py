#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import csv

import pandas as pd
import statistics as stats

from os import listdir
from os.path import isfile, join

"""
Read a path and returns a list with all the files contained inside it
parms:
    mypath = target path
"""
def get_files_from_dir(mypath):

    #returns a list that contains all files from mypath | reference -> https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory
    all_files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    return all_files


"""
Converts a dict to a csv file
parms:
    csv_name   = name of the csv that will be created
    my_results = a list where each value is a dict instance (like a json file) 
"""
def results_to_csv(csv_name, my_results):

    #keys of the dict will be the columns
    dict_data = my_results
    csv_columns = dict_data[0].keys()

    #reference -> https://www.tutorialspoint.com/How-to-save-a-Python-Dictionary-to-CSV-file
    try:
        with open(csv_name, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in dict_data:
                writer.writerow(data)
    except IOError:
        print("E: I/O error")
        sys.exit(-1) 


"""
Given a csv file with metrics compute HAM and MVM
params:
    afile = target csv file
    repo_filter = a csv file to filter afile before compute other operations
"""
def compute_HAM_MVM(afile):

    #will store the results
    HAM_values = {}
    MVM_values = {}    

    #read csv and drop LCOM metric
    repository = pd.read_csv(afile)
    try:
    	repository.drop('LCOM', axis=1, inplace=True)
    except Exception as e:
    	print("Error file: {}".format(afile))

    columns = repository.columns

    #calculate HAM 
    for c in columns[1:]:
        HAM = repository[c].mean()/2
        HAM_values[c] = HAM

    #iterate over the rows to calculate de MVM
    for index, row in repository.iterrows():
        
        #results array
        results = []

        #gonna check the metric values for each column
        for c in columns:
            
            #First column is the name of the module. Avoid and store the name of the module analyzed 
            if c == "Type":
                module = str(row[c])
                continue
            
            #get the value of the metric
            value = row[c]
            
            #The value of the result with the HAM value of the metric
            if value > HAM_values[c]:
                results = results + [1]
            else:
                results = results + [0]

        #sometimes we have modules with the same name. This avoid the replacement of values in the dict
        while module in MVM_values:
            module = module + "_duplicated"

        MVM_values[module] = results
    
    return HAM_values, MVM_values


"""
Compute threshold in order to verify if some instance is fault proner or not
parms:
    HAM_values = a dict that contains the hamonic mean of each evaluated module
    MVM_values = a dict that contaions the metrics value matrix of each evaluated module
"""
def compute_cutoff(HAM_values, MVM_values):

    #store final results
    results = []
    
    number_of_metrics = len(list(HAM_values.keys()))
    number_of_instances = len(list(MVM_values.keys()))

    mivs_values = {}
    possible_defects = 0

    for key, values in MVM_values.items():    
        
        mivs = sum(values)
        mivs_values[key] = mivs

        if mivs > (number_of_metrics/2):
            possible_defects = possible_defects + 1
    
    #a list with the mivs results
    mivs_list   = mivs_values.values()

    amivs = stats.mean(mivs_list) #average of mivs
    amivs_plus  = stats.mean(set(mivs_list)) #average of disticts mivs  
    mivs_median = stats.median(mivs_list) #median of mivs

    hmivs_mean  = stats.harmonic_mean([amivs_plus,mivs_median]) #hamonic mean of amivs+ and mivs_median

    possible_defects_rate = possible_defects / number_of_instances

    if possible_defects_rate > 0.5:
        cutoff = hmivs_mean * possible_defects_rate + (number_of_metrics - amivs) * (1 - possible_defects_rate) 
    else:
        cutoff = 2 * number_of_metrics * (1-possible_defects_rate) * hmivs_mean / number_of_metrics * (1 - possible_defects_rate) + hmivs_mean 

    for instance, value in mivs_values.items():

        if value > cutoff:
            results.append({"Component" : instance, "Threshold" : value, "Cutoff" : cutoff, "Status" : "Fault_proner"})
            #print("{} : buggy".format(instance))
        else:
            results.append({"Component" : instance, "Threshold" : value, "Cutoff" : cutoff, "Status" : "Clean"})
            #print("{} : clean".format(instance))

    return results



if __name__ == '__main__':
    
    all_results = {}

    #base dir
    base_dir = os.getcwd()
    
    #Check python version
    if sys.version_info[0] < 3:
        raise Exception("Python 3 or a more recent version is required.")

	#choices
    print("1 - Run on VR projects")
    print("2 - Run on Non-VR projects")

    #read the option
    switch = int(input("Chose a target: "))

    #execute according to the option
    if switch not in [1, 2]:
        print("W: Invalid option!")


    repositories_vr_path  = base_dir + "/results/full_results/metrics/vr/"
    repositories_non_vr_path  = base_dir + "/results/full_results/metrics/non-vr/"

    #change to the targeted path.: VR analize all classes. Non-VR analize only tested classes
    if(switch == 1):    
        repositories_path = repositories_vr_path
        results_path = base_dir + "/results/full_results/faultproneness/vr/"
    else:
        repositories_path = repositories_non_vr_path
        results_path = base_dir + "/results/full_results/faultproneness/non-vr"

    #get the name of the result file of each repository
    repositories_list = get_files_from_dir(repositories_path)

    #simple dir check
    try:
        #verifies if its a valid dir	
        os.stat(results_path)
    except:
        #since the dir doesn't exist, create it!
        os.mkdir(results_path)

    #change to results folder
    os.chdir(results_path)

    for rep in repositories_list:
        
        #path of csv file
        target_dir = repositories_path + rep

        #compute results for rep
        if switch == 1:
            HAM_values, MVM_values = compute_HAM_MVM(target_dir) #VR
        else:
            HAM_values, MVM_values = compute_HAM_MVM(target_dir) #Non-VR
        
        #compute cutoff
        result = compute_cutoff(HAM_values, MVM_values)

        #store the results in a csv_file
        csv_name = rep 
        all_results[rep] = result
        results_to_csv(csv_name, result)

    #dont need to filter the results
    if switch == 1:

        for key, values in all_results.items():
            faults = 0
            total = 0
            for v in values:
                total += 1
                if "Fault_proner" in v["Status"]:
                    faults += 1
            print("{},{},{}".format(key[:-4], faults, total))


    #filter the results before print
    else:

        #open the csv filter
        repo_filter = base_dir + "/results/sampled_results/non_vr_tested_classes.csv"
        repo_filter = pd.read_csv(repo_filter, sep=',')

        #loop the results.: key is the project, values are the classses and information whether is fautpronner or not
        for key, values in all_results.items():
            
            faults = 0
            total = 0

            #for each class of every file
            for instance in values:

                #check if the result is one of the non-tested non-vr classes
                if repo_filter['Type'].str.contains(instance['Component']).any():

                    #count the result
                    total += 1

                    #check whether it's faultprone or not
                    if "Fault_proner" in instance["Status"]:
                        faults += 1

            #after read every file information, print the results            
            print("{},{},{}".format(key[:-4], faults, total))