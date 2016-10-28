#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import re
from HTMLParser import HTMLParser
import cgi
from bs4 import BeautifulSoup
import pymysql.cursors

times = 5

run_num = 0

url_arry = {
    'domain' : 'http://www.cnki.net',
    "endomain" : "http://lks.cnki.net/index.html",
    'uid' : "",
    'kcms' : 'kcms',
    'detail' : 'detail',
    'frame' : 'frame',
    'detailfile' : 'detail.aspx',
    'listfile' : 'detaillist.aspx'
}

reftype = {
    'reference' : 1,
    'similarity' : 7,
    'focus' : 8
}

htmldom = {
    'titleid' : 'chTitle',
    'entitleid' : 'entitle',
    'authorclass' : 'KnowledgeNetLink',
    'abstractid' : 'ChDivSummary',
    'keywordid' : 'ChDivKeyWord',
    'listvid' : 'listv',
    'zwjdown' : 'zwjdown',
    'zwjRightRow' : 'zwjRightRow',
    'entable' : 'table[bgcolor=#f1f1f1]',
    'strContext' : 'strContext',
    'filenameid' : 'filename',
    'tablenameid' : 'tablename'
}

def replace_char(old_str):
    if(old_str == None):
        return '';
    new_str = re.sub(r'\'', "\\\'", old_str)
    new_str = re.sub(r'\"', "\\\"", new_str)
    return new_str

def get_text_by_id(soup, id_string):
    elem = soup.find(id=id_string)
    if elem != None:
        return elem.get_text()
    else :
        return ''

def get_text_by_class_once(soup, class_string):
    elem = soup.select('.'+class_string)
    if elem != []:
        return elem[0].get_text()
    else :
        return ''

def get_text_by_class(soup, class_string):
    elem = soup.select('.'+class_string)
    if elem != []:
        return elem.get_text()
    else :
        return ''

def get_article_elements_num(soup, class_string):
    elem = soup.select('.'+class_string)
    if elem != []:
        return len(elem)
    else :
        return ''

def create_html(url):
    r = requests.get(url)
    return r.text

def get_articles_id(conn):
    get_cur = conn.cursor()
    insert_cur = conn.cursor()

    get_cur.execute("SELECT DISTINCT `title`,`filename` FROM `articles`")

    for row in get_cur:
        article_title = row.get('title')
        article_filename = row.get('filename')

        insert_sql_string = "INSERT IGNORE INTO `articles_id` (`title`, `filename`) VALUES ('%s', '%s');" % (replace_char(article_title), article_filename)
        # print insert_sql_string
        insert_cur.execute(insert_sql_string)
        conn.commit()

    get_cur.close()
    insert_cur.close()

def reorder_data(conn):
    select_cur = conn.cursor()

    select_sql_string = "SELECT `title`, `author`, `abstract`, `keywords`, `filename`, `dbcode`, `type`, `level`, `href`, `toname` FROM `articles`;"

    try:
        select_cur.execute(select_sql_string)
    except:
        print "select error"

    i = 0
    for row in select_cur:
        article_title = row.get('title')
        article_filename = row.get('filename')

        i = i + 1

        get_row_cur = conn.cursor()

        sql_string = "SELECT `id`, `title`, `filename` FROM `articles_id` WHERE `title` = '%s' AND `filename` = '%s';" % (replace_char(row.get('title')), row.get('filename'))

        try:
            get_row_cur.execute(sql_string)
        except:
            print "get select error"

        file_id = get_row_cur.fetchone()
        print file_id['id']
        article_fileid = file_id['id']

        insert_cur = conn.cursor()
        sql_string = 'INSERT INTO `resort_articles` (`title`, `author`, `abstract`, `keywords`, `filename`, `fileid`, `dbcode`, `type`, `level`, `href`, `toname`) VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%d", "%d", "%s", "%s");' % (replace_char(row.get('title')), replace_char(row.get('author')), replace_char(row.get('abstract')), replace_char(row.get('keywords')), row.get('filename'), article_fileid, row.get('dbcode'), row.get('type'), row.get('level'), replace_char(row.get('href')), row.get('toname'))
        print sql_string
        try:
            insert_cur.execute(sql_string)
        except:
            print "insert error"
        conn.commit()
        print i

    get_row_cur.close()
    select_cur.close()
    insert_cur.close()

