#!/usr/bin/python

import json

if __name__ == "__main__":
    ratings = "./ratings.csv"
    usrlist = "./usrlist"
    with open(ratings, 'r') as f:
        f.readline()
        preusr = 0
        usrinfos = []
        for line in f:
            cont = line.split(',')
            usr, mov, rat = int(cont[0]), cont[1], cont[2] 
            if usr != preusr:
                usrinfos.append({'l':[], 'u':[]})
                preusr = usr
            if float(rat) > 2.5:
                usrinfos[usr-1]['l'].append(mov)
            else:
                usrinfos[usr-1]['u'].append(mov)
    with open(usrlist, 'w') as f:
        f.write("%s" % json.dumps(usrinfos))
