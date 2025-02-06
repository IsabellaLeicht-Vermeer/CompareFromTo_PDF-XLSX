import pymupdf


docDirectory = input("Input full directory and name of file: ")
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

totalTables = 0
for docNum in range(0, len(doc)):

    tables = pymupdf.find_tables(doc[docNum], **findTableParams)
    
    for i in range(0, len(tables.tables)):
        if ((len(tables[i].extract()[0]) in range (3, 5)) and (len(tables[i].extract()[0][1]) > 1)):
            if (tables[i].extract()[0][0] == 'POS'):
                print(tables[i].extract()[1:])
            else:
                print(tables[i].extract())
            totalTables = totalTables + 1
print(totalTables)
