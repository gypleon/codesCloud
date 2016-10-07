#!/usr/bin/python

import mincemeat
import glob
import logging

datafile = './ml-20m/likeorunlike'

def file_contents(file_name):
    f = open(file_name)
    try:
        return f.read()
    finally:
        f.close()

def mapfn(k, v):
    ratinglist = list()
    # get the amount of user in order to initiate the ratinglist
    # logging.debug("datafile: %s", datafile)
    with open('./ml-20m/likeorunlike', 'r') as df:
        df.seek(-50, 2)
        useramount = int(df.readlines()[-1].split()[0])
    for i in range(0, useramount+1):
        ratinglist.append({'l':set(), 'u':set()})
    # logging.debug("ratinglist length: %d, useramount: %d", len(ratinglist), useramount)
    for line in v.splitlines():
        content = line.split(' ')
        userid = int(content[0])
        movieid = int(content[1])
        rating = content[2]
        # logging.debug("%d %d %s", userid, movieid, rating)
        if 'l' == rating:
            ratinglist[userid]['l'].add(movieid)
        elif 'u' == rating:
            ratinglist[userid]['u'].add(movieid)
    # logging.debug("ratinglist created, length: %d", len(ratinglist))
    for user1 in range(1, len(ratinglist)-1):
        for user2 in range(user1+1, len(ratinglist)):
            # logging.debug("%2d-%2d", user1, user2)
            yield (user1, user2), (ratinglist[user1], ratinglist[user2])

def reducefn(k, vs):
    # compute the Jaccard similarity
    u1itu2l = vs[0][0]['l'].intersection(vs[0][1]['l'])
    u1itu2u = vs[0][0]['u'].intersection(vs[0][1]['u'])
    u1unu2l = vs[0][0]['l'].union(vs[0][1]['l'])
    u1unu2u = vs[0][0]['u'].union(vs[0][1]['u'])
    result = round(float(len(u1itu2l.union(u1itu2u))) / len(u1unu2l.union(u1unu2u)), 4)
    return result

if __name__ == "__main__":
    # logging.basicConfig(filename='./logs/debug.log', filemode = 'w', level=logging.DEBUG)

    like_files = glob.glob(datafile)
    # The data source can be any dictionary-like object
    datasource = dict((file_name, file_contents(file_name))
                      for file_name in like_files)
    
    s = mincemeat.Server()
    s.datasource = datasource
    s.mapfn = mapfn
    s.reducefn = reducefn
    
    # results here is a dict that cannot be sorted 
    resultsdict = s.run_server(password="leon")
    print 'Top 100 similar users:'
    results = [ (i, resultsdict[i]) for i in resultsdict ]
    results = sorted(results, key = lambda x:x[1], reverse=True)
    for i in range(100):
        u1u2, JS = results[i]
        print '%d %d %.2f' % (u1u2[0], u1u2[1], JS)

