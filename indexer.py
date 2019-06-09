import os
from pathlib import Path

class Indexer():

    def __init__(self, *args, **kwargs):
        self.files = {} # file template > {"index":"name"}
        self.old = self.files
        self.new_file = None
        self.new_index = None
        # start to index
        self.index()

    def index(self):
        formats = {"py":False,"exe":False}
        for _,_,files in os.walk(Path('.')):
            for file in files:
                if not file.split('.')[-1] in formats.keys():
                    try:
                        a = file.split(" ")
                        index = int(a[0])
                        name = " ".join(a[1:])[0:]
                        self.files[index] = name
                    except:
                        print(f"there is no index for file: {file}")
                        self.new_file = file

    def full_names(self,dict):
        full_names = []
        for index,name in zip(dict.keys(),dict.values()):
            full_names.append(str(index) + " " + name)
        return full_names

    def increment(self, from_index):
        if self.new_file == None:
            return False
        self.new_index = from_index
        # self.pprint(self.files)
        self.files = self.sort(self.files) # first sorting for insurance
        # self.pprint(self.files)
        old_part = list(self.files.items())[from_index-1:]

        # if the new file is wanted to be the last index
        print(len(self.files))
        if len(old_part) == 0 and (self.new_index > len(self.files)):
            os.rename(self.new_file,f"{str(len(self.files)+1)} {self.new_file}")
        else:
            for old_index,file in old_part:
                # adding the new file
                if old_index == self.new_index:
                    os.rename(self.new_file,f"{str(self.new_index)} {self.new_file}")
                # incrementing the old files
                os.rename(f"{str(old_index)} {file}",f"{str(old_index+1)} {file}")
        self.index()

    def order_rename(self):
        if self.new_file != None:
            return False
        file_list = sorted(self.files.items())
        new_index = 1
        for old_index,file in file_list:
            os.rename(f"{str(old_index)} {file}",f"{str(new_index)} {file}")
            new_index+=1

    def pprint(self,file):
        if type(file) == type(dict()):
            for x in file.items():
                print(x)
        elif type(file) == type(list()):
            for x in file:
                print(x)

    def sort(self, old, reverse = False):
        new = dict(sorted(self.files.items(),reverse = reverse))
        return new
