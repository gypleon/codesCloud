#!/usr/bin/python

import logging
import sys

def read_input(file):
    for line in file:
        yield line.split(' ')

def main():
    ratinglist = list()
    # get the amount of user in order to initiate the ratinglist
    # logging.debug("datafile: %s", datafile)
    with open('./ml-20m/likeorunlike.test', 'r') as df:
        df.seek(-50, 2)
        useramount = int(df.readlines()[-1].split()[0])
    for i in range(0, useramount+1):
        ratinglist.append({'l':set(), 'u':set()})
    # logging.debug("ratinglist length: %d, useramount: %d", len(ratinglist), useramount)
    data = read_input(sys.stdin)
    for content in data:
        userid = int(content[0])
        movieid = int(content[1])
        rating = content[2].strip('\n')
        # logging.debug("%d %d %s", userid, movieid, rating)
        if 'l' == rating:
            ratinglist[userid]['l'].add(movieid)
        elif 'u' == rating:
            ratinglist[userid]['u'].add(movieid)
    # logging.debug("ratinglist created, length: %d", len(ratinglist))
    for user1 in range(1, len(ratinglist)-1):
        for user2 in range(user1+1, len(ratinglist)):
            # logging.debug("%2d-%2d", user1, user2)
            print "%s:%s\t%s:%s:%s:%s" % (str(user1), str(user2), repr(ratinglist[user1]['l']), repr(ratinglist[user2]['l']), repr(ratinglist[user1]['u']), repr(ratinglist[user2]['u']))

if __name__ == "__main__":
    main()
