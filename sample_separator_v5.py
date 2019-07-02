from Tkinter import Tk
from tkFileDialog import askopenfilename
import csv

global start_index
global sampleCnt
global totalRead
global wrongID_cnt
global id_tab
global idf
start_index = 0
sampleCnt = 1
totalRead = 0

def getAllLineNo(file):
    '''Count total Lines of input fastq'''
    lineNo = 0
    for line in file:
        lineNo += 1
    return lineNo

def modifyTable(sampleL, binPos):
    global id_tab
    id_tab[binPos][1] = 'T'
    id_tab[binPos][2] += len(sampleL)
    return

def ck_1_mismatch(bc, id_list):
    '''Check the mismatch between input ID and seq ID. 1 mismatch is allowed.Return position of correct ID (in the case of 1 mismatch) for maping'''
    accept = -1
    match = 0
    mismatch = 0
    for i in range(len(id_list)): # loop each ID in the input ID list
        temp = list(id_list[i])
        bc = list(bc)

        for j in range(len(temp)): # loop each base in one bc / ID
            if bc[j] == temp[j]:
                match += 1
            else:
                mismatch += 1

            if mismatch == 2:
                accept = -1
                match = 0
                mismatch = 0
                break
            elif match == (len(temp)-1):
                accept = i
                break
        if accept != -1:
            break

    return accept

def ck_HammingD(mother_str, sub_strList):
    position = 0
    mother_str = list(mother_str)
    match = 0
    mismatch = 0

    for startPosition in range(1 + len(mother_str) - len(sub_strList)):
            shift = startPosition
            position = startPosition
            for z in range(len(sub_strList)): #loop each sub_str base
                if sub_strList[z] == mother_str[shift]:
                    match += 1
                else:
                    mismatch += 1

                shift += 1

                if mismatch == 2:
                    match = 0
                    mismatch = 0
                    position = 0
                    break

                if match == 9:
                    return position
                
    return position

def setDefaultTable(ID_list):
    '''Set a table with content of ID, missing/True, ID count'''
    table = []
    for i in range(len(ID_list)):
        table.append([])
        table[i].append(ID_list[i]) # ID
        table[i].append('M') # M = missing / T = True
        table[i].append(0) # count

    return table

def splitSample(combiList, idList):
    
    lastPos = len(combiList)-1
    endPos = 0
    global start_index 
    global sampleCnt
    sample = []
    for i in range(start_index,len(combiList)): #loop each extracted read in the list
        if i == start_index:
            sample.append(combiList[i])
        elif combiList[i][0] == sample[0][0]:
            sample.append(combiList[i])
        else:
            bingoIndex = idList.index(combiList[start_index][0]) # get the position of ID in input sample ID that match with the seq sample ID
            modifyTable(sample, bingoIndex)
            f = open("sample_"+ str(combiList[start_index][0])+".txt", "wb") # save as text file
            for k in range (len(sample)): # loop each single read in sample
                for j in range(len(sample[k])):
                    f.write(str(sample[k][j]))
                    f.write(" ")
                f.write("\n")
                sampleCnt += 1
            f.close()
            k = 0
            
            start_index = i
            break
        endPos = i

    if endPos == lastPos:
        bingoIndex = idList.index(combiList[start_index][0]) # get the position of ID in input sample ID that match with the seq sample ID
        modifyTable(sample, bingoIndex)
        f = open("sample_"+ str(combiList[start_index][0])+".txt", "wb") # save as text file
        for k in range (len(sample)): # loop each single read in sample
            for j in range(len(sample[k])):
                f.write(str(sample[k][j]))
                f.write(" ")
            f.write("\n")
        f.close()                   

        start_index = endPos+1
        k = 0


    return


def compareIDlist(filename): # input ID file should separate each ID with space
    inputF = open(filename, "r")
    all = inputF.read()
    splitAll = all.split()
    inputF.close()
    return splitAll

def splitSample_for_nonFirst_round(combiList, idList):
    
    lastPos = len(combiList)-1
    endPos = 0
    global start_index
    global sampleCnt
    sample = []
    for i in range(start_index,len(combiList)): #loop each extracted read in the list
        if i == start_index:
            sample.append(combiList[i])
        elif combiList[i][0] == sample[0][0]:
            sample.append(combiList[i])
        else:
            bingoIndex = idList.index(combiList[start_index][0]) # get the position of ID in input sample ID that match with the seq sample ID
            modifyTable(sample, bingoIndex)
            f = open("sample_"+ str(combiList[start_index][0])+".txt", "ab") # save as text file
            for k in range (len(sample)): # loop each single read in sample
                for j in range(len(sample[k])):
                    f.write(str(sample[k][j]))
                    f.write(" ")
                f.write("\n")         
                sampleCnt += 1
            f.close()
            
            start_index = i
            k = 0
            break
        endPos = i

    if endPos == lastPos:
        bingoIndex = idList.index(combiList[start_index][0]) # get the position of ID in input sample ID that match with the seq sample ID
        modifyTable(sample, bingoIndex)
        f = open("sample_"+ str(combiList[start_index][0])+".txt", "ab") # save as text file
        for k in range (len(sample)): # loop each single read in sample
            for j in range(len(sample[k])):
                f.write(str(sample[k][j]))
                f.write(" ")
            f.write("\n")
        f.close()                   

        start_index = endPos+1
        k = 0


    return