def run_article_list(url, aricle_from, run_times, conn):
    # print url
    list_html_code = create_html(url)
    list_soup = BeautifulSoup(list_html_code, 'html.parser')
    list_li = list_soup.find_all('li')
    for li in list_li:
        list_a = li.find('a')
        if list_a != None:
            if list_a.has_attr('href'):
                run_article(url_arry['domain']+list_a['href'], aricle_from, run_times, conn)
                # print list_a['href']
            elif list_a.has_attr('onclick'):
                article_click = list_a['onclick']

                article_click = re.sub(r'\'\)\;', "&", article_click)

                article_title = ''
                article_sid = ''
                article_author = ''

                # print article_click
                pm = re.compile('title=([^&]+)')
                match = re.search(pm, article_click)

                if match:
                    article_title = match.group(1)

                pm = re.compile('sid=([^&]+)')
                match = re.search(pm, article_click)

                if match:
                    article_sid = match.group(1)

                pm = re.compile('aufirst=([^&]+)')
                match = re.search(pm, article_click)

                if match:
                    article_author = match.group(1)

                temp_article_url = url_arry["endomain"] + "?title=" + article_title + "&sid=" + article_sid + "&aufirst=" + article_author + '&'
                run_article(temp_article_url, aricle_from, run_times, conn)
            # else:
            #     print list_a.get_text()
        else:
            lp = re.compile('\s+')
            li_text = re.sub(lp, '', li.get_text())
            # print li_text
    # print list_li

