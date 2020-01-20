import sys
import os
import argparse
from glob import glob
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer as wnl
from nltk.corpus import framenet
import csv


def find_frames(dir, frame_list):
  frame_list = []
  for filename in dir:
    with open(filename, "r") as thefile:
      verbs = []
      for line in thefile:
        word_tmp = nltk.pos_tag(word_tokenize(line))
        for word in word_tmp:
          if word[1][0:2] == "VB":
            verb_lemma = lemmatizer.lemmatize(word[0], pos ="v")
            verbs.append(verb_lemma)
            for frame in framenet.frames('(?i)'+ verb_lemma):
              if frame.ID not in frame_list:
                frame_list.append(frame.ID)

  return frame_list


def count_document_frame(dir):
  dir_verb_dict_list = []
  for filename in dir:
    with open(filename, "r") as thefile:
      verbs = []
      frame_list = []
      frame_dict = {}
      for line in thefile:
        word_tmp = nltk.pos_tag(word_tokenize(line))
        for word in word_tmp:
          if word[1][0:2] == "VB":
            verb_lemma = lemmatizer.lemmatize(word[0], pos ="v")
            verbs.append(verb_lemma)
            for frame in framenet.frames('(?i)'+ verb_lemma):
              if frame.ID not in frame_list:
                frame_list.append(frame.ID)
                frame_dict[frame.ID] = 1
              else:
                frame_dict[frame.ID] += 1

    dir_verb_dict_list.append(frame_dict)
  return dir_verb_dict_list


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build and evaluate trigram model for characters.")
    parser.add_argument("directory_1", type=str, help="Name of the directory to be modeled.")
    parser.add_argument("directory_2", type=str, help="Name of the directory to be modeled.")

    args = parser.parse_args()

    class_1_path = glob("{}/*.txt".format(args.directory_1))
    class_2_path = glob("{}/*.txt".format(args.directory_2))
    class_1_name_tmp = glob("{}/*.txt".format(re.sub(r'[^\w\s]','',args.directory_1)))
    class_2_name_tmp = glob("{}/*.txt".format(re.sub(r'[^\w\s]','',args.directory_2)))
    
    class_names_tmp = class_1_name_tmp + class_2_name_tmp
    class_names = []
    for name in class_names_tmp:
      str_tmp = name.split('/')
      new_document_name = [str_tmp[1]+'_'+str_tmp[0], str_tmp[0]]
      class_names.append(new_document_name)

    lemmatizer = wnl() 

    #find out all the frame IDS in 2 classes and sort by increasing order
    frame_list_all = find_frames(class_2_path, find_frames(class_1_path, []))
    frame_list_all.sort()

    #count frame ids in documents
    doc_frame_dict_list = count_document_frame(class_1_path) + count_document_frame(class_2_path)

    #write into the csv file
    with open("test.csv","w") as csvfile: 
      writer = csv.writer(csvfile)

      #header of the chart
      writer.writerow(['filename', 'class']+frame_list_all)

      # print out the rows of the info of each document
      for dict in range(0, len(doc_frame_dict_list)):
        document_frames = []
        for frame in frame_list_all:
          if frame in doc_frame_dict_list[dict].keys():
            document_frames.append(doc_frame_dict_list[dict][frame])
          else:
            document_frames.append(0)
        document_frames.insert(0, class_names[dict][1])
        document_frames.insert(0, class_names[dict][0])
        
        writer.writerow(document_frames)


