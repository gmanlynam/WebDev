    
def cWordLists():
   with open('/usr/share/dict/words') as wordList:
      with open('7_bigger_wordList','w') as aList: 
         with open('3_7_wordList','w') as bList: 
            i = 0
            for line in wordList:
               line = line[:-1]
               if len(line) >= 7:
                  #line = line[:-1]   
                  i += 1       
                  print(line, file=aList)
               if len(line) >= 3 and len(line) <= 7:
                  print(line, file=bList)
            return i

num = cWordLists()        
print(num)

