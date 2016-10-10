===================================================================
Dear Prof Lyu,

It is my most regret that I have yet got the final results due to the server, which supported my program, failed several times.
I am still trying my best to output the result and planning to submit them later.

Best regard,
Guo Yinpeng
===================================================================
HOW TO RUN:
1. run "preprocess.py" with "./ratings.csv" to generate "./usrlist"
2. "bin/hdfs dfs -put usrlist..." into HDFS
3. run "mapper.py" and "reducer.py" using "HDFS Streaming" with "usrlist" sent
4. check results
