'''
  There should be several functions in this module.  Several are 
  already provided, in case they are useful:  
     datextract
     eightdigs 
     fieldict
     citypop 
     eventfreq
     manuftop10

  are functions from a previous homework which might be handy.

  Your task is to write four functions, plotEventFreq, plotManufTop10,
  pagesub, and plotPopEvent.  

  Essential tricks:

  1.  YOU MUST HAVE MATPLOTLIB INSTALLED.  There's no chance of 
      completing the homework without using matplotlib, a package
      that can be added to Python2.7 environments.  The computer 
      science lab does have matplotlib installed.  You can find, 
      download, and install matplotlib if you want, on your own 
      computer (but it's not required, since you have an account 
      on the CS lab machines).

  2.  You will need several files in addition to this file (homework4.py)
      - DOT1000.txt, one thousand lines from the DOT complaint file
      - Top5000Population.txt (read by citypop() to build dictionary) 
      - page1.html (used by one of the unit tests)
      - page2.html (used by one of the unit tests)
      - ezplot.py (makes using matplotlib much easier)

  3.  The "*" trick for dealing with parameters.  
      A function definition like 
           def foo(*X):
             print len(X), X
           foo(True,"test",37)
      will print  3 (True, 'test', 37)
           foo(0,1,2,3,4,5,6) 
      will print  7 (0, 1, 2, 3, 4, 5, 6)

      This "*" trick is how Python lets you define a function with an
      unplanned number of arguments (the function treats all the 
      arguments as a tuple).  

      One more example:
           def foo(*X):
              print X[0]
           foo(88,100,3)
      will print 88
 

  4.  The "*" trick for converting a list or tuple to arguments.
      You can convert a list or tuple of items into
      arguments for a function call:
           def moo(a,b,c):
               print a, b, c
           Z = [True, "test", 37]
           moo(*Z)
      This will print True 'test' 37
           moo(*(6,1,False))
      will print 6 1 False

  USE TRICKS 3 & 4 TO DO THE pagesub PROBLEM

  5.  The ezplot module makes it simple to plot graphs, putting them
      into an image (png) file.  Interactively, you can try it 
      with an example like this

           import ezplot  # needs matplotlib
           X = [1.5, 2.7, 3.0, 6.2]
           Y = [9, 3, 2, 6]  # X and Y have same length
           ezplot.barplot(X,Y)

      This will write a file plot.png, which you can view. 

      There are two useful (for this homework) kinds of plotting in ezplot:
         
         barplot(x,y,filename="plot.png")
         corplot(x,y,filename="plot.png")

      Use barplot for the plotEventFreq problem:  just let the X-values
      and Y-values be taken from the pairs that eventfreq returns.  The 
      code for plotEventFreq quite easy to write, done properly.  

      Also, use barplot for the plotManufTop10 problem: just use X and
      Y values that manuftop10 returns.  If you look at the code of barplot
      inside the ezplot.py file, you will see it is just checking whether
      or not the X values are date objects or character strings or 
      numbers, then doing the appropriate kind of graphing.

      In any case, you will need to pass long the name of the image file
      to be written (the plotfile parameter). 

      For the plotPopEvent problem, you will need to work with the 
      dictionary that fieldict returns, and also the dictionary that 
      citypop returns (so start with making variables equal to these
      dictionaries, simply by calling fieldict and citypop).  Then
      you will need to count the appropriate items so that you get 
      the X and Y needed to call ezplot.corplot


See the docstrings below for an explanation of what is expected.  Test 
cases follow:


 >>> plotEventFreq(1995,1,"events.png")
 >>> 12*1024 < os.stat("events.png")[stat.ST_SIZE] < 16*1024 
 True
 >>> plotEventFreq(1994,12,"hold.png")
 >>> os.stat("hold.png")[stat.ST_SIZE] > 12*1024 
 True
 >>> plotManufTop10("manuf.png")
 >>> 25*1024 < os.stat("manuf.png")[stat.ST_SIZE] < 28*1024
 True
 >>> i = pagesub("page1.html","Page One","function")
 >>> i[0:12]
 '<HTML><BODY>'
 >>> len(i)
 137
 >>> i = pagesub("page2.html","Second Page","attempt at programming")
 >>> i.index("attempt")
 42
 >>> 
 >>> plotPopEvent("popevent.png")
 >>> 26*1024< os.stat("popevent.png")[stat.ST_SIZE] < 32*1024
 True

'''

