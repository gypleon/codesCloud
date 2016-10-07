#!/usr/bin/python

import logging
import sys

def read_input(file):
    for line in file:
        yield line.split(' ')

def main():
    ratinglist = list([{'l':set(), 'u':set()}])
    data = read_input(sys.stdin)
    preuserid = 0
    for content in data:
        userid = int(content[0])
        if userid != preuserid:
            preuserid = userid
            ratinglist.append({'l':set(), 'u':set()})
        movieid = int(content[1])
        rating = content[2].strip('\n')
        # logging.debug("%d %d %s", userid, movieid, rating)
        if 'l' == rating:
            ratinglist[userid]['l'].add(movieid)
        elif 'u' == rating:
            ratinglist[userid]['u'].add(movieid)
    logging.debug("ratinglist created, length: %d", len(ratinglist))
    sendthreshold = 1000
    sendcount = 0
    sendlist = list()
    for user1 in range(1, len(ratinglist)-1):
        for user2 in range(user1+1, len(ratinglist)):
            logging.debug("%2d-%2d", user1, user2)
            predict = float(len(ratinglist[user1]['l'])+len(ratinglist[user1]['u']))/(len(ratinglist[user2]['l'])+len(ratinglist[user2]['u']))
            if predict < 0.95 or predict > 1.05:
                continue
            elif 0 == len(ratinglist[user1]['l'].intersection(ratinglist[user2]['l'])) and 0 == len(ratinglist[user1]['l'].intersection(ratinglist[user2]['l'])):
                continue
            else:
                # print "%d:%d\t%s:%s:%s:%s" % (user1, user2, repr(ratinglist[user1]['l']), repr(ratinglist[user2]['l']), repr(ratinglist[user1]['u']), repr(ratinglist[user2]['u']))
                sendlist.append((user1, user2))
                sendcount += 1
                if sendcount >= sendthreshold:
                    sendcount = 0
                    sendstring = list()
                    for userp in sendlist:
                        sendstring.cat
                    sendlist = []
                    print sendstring

if __name__ == "__main__":
    logging.basicConfig(filename='mapper.log', filemode='w', level=logging.DEBUG)
    main()
