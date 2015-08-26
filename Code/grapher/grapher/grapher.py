#For network analysis and pickle
import pickle
import snap

#Specify the input file
basic = open('basic.txt','r')

#Export file for the map
map = open('map.pckl','w')
hashes = open('hashes.pckl','w')

#create the graph
G2 = snap.TNGraph.New()

#index counter for number of nodes
i = 0

#is this a unique entry
q = True

#tokens to determine how to clasify the links
tokOpen = '[['
tokCol = ':'
tokBar = "|"
tokEnd = ']]'

#hash table for checking link duplication
h = snap.TIntStrH()

#for every line
for line in basic:

    #find if the line contains links or titles
    obsOpen = line.find(tokOpen)

    #if it is a title
    if obsOpen<0:
        
        #reset the unique entry
        q = True

        #reset the index counter
        n = 0
        
        #for every index in the hashtable
        for n in range(0,h.Len()):

            #if an index exists that matches
            if h[n] == str(line):

                #this is not a unique entry
                q = False         
                       
                #record the title index anyway
                titleIndex = n

                #stop searching
                break

        #if it is a unique entry
        if q == True:

            #add the unique entry to the hashtable
            h[i] = str(line)

            #and to the graph
            G2.AddNode(i)

            #record the title index
            titleIndex = i

            #increment the number of nodes
            i = i+1
            print(str(i))

    #empty the text holder 

    #while there is a still an undiscovered [[ in the line                                                                                                                            
    while obsOpen>0:

        #find a colon in the current link         
        obsCol = line.find(tokCol,obsOpen+2)
        
        #find a pipe | in the current link
        obsBar = line.find(tokBar,obsOpen+2)
        
        #if there is a colon
        if obsCol>0:
            
            #disregard this link and start finding in the next one
            obsOpen = line.find(tokOpen, obsOpen+2)
            
            #and jump to the next iteration (I think we can remove the previous 'if link needs to be writte n' if we put it after this break)
            break

        #if there is a pipe |
        elif obsBar>0:
            
            #take stuff up to the pipe |
            text = line[obsOpen+2:obsBar]
            
            #and start finding the next link
            obsOpen = line.find(tokOpen, obsOpen+2)
        
        #otherwise
        else:
        
            #find the end of the link
            obsEnd = line.find(tokEnd,obsOpen)
            
            #take just the link text
            text = line[obsOpen+2:obsEnd]
            
            #and find the next link
            obsOpen = line.find(tokOpen, obsOpen+2)

        #reset the unique entry indentifier
        q = True

        #reset the index counter
        n = 0

        #for every entry in the graph
        for n in range(0,h.Len()):

            #if this is the duplicate entry
            if h[n] == str(text):

                #note it
                q = False

                #record the link to index
                currIndex = n

                #stop searching
                break
            
        #if this a unique entry    
        if q == True:

            #put it in the hashtable
            h[i] = str(text)
                
            #add it to the graph
            G2.AddNode(i)

            #record the link to index
            currIndex = i

            #and increment the index
            i = i+1
            print(str(i))
        #assign the link
        G2.AddEdge(titleIndex,currIndex)
        print(str(currIndex))             
              
#dump the data
pickle.dump(G2,map)
pickle.dump(h,hashes)

#close the files
map.close
h.close
basic.close        
