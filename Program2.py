'''
  There should be several functions in this module.  Two are 
  already provided, in case they are useful:  datextract and eightdigs 
  are functions from a previous homework which might be handy.

  Three new functions to write are:

  1.  citylist(filename)  reads a file in the DOT format
      and returns a list of city names, one for each line in 
      the file.  The DOT format may have trailing spaces on 
      the city name;  make sure citylist creates a list of 
      city names with trailing spaces removed (easy using
      Python's strip() method).  Two test cases are shown 
      below, for lines at index 3 and 347.  When we grade, we 
      will use other tests at different index values.

  2.  statecount(filename) reads a file in DOT format 
      and returns a dictionary with two-letter state abbreviations
      as keys and the number of lines in the DOT file for that 
      state.  

  3.  fieldict(filename) reads a file in DOT format and 
      returns a dictionary with the DOT CMPLID, converted to an
      integer, as the key, and a tuple as the corresponding value
      for that key.  The format of the tuple is:
         (manufacturer, date, crash, city, state)
      where these tuple items have the following types:
         manufacturer -- this comes from the MFR_NAME field in the DOT format 
	 date -- this comes from the FAILDATE field in the DOT format, 
	         but converted to a Python datetime.date object
	 crash -- this comes from the CRASH field in the DOT format, 
	         but converted to a Python bool type (True for a crash)
         city -- comes from the CITY field in the DOT format
	 state -- comes from the STATE field in the DOT format

  Advice:
     - The only DOT file used for testing below is the file "DOT500.txt", which
       must be in the same place as this Python module, so it can be found.  
     - Study the file CMPL.txt to learn about the DOT format
     - Study the file Example.py to learn how to read a file one record at a time
     - Be careful not to fully trust the DOT format -- there can be fields
       in some lines of the file which have bad data.  Your functions should be
       able to overcome the bad data without getting a Python error that stops
       it from runnin.

  Test cases for your functions follow:

  >>> citylist("DOT500.txt")[3]
  'TUCSON'
  >>> citylist("DOT500.txt")[347]
  'NORTH VILLE'
  >>> statecount("DOT500.txt")['CA']
  76
  >>> statecount("DOT500.txt")['NV']
  4
  >>> fieldict("DOT500.txt")[416]
  ('DAIMLERCHRYSLER  CORPORATION', datetime.date(1995, 1, 9), False, 'ARCADIA', 'FL')
  >>> fieldict("DOT500.txt")[82]
  ('FORD MOTOR COMPANY', datetime.date(1995, 1, 1), False, 'MARBLE HEAD', 'MA')

'''
# for your convenience, here are some functions and an import statement 
# that may be helpful in doing the homework
import datetime
def datextract(S):
  return (int(S[:4]),int(S[4:6]),int(S[6:]))
def eightdigs(S):
  return type(S)==str and len(S)==8 and all([c in "0123456789" for c in S]) 

#----- define your functions here ------------------------

def citylist(filename):
    with open(filename) as f:
        return [ line.split('\t')[12].strip() for line in f ]


from collections import defaultdict

def statecount(filename):
    with open(filename) as f:
        x=[ line.split('\t')[13].strip() for line in f ]
        d = {}
        for j in x:
            d[j] = d.get(j,0) + 1
        return d



import csv
import datetime
def datextract(S):
  return (int(S[:4]),int(S[4:6]),int(S[6:]))

def fieldict(filename):
    complaints = {}
    with open(filename, "rb") as in_f:                      
        reader = csv.reader(in_f, delimiter='\t')           #csv module
        complaint_id_idx = 0                #Assign indexes of all the info I want in tuple
        manufacturer_idx = 2
        Date_idx= 7
        crash_idx = 6               #Change from index 8 to 6
        city_idx = 12
        state_idx = 13

        
        for line in reader:
            if 'Y' in line[crash_idx]:              #Converts Y or N into True or False
              line[crash_idx]=True
            else:
              line[crash_idx]=False


            complaint_id = int(line[complaint_id_idx])
            data= (
                         line[manufacturer_idx],
                         datetime.date(datextract(line[Date_idx])), 
                         line[crash_idx],      
                         line[city_idx].strip(),
                         line[state_idx],
                        )

            complaints[complaint_id] = data             #Final dict
    return complaints


#As close as I could get it .. 





# run unit testing as found in the docstring
if __name__ == "__main__":
    import doctest
    doctest.testmod() 



