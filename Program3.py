'''
  There should be several functions in this module.  Two are 
  already provided, in case they are useful:  
     datextract
     eightdigs 
     fieldict
  are functions from a previous homework which might be handy.

  Essential tricks:

     CSV FILES

     One of the data files is a Comma Separated File 
     (see http://en.wikipedia.org/wiki/Comma-separated_values if needed)

     Python has a module, the csv module, for reading and writing csv files.
     Some information is found in these two links:
         http://docs.python.org/2/library/csv.html
         http://www.doughellmann.com/PyMOTW/csv/

     In case you don't read these, the brief example is this:

        import csv
        F = open("somedata.csv")  # open a CSV file
	csvF = csv.reader(F)      # makes a "csv reader" object
	for row in csvF:
	   print row              # row is a tuple of the CSV fields (per line) 

     The beauty of this csv module is that it can handle ugly CSF records like:

        Washer Assembly, 2504, "on order", "2,405,318"

     Notice that this has four fields, separated by commas.  But we cannot use
     an expression like  line.split(',') to get the four fields!  The reason is
     that Python will try to also split the last field, which contains commas.
     The csv reader is smarter.  It will respect the quoted fields.

     Each row that a csv reader produces is a tuple of strings.  

     So how can you convert a string like '2,405,318' to a number?  
     There are two simple ideas:
        
	1.  x = field[2].split(',') 
	    x = ''.join(x)  # comma is gone!
	    x = int(x)
	2.  x = field[2].replace(',','')  # replace comma by empty
	    x = int(x)



     SORTING BY FIELD

     Suppose you have a list of tuples, like M = [("X",50,3),("Y",3,6),("J",35,0)] 
     What is needed, however is to make a sorted version of M, sorted by the second
     item of the tuples.  That is, we want N = [("Y",3,6),("J",35,0),("X",50,3)]. 

     The problem is that if we just write N = sorted(M), we will get the tuples
     sorted by the first item, so N would be  [("J",35,0),("X",50,3),("Y",3,6)]

     Is there some way to tell Python's sort which of the items to use for sorting?
     YES!  There's even a page on the subject: 
        http://wiki.python.org/moin/HowTo/Sorting/
     But a brief example is helpful here.  The idea is to use keyword arguments
     and another Python module, the operator module.  

     Here's the example:

        from operator import itemgetter  # used to customize sorting
	N = sorted(M,key=itemgetter(1))  # says to use item 1 (0 is first item)

     This will give us the needed result in variable N.  What if, instead, we
     wanted the result to be in decreasing order, rather than increasing order?
     Another keyword argument does that:

	N = sorted(M,key=itemgetter(1),reverse=True)  



     DICTIONARY ACCUMULATION

     What if we need to build a dictionary where the key comes from some part
     of a record in a file, and the value is the number of records that have
     the same thing for that part.  Maybe, if we are counting states (with 
     two-letter abbreviations), the dictionary might be something like this:

         {'CA':620978, 'NY':583719, 'IA':2149}

     This dictionary could be the result of reading through a data file that
     had 620,978 records for California and 583,719 records for New York (plus
     some for Iowa).  As an example of creating this dictionary, consider a 
     data file with the state abbreviation as the first field of each record.

        D = { }  # empty dictionary for accumulation
	for line in sys.stdin:  # data file is standard input 
	   st = line.split()[0] # get state abbreviation
	   if st not in D.keys():
	      D[st] = 1   # first time for this state, count is 1
	   else:
	      D[st] += 1

     There is another way to do the same thing, using a more advanced idea: 
     the get() method of the dictionary type, which has a default value argument.

        D = { }  # empty dictionary for accumulation
	for line in sys.stdin:  # data file is standard input 
	   st = line.split()[0] # get state abbreviation
           D[st] = D.get(st,0) + 1

     What you see above is D.get(st,0), which attempts to get the value D[st], 
     but will return 0 if st is not in the dictionary.  The trick here is that
     0+1 is 1, which is the right value to store into D[st] for the first time 
     a state abbreviation is found while reading the dictionary.  It is a tricky
     idea, which some Python programmers like.


     DATETIME.DATE BREAKDOWN

     Suppose G is a datetime.date object, for instance
         import datetime
         G = datetime.date(2012,12,1)  # This is 1st December, 2012
     In a program, can you get the year, month and day as integers
     out of the datetime.date object G?  Yes, it's easy:

         1 + G.year  # G.year is an integer, equal to the year
	 # expression above is "next year"

     Similarly, G.month is the month as an integer, and G.day is the day.


The task is to write three functions, citypop, eventfreq, and manuftop10.

See the docstrings below for an explanation of what is expected.  Test 
cases follow:

  >>> citypopdict = citypop()
  >>> len(citypopdict)
  4991
  >>> citypopdict[ ('DES MOINES','IA') ]
  197052
  >>> citypopdict[ ('CORALVILLE','IA') ] 
  18478
  >>> citypopdict[ ('STOCKTON','CA') ] 
  287037
  >>> evlist = eventfreq(1995,1)
  >>> len(evlist)
  17
  >>> evlist[0]
  (datetime.date(1995, 1, 1), 5)
  >>> evlist[14]
  (datetime.date(1995, 1, 15), 1)
  >>> len(eventfreq(1994,12))
  22
  >>> len(eventfreq(2012,2))
  0
  >>> manlist = manuftop10()
  >>> len(manlist)
  10
  >>> manlist[3]
  ('HONDA (AMERICAN HONDA MOTOR CO.)', 67)
  >>> manlist[8]
  ('MITSUBISHI MOTORS NORTH AMERICA, INC.', 16)

'''

