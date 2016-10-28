# Spider_CNKI
Spider CNKI in python

# File
- spider_cnki.py
  ```python
  python spider_cnki.py
  ```
  抓知网文献数据

  这一步运行完后会在数据库中产生文献信息数据，数据在表 articles 和 resort_articles 中

- get_slink.py
  ```python
  python get_slink.py
  ```
  生成文献引用网络

  这一步运行完后会产生引用关系数据，数据在表 slink 中，并且生成 slink.net 文件

- data_cnki_py_db

  sql File

  运行前请保证你已在 mysql 数据库中建立了相应的表结构（在 data_cnki_py_db/cnki_py1_db.sql 文件中）

  请直接导入 data_cnki_py_db/cnki_py1_db.sql 文件


  并且，在文件 spider_cnki.py 的 main 中修改你的数据库相关配置信息（库名、用户名、密码）：

  ```python
  def main():
      conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='cnki_py1_db', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
  ```

- in.txt
  爬虫入口

  我是使用 in.txt 里面的文章链接作为爬虫的入口，每一个链接都会引发一棵引文树，采集的多了互有交叉就形成了一个引文网。

  具体的流程：

  文章链接入口 -> 引文列表 -> 遍历文章链接 ->...

  如图：

  ![qq20161013-0](https://cloud.githubusercontent.com/assets/12579211/19353861/564aef54-9197-11e6-8c92-ed8d119f7f18.png)

  循环次数通过 spider_cnki.py 中的全局变量 times 设置，这里我设置的是 5，即循环 5 次。

  ```python
  times = 5
  ```

  in.txt 下链接数目酌情增减，我跑这个花了几十分钟吧（还是一两个小时？具体忘了）

  需求量小的话可以改少一点链接入口，也可以改小全局循环次数，需求大的相反。


- slink.net
  文献引用网络

  抓到的数量如图（Gephi 上显示）：

  ![qq20161013-1](https://cloud.githubusercontent.com/assets/12579211/19355033/6a3d3cac-919b-11e6-98a3-714e0b99a298.png)
