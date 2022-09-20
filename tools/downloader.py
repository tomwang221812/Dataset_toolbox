from genericpath import isdir
from logging.config import valid_ident
import os, sys, tarfile
import requests

class voc_datasets():
    
    def __init__(self, year=2012, sets={'trainval', 'test', 'devkit'}, save_dir='.', decompress=True):
        
        self.valid_years = (2007, 2008, 2009, 2010, 2011, 2012)
        self.valid_sets = {'trainval', 'test', 'devkit'}

        assert year in self.valid_years, \
                        '(EE) The dataset has no year {:d}, please choose one of {}'.format(year, self.valid_years)
        self.year = year
        self.url = 'http://host.robots.ox.ac.uk/pascal/VOC/voc{:d}'.format(year)
        self.test_set_2007_url = ' http://host.robots.ox.ac.uk/pascal/VOC/voc2007/VOCtest_06-Nov-2007.tar'
        assert os.path.exists(save_dir) and os.path.isdir(save_dir), \
                        '(EE) Save directory {} is not found or not a diretory'.format(save_dir)
        if len(os.listdir(save_dir)) > 0: \
                        '(WW) Save directory {} is not empty!'.format(save_dir)
        
        self.save_dir = save_dir

        assert sets.intersection(self.valid_sets), '(EE) No {} set avaliable'.format(sets)
        self.sets = sets
        

    def download(self, chunk_size=1024):

        downloaded_file = []
        
        for s in self.sets:
            filename = self.get_file_name(self.year, s)
            url = '{}/{}'.format(self.url, filename) if s != 'test' else '{}/{}'.format(self.test_set_2007_url, filename)
            req = requests.get(url, stream=True, allow_redirects=True)
            req.raise_for_status()
            headers = req.headers
            file_size = int(headers.get('Content-Length'))
            print('(**) Starting... Total file size: {:d}\n'.format(file_size))
            with open(os.path.join(self.save_dir, filename), 'wb') as tar_file:
                for chunk_id, current_chunk in enumerate(req.iter_content(chunk_size=chunk_size)):
                    if current_chunk : 
                        print('(**) Downloading... [{:>10d}/{:>10d} Bytes] {:s}'.format(chunk_id, file_size, filename), end='\r', flush=True)
                        tar_file.write(current_chunk)
            
            downloaded_file.append(os.path.join(self.save_dir, filename))
            print('(**) Done! Saved to {}/{}\n'.format(self.save_dir, filename))

        return downloaded_file

    def extract_tarfile(self, tar_path):

        if isinstance(tar_path, list):
            for idx_p, p in enumerate(tar_path):
                assert os.path.exists(p) and tarfile.is_tarfile(p), '(EE) No path to be extracted! Given {:s}'.format(p)

                print('(**) Extracting... [{:>2d}/{:>2d}] {:s}'.format(idx_p+1, len(tar_path), p))

                extract_dir = os.path.join(self.save_dir, os.path.split(p)[-1].replace('.tar', ''))
                tar_file = tarfile.open(p)
                tar_file.extractall(extract_dir) # specify which folder to extract to
                tar_file.close()
        else:
            assert os.path.exists(tar_path) and tarfile.is_tarfile(tar_path), '(EE) No path to be extracted! Given {:s}'.format(tar_path)

            print('(**) Extracting... {:s}'.format(tar_path))

            extract_dir = os.path.join(self.save_dir, os.path.split(p)[-1].replace('.tar', ''))
            tar_file = tarfile.open(p)
            tar_file.extractall(self.save_dir) # specify which folder to extract to
            tar_file.close()

        print('(!!) Done extract!')
                
    def get_file_name(self, year, set):

        prefix = 'VOC'

        if set == 'trainval':
            prefix = '{}{}'.format(prefix, 'trainval')
        elif set == 'test':
            prefix = '{}{}'.format(prefix, 'test')
        elif set == 'devkit':
            prefix = '{}{}'.format(prefix, 'devkit')
        else:
            print('(EE) set {:s} not found!'.format(set))

        if year == self.valid_years[0]:
            if set == 'trainval': return '{}_{}-{:d}.tar'.format(prefix, '06-Nov', year)
            elif set == 'test': return '{}_{}-{:d}.tar'.format(prefix, '06-Nov', year)
            elif set == 'devkit': return '{}_{}-{:d}.tar'.format(prefix, '08-Jun', year)
        elif year == self.valid_years[1]:
            if set == 'trainval': return '{}_{}-{:d}.tar'.format(prefix, '14-Jul', year)
            elif set == 'test': return '{}_{}-{:d}.tar'.format(prefix, '06-Nov', 2007)
            elif set == 'devkit': return '{}_{}-{:d}.tar'.format(prefix, '14-Apr', year)
        elif year == self.valid_years[2]:
            if set == 'trainval': return '{}_{}-{:d}.tar'.format(prefix, '11-May', year)
            elif set == 'test': return '{}_{}-{:d}.tar'.format(prefix, '06-Nov', 2007)
            elif set == 'devkit': return '{}_{}-{:d}.tar'.format(prefix, '14-Aug', year)
        elif year == self.valid_years[3]:
            if set == 'trainval': return '{}_{}-{:d}.tar'.format(prefix, '03-May', year)
            elif set == 'test': return '{}_{}-{:d}.tar'.format(prefix, '06-Nov', 2007)
            elif set == 'devkit': return '{}_{}-{:d}.tar'.format(prefix, '08-May', year)
        elif year == self.valid_years[4]:
            if set == 'trainval': return '{}_{}-{:d}.tar'.format(prefix, '25-May', year)
            elif set == 'test': return '{}_{}-{:d}.tar'.format(prefix, '06-Nov', 2007)
            elif set == 'devkit': return '{}_{}-{:d}.tar'.format(prefix, '25-May', year)
        elif year == self.valid_years[5]:
            if set == 'trainval': return '{}_{}-{:d}.tar'.format(prefix, '11-May', year)
            elif set == 'test': return '{}_{}-{:d}.tar'.format(prefix, '06-Nov', 2007)
            elif set == 'devkit': return '{}_{}-{:d}.tar'.format(prefix, '18-May', 2011)
        else:
            print('(EE) Year {:d} not found!'.format(year))

if __name__ == '__main__':
    pass