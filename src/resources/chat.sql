/*
SQLyog Ultimate v9.30 
MySQL - 5.5.31-log : Database - chat
*********************************************************************
*/


/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`chat` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `chat`;

/*Table structure for table `user` */

DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `pid` int(11) NOT NULL AUTO_INCREMENT,
  `loginName` varchar(20) NOT NULL COMMENT '登录名',
  `password` varchar(64) NOT NULL COMMENT '密码',
  `nickName` varchar(20) NOT NULL COMMENT '呢称',
  `serial` varchar(64) NOT NULL COMMENT '唯一序列号',
  `status` int(1) DEFAULT '1' COMMENT '用户状态。1未登录，2已登录',
  PRIMARY KEY (`pid`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8;

/*Data for the table `user` */

insert  into `user`(`pid`,`loginName`,`password`,`nickName`,`serial`,`status`) values (16,'chenghao','96e79218965eb72c92a549dd5a330112','那脸憔悴','ef7ea180-5371-4332-9903-5a4f12fbdf30',0),(17,'abc','96e79218965eb72c92a549dd5a330112','左手','4e4f9c74-daca-465e-b980-83394c8a504f',0);

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
