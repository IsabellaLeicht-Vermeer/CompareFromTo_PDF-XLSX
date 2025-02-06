#TODO
Implement detection and merge of split-tables on PDF\ 
Test on more documents and note any issues\
general cleanup stuff\
figure out a better way to deal with cable assies that don't contain wire gauge\


#How to Use
First time users:\
    install python3\
    run command "pip -r requirements.txt" from project directory\
  
run command "python .\main.py" from project directory\
Enter full directory path of file FromTo docs (including filename but excluding file extension)\
    Example: C:\Users\il36825\Documents\storage\ECNs\284719\163772367 \

Script will output any entries that it doesn't see on the other document.\
    If a PDF has connector P123 with wire 456-CR-14 on terminal 1 but doesn't see that on the excel sheet, it will output that info\
        same vice-versa\


