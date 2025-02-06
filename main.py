import lib.functions

if __name__ == "__main__":
    dirFile = input("Input file directory including filename (no file extension): ")
    pdfTables = (lib.functions.GetTables(docDirectory = dirFile + ".pdf"))
    excelTables = lib.functions.GetExcel(docDirectory = dirFile + ".xlsx")
    parsedExcel = sorted(lib.functions.ParseExcel(excelTables), key=lambda d: d['signal'])
    parsedPDF = sorted(lib.functions.ParsePDFTables(pdfTables), key=lambda d: d['signal'])
    outputCompare = lib.functions.CompareFromTo(parsedExcel, parsedPDF)
    

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
