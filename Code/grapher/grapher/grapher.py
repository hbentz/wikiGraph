#For network analysis and pickle
import pickle
import snap

#Specify the input file
basic = open('basic.txt','r')

#create the graph
G2 = snap.TNGraph.New()

#index counter for number of nodes
i = 0
an = 0
skipNextxNodeCreations = 0

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

    incr = False

    #find if the line contains links or titles
    obsOpen = line.find(tokOpen)

    #if it is a title
    if obsOpen<0:
        line = line[:-2]
        print('Checking if '+line+' exists as a node (article number '+str(an)+')')

        #reset the unique entry
        q = True

        #reset the index counter
        n = 0
        
        #for every index in the hashtable
        for n in range(0,h.Len()):

            #if an index exists that matches
            if h[n] == line:

                #this is not a unique entry
                q = False         
                       
                #record the title index anyway
                titleIndex = n
                print(line+' already exists at node '+str(n))

                #stop searching
                break

        #if it is a unique entry
        if q == True:

            #add the unique entry to the hashtable
            h[i] = line

            #and to the graph
            if skipNextxNodeCreations>0:
                skipNextxNodeCreations=skipNextxNodeCreations-1
                print('Unique node creation for article number '+str(an)+' was skipped because node '+str(i)+' already exists')
            else:
                G2.AddNode(i)
            #record the title index
            titleIndex = i

            #increment the number of nodes
            print(line+' has been assigned to node '+ str(i))
            i = i+1
            
        
        an = an+1
        #skip the rest of the loop
        continue
    
    text = ''

    #while there is a still an undiscovered [[ in the line                                                                                                                            
    while obsOpen>0:

        #find the end of the link
        obsEnd = line.find(tokEnd,obsOpen+2)
        
        clicky = line[obsOpen+2:obsEnd]

        #find a colon in the current link         
        obsCol = clicky.find(tokCol)
        
        #find a pipe | in the current link
        obsBar = clicky.find(tokBar)
        
        #if there is a colon
        if obsCol>0 & (obsCol<obsBar | obsBar<0):
            
            #disregard this link and start finding in the next one
            obsOpen = line.find(tokOpen, obsOpen+2)
            
            #and jump to the next iteration (I think we can remove the previous 'if link needs to be written' if we put it after this break)
            break

        #if there is a pipe |
        elif obsBar>0:
            
            #take stuff up to the pipe |
            text = clicky[0:obsBar]
            
            #and start finding the next link
            obsOpen = line.find(tokOpen, obsOpen+2)
        
        #otherwise
        else:
       
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
            if h[n] == text:

                #note it
                q = False

                #record the link to index
                currIndex = n
                print('Found '+text+' at index '+str(n)+' assigning appropriate links...')
                #stop searching
                break
            
        #if this a unique entry    
        if q == True:

            #put it in the hashtable
            h[i] = text
                
            #add it to the graph
            if skipNextxNodeCreations>0:
                skipNextxNodeCreations=skipNextxNodeCreations-1
                print('Unique node creation for target '+text+' was skipped because node '+str(i)+' already exists')
            else:
                G2.AddNode(i)
            #record the link to index
            currIndex = i

            #and increment the index
            print(text+' was assigned as a unique entry at index '+str(i))
            i = i+1
        #assign the link
        G2.AddEdge(titleIndex,currIndex)
        print('An edge was created between nodes '+str(titleIndex)+' and '+str(currIndex))
                 
    if text == '':
        print('No edges were created for article number '+str(an-1))
        i = i-1
        skipNextxNodeCreations=skipNextxNodeCreations+1   
        print('The hash table index has been decremented to componsate, the next '+str(skipNextxNodeCreations)+' Node creations will be sklipped')                    
              
#Export file for the map
map = TFOut('map.graph')
G2.Save(map)

hashes = open('hashes.pckl','w')
pickle.dump(h,hashes)

#close the files
basic.close
hashes.close