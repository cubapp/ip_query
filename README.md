# ip_query
Small simple SQLite frontend for registering IP addresses. 

As I work with more and more malware samples from different IPs, I lost track. So this small python script
1. makes a SQLite DB in `/home/user/bin/ip_log.db` 
2. query either the whole IP or just a prefix like `45.67.87`
3. adds new IPs via `-i` parameter

```
$ ip_query.py

Usage:
-i, --import IP_ADDRESS   : Import IP address into the database
IP_ADDRESS               : Query the database for the specified IP address
No parameters            : Print help and number of records
Number of Records: 83531
```


If you need to add more IPs, then have them in the separate file, say ips.today.txt, one IP per line
and call ip_query.py like this: 
```
xargs -l ip_query.py -i  < /tmp/ips.today.txt
```

