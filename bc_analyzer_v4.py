from Tkinter import Tk
from tkFileDialog import askopenfilenames
from tkFileDialog import askopenfilename

global totalRead
global totalDiscard
global totalSuccess
global cntLine
global rubbish_cnt
totalRead = 0
totalDiscard = 0
totalSuccess = 0
posBC_list_F_name = []

def ck_mismatch(bc, listBC): # output: 'yes' for discard || mapped correct barcode
    discard = "yes"
    match = 0
    mismatch = 0
    bc = list(bc)
    bcLen = len(bc)
    for i in range(len(listBC)): # loop every single bc in list
        temp = list(listBC[i])
        for j in range(len(temp)): # loop every base in each BC
            if bc[j] == temp[j]:
                match += 1
                if match == bcLen-1:
                    return listBC[i]
            else:
                mismatch += 1
                if mismatch == 2:
                    match = 0
                    mismatch = 0
                    break
    return discard # double confirmed, logic correct

def correctBC(bc, libBCList): # output: correct bc or 'discard'
    
    barcode = bc
    if barcode in libBCList:
        return barcode
    else:
        barcode = ck_mismatch(barcode,libBCList) # barcode = barcode or "yes"
        if barcode != "yes":
            return barcode
        else:
            barcode = "discard"

    return barcode

def main(filename, positionBC_list_fileNames):
    global cntLine
    global rubbish_cnt
    fi = open(filename, "r")
    data = [] # all data including ID, combinations and count will be stored in this list
    data.append([]) # ID
    data.append([]) # combination
    data.append([]) # count
    cntLine = 0
    rubbish_cnt = 0
    empty = True
    posBC_list = [] # store all the position BC from last position to first position

    for posBC in range(len(positionBC_list_fileNames)): # open position BC files and assign them to posBC_list []
        posBC_list.append([]) # position BC list of one position
        fileOpen = open(positionBC_list_fileNames[posBC], "r")
        posBC_list[posBC] = fileOpen.read().split('\n')
        fileOpen.close()



    for line in fi:
        successBC = []
        if cntLine == 0:
            read = line.split(' ')
            read.remove('\n')
            data[0] = read[0] # get the sample ID once
            read.remove(read[0])
            # cntLine = 1
        else:
            read = line.split(' ')
            read.remove('\n')
            read.remove(read[0])
            # print(str(len(read)))
        
            # read[] is a list to store barcode only, no ID

        for i in range(len(read)): #check for mismatch and correct to the match one
            read[i] = correctBC(read[i], posBC_list[i])
            if read[i] != "discard":
                successBC.append(read[i])
            else:
                successBC = []
                rubbish_cnt += 1
                break

        if successBC == []:
            pass # go to next line
        elif empty == True:
            data[1].append(successBC) # store barcode
            data[2].append(1) # store count
            empty = False
        else:
            if successBC in data[1]:
                index = data[1].index(successBC)
                data[2][index] += 1
            else:
                data[1].append(successBC)
                data[2].append(1)
        
        cntLine += 1
        
        print(str(cntLine))

    return data









Tk().withdraw()
opM = raw_input("Please enter sample file(s): ")
opfilenames = askopenfilenames() # allow multiple files input
# opL = raw_input("Please enter a text file for barcode library: ")
# opbclibname = askopenfilename()

ask_n_wise = raw_input("How many barcode in each read? (default is 4): ")
if ask_n_wise == '':
    ask_n_wise = 4
else:
    ask_n_wise = int(ask_n_wise)

pos = ask_n_wise

for count_n in range(ask_n_wise): #loop for input position BC list start from last position
    msg = raw_input("Position "+ str(pos) +" barcode list (text file): ")
    pos_BC = askopenfilename()
    posBC_list_F_name.append(pos_BC)
    pos -= 1


# End of user input

# libF = open(opbclibname,"r")
# lib = libF.read().split('\n')
# libF.close()

for i in range(len(opfilenames)): # save the output in a csv file
    outputList = main(opfilenames[i], posBC_list_F_name) # process each file one by one
    saveFname = opfilenames[i]
    if i <= 9:
        saveFname = saveFname[-19:-4]
    else:
        saveFname = saveFname[-19:-4]
    cnt_success = 0
    totalRead += cntLine
    totalDiscard += rubbish_cnt
    for p in range(len(outputList[2])):
        cnt_success += outputList[2][p]

    
    totalSuccess += cnt_success

    fo = open(saveFname + "_count.csv", "w")
    print >> fo, "Sample ID: ," + outputList[0]
    print >> fo, "Input count: ," + str(cntLine)
    print >> fo, "Combinations: ," + str(len(outputList[1]))
    print >> fo, "Success count: ," + str(cnt_success)
    print >> fo, "Discard count: ," + str(rubbish_cnt)
    print >> fo, ''
    print >> fo, "Combination,,,,,Count"
    for y in range(len(outputList[1])):
        toString = ''
        for k in range(len(outputList[1][y])):
            toString = toString + str(outputList[1][y][k]) + ","
        print >> fo, toString + ',' + str(outputList[2][y])

fr = open("Count Report.csv","w")
print >> fr, "Total Input Reads: ," + str(totalRead)
print >> fr, "Total Success reads: ," + str(totalSuccess)
print >> fr, "Total Discard count: " + str(totalDiscard)
