import matplotlib.pyplot as plt
import csv
import sys

x1 = []
x2=[]
x3=[]
y1=[]
y2=[]
timeDiffBF_DF=[]

t=0
noOfTrials=0
timeNetwork=0
fileName=''

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
        for row in csvfile:
            x1.append(int(row["kFoundTCSeqBF"]))
            x2.append(int(row["kNw"]))
            x3.append(int(row["kFoundTCSeqDF"]))
        
            timeNetwork+=float(row["timeNetwork"])
            t1=float(row["timeSeqTCSeqBF"])
            y1.append(t1)
            t2=float(row["timeSeqTCSeqDF"])
            y2.append(t2)    
            timeDiffBF_DF.append(t1-t2)
        
            t+=t1+t2
            noOfTrials+=1
       
        print t/3600
        print timeNetwork
        print noOfTrials
        print x1
        
        
        
        plt.figure(figsize=(8, 20), dpi=80)
        
        plt.subplot(511)
        plt.yscale('log')
        plt.scatter(x1,y1, label="TCSeqBF", alpha=0.6)
        plt.scatter(x1,y2, label="TCSeqDF", alpha=0.6)
        
        plt.xlabel('reticulations Found')
        plt.ylabel('time (s)')
        plt.title('Running time (total ~ '+ str(int(t/3600))+' hours)')
        plt.legend()
        

        plt.subplot(512)
        plt.yscale('log')
        plt.scatter(x2,y1, label="TCSeqBF", alpha=0.6)
        plt.scatter(x2,y2, label="TCSeqDF", alpha=0.6)
        
        plt.xlabel('reticulations Original')
        plt.ylabel('time (s)')
        plt.title('Running time (total ~ '+ str(int(t/3600))+' hours)')
        plt.legend()


        
        plt.subplot(513)
        
        plt.scatter(x1,timeDiffBF_DF, label="BF-DF", alpha=0.3)
        
        plt.xlabel('reticulations')
        plt.ylabel('timeDiff (s)')
        plt.title('Breadth first - Depth first time')
        plt.legend()
        
        plt.subplot(514)
        
        plt.scatter(x3,x2, label="k DF Found and real k", alpha=0.3)
        
        plt.xlabel('k DF Found')
        plt.ylabel('real k')
        plt.title('Right k? DF')
        plt.legend()
        

        plt.subplot(515)
        
        plt.scatter(x1,x2, label="k BF Found and real k", alpha=0.3)
        
        plt.xlabel('k BF Found')
        plt.ylabel('real k')
        plt.title('Right k? BF')
        plt.legend()

        
        plt.savefig(fileName+'.pdf', bbox_inches='tight')
else:
    print( "No input file, type -f [filename]")
