#For network analysis
import snap

#Specify the tokens that gives wiki links
tok1 = '[['
tok2 = ']]'

#Specify the tokens that indicate a new page
tok3 = '<title>'
tok4 = '</title>'
i = 0;

#Specify the output file
basic = open('basic.txt','w')

#specify the wikixml file
with open("wiki.xml",'r') as infile:

    #for each line in the wiki file
    for line in infile:
        #try to find the 'new entry' token
        tok3p = line.find(tok3)

        #if this line is a new page
        if tok3p > 0:
            #find the end of the title
            tok4p = line.find(tok4)
            i = i+1
            #write that line to the output file
            basic.write('\r\n'+line[tok3p+7:tok4p:1]+'\r\n')
            print(str(i)+'  '+line[tok3p+7:tok4p:1])
        else:
            #otherwise try and find a link
            tok1p = line.find(tok1)

            #and the end of the link
            tok2p = line.find(tok2)

            #while there is still a link in the line
            while tok1p>0:

                #write that link to the output file
                basic.write(' '+line[tok1p:tok2p+2:1])
                
                #find the next link and the end of that link
                tok1p = line.find(tok1, tok1p+2)
                tok2p = line.find(tok2, tok2p+2)
#close the file
basic.close        
