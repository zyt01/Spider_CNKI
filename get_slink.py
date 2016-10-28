#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import pymysql
import pymysql.cursors

def replace_char(old_str):
    if(old_str == None):
        return '';
    new_str = re.sub(r'\'', "’", old_str)
    new_str = re.sub(r'\"', "”", new_str)
    new_str = re.sub(r'\n', "", new_str)
    return new_str

def create_net(conn, file_write):
	fw = open(file_write, 'w+')

	get_article_cur = conn.cursor()
	get_slink_cur = conn.cursor()

	# get_article_cur.execute("SELECT DISTINCT `id`, `title` FROM `resort_articles` ORDER BY `id`")
	get_article_cur.execute("SELECT DISTINCT `id`, `title` FROM `articles_id` ORDER BY `id`")

	file_write_node = '*Vertices %d\n' % (get_article_cur.rowcount)
	print file_write_node
	fw.write(file_write_node)
	for article_row in get_article_cur:
		article_id = article_row.get('id')
		article_title = article_row.get('title').encode('utf-8')

		file_write_str = "%s \"%s\"\n" % (article_id, replace_char(article_title))
		print(file_write_str)
		fw.write(file_write_str)

	get_slink_cur.execute("SELECT DISTINCT `article_id`, `reference_id` FROM `slink` ORDER BY `id`")

	file_write_edge = '*arcs\n'
	print file_write_edge
	fw.write(file_write_edge)
	for slink_row in get_slink_cur:
		article_id = slink_row.get('article_id')
		reference_id = slink_row.get('reference_id')

		file_write_str = "%s %s\n" % (article_id, reference_id)
		print(file_write_str)
		fw.write(file_write_str)

	get_article_cur.close()
	get_slink_cur.close()

	fw.close()

def get_slink(conn):
	get_cur = conn.cursor()
	insert_cur = conn.cursor()

	get_cur.execute("SELECT DISTINCT `id`,`filename` FROM `articles_id` WHERE `filename` != 'None'")

	i = 0
	j = 0
	for row in get_cur:
		article_id = row.get('id')
		article_filename = row.get('filename')
		i = i + 1
		print(i,article_id,article_filename)

		# insert_sql_string = ''
		get_row_cur = conn.cursor()
		sql_string = "SELECT DISTINCT `fileid` FROM `resort_articles` WHERE `toname` = '%s'" % (article_filename)
		# print sql_string
		get_row_cur.execute(sql_string)

		for reference_row in get_row_cur:
			reference_id = reference_row.get('fileid')
			if reference_id != '':
				j = j + 1
				insert_sql_string = "INSERT IGNORE INTO `slink` (`id`, `article_id`, `reference_id`) VALUES (%d, '%s', '%s');" % (j, article_id, reference_id)
				print insert_sql_string
				insert_cur.execute(insert_sql_string)

			print(j,article_id,reference_id)
			get_row_cur.close()
			conn.commit()

			# create_net('slink.net', file_write_str)

	get_cur.close()
	insert_cur.close()

def main():
	conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='cnki_py2_db', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

	get_slink(conn)
	create_net(conn, 'slink1.net')
	conn.close()

if __name__ == '__main__':
	main()