def datextract(S):
  return (int(S[:4]),int(S[4:6]),int(S[6:]))
def eightdigs(S):
  return type(S)==str and len(S)==8 and all([c in "0123456789" for c in S]) 

def citylist(filename):
  with open(filename) as FileObject:
     X = []
     for line in FileObject:
          T = line.strip().split('\t')
          city = T[12].strip()
          X.append(city)
  return X

def statecount(filename):
  with open(filename) as FileObject:
     D = { }
     for line in FileObject:
          T = line.strip().split('\t')
          state = T[13]
          D[state] = 1 + D.get(state,0)
  return D

def fieldict(filename):
  '''
  Returns a dictionary with record ID (integer) as
  key, and a tuple as value.  The tuple has this form:
         (manufacturer, date, crash, city, state)
  where date is a datetime.date object, crash is a boolean, 
  and other tuple items are strings.
  '''
  import datetime
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

### Struggled with these ....Best I could do, I thought these functions were deceptively difficult and I didn't allocate enough time to this assignment. I will be better prepared for the next one###


def citypop():
  from csv import reader
  D = {}                                                    #empty dict for accumulation
  with open("Top5000Population.txt") as F:                  #open text file
    for city, state, population in reader(F):
      city = city.upper()[:12]                              #Upper method
      D[(city, state)] = int(population.replace(',',''))    #Final Dictionary 
  return D
  

def eventfreq(year, month):
    F=fieldict('DOT1000.txt')                                                       #generate fieldict 
    lst = [i[1] for i in F if((i[1].year == year) and (i[1].month == month))]       #Get a list of datetimes matching year and month
    return [(i, lst.count(i)) for i in set(lst)]                                    #return a list of tuples (datetime, count)
  
    

def manuftop10():
    F=fieldict('DOT1000.txt')
    counts = defaultdict(int)                                                     
    for manufacturer, date, crash, city, state in F.values():    #for loop iterates tuple
      counts[manufacturer] += 1                                 #List Accumulation
      while counts<=10:  
        return sorted(counts.items())                                 #return sorted list 
   
        
if __name__ == "__main__":
    import doctest
    doctest.testmod() 
