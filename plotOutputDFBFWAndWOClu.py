import matplotlib.pyplot as plt
import csv
import sys

x1=[]
x2=[]
x3=[]

y1=[]
y2=[]
y3=[]
y4=[]
timeDiffBF_DF=[]
timeDiffBF_DFClu=[]
timeDiffNoClu_Clu_BF=[]
timeDiffNoClu_Clu_DF=[]



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
            x2.append(int(row["ClukFoundTCSeqBF"]))
            x3.append(int(row["kNw"]))

            if int(row["kFoundTCSeqBF"])!=int(row["ClukFoundTCSeqBF"]):
                print('cluster gives other number of reticulations')
                print(row["trees"])
                print(row["network"])
                print(row["CluseqTCSeqBF"])
                print(row["seqTCSeqBF"])
                print('\n')
        
            timeNetwork+=float(row["timeNetwork"])
            t1=float(row["timeSeqTCSeqBF"])
            y1.append(t1)
            t2=float(row["timeSeqTCSeqDF"])
            y2.append(t2)    
            timeDiffBF_DF.append(t1-t2)

            t3=float(row["ClutimeSeqTCSeqBF"])
            y3.append(t3)
            t4=float(row["ClutimeSeqTCSeqDF"])
            y4.append(t4)    
            timeDiffBF_DFClu.append(t3-t4)
            timeDiffNoClu_Clu_DF.append(t1-t3)
            timeDiffNoClu_Clu_BF.append(t2-t4)

        
            t+=t1+t2+t3+t4
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
        plt.title('Running time No Clu (total ~ '+ str(int(t/3600))+' hours)')
        plt.legend()
        

        plt.subplot(512)
        plt.yscale('log')
        plt.scatter(x2,y3, label="TCSeqBF", alpha=0.6)
        plt.scatter(x2,y4, label="TCSeqDF", alpha=0.6)
        
        plt.xlabel('reticulations Original')
        plt.ylabel('time (s)')
        plt.title('Running time Clu (total ~ '+ str(int(t/3600))+' hours)')
        plt.legend()


        
        plt.subplot(513)
        
        plt.scatter(x1,timeDiffNoClu_Clu_BF, label="BF", alpha=0.3)
        plt.scatter(x1,timeDiffNoClu_Clu_DF, label="DF", alpha=0.3)
 
         
        plt.xlabel('reticulations')
        plt.ylabel('timeDiff (s)')
        plt.title('No Clu - Clu time')
        plt.legend()        
        
#==============================================================================
#         plt.scatter(x1,timeDiffBF_DF, label="NoClu", alpha=0.3)
#         plt.scatter(x2,timeDiffBF_DFClu, label="Clu", alpha=0.3)
# 
#         
#         plt.xlabel('reticulations')
#         plt.ylabel('timeDiff (s)')
#         plt.title('Breadth first - Depth first time')
#         plt.legend()
#==============================================================================
        
        plt.subplot(514)
        
        plt.scatter(x1,x3, label="k NoClu Found and real k", alpha=0.3)
        
        plt.xlabel('k NoClu Found')
        plt.ylabel('real k')
        plt.title('Right k?')
        plt.legend()
        

        plt.subplot(515)

        diff=map(lambda x: x[1]-x[0],zip(x1,x2))
        
        
        plt.scatter(x1,diff, label="k No Clu Found and k NoClu Found", alpha=0.3)
        
        
        plt.xlabel('k No Clu Found')
        plt.ylabel('Extra k in Clustered algorithm')
        plt.title('Right k?')
        plt.legend()

        
        plt.savefig(fileName+'.pdf', bbox_inches='tight')
else:
    print( "No input file, type -f [filename]")
