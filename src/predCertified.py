import sys
import os

# predCertified.py
# Implements a class that facilitates efficient computation of statistics from a CSV file.
# Functions exist to find the column indices of desired data, generate a histogram of entires
# for these columns, and output sorted data to a file. 
class predCertified():

    def __init__(self, file_dir):
        self.file_dir = file_dir
    
    # find the index of status, WORKSITE_STATE / SOC_NAME

    def desireItems(self, dsrItems):
        idxTracker = []

    # file exception handling
        try:
    # encode to UTF-8
            with open(self.file_dir, encoding="utf8") as file:
    # only read the first line of the file, and also get rid of "\n" delimiter
    # seperate the first line with the ; delimiter
                title = file.readline().rstrip().split(";") 
    # print error message        
        except FileNotFoundError as file_error:
            print("something is wrong!", file_error)
    # if file gets found, then continue
        else:
            for n, value in enumerate(title):
    # the status may not be exactly the same, sometimes could be "STATUS_CASE"
    # so to find the exact words by getting rid of the noise
                try:
                    if any(item in value for item in dsrItems):
                        idxTracker.append(n)
                except:
                    print("no such columns")
            tracker = {key: value for key, value in zip(dsrItems, idxTracker)}
    # find the index of the instered items, in this case, STATUS, WORKSITE_STATE, SOC_NAME
            dsr_idx = list(tracker.values())
        
            return dsr_idx

    # find the insterested items with certified STATUS
    def stJob_Cer(self, idx):

    # claim a dictionary to track the instereted items with certified STATUS
    
        stJob_dict = {}


        with open(self.file_dir, encoding="utf8") as file:
    # ignore the csv title (first row)
            next(file)
            for line in file:
    # separate each row the ; delimiter
                words = line.rstrip().split(";")
                
    # use the first element of idx to identify the STATUS
                if words[idx[0]] == "CERTIFIED":
                    # if the items string has delimiter "", get rid of it
                    words[idx[1]] = words[idx[1]].replace('"','')
    # calculate the times for each interested items (state, job title) appear
    # make sure the item value is not empty
                    if words[idx[1]] != "":

                        if words[idx[1]] not in stJob_dict:
                            stJob_dict[words[idx[1]]] = 1
                        else:
                            stJob_dict[words[idx[1]]] += 1

            return stJob_dict

    # find the top 10 items and store the names and values separately
    def topTen(self, dictry):


        perc = []
    # sort the dictionary in a descending order based on the values
        dic = sorted(dictry.items(), key=lambda k: k[1], reverse=True)
    # get the top 10 items based on the values in the dictionary
        if len(dic) < 10:
            temp = len(dic)
        else:
            temp = 10
        for i in range(temp):
            perc.append(dic[i])
    # iterate the perc and store the item names and values into restName and restValue
        restName = []
        restValue = []
        for name, values in perc:
            restName.append(name)
            restValue.append(values)

        return restName, restValue

    # count all the certified item (WORKSITE_STATE / SOC_NAME)
    def allCertified(self, dictry_t):


        perc_t = []
        dic_t = sorted(dictry_t.items(), key=lambda k: k[1], reverse=True)
    # get all the values with certified item
        for i in range(len(dic_t)):
            perc_t.append(dic_t[i][1])
        percSum = sum(perc_t)
        return percSum


    # calculate the ratio, ratio = top 10 certified items / all certified items
    def topRatio(self, topTen, certified):

        topRatio = []

        for i in range(len(topTen)):
            temp = (topTen[i] / certified) * 100
     # round the number and format it
            temp = '{0:.1f}%'.format(round(temp))
            topRatio.append(temp)
        return topRatio


    # put the item, name and ratio and read them into a list    
    def prepTxt(self, topTenName, topTenValue, ratioF):
    
        list4Txt = []
        for m, n, l in zip(topTenName, topTenValue, ratioF):
            list4Txt.append("{0};{1};{2}".format(m, n, l))

        return list4Txt
    
    # write an output txt file
    def w2Txt(self, firstItem, fileName, inputList):
        
        # sort the list with the interested items with ascending order, then descending order when
        # the interested items are equal.
        
        # check if the item string has multiple words with space delimiter when the first word
        # in the string is equal

        for i in range(len(inputList)):
            # if the item string has multiple words with space delimiter when the first word in
            # the string is equal, then it sorts based on the second word
            if ' ' in inputList[i].split(";")[0]:
                inputList.sort(key = lambda x: (x.split(";")[1],
                                        -ord(x.split(";")[0][0]), -ord(x.split(";")[0].split(" ")[1][0])), reverse=True)
            
            else:
                inputList.sort(key = lambda x: (x.split(";")[1], -ord(x.split(";")[0][0])), reverse=True)
        with open(fileName, 'w') as file1:
            file1.write(firstItem + ";NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE\n")
            for line in inputList:
                file1.write(line + "\n")
        file1.close()
    
    # encapsulate the previous few functions
    def getResults(self, dsrItem):
                   
        dsr_idx = self.desireItems(dsrItems)
        stJob_dict = self.stJob_Cer(dsr_idx)
        topTen_name, topTen_value = self.topTen(stJob_dict)
        perSum = self.allCertified(stJob_dict)
        topRatio = self.topRatio(topTen_value, perSum)
        list4Txt = self.prepTxt(topTen_name, topTen_value, topRatio)

        return list4Txt



if __name__ == "__main__":
    
    # input arguments checking
    if (len(sys.argv) != 4):
        print("Usage: predCertified.py InputFilename OccupationOutputFile StateOutputFile")

        sys.exit(0)


    pred = predCertified(sys.argv[1])

    # find the certified job
    dsrItems = ["STATUS", "SOC_NAME"]
    list4Txt = pred.getResults(dsrItems)
    pred.w2Txt("TOP_OCCUPATIONS", sys.argv[2], list4Txt)

    # find the certified state
    dsrItems = ["STATUS", "WORKSITE_STATE"]
    list4Txt = pred.getResults(dsrItems)
    pred.w2Txt("TOP_STATES", sys.argv[3], list4Txt)



