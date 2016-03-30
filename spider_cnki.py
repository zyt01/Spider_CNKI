# coding = utf-8
import requests
import jieba
import jieba.analyse
import re
from bs4 import BeautifulSoup
# from wordcloud import WordCloud
import matplotlib.pyplot as plt

def create_html(url):
    r = requests.get(url)
    return r.text

def run_article(url, aricle_from, run_times):
    html_code = create_html(url)
    soup = BeautifulSoup(html_code, 'html.parser')

    article_title = soup.find(id="chTitle").get_text()

    abstract = soup.find(id="ChDivSummary").get_text()

    keywords = soup.find(id="ChDivKeyWord").get_text()
    p=re.compile('\s+')
    keywords = re.sub(p, '', keywords)

    seg_list = jieba.cut(abstract, cut_all=False)

    print article_title

    print abstract

    print keywords

    print("/ ".join(seg_list))
    for x, w in jieba.analyse.extract_tags(abstract, withWeight=True):
        print('%s %s' % (x, w))

    # wordcloud = WordCloud(max_font_size=40, relative_scaling=.5).generate(abstract)
    # plt.figure()
    # plt.imshow(wordcloud)
    # plt.axis("off")
    # plt.show()

def main():
    fd = open('in.txt', 'r')
    for line in fd:
        print line.strip('\n')
        run_article(line.strip('\n'), 0, 0)
    # article_url = 'http://www.cnki.net/KCMS/detail/detail.aspx?dbcode=CMFD&dbname=CMFD201301&filename=1013121221.nh'
    # run_article(article_url, 0, 0)

if __name__ == '__main__':
    main()
