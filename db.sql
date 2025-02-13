/*
SQLyog Enterprise - MySQL GUI v6.56
MySQL - 5.5.5-10.1.13-MariaDB : Database - missing_child
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/`missing_child` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `missing_child`;

/*Table structure for table `child_identification_data` */

DROP TABLE IF EXISTS `child_identification_data`;

CREATE TABLE `child_identification_data` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `child_id` varchar(100) DEFAULT NULL,
  `child_name` varchar(100) DEFAULT NULL,
  `parent_name` varchar(100) DEFAULT NULL,
  `parent_number` varchar(100) DEFAULT NULL,
  `date` varchar(100) DEFAULT NULL,
  `time` varchar(100) DEFAULT NULL,
  `station_email` varchar(100) DEFAULT NULL,
  `photo` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;

/*Data for the table `child_identification_data` */

insert  into `child_identification_data`(`id`,`child_id`,`child_name`,`parent_name`,`parent_number`,`date`,`time`,`station_email`,`photo`) values (1,'MSID1','lakshmi','Bala','9458752125','2023-02-28','13:16:15','nagamchenchulakshmim@gmail.com','MSID1.jpg'),(2,'MSID1','lakshmi','Bala','9458752125','2023-02-28','13:16:16','nagamchenchulakshmim@gmail.com','MSID1.jpg'),(3,'MSID2','Balram','Bhagaban','7410258963','2023-02-28','13:28:32','nagamchenchulakshmim@gmail.com','MSID270.jpg'),(4,'MSID2','Balram','Bhagaban','7410258963','2023-02-28','13:28:33','nagamchenchulakshmim@gmail.com','MSID29.jpg'),(5,'MSID1','lakshmi','Bala','9458752125','2023-02-28','13:28:34','nagamchenchulakshmim@gmail.com','MSID162.jpg'),(6,'MSID2','Balram','Bhagaban','7410258963','2023-02-28','13:28:35','nagamchenchulakshmim@gmail.com','MSID274.jpg');

/*Table structure for table `missing_child_data` */

DROP TABLE IF EXISTS `missing_child_data`;

CREATE TABLE `missing_child_data` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `child_id` varchar(100) DEFAULT 'MSID1',
  `child_name` varchar(100) DEFAULT NULL,
  `parent_name` varchar(100) DEFAULT NULL,
  `parent_number` varchar(100) DEFAULT NULL,
  `address` varchar(100) DEFAULT NULL,
  `date` varchar(100) DEFAULT NULL,
  `time` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `missing_child_data` */

insert  into `missing_child_data`(`id`,`child_id`,`child_name`,`parent_name`,`parent_number`,`address`,`date`,`time`) values (1,'MSID1','lakshmi','Bala','9458752125','Ongole','2023-02-25','15:29:00'),(2,'MSID1','lakshmi','Bala','9458752125','Ongole','2023-02-25','16:10:30'),(3,'MSID2','Balram','Bhagaban','7410258963','Odissa','2023-02-28','13:28:05');

/*Table structure for table `police_station` */

DROP TABLE IF EXISTS `police_station`;

CREATE TABLE `police_station` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `station_id` varchar(100) DEFAULT NULL,
  `station_name` varchar(100) DEFAULT NULL,
  `contact_number` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `address` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `police_station` */

insert  into `police_station`(`id`,`station_id`,`station_name`,`contact_number`,`email`,`address`) values (1,'AP12PS23','Vijayawada City Police','9458752124','nagamchenchulakshmim@gmail.com','GJ3P+8FM, RTA Office Rd, Punammathota, Labbipet, Vijayawada, Andhra Pradesh 520010');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
