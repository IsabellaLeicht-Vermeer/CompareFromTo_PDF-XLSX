import lib.functions

if __name__ == "__main__":
    dirFile = input("Input file directory including filename (no file extension): ")
    pdfTables = lib.functions.ExtractPDFTables(*lib.functions.GetTables(docDirectory = dirFile + ".pdf"))
    #for i in pdfTables:
    #    print(i)
    #print(len(pdfTables))


    excelTables = lib.functions.GetExcel(docDirectory = dirFile + ".xlsx")
    #for i in excelTables:
    #    print(i)
    #print(len(excelTables))

    parsedExcel = sorted(lib.functions.ParseExcel(excelTables), key=lambda d: d['signal'])
    #for i in parsedExcel:
    #    print(i)
    #print(len(parsedExcel))
    #print("")
    
    parsedPDF = sorted(lib.functions.ParsePDFTables(pdfTables), key=lambda d: d['signal'])
    #for i in parsedPDF:
    #    print(i)
    #print(len(parsedPDF))

    #print("")
    outputCompare = lib.functions.CompareFromTo(parsedExcel, parsedPDF)
    #lib.functions.CompareFromTo(parsedExcel, parsedPDF)
    
    #print("")
    if len(outputCompare[0]) > 0:
        print("Unaccounted for from Excel: ", end="\n")
        for i in (outputCompare[0]):
            print(i)
    else:
        print("Excel sheet is all accounted for!")   


    if len(outputCompare[1]) > 0: 
        print("")
        print("Unaccounted for from PDF: ", end="\n")
        for i in (outputCompare[1]):
            print(i)
    else:
        print("PDF is all accounted for!")
