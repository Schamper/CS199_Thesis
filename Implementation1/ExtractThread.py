import os, threading
from binascii import hexlify
from operator import itemgetter

class ExtractingThread(threading.Thread):
    top = ['', 999999999]
    count = 0

    def __init__(self, Sigs):
        threading.Thread.__init__(self)
        self.Sigs = Sigs

    def run(self):
        dir_list = os.listdir(os.path.dirname(os.path.realpath(__file__)))
        number_of_files = len(dir_list)       
        for Sig in self.Sigs:
            for filename in dir_list:
                with open(filename, 'r') as f:
                    content = f.read()
                    file_content = hexlify(content)
                if Sig in file_content:
                    self.count = self.count + 1
            false_positive_rate = float(self.count) / number_of_files
            if self.top[1] > false_positive_rate:
                self.top = []
                self.top.append(Sig)
                self.top.append(false_positive_rate)
            self.count = 0
