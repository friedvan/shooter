#coding: utf-8
#author: pzc, @friedvan, rabbitpzc#gmail.com
#2013-3-1 0:07:05
#自动从射手下载字幕

import urllib2, urllib
from bs4 import BeautifulSoup as bs
import time

shooter = 'http://shooter.cn'
    
def search(key):
    return urllib2.urlopen('http://shooter.cn/sub/?searchword=' + urllib.quote(key)).read()

def getHTML(href):
    return urllib2.urlopen(href).read()

def getSubtileNumber(html):
    try:
        href = bs(html).find('a', {'class':'introtitle'})['href']
        downloadPage = getHTML(shooter + href)
        downURL = bs(downloadPage).find('a', {'class':'btn_download'})['onclick']
        return downURL.split(',')[1].split(')')[0]
    except:
        return ''

def b(j):
    g = ''
    for f in j:
        h = ord(f)
        if h + 47 >= 126:
            temp = chr(ord(' ') + (h + 47) % 126)
        else:
            temp = chr(h + 47)
        g += temp
    return g

#reverse g
def d(g):
    return g[::-1]

def c(j, h, g, f):
    return j[len(j) - f + g - h: len(j) - f + g] + j[len(j) - f: len(j) - f + g - h] + j[len(j) - f + g: len(j) - f + g + f - g] + j[0: len(j) - f]

##WTF!!!
def shtg_calcfilehash(a):
    if len(a) > 32:
        ch = a[0]
        if ch == 'o':
            return b(c(a[1:], 8, 17, 27))
        if ch == "n":
            return b(d(c(a[1:], 6, 15, 17)))
        if ch == "m":
            return d(c(a[1:], 6, 11, 17))
        if ch == "l":
            return d(b(c(a[1:], 6, 12, 17)))    
        if ch == "k":
            return c(a[1:], 14, 17, 24)         
        if ch == "j":
            return c(b(d(a[1:])), 11, 17, 27)   
        if ch == "i":
            return c(d(b(a[1:])), 5, 7, 24)       
        if ch == "h":
            return c(b(a[1:]), 12, 22, 30)
        if ch == "g":
            return c(d(a[1:]), 11, 15, 21)
        if ch == "f":
            return c(a[1:], 14, 17, 24)
        if ch == "e":
            return c(a[1:], 4, 7, 22)
        if ch == "d":
            return d(b(a[1:]))
        if ch == "c":
            return b(d(a[1:]))
        if ch == "b":
            return d(a[1:])
        if ch == "a":
            return b(a[1:])
    return a

#ref:loadmain.js @shooter.cn
#this function may magically does not work because of those magic tricks~~~
def local_downfile(number):
    #the magic file hash
    shtg_filehash = 'duei7chy7gj59fjew73hdwh213f'
    #the magic php file
    b = urllib2.urlopen(shooter + "/files/file3.php?hash=" + shtg_filehash + "&fileid=" + number).read()
    #the magic hash function
    b = shtg_calcfilehash(b)
    #the magic file server
    return 'http://file0.shooter.cn' + b  

#
def urlcallback(a,b,c):  
    """ 
        call back function 
        a,已下载的数据块 
        b,数据块的大小 
        c,远程文件的大小 
    """  
##    print "callback"  
    prec=100.0*a*b/c  
    if 100 < prec:  
        prec=100  
    print "%.2f%%"%(prec,)


def getSubtitle(key, index = 0):
    subtile_number = getSubtileNumber(search(key))
    if subtile_number == '':
        print key, 'error!!!!!!!!!!!!!!'
        return
    download_addr = local_downfile(subtile_number)
    filetype = download_addr.split('?')[0][-4:]
    filename = (str(index) + '_' + str(key) + filetype).decode('utf-8').encode('gbk')
    print filename
    urllib.urlretrieve(download_addr, filename, urlcallback)  
##http://file0.shooter.cn/c/_____________________________________________________________rar.zip?p=20130228&s=064cd6358319eed151b26dda3631af0f&t=1362067108&h=DMNlI-CF9rD8D3O48VSzZA
##http://file0.shooter.cn/c/_____________________________________________________________rar.zip?p=20130228&s=064cd6358319eed151b26dda3631af0f&t=1362067316&h=JaKRK93alCQZ1HUoYOHtvg

##sfile = open('测试测试'.decode('utf-8').encode('gbk'), 'w')
##sfile.close()

def readMovieList():
    Movie = []
    mfile = open('movielist.txt')
    while True:
        line = mfile.readline().rstrip()
        if not line:
            break
        Movie.append(line)
    mfile.close()
    return Movie

#main
def main():
    Movie = readMovieList()
    for m in Movie:
        print m
    i = 0
    for m in Movie:
        i += 1
        getSubtitle(m)
        time.sleep(3)
        
        

if __name__ == '__main__':
    main()
