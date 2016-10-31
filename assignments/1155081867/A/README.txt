===================================================================
HOW TO RUN:
1. run "preprocess.py" with "./ratings.csv" to generate "./usrlist"
2. "bin/hdfs dfs -put usrlist..." into HDFS
3. run "mapper.py" and "reducer.py" using "HDFS Streaming" with "usrlist" sent
4. check results
