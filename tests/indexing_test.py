import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import csv
import logic
import json

def store_indexing_test():
   if(os.path.exists("tests/indexing.txt")):
      os.remove("tests/indexing_test.txt")
   file = open("tests/store_indexing_test.txt", "r")
   testcase_list = file.readlines()
   file.close()
   for testcase in testcase_list:
      logic.StoreIndexing(testcase, "tests/indexing_test.txt")
      file = open("tests/indexing_test.txt", "r")
      stored_dictionary = file.read()
      file.close()
      if stored_dictionary != testcase:
         print(f"Failed at test case {testcase_list.index(testcase)}: {testcase}")

def create_indexing_test():
   file = open("tests/create_indexing_test.txt", "r")
   testcase_list = file.readlines()
   file.close()
   for testcase in testcase_list:
      (sentence, line_id, input_dictionary, output_dictionary) = testcase.split('###')
      dictionary = json.loads(input_dictionary)
      expected_output = json.loads(output_dictionary)
      actual_output = logic.CreateIndexing(sentence, int(line_id), dictionary)
      if actual_output != expected_output:
         print(f"Failed at test case {testcase_list.index(testcase)}: {testcase}")

create_indexing_test()
store_indexing_test()