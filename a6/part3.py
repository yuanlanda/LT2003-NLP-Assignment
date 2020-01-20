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

def find_frames(dir_list):
  """ 
   Find all frame IDs and the counts of each frame IDs in each docments.

   Args:
      dir_list: the path list of the two classes.
   
   Returns:
      Two values. The first one('frame_list') is the frame list of all the frame IDs found 
      in the two classes. The second one('dir_verb_dict_list') is a dictionary, the keys of 
      the dictionary are the frame IDs of all the verb in each document, the values of the 
      dictionary are the counts of the frame ID according to the related frame ID.
  """

  dir_verb_dict_list = []
  frame_list = []
  for dir in dir_list:
    for filename in dir:
      with open(filename, "r") as thefile:
        frame_dict = {}
        for line in thefile:
          word_tmp = nltk.pos_tag(word_tokenize(line))
          for word in word_tmp:
            if word[1][0:2] == "VB":
              verb_lemma = lemmatizer.lemmatize(word[0], pos ="v")
              for frame in framenet.frames('(?i)'+ verb_lemma):
                if frame.ID not in frame_list:
                  frame_list.append(frame.ID)
                  
                if frame.ID not in frame_dict.keys():
                  frame_dict[frame.ID] = 1
                else:
                  frame_dict[frame.ID] += 1

      dir_verb_dict_list.append(frame_dict)

  return frame_list, dir_verb_dict_list


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build and evaluate trigram model for characters.")
    parser.add_argument("directory_1", type=str, help="Name of the directory 1 to be modeled.")
    parser.add_argument("directory_2", type=str, help="Name of the directory 2 to be modeled.")

    args = parser.parse_args()

    class_1_path = glob("{}/*.txt".format(args.directory_1))
    class_2_path = glob("{}/*.txt".format(args.directory_2))
    
    classes_path_list = class_1_path + class_2_path
    classed_file_name_list =[]
    classes_name_list = []

    for path in classes_path_list:
      path_tmp = path.rsplit('/',1)
      class_name = re.sub(r'[^\w\s]','',path_tmp[0])
      classed_file_name_list.append(path_tmp[1]+'_'+class_name)
      classes_name_list.append(class_name)

    lemmatizer = wnl() 

    #find out all the frame IDS in 2 classes and sort by increasing order
    path_list = [class_1_path, class_2_path]
    result = find_frames(path_list)
    
    frame_list = result[0]
    frame_list.sort()

    #count frame ids in documents
    doc_frame_dict_list = result[1]

    #write into the csv file
    with open("result.csv","w") as csvfile: 
      writer = csv.writer(csvfile)

      #header of the chart
      writer.writerow(['filename', 'class']+frame_list)

      # print out the rows of the info of each document
      for dict in range(0, len(doc_frame_dict_list)):
        document_frames = []
        for frame in frame_list:
          if frame in doc_frame_dict_list[dict].keys():
            document_frames.append(doc_frame_dict_list[dict][frame])
          else:
            document_frames.append(0)
        document_frames.insert(0, classes_name_list[dict])
        document_frames.insert(0, classed_file_name_list[dict])
        
        writer.writerow(document_frames)


