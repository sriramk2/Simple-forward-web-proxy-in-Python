import socket, sys
from _thread import *
import hashlib
import os
import re
from time import strftime, gmtime, ctime
import sys
temp = []
l = len(temp)
list_port = sys.argv[1]
host = ''
backlog = 100
buffer = 8192

#print(tm)
#print(ct)
#print(fl)
def main():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((host,int(list_port)))
        s.listen(backlog)
        
        print("Starting socket")
    except:
        print("Socket failed")
        sys.exit(2)
    
    while 1:
        try:
            s.settimeout(5)
            conn, addr = s.accept()
            data = conn.recv(buffer)
            #print(data)
            start_new_thread(req_str, (conn, data, addr))
            #print("Proxy on")
            
        except:
            continue
    s.close()


def req_str(conn, data, addr):
    try:
        #print(data)
        
        data1 = data.decode('utf-8')
        first_line = []
        first_line = data1.split('\n')[0]
        
        url = []
        
        url = first_line.split(' ')
        
        #print(url[1])
    
        http_pos = url[1].find('://')
        #print("This is position")
        if http_pos == 1:
            temp = url[1]
        else:
            temp = (url[1])[(http_pos + 3):]
            #print("KANE")
        port_pos = temp.find(':')
        webserver_pos = temp.find("/")
        if webserver_pos == -1:
            webserver_pos = len(temp)
        webserver = ''
        url1 = url[1].encode('ascii')
        print(url1)
        #print("ACM")
        port = -1
        if port_pos == -1 or webserver_pos < port_pos:
            port = 80
            webserver = temp[:webserver_pos]
        #print(port)    
        send_data(webserver, port, conn, addr, data, url1)
        #print("Thread")
        
    except:
        pass

def send_data(webserver, port, conn, addr, data, url1):
    
    
    try:   
        t = strftime("%a, %d %b %Y %H:%M", gmtime()).split(':')
        tm = t[1]
        
        hash1 = hashlib.sha256()
        hash1.update(url1)
        if os.path.isfile(hash1.hexdigest() + ".txt"):
            print("CACHE")
            op = open(hash1.hexdigest() + ".txt",'rb')
            #print(op)
            while 1:
                
                f = ctime(os.path.getctime(hash1.hexdigest() + ".txt")).split(':')
                ft = f[1].split(':')
                ct = ft[0]
                print(ct)
                diff = int(tm) - int(ct)
                print(diff)
                if diff < 0:
         
                    diff  = 60 + diff
                    print(diff)
                if diff > 35:
                    #os.remove(hash1.hexdigest() + ".txt")
                    b = 2               
                    print("Delete..")
                    
                    break            
                else:
                    r = op.read(8192)
                    conn.send(r)
                
                    if len(r) == 0:
                        b == 2
         
                        break
        if os.path.isfile(hash1.hexdigest() + ".txt") == 0 or b == 2 :            
            
         
            s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)          
            s1.connect((webserver, port))        
                                          
            data = data.replace(b'http://' + webserver.encode('utf-8'),b'')
            print(data)
            print(webserver)
            hash1 = hashlib.sha256()
            hash1.update(url1)
            print("HASH OF REQUEST:" + hash1.hexdigest())
                
            f = open(hash1.hexdigest() + ".txt",'wb')
   
    
            s1.settimeout(5)
            s1.send(data)
                
            #         print(port)
            while 1:
                    
                        
                reply = s1.recv(buffer)
                print(reply)
                        
                        
                if len(reply) > 0:
                    conn.send(reply)
                    #print(len(reply))
                    f.write(reply)
                else:
                        #print(broken")
                            #print(temp)
                            
                    break
                        
            
                       
         
                    s1.close()
                    conn.close()
    
        
        
    except:    
        
        #print("Socket error")
        s1.close()
        conn.close()
        sys.exit(1)


main()    
