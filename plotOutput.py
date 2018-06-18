import matplotlib.pyplot as plt
import csv
import sys

xs = {}
ys = {}



t=0
noOfTrials=0
timeNetwork=0
fileName=''
labels=set()


option_f = False
option_f_argument = ""
i = 1
while i < len(sys.argv):
    arg= sys.argv[i]
    if arg == "-f":
        option_f = True
        i+=1
        fileName = str(sys.argv[i])
    i+=1



if option_f:

    with open(fileName+".csv") as inputfile:
        csvfile = csv.DictReader(inputfile)
        header=csvfile.fieldnames
        timeColumns=[]
        kColumns=[]
        i=5
        while i < len(header):
            if (i-5)%3==0:
                kColumns+=[header[i]]
            if (i-6)%3==0:
                print header[i]
                timeColumns+=[header[i]]
            i+=1
        
        for row in csvfile:
            for h in zip(kColumns,timeColumns):
                lbl=str(row["noOfTrees"])+'Trees'+str(h[1])
                if lbl not in xs:
                    xs[lbl]=[]
                    ys[lbl]=[]
                labels.add(lbl)
                print(h[0])
                print(row[h[0]])
                xs[lbl].append(int(row[h[0]]))
            #    x.append(int(row["kNw"]))

      
                timeNetwork+=float(row[h[1]])
                t1=float(row[h[1]])
                ys[lbl].append(t1)
                t+=t1
            noOfTrials+=1
        
        print t/3600
        print timeNetwork
        print noOfTrials
        print xs
        
        
        
        plt.figure(figsize=(8, 12), dpi=80)
        
        plt.yscale('log')
        for lbl in labels:
            plt.scatter(xs[lbl],ys[lbl], label="times"+str(lbl), alpha=0.6)
        
        plt.xlabel('reticulations')
        plt.ylabel('time (s)')
        plt.title('Running time (total ~ '+ str(int(t/3600))+' hours)')
        plt.legend()
        
        
        plt.savefig(fileName+'.pdf', bbox_inches='tight')
else:
    print( "No input file, type -f [filename]")
