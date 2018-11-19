
import json
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
from mutagen import File
import os
import pandas as pd
import pprint
from pymongo import MongoClient
import sys

#database operation and metadata operation



class data_op(object):


    def __init__(self,ip='localhost',port=27017,db='inf551',col='music'):
        self.metadata=None
        self.file_name=None
        self.__client = MongoClient(ip, port)
        self.__db = self.__client[db]
        self.__collection = self.__db[col]
    def cn_status(self):
        if self.__client==None:
            print('connection to database failed')
            return -1
        else:
            return 1

    def extract_metadata(self,path_name):
        audio = MP3(path_name, ID3=EasyID3)
        self.file_name=os.path.basename(path_name)
        title=[x for x in audio.keys()]
        title.append('duration')
        title.remove('performer')
        title=sorted(title)
        value={}
        #value=[audio[y][0] for y in title]
        for y in title:
            if y !='duration':

                value.setdefault(y,audio[y][0])

            else:
                value.setdefault(y,audio.info.length)
        value.setdefault('file_name',self.file_name)
        self.metadata=value


    def upload_metadata(self):
        is_exist = self.__collection.find_one(self.metadata)
        if is_exist==None:

            self.__collection.insert_one(self.metadata)
            print("inserting...")
        else:
            self.__collection.replace_one(is_exist,self.metadata)
            print('replacing %s'%self.file_name)


    def get_metadata(self,content):
        res=self.__collection.find(content)
        for x in res:
            yield x



    def metadata_from_dir(self,path_name):
        files=os.listdir(path_name)
        for file in files:
            self.extract_metadata(file)
            self.upload_metadata()
        print('done')

    def db_authorize(self):
        pass
if __name__=="__main__":
    a=data_op()
    a.extract_metadata('music/22.mp3')
    for dat in a.get_metadata({'file_name':'22.mp3'}):
        print(dat)
    # print(a.get_metadata())
