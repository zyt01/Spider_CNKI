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
  运行前请保证你已在 mysql 数据库中建立了相应的表结构（在三个 .sql 文件中）

  如下：
  ```
  CREATE TABLE IF NOT EXISTS `articles` (
    `id` int(11) NOT NULL,
    `title` varchar(500) DEFAULT NULL,
    `author` varchar(300) DEFAULT NULL,
    `abstract` text,
    `keywords` varchar(300) DEFAULT NULL,
    `dbcode` varchar(50) DEFAULT NULL,
    `sid` varchar(300) DEFAULT NULL,
    `filename` varchar(200) DEFAULT NULL,
    `type` int(11) DEFAULT NULL,
    `level` int(11) DEFAULT NULL,
    `href` varchar(500) DEFAULT NULL,
    `toname` varchar(200) DEFAULT NULL
  ) ENGINE=InnoDB AUTO_INCREMENT=13913 DEFAULT CHARSET=utf8;
  ```

  并且，在文件 spider_cnki.py 的 main 中修改你的数据库相关配置信息（库名、用户名、密码）：

  ```python
  def main():
      conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='cnki_py_db', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
  ```

- in.txt
  爬虫入口

- slink.net
  文献引用网络
