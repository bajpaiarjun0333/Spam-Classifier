# -*- coding: utf-8 -*-
"""naiveBayes.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1FJ1c260UEsTJ7xHyRoEGIFZWbsIfJQ5H
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import words

#global variables 
collection={}
#it will store all the words withindex numbers
nltk.download('words')
word_set=set(words.words())

def loadData():
  df=pd.read_csv("dataset.csv")
  df=df.to_numpy()
  n=df.shape[0]
  m=df.shape[1]
  email=df[:,2]
  label=df[:,3]
  return (email,label,n)

# Function that reads and appends the data of each text file in the test folder into a list
def readfile(fp):
  global test_mails
  with open(fp, 'r') as f:
      test_mails.append([f.read()])

#code for testing using the test folder
import os
import csv
#library for file manipulation have been loaded successfully
#create a vector to read and push all the emails into it
test_mails=[]
#extract the current path
curr_path=os.getcwd()
#save the current path
old_path=curr_path
#old path is required to come back to same place
#appending the current path
curr_path=curr_path+"/test"
#changing the directory to enter the test folder
os.chdir(curr_path)
# Calling the read_text_file function for all .txt files in folder test 
for file in os.listdir():
    if file.endswith(".txt"):
        fp = f"{curr_path}/{file}"
        readfile(fp)

# Back to directory out of test
os.chdir(old_path)

#write all the mails present in the test_mails to the new csv file
filename = "test_dataset.csv"

with open(filename,'w') as csvfile:
    csvwriter = csv.writer(csvfile) 
    csvwriter.writerows(test_mails)

def buildDict(email):
  curr_index=len(collection)
  #initially curr_index will be 0
  for word in email:
    if word.lower() not in collection and word.lower() in word_set:
      collection[word]=curr_index
      curr_index=curr_index+1
  #no need to return as dictonary is global variable

#loop over all the emails and all words in it: map word number to probablity score
def calculateProbab(email,label):
  global no_of_ham
  global no_of_spam
  global probab_word_ham
  global probab_word_spam
  for i in range(n):
    new=' '.join(dict.fromkeys(email[i].split()))
    curr=new.split()
    if label[i]==0:
      no_of_ham=no_of_ham+1
    elif label[i]==1:
      no_of_spam=no_of_spam+1

    for word in curr:
      if word.lower() in collection and word.lower() in word_set:
        key=collection[word]
        if label[i]==0:
          #not spam case
          probab_word_ham[key]=probab_word_ham[key]+1
        elif label[i]==1:
          #spam case
          probab_word_spam[key]=probab_word_spam[key]+1
  #now convert to actual probablity
  for i in range(len(probab_word_spam)):
    probab_word_spam[i]=probab_word_spam[i]/no_of_spam
  for i in range(len(probab_word_ham)):
    probab_word_ham[i]=probab_word_ham[i]/no_of_ham
  #successfully created the entire frequency set

#controlling the calling of all the functions
email,label,n=loadData()
for i in range (n):
  curr=email[i].split()
  buildDict(curr)
#task count number of time word in spam and count number of time word in non spam calculate probablity score for both spam and not spam
probab_word_spam={}
probab_word_ham={}
for i in range(len(collection)):
  probab_word_spam[i]=1
  probab_word_ham[i]=1
#note that word must be present in the word set and vocablury
no_of_spam=0
no_of_ham=0
calculateProbab(email,label)

#everything is set now we need to apply formula
def testing(email):
  new=' '.join(dict.fromkeys(email.split()))
  curr=new.split()
  val=1
  for word in collection:
    key=collection[word]
    if word in curr:
      #probablity hone ki
      p1=probab_word_spam[key]
      p0=probab_word_ham[key]
      val=val*(p1/p0)
    else :
      p1=1-probab_word_spam[key]
      p0=1-probab_word_ham[key]
      val=val*(p1/p0)
  #calculating p hat
  p=no_of_spam/(no_of_spam+no_of_ham)
  val=val*(p/(1-p))
  val=np.log(val)
  if val>0:
    return 1
  else:
    return 0

#test over this data only
testdf=pd.read_csv("test_dataset.csv",header=None)
testdf=testdf.to_numpy()
test_x=testdf[:,0]
num=testdf.shape[0]
predicted_label=[]
error=0
for i in range(num):
  #correct_res=label[i]
  res=testing(test_x[i])
  predicted_label.append([test_x[i],res])
  #if res!=correct_res:
    #error=error+1
#print(error/n)

#storing the result back into a file
file_name = "test_result.csv"

with open(file_name,'w') as csvfile:
    csvwriter = csv.writer(csvfile) 
    csvwriter.writerow(['emails','predicted label'])
    csvwriter.writerows(predicted_label)