# coding = utf-8
import requests
import jieba
import jieba.analyse
import re
from bs4 import BeautifulSoup
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def create_html(url):
    r = requests.get(url)
    return r.text

def main():
    article_url = 'http://www.cnki.net/KCMS/detail/detail.aspx?dbcode=CMFD&dbname=CMFD201301&filename=1013121221.nh'
    html_code = create_html(article_url)
    soup = BeautifulSoup(html_code, 'html.parser')

    article_title = soup.find(id="chTitle").get_text()

    abstract = soup.find(id="ChDivSummary").get_text()

    keywords = soup.find(id="ChDivKeyWord").get_text()

    seg_list = jieba.cut(abstract, cut_all=False)

    print article_title
    print abstract
    print keywords
    # re.sub(r"/\s(?=\s)/", "\\1", keywords)
    # keywords.replace(u"\n", "")
    print keywords
    print("/ ".join(seg_list))
    for x, w in jieba.analyse.extract_tags(abstract, withWeight=True):
        print('%s %s' % (x, w))

    wordcloud = WordCloud(max_font_size=40, relative_scaling=.5).generate(abstract)
    plt.figure()
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()

if __name__ == '__main__':
    main()
