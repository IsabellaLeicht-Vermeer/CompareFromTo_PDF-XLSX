import pymupdf
import pandas as pd
import copy


def CompareFromTo(excelTable, pdfTable):
    pdfTableMod = copy.deepcopy(pdfTable)

    outExcelInit = []
    outExcelFinal = []
    outPDF = []

    # Checks from excel table against pdf
    # without worrying about missing gauge
    # from cable assemblies
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

    for i in pdfTableMod:
        i['wireGauge'] = ''
    #print("")
    #print(pdfTableMod)

    # Checks from excel table against pdf
    # while considering gauge missing
    # from cable assemblies
    for i in outExcelInit:
        if i not in pdfTableMod:
            outExcelFinal.append(i)

        
    return outExcelFinal, outPDF            


def ParsePDFTables(tables):
    outList = []
    for i in tables:
        for j in i:
            splitVal = j[1].split("-", 2)
            if len(splitVal) < 3:
                continue
            # gross, don't want to think anymore rn to fix this
            if splitVal[1] == "OR":
                splitVal[1] = "OG"
            elif splitVal[1] == "PU":
                splitVal[1] = "VT"
            elif splitVal[1] == "TN":
                splitVal[1] = "BG"
            elif splitVal[1] == "YL":
                splitVal[1] = "YE"
            
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
    for docNum in range(0, len(doc)):
        tables = pymupdf.find_tables(doc[docNum], **findTableParams)
        for i in range(tableStart, len(tables.tables)):
            topLeftX = (tables.tables[i].bbox[0])
            topLeftY = (tables.tables[i].bbox[1]-22)
            bottomRightX = tables.tables[i].bbox[2]
            bottomRightY = tables.tables[i].bbox[1]
            rect = pymupdf.Rect(topLeftX, topLeftY, bottomRightX, bottomRightY)
            componentNames.append((doc[docNum].get_textbox(rect)))
    

    return tables, componentNames
       
def ExtractPDFTables(tables, componentNames):
    totalTables = []
    for i in range(0, len(tables.tables)):
        if ((len(tables[i].extract()[0]) in range (3, 5)) and (len(tables[i].extract()[0][1]) != 1)):
            if (tables[i].extract()[0][0] == 'POS'):
                totalTables.append(tables[i].extract()[1:])
            else:
                totalTables.append(tables[i].extract())
            totalTables[len(totalTables)-1].append(componentNames[i].partition("\n")[0])
    return totalTables
