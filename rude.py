#coding=utf-8
import nude,os,threading
def nude_yesorno(num):
    try:
        res=nude.is_nude(str(num)+'.jpg')
        return res
    except:
        return False
def panduan(first,bigest):
    for i in range(first,bigest):
        res=nude_yesorno(i)
        if res==False:
            try:
                os.remove(str(i)+".jpg")
            except:
                pass
        print i,res
def thread_panduan(biggest):
    a_5=biggest//5
    threads = []
    t1 = threading.Thread(target=panduan, args=(0,a_5))
    threads.append(t1)
    t2 = threading.Thread(target=panduan, args=(a_5, 2*a_5))
    threads.append(t2)
    t3 = threading.Thread(target=panduan, args=(2*a_5, 3 * a_5))
    threads.append(t3)
    t4 = threading.Thread(target=panduan, args=(3*a_5, 4 * a_5))
    threads.append(t4)
    for t in threads:
        t.join()
    print "over"
