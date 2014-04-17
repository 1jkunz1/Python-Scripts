'''
Functions to write:
 (1) nopuncend(S) -- returns S with any trailing punctuation removed, where 
     a punctuation character is any of these:  !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
     NOTE:  instead of typing these in yourself, this file defines punctuation
     to be a string containing all these characters.
 (2) notrail(S) -- returns S with any trailing whitespace characters removed,
     where a whitespace character is any of these:  \t\n\r (and blank of course)
     NOTE:  instead of typing these in yourself, this files deines whitespace
     to be a string containing all these characters
     SECOND NOTE:  look up "python rstrip" on a search engine, it can simplify
     your answers to (1) and (2)
 (3) eightdigs(S) -- returns True if S is a string consisting of exactly 8 digits
 (4) datextract(S) -- returns a tuple of (year,month,day) from an 8-digit string
 (5) strcount(S) -- returns a dictionary with words as keys and the number of times
     that word appears as the corresponding value
 (6) sumcounts(D) -- where D is a dictionary with numbers as values, 
     returns the sum of all the values
     NOTE:  some useful things for this might be these methods:
        D.keys() -- a list of all the keys in dictionary D
	D.values() -- a list of all the values in dictionary D
	len(D) -- how many items D has
	D.items() -- a list of all items, as (key,value) pairs
 (7) freqitems(S,p) --- returns a sorted list of the items in sequence S that 
     occur with at least p percent frequency, with no duplicates
     NOTE:  how to get a sorted list?  If L is a list, then sorted(L) is 
            that same list in sorted order
     SECOND NOTE:  how to remove duplicates from a list?
            { k:0 for k in L }.keys()  -- gives L with duplicates removed

 What follows are test cases on (1)--(6)

>>> nopuncend("ordinary")
'ordinary'
>>> nopuncend("what?")
'what'
>>> nopuncend("so...")
'so'
>>> nopuncend("stop!")
'stop'

>>> notrail("simple")
'simple'
>>> notrail("let there be no more   ")
'let there be no more'

>>> eightdigs("test")
False
>>> eightdigs("123456")
False
>>> eightdigs(8*'0')
True
>>> eightdigs("11112222") and eightdigs("80041209")
True

>>> datextract("20080702")
(2008, 7, 2)
>>> [datextract("19941128")]
[(1994, 11, 28)]


>>> strcount("a a a a b b")
{'a': 4, 'b': 2}
>>> strcount("one")
{'one': 1}
>>> sorted(strcount("this one and that one for one time").items())
[('and', 1), ('for', 1), ('one', 3), ('that', 1), ('this', 1), ('time', 1)]

>>> sumcounts({"a":2.5, "b":7.5, "c":100})
110.0
>>> sumcounts({ })
0
>>> sumcounts(strcount("a a a b"))
4

>>> freqitems([2,2,2,3],50)
[2]
>>> freqitems(5*["alpha"]+["beta"]+3*["gamma"]+7*["delta"], 25)
['alpha', 'delta']
>>> freqitems(5*["alpha"]+["beta"]+3*["gamma"]+7*["delta"], 33)
['delta']
'''
from string import punctuation
from string import whitespace


def nopuncend(S):
        return S.rstrip(punctuation)

def notrail(S):
	return S.strip()
    

def eightdigs(S):
	if type(S)==str and len(S)==8:
		return True
	else:
		return False

def datextract(S):
	    return int (S[:4]) ,int(S[4:6]),int(S[6:8])
    


def strcount(S):
    sub=S.split()
    table={}.fromkeys(sub,0)
    for j in sub:
            table[j] +=1
    return table
    


def sumcounts(D):
	D==dict
	return sum(D.values())



def freqitems(S,p):
    S=sorted(S)
    b=0
    k=0
    t=[]
    t.append(S[0])
    for i in range(0,len(S)):
        if S[i]!=t[b]:
            t.append(S[i])
            if (i-k)/float(len(S))>=(p/100.00):
                b=b+1
            else:
                del t[b]
            k=i
    if (len(S)-k)/float(len(S))<(p/100.00):
        del t[b]
    return t


def freqitems(S, p):
  import collections
  counter = collections.Counter(S)
  return sorted([k for k,v in counter.iteritems() if 100.*v/len(S) >= p])

# could not  figure how to do numbers 5 and 7 without loops ect.




if __name__ == "__main__":
    import doctest
    doctest.testmod() 
