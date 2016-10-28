-- phpMyAdmin SQL Dump
-- version 4.4.10
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: 2016-10-25 19:08:01
-- 服务器版本： 5.6.25
-- PHP Version: 5.5.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `cnki_py2_db`
--

-- --------------------------------------------------------

--
-- 表的结构 `articles`
--

CREATE TABLE IF NOT EXISTS `articles` (
  `id` int(11) NOT NULL,
  `title` varchar(500) DEFAULT NULL,
  `author` varchar(300) DEFAULT NULL,
  `abstract` text,
  `keywords` varchar(300) DEFAULT NULL,
  `dbcode` varchar(50) DEFAULT NULL,
  `sid` varchar(300) DEFAULT NULL,
  `filename` varchar(200) DEFAULT NULL,
  `fileid` int(11) DEFAULT NULL,
  `type` int(11) DEFAULT NULL,
  `level` int(11) DEFAULT NULL,
  `href` varchar(500) DEFAULT NULL,
  `toname` varchar(200) DEFAULT NULL
) ENGINE=InnoDB AUTO_INCREMENT=6313 DEFAULT CHARSET=utf8;


-- --------------------------------------------------------

--
-- 表的结构 `articles_id`
--

CREATE TABLE IF NOT EXISTS `articles_id` (
  `id` int(11) NOT NULL,
  `title` varchar(500) DEFAULT NULL,
  `filename` varchar(200) DEFAULT NULL
) ENGINE=InnoDB AUTO_INCREMENT=5554 DEFAULT CHARSET=utf8;


-- --------------------------------------------------------

--
-- 表的结构 `resort_articles`
--

CREATE TABLE IF NOT EXISTS `resort_articles` (
  `id` int(11) NOT NULL,
  `title` varchar(500) DEFAULT NULL,
  `author` varchar(500) DEFAULT NULL,
  `abstract` text,
  `keywords` varchar(500) DEFAULT NULL,
  `dbcode` varchar(50) DEFAULT NULL,
  `sid` varchar(300) DEFAULT NULL,
  `filename` varchar(200) DEFAULT NULL,
  `fileid` int(11) DEFAULT NULL,
  `type` int(11) DEFAULT NULL,
  `level` int(11) DEFAULT NULL,
  `href` varchar(500) DEFAULT NULL,
  `toname` varchar(200) DEFAULT NULL
) ENGINE=InnoDB AUTO_INCREMENT=6313 DEFAULT CHARSET=utf8;


-- --------------------------------------------------------

--
-- 表的结构 `slink`
--

CREATE TABLE IF NOT EXISTS `slink` (
  `id` int(11) NOT NULL,
  `article_id` varchar(200) DEFAULT NULL,
  `reference_id` varchar(200) DEFAULT NULL
) ENGINE=InnoDB AUTO_INCREMENT=6270 DEFAULT CHARSET=utf8;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `articles`
--
ALTER TABLE `articles`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `articles_id`
--
ALTER TABLE `articles_id`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `resort_articles`
--
ALTER TABLE `resort_articles`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `slink`
--
ALTER TABLE `slink`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `articles`
--
ALTER TABLE `articles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=6313;
--
-- AUTO_INCREMENT for table `articles_id`
--
ALTER TABLE `articles_id`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=5554;
--
-- AUTO_INCREMENT for table `resort_articles`
--
ALTER TABLE `resort_articles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=6313;
--
-- AUTO_INCREMENT for table `slink`
--
ALTER TABLE `slink`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=6270;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
