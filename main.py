import os, sys
from tools import downloader

if __name__ == '__main__':
    d = downloader.voc_datasets(year=2012)
    #d.download()
    d.extract_tarfile([os.path.join('C:/Users/tomwa/Desktop/Dataset_toolbox', f) for f in os.listdir('C:/Users/tomwa/Desktop/Dataset_toolbox') if f.endswith('.tar')])