def writeCSV_firstRound(idBClist):
    global idf
    idBClist.sort()
    splitSample(idBClist, idf)
    while start_index < len(idBClist):
        splitSample(idBClist, idf)
    return


def writeCSV_non1st_round(idBClist):
    idBClist.sort()
    global idf
    splitSample_for_nonFirst_round(idBClist, idf)
    while start_index < len(idBClist):
        splitSample_for_nonFirst_round(idBClist, idf)
    return

def extract_BC(inputFile, idList, bcLen, linkerLen):
    '''extract BC and sample ID according to "testseq.fastq"'''
    extract = []
    firstRound = True
    fi = open(inputFile, "r")
    i = 0
    read = 0
    wrongID = True
    global wrongID_cnt
    global totalRead
    wrongID_cnt = 0
    cnt_line = 0

    totalLines = getAllLineNo(fi)
    print(totalLines)
    fi.close()

    fi = open(inputFile, "r")

    for line in fi:
        cnt_line += 1
        if cnt_line == totalLines: # reach last line
            # it must be i = 4
            read += 1
            totalRead += 1
            writeCSV_non1st_round(extract)
            extract = []
        
        else:
            if i==0:
                idPos = line.find("#") # return the position of #
                extract.append([])
                extract[read].append(line[idPos+1:idPos+9]) # get sample ID

            
                if extract[read][0] in idList: #ck sample ID correct or not, allow 1 mismatch
                    wrongID = False
                   # print ("correctID")
                elif ck_1_mismatch(extract[read][0], idList) != -1: # mapping ID
                    wrongID = False
                    extract[read][0] = idList[ck_1_mismatch(extract[read][0],idList)]
                    # print ("mismatchID")
                else: # incorrect ID
                    wrongID = True
                    extract.remove(extract[read])
                    read -= 1
                    wrongID_cnt += 1
                   # print ("wrongID")



            if i==1 and wrongID == False:
                # print("i==1 block")
                temp = []
                currentBC_cnt = 1
                bc_start_position = 0
                bc_end_position = bcLen

                while currentBC_cnt <= nwise_num:
                    temp.append(line[bc_start_position:bc_end_position])
                    bc_start_position = bc_start_position + bcLen + linkerLen
                    bc_end_position = bc_end_position + bcLen + linkerLen
                    currentBC_cnt = currentBC_cnt + 1

                for count in range(len(temp)):
                    extract[read].append(temp[count])

                #print (extract[read])
            

            i += 1
            if i==4: # one sample have 4 lines
                i=0
                read += 1
                totalRead += 1
                
                if read == 10000:
                    if firstRound == True:
                        writeCSV_firstRound(extract)
                        extract = []
                        read = 0
                        firstRound = False
                    else:
                        writeCSV_non1st_round(extract)
                        extract = []
                        read = 0
                    
                    global start_index
                    start_index = 0


            if totalRead % 100000 == 0:
                print(totalRead)
    
    
    fi.close()
    return extract 

Tk().withdraw()
op1 = raw_input("Please open a NGS fastq file: " ) 
opfilename = askopenfilename()

op2 = raw_input("Please open the sample ID txt file: ")
idfilename = askopenfilename()

bcLength = raw_input("Barcode length (default is 8): ")
if bcLength == '':
    bcLength = 8
else:
    bcLength = int(bcLength)

linkerLength = raw_input("Linker Length (default is 6): ")
if linkerLength == '':
    linkerLength = 6
else:
    linkerLength = int(linkerLength)

nwise_num = raw_input("Number of barcode in one construct (n-wise?) (default is 2): ")
if nwise_num == '':
    nwise_num = 2
else:
    nwise_num = int(nwise_num)

#consBC = raw_input("10 bases of constant region (default is GANNNCAAGC): ")
#if consBC == '':
#    consBC = 'GANNNCAAGC'
#split_consBC = list(consBC)



# End of user input part

idf = compareIDlist(idfilename)
id_tab = setDefaultTable(idf)

extract_BC(opfilename, idf, bcLength, linkerLength)


sum = 0
for p in range(len(id_tab)):
    sum += id_tab[p][2]

totalRead = sum + wrongID_cnt

fo = open("NGS_analysis.csv", "w")
print >> fo, "Total number of reads: ," + str(totalRead)
print >> fo, "Success reads: ," + str(sum)
print >> fo, "Wrong ID: ," + str(wrongID_cnt)
print >> fo, "Discarded reads: ," + str(totalRead-sum)
print >> fo, ''
print >> fo, "Sample ID,True / Missing,Count" 
for i in range(len(id_tab)):
    print >> fo, str(id_tab[i][0]) + ',' + str(id_tab[i][1]) +',' + str(id_tab[i][2])
fo.close()