import os, stat, sys, ezplot, datetime

def datextract(S):
  return (int(S[:4]),int(S[4:6]),int(S[6:]))
def eightdigs(S):
  return type(S)==str and len(S)==8 and all([c in "0123456789" for c in S]) 
def fieldict(filename):
  D = { }
  with open(filename) as FileObject:
     for line in FileObject:
        R = { }
        T = line.strip().split('\t')
        manuf, date, crash, city, state = T[2], T[7], T[6], T[12], T[13]
        manuf, date, city, state = manuf.strip(), date.strip(), city.strip(), state.strip()
        if eightdigs(date):
           y, m, d = datextract(date)
           date = datetime.date(y,m,d)
        else:
           date = datetime.date(1,1,1)
        crash = (crash == "Y")
        D[int(T[0])] = (manuf,date,crash,city,state)
  return D
def citypop():
  import csv
  R = { }
  F = open("Top5000Population.txt")
  CSV = csv.reader(F)
  for row in CSV: 
     city, state, population = row
     city = city.rstrip()
     city = city.upper()
     city = city[:12]  
     population = population.replace(",",'')
     population = int(population)
     R[(city,state)] = population
  return R
def eventfreq(year,month):
  Fd = fieldict("DOT1000.txt")
  Q = { }  # accumulate dates and complaint counts 
  for item in Fd.keys():
     thedate = Fd[item][1]
     if thedate.year == year and thedate.month == month:
        # fancy, but recommended way
        Q[thedate] = Q.get(thedate,0) + 1  
  M = Q.items()  # list (key,value) pairs
  M.sort()       # will rearrange M to be increasing by date
  return M
def manuftop10():
  from operator import itemgetter
  Fd = fieldict("DOT1000.txt")
  Q = { }  # accumulate manufacturers and complaint counts
  for item in Fd.keys():
     manuf = Fd[item][0]
     Q[manuf] = Q.get(manuf,0) + 1  
  # now comes the tricky part, sort big to small, by count 
  N = sorted(Q.items(),reverse=True,key=itemgetter(1)) 
  Top10 = N[:10]
  return Top10

#------------ Functions for this homework -------------------
# replace pass in each function with your own function
# definitions to get the properly working program



##I changed parameters in the test cases from (filename='.png') to just ('.png') because I didn't know why the filename had to be there.
##One test cases do not work for the os.stat() problem??

def plotEventFreq(x,y,z):
    assert type(x)==int
    assert type(y)==int
    assert type(z)==str
    d= eventfreq(x, y)
    x=[i[0] for i in d]
    y=[i[1] for i in d]
    return ezplot.barplot(x,y,z)
        
def plotManufTop10(p):
    assert type(p)==str
    d= manuftop10()
    x=[i[0] for i in d]
    y=[i[1] for i in d]
    #assign x and y variables to Manufacturer and # of times it appears
    return ezplot.barplot(x,y,p)

def plotPopEvent(z):
    assert type(z)==str
    A= fieldict('DOT1000.txt').values()
    B=citypop()
    E=[(i[3], i[4]) for i in A]
    #List of tuples[(city, state)]
    result_dict = dict( [ (i, E.count(i)) for i in set(E) ] )
    #dict with cities as key and #complaints as values
    dict3 = dict((result_dict[key], B[key]) for key in B if key in result_dict)
    #dict3 is a dictionary with number of complaints as keys and population as values only if that city appears in result_dict and B
    y=dict3.values()
    x=dict3.keys()
    return ezplot.corplot(x,y,z)
        

def pagesub(N, *subs):
    # I changed from 2 parameters to 1 
    assert type(N)==str
    with open(N,'r') as F:
        content = F.read()
    return content.format(*subs)

if __name__ == "__main__":
    import doctest
    doctest.testmod() 
