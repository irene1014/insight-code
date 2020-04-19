"""
====================================
 :mod:insight-code.scr
====================================
.. moduleauthor:: Irene Cho <sisang.cho@sjsu.edu>

Description
===========
Insight Data Engineer Code Challenge
"""

################################################################################
import os
import csv
import sys
from collections import defaultdict, Counter


################################################################################

class Insightcode(object):
    # ==========================================================================
    def __init__(self, inputfile, outputfile):
        if not os.path.exists(inputfile):
            raise IOError('Cannot read image file "%s"' % inputfile)
        self.inputfile = inputfile
        self.outputfile = outputfile
        self.lst = []
        self.df1 = []
        self.processed_dict = []

    # ==========================================================================
    def process_dt(self):
        with open(self.inputfile) as csvfile:
            dt = csv.reader(csvfile, delimiter=',')
            for row in dt:
                self.lst.append(row)
        for i in self.lst:
            df = {}
            k0 = i[0].rstrip()
            df['year'] = k0[0:4]
            df['product'] = i[1].lower()
            df['company'] = i[7].lower()
            self.df1.append(df)
        counts = defaultdict(lambda: [0, 0])
        for line in self.df1:
            entry = counts[(line['product'], line['year'])]
            entry[0] += 1
            entry.append(line['company'])
        for k, v in sorted(counts.items(), key=lambda item: item[0]):
            c = Counter(v[2:])
            p = round(max([(c[i] / float(len(v[2:])) * 100.0) for i in c]))
            self.processed_dict.append({'product': str(k[0]),'year': k[1],
              'total_complaints': v[0],'total_companies':len(set(v[2:])),
              'highest_percentage': int(p)} )
        return self.processed_dict

    # ==========================================================================
    def exportcsv(self):
        self.process_dt()
        csv_file = self.outputfile
        csv_columns = ['product', 'year', 'total_complaints', 'total_companies',
                       'highest_percentage']
        try:
            with open(csv_file, 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                writer.writeheader()
                for data in self.processed_dict:
                    writer.writerow(data)
        except IOError:
            print("I/O error")


################################################################################
if __name__ == '__main__':
    k = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
    file1 = os.path.join(k,'input/complaints.csv')
    file2 =  os.path.join(k,'output/report.csv')
    op = Insightcode(file1, file2)
    #print(op.process_dt())
    op.exportcsv()
    

