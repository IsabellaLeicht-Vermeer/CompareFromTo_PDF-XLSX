import pymupdf
import pandas as pd
import copy


def CompareFromTo(excelTable, pdfTable):
    pdfTableMod = copy.deepcopy(pdfTable)

    outExcelInit = []
    outExcelFinal = []
    outPDF = []

    # checks excel against pdf without
    # cable assy gauge correction
    for i in excelTable:
        if i in pdfTable:
            continue
        outExcelInit.append(i)

    # Checks pdf against the excel sheet
    for i in pdfTableMod:

        # assuming the excel table has gauge
        if i in excelTable:
            continue

        # then checks for cable assy making no gauge
        i['wireGauge'] = ''
        if i in excelTable:
            continue    
        outPDF.append(i)

    # checks excel against pdf with
    # cable assy gauge correction
    for i in pdfTableMod:
        i['wireGauge'] = ''
    for i in outExcelInit:
        if i not in pdfTableMod:
            outExcelFinal.append(i)
    return outExcelFinal, outPDF            


def ParsePDFTables(tables):
    colorCorrector = {"OR":"OG", "PU":"VT", "TN":"BG", "YL":"YE"}

    outList = []
    for i in tables:
        for j in i:
            
            # skip undesirable values and correct color acronyms
            if j[1] == "- -":
                continue
            splitVal = j[1].split("-")
            if len(splitVal) < 3:
                continue
            if splitVal[1] in colorCorrector:
                splitVal[1] = colorCorrector[splitVal[1]]
            
            outList.append({"signal":splitVal[0], "designation":i[len(i)-1], "terminal":j[0], "wireColor":splitVal[1], "wireGauge":splitVal[2]})
    return outList
        
    
        
    

def ParseExcel(excelList):
    outList = []
    for i in excelList:
        if (str(i[2])[0:2] != 'SP'):
            outList.append({"signal":i[0], "designation":i[2], "terminal":i[3], "wireColor":i[9], "wireGauge":str(i[8])[4:6]})
        
        if (str(i[5])[0:2] != 'SP'):
            outList.append({"signal":i[0], "designation":i[5], "terminal":i[6], "wireColor":i[9], "wireGauge":str(i[8])[4:6]})
    return outList

def GetExcel(docDirectory = None):
    if docDirectory == None:
        return None
    df = pd.read_excel(docDirectory)
    return (df.values.tolist())[6:-1]

def GetTables(docDirectory = None):
    if docDirectory == None:
        return None
    doc = pymupdf.open(docDirectory, filetype="pdf")
    #doc = pymupdf.open("C:\\Users\\il36825\\Downloads\\163772367_old.pdf", filetype="pdf")


    # arbitrary params, this is just the best i found
    findTableParams = {
        "horizontal_strategy":"lines_strict",
        "vertical_strategy":"lines_strict",
        "snap_y_tolerance":.5,
        "snap_x_tolerance":.5,
        "join_y_tolerance":.5,
        "join_x_tolerance":.5,
        "intersection_y_tolerance":.5,
        "intersection_x_tolerance":.5,
        "text_y_tolerance":.5,
        "text_x_tolerance":.5,
        "edge_min_length":1,
        "clip":None    
    }

    tableStart = 0
    componentNames = []
    tables = []
    totalTables = []
    for docNum in range(0, len(doc)):
        tables.append(pymupdf.find_tables(doc[docNum], **findTableParams).tables)
        for i in range(0, len(tables[docNum])):
            topLeftX = (tables[docNum][i].bbox[0])
            topLeftY = (tables[docNum][i].bbox[1]-22)
            bottomRightX = (tables[docNum][i].bbox[2])
            bottomRightY = (tables[docNum][i].bbox[1])
            rect = pymupdf.Rect(topLeftX, topLeftY, bottomRightX, bottomRightY)
            componentName = (doc[docNum].get_textbox(rect))    
            if ((len(tables[docNum][i].extract()[0]) in range (3, 5)) and (len(tables[docNum][i].extract()[0][1]) != 1)):
                if (tables[docNum][i].extract()[0][0] == 'POS'):
                    totalTables.append(tables[docNum][i].extract()[1:])
                else:
                    totalTables.append(tables[docNum][i].extract())
                totalTables[len(totalTables)-1].append(componentName.partition("\n")[0])


    return totalTables
