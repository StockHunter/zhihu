import re
import urllib.request
import pymysql
import time
import chardet
import os

PATH_FILE1 = "E:\\python_SRC\\zhihu\\webInfo\\temo\\"
PATH_FILE2 = "E:\\\\python_SRC\\\\zhihu\\\\webInfo\\\\temo\\\\"
PATH_FILE3 = "E:\\python_SRC\\zhihu\\webInfo\\"
HIS_LOG = "%shisLog.txt" % PATH_FILE1
WEB_DATA = "%swebinfo.txt" % PATH_FILE1
WEB_DATA_FLAG = 0
FORMAT_LIST = {'jpg', 'png', 'jpeg'}

DISTORY_NOTEXIST = "[Errno 2] No such file or directory: ''"
WEB = ""
WEB2 = ""
X = 0

def WriteFile(fname,data):
    f = open(fname, 'a')
    if f:
        f.write(data)
        f.close()
    else:
        return False

def Code_detect(url):
    urldet = getHtml(url)
    codede = chardet.detect(urldet)['encoding']
    print('%s <- %s' %(url,codede))
    return codede

def getHtml(url):
    error = 0
    cnt = 1
    while error == 0 and cnt < 10:
        error = 1
        try:
            page = urllib.request.urlopen(url, timeout=520)
        except urllib.request.HTTPError as e:
            if e.code == 500:
                print(e.msg)
                return -2
            print(e.code)
            print(e.msg)
            print(url)
            time.sleep(9)
            cnt = cnt +1
            print("sleep 9 seconds. url:%s cnt:%d" % (url, cnt))
            error = 0
    if cnt == 10:
        return -1
    html_tmp = page.read()
##    codetype = chardet.detect(html_tmp)['encoding']
    html = html_tmp.decode('gb2312', 'ignore')
##    html = html.decode('gb2312')
    page.close()
    return html

def getImg(html):
    global DISTORY_NOTEXIST
    global WEB2
    global WEB
    global X
    global PATH_FILE1
    global PATH_FILE2
    global WEB_DATA
##    reg_jpeg = r'data-original="(.*?\.jpeg)"'
##    reg_jpg = r'data-original="(.*?\.jpg)"'
##    reg_png = r'data-original="(.*?\.png)"'
    global FORMAT_LIST

    for cnt in range(0, 3):
        if cnt == 0:
            reg = r'data-actualsrc="(.*?\.jpg)"'
        if cnt == 1:
            reg = r'data-actualsrc="(.*?\.jpeg)"'
        if cnt == 2:
            reg = r'data-actualsrc="(.*?\.png)"'
        print(cnt)
        imgre = re.compile(reg)
        imglist = imgre.findall(html)
        set_imglist = set(imglist)
        list_imglist_tmp = list(set_imglist)
        if cnt == 0:
            imglist_all = list_imglist_tmp
            continue
        for listcnt in list_imglist_tmp:
            if listcnt not in imglist_all:
                imglist_all.append(listcnt)
    WriteFile(WEB_DATA, str(imglist_all))
##    print("set_imglist2(set):%s" % (set_imglist2))
##    print(type(set_imglist2))
##    print(type(imglist2))
##    print(imglist2)
    for imgurl in imglist_all:
        t1 = time.localtime()
        str1 = "%s%s_%d%02d%02d\\%d.jpg" % (PATH_FILE1, WEB2, t1.tm_year, t1.tm_mon, t1.tm_mday, X)
        str2 = "%s%s_%d%02d%02d\\\\%d.jpg" % (PATH_FILE2, WEB2, t1.tm_year, t1.tm_mon, t1.tm_mday, X)
        path = "%s%s_%d%02d%02d\\" % (PATH_FILE1, WEB2, t1.tm_year, t1.tm_mon, t1.tm_mday,)
        DISTORY_NOTEXIST = "[Errno 2] No such file or directory: '%s'" % str2
        try:
            urllib.request.urlretrieve(url=imgurl, filename=str1)
        except Exception as e:
            e = str(e)
            if e == DISTORY_NOTEXIST:
                print("Dict Make")
                os.makedirs(path)
                urllib.request.urlretrieve(url=imgurl, filename=str1)
            print(e)
            print("Error")
            continue
        print(str1)
        X = X + 1

#WEB = "https://www.zhihu.com/question/30941719"23147606
WEB = "https://www.zhihu.com/question/27378077"
WEB2 = WEB.replace("https://www.zhihu.com/question/", "")
print("WEB2:%s" % WEB2)
htmlinfo = getHtml(WEB)
if WEB_DATA_FLAG == 1:
    WriteFile(WEB_DATA, htmlinfo)
getImg(htmlinfo)
WriteFile(HIS_LOG, "%s\n" % WEB2)