def run_article(url, aricle_from, run_times, conn):
    if run_times is 0:
        return 0

    # print 'run_times:%d' % (run_times)
    # print url

    html_code = create_html(url)
    soup = BeautifulSoup(html_code, 'html.parser')

    article_title = soup.find(id=htmldom['titleid'])

    article_information = {
        'title' : '',
        'author' : '',
        'abstract' : '',
        'filename' : '',
        'dbcode' : '',
        'dbname' : '',
        'keywords' : '',
        'sid' : ''
    }

    if article_title != None:

        article_information['title'] = article_title.get_text()

        article_information['author'] = get_text_by_class_once(soup, htmldom['authorclass'])

        article_information['abstract'] = get_text_by_id(soup, htmldom['abstractid'])

        # print article_information['title']
        #
        # print article_information['abstract']
        ################
        keywords = get_text_by_id(soup, htmldom['keywordid'])
        p = re.compile('\s+')
        article_information['keywords'] = re.sub(p, '', keywords)

        # print article_information['keywords']

        listv = soup.find(id=htmldom['listvid'])['value']
        elem = soup.find('div', {'class': htmldom['zwjdown']})

        if(elem != None):
            zwjdown_string = elem.a['href'].strip()
        else:
            zwjdown_string = ''

        pm = re.compile('filename=([^&]+)&dbcode=([^&]+)&dbname=([^&]+)')
        match = re.search(pm, zwjdown_string)
        if match:
            article_information['filename'] = match.group(1)
            article_information['dbcode'] = match.group(2)
            article_information['dbname'] = match.group(3)

        select_sql_string = "SELECT `title`, `filename` FROM `articles` WHERE `title` = '%s' AND `filename` = '%s';" % (article_information['title'], article_information['filename'])

        select_cur = conn.cursor()

        try:
            rownum = select_cur.execute(select_sql_string)
        except:
            print "select error"

        sql_string = "INSERT INTO `articles` (`title`, `author`, `abstract`, `keywords`, `filename`, `dbcode`, `type`, `level`, `href`, `toname`) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%d', '%d', '%s', '%s');" % (article_information['title'], article_information['author'], article_information['abstract'], article_information['keywords'], article_information['filename'], article_information['dbcode'], 1, run_times, url, aricle_from)
        # print 'run_num:%d' % (run_num)
        # run_num = run_num + 1
        # print sql_string

        insert_cur = conn.cursor()

        try:
            insert_cur.execute(sql_string)
        except:
            print url
        conn.commit()
        select_cur.close()
        insert_cur.close()

        if(rownum == 0):
            listurl = url_arry['domain'] + '/' + url_arry['kcms'] + '/' + url_arry['detail'] + '/' + url_arry['frame'] + '/' + url_arry['listfile']\
            + '?filename=' + article_information['filename'] + '&dbcode=' + article_information['dbcode'] + '&dbname=' + article_information['dbname']\
            + '&reftype=' + str(reftype['reference']) + '&vl=' + listv
            run_article_list(listurl, article_information['filename'], run_times-1, conn)

    elif soup.find(id=htmldom['entitleid']) != None:
        article_title = soup.find(id=htmldom['entitleid'])
        article_information['title'] = article_title.get_text()
        article_information['filename'] = soup.find(id=htmldom['filenameid'])['value']
        article_information['dbcode'] = soup.find(id=htmldom['tablenameid'])['value']

        article_author = soup.select('.strContext')[0].get_text()
        article_information['author'] = ' '.join(article_author.split())

        num = get_article_elements_num(soup, htmldom['strContext'])

        article_abstract = soup.select('.strContext')[num-1].get_text()
        article_keywords = soup.select('.strContext')[num-2].get_text()
        article_information['abstract'] = ' '.join(article_abstract.split())
        article_information['keywords'] = ' '.join(article_keywords.split())

        # print article_information['title']
        # print article_information['filename']
        # print article_information['author']
        # print article_information['abstract']
        # print article_information['keywords']
        # print url
        sql_string = "INSERT INTO `articles` (`title`, `author`, `abstract`, `keywords`, `filename`, `dbcode`, `type`, `level`, `href`, `toname`) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%d', '%d', '%s', '%s');" % (replace_char(article_information['title']), replace_char(article_information['author']), replace_char(article_information['abstract']), replace_char(article_information['keywords']), replace_char(article_information['filename']), article_information['dbcode'], 2, run_times, url, aricle_from)
        # print 'run_num:%d' % (run_num)
        # run_num = run_num + 1
        # print sql_string

        insert_cur = conn.cursor()
        try:
            insert_cur.execute(sql_string)
        except:
            print url
        conn.commit()
        insert_cur.close()

    else :
        # print url

        pm = re.compile('title=([^&]+)')
        match = re.search(pm, url)

        if match:
            article_information['title'] = match.group(1)

        pm = re.compile('sid=([^&]+)')
        match = re.search(pm, url)

        if match:
            article_information['sid'] = match.group(1)

        pm = re.compile('aufirst=([^&]+)')
        match = re.search(pm, url)

        if match:
            article_information['author']  = match.group(1)

        sql_string = "INSERT INTO `articles` (`title`, `author`, `sid`, `type`, `level`, `href`, `toname`) VALUES ('%s', '%s', '%s', '%d', '%d', '%s', '%s');" % (replace_char(article_information['title']), replace_char(article_information['author']), replace_char(article_information['sid']), 3, run_times, url, aricle_from)
        # print 'run_num:%d' % (run_num)
        # run_num = run_num + 1
        # print sql_string

        insert_cur = conn.cursor()
        try:
            insert_cur.execute(sql_string)
        except:
            print url
        conn.commit()
        insert_cur.close()
        return 0

def main():
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='cnki_py2_db', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

    line_num = 0
    fd = open('in.txt', 'r')
    for line in fd:
        # print line.strip('\n')
        print 'line:%d' % (line_num)
        run_article(line.strip('\n'), 0, times, conn)
        line_num += 1

    # run_article('', 0, times, conn)
    # article_url = 'http://www.cnki.net/kcms/detail/detail.aspx?filename=XTIB201601002&dbcode=CJFQ&dbname=CJFDTEMP&v='
    # article_url = 'http://www.cnki.net/kcms/detail/detail.aspx?filename=JSJC200315041&dbcode=CJFQ&dbname=CJFD2003&v='
    # run_article(article_url, 0, times, conn)

    get_articles_id(conn)

    reorder_data(conn)

    conn.close()

if __name__ == '__main__':
    main()
