import urllib.request
import re
import time
import urllib.parse
import os

def open_url(url,headers=None):
    try_c=0
    while try_c<3:
        try:
            if headers==None:
                headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) Ap\
pleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Co\
re/1.53.3103.400 QQBrowser/9.6.11372.400'}
                req=urllib.request.Request(url,headers=headers)
    
                page = urllib.request.urlopen(req)
                html = page.read().decode('utf-8')
                try_c=3
        except:
            try_c=try_c+1
            print('重试\n')
    
    return html

def get_url(url):
    try_c=0
    while try_c<3:
        try:
            html = open_url(url)
            urllist = re.findall("<a class='igalleryli_link' href='/g/([^/]+?)/'",html)
            try_c=3
        except:
            try_c=try_c+1
            print('重试\n')
    return urllist
def get_1_url(url):
    try_c=0
    while try_c<3:
        try:
            html = open_url(url)
            urllist = re.findall(r"href='/g/(\d+?)/'",html)
            try_c=3
        except:
            try_c=try_c+1
            print('重试\n')
    return urllist

def get_img(html,headers):
    p = r"<img src='([^']+?)'"
    imglist = re.findall(p,html)
    for each in imglist:
        print(each)
        filename = each.split('/')[-1]
        req=urllib.request.Request(each,headers=headers)
        try_c=0
        while try_c<3:
            try:
                page = urllib.request.urlopen(req,timeout=5)
                html = page.read()#.decode('utf-8')
                with open(filename,'wb') as f:
                    f.write(html)
                    f.close()
                try_c=3
            except:
                try_c=try_c+1
                print('重试\n')

if __name__=='__main__':
    while 1:
        m_name_search=input('输入要搜索的妹子：')
        if m_name_search == '1':
            o_url = 'https://www.nvshens.com/gallery/'
            urllist=get_1_url(o_url)
        else:
            m_search = urllib.parse.quote(m_name_search)
            o_url = 'https://www.nvshens.com/girl/search.aspx?name='+m_search
            o_html = open_url(o_url)
            girl1 = re.findall("href='/girl/([^/]+?)/' target='_blank'>",o_html)[0]
            print(girl1)
            o_url = 'https://www.nvshens.com/girl/'+girl1+'/album/'
            urllist=get_url(o_url)
        print(urllist)
        a_cont=0
        exist_dir_search =os.path.isdir(m_name_search)
        if not exist_dir_search:
            os.mkdir(m_name_search)
        os.chdir(m_name_search)
        download_time = input('输入要下的专辑数：')
        while not download_time.isnumeric():
            download_time = input('请输入数字：')
        download_time = int(download_time)
        download_time_counter = 1  #下载的专辑数计数
        for url in urllist:
            url = 'https://www.nvshens.com/g/'+url+'/'
            print(url)
            html_new_dir=open_url(url)
            new_dir_name = re.findall('<title>(.+?)</title>',html_new_dir)[0]
            dir_exist = os.path.isdir(new_dir_name)
            if dir_exist:
                continue
            os.mkdir(new_dir_name)
            os.chdir(new_dir_name)
            new_href='10'
            for i in range(1,100):
                url_new = url+str(i)+'.html'
                a= open_url(url_new)
                if i <= 1:
                    #new_href = re.findall(">([^<]+?)</a><a class='a1'[^>]+?>下一页</a>",a)[0]
                    a_cont += 1#表示示正在下专辑序数
                if i!=int(new_href):#当前不是最后一页就找最后一页
                    new_href = re.findall(">([^<]+?)</a><a class='a1'[^>]+?>下一页</a>",a)[0]
                headers={'Referer':url_new,
    'User-Agent':'Mozilla/5.0 (Window\
    s NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, \
    like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53\
    .3103.400 QQBrowser/9.6.11372.400'}
                get_img(a,headers)
                print(i)
                print(new_href)
                
                print(a_cont)
                if i > 1:
                    if i==int(new_href):
                        break
                
                #time.sleep(0.1)
                time.sleep(0.2)
            os.chdir('..')
            if download_time_counter >= download_time:
                break
            download_time_counter +=1
            time.sleep(0.2)
        os.chdir('..')
