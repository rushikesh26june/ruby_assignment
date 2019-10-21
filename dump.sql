CREATE DATABASE  IF NOT EXISTS `ruby_assignment` /*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_bin */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `ruby_assignment`;
-- MySQL dump 10.13  Distrib 8.0.17, for macos10.14 (x86_64)
--
-- Host: localhost    Database: ruby_assignment
-- ------------------------------------------------------
-- Server version	8.0.17

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `main_group`
--

DROP TABLE IF EXISTS `main_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_group` (
  `idmain_group` varchar(45) COLLATE utf8_bin NOT NULL,
  `name_main_group` varchar(45) COLLATE utf8_bin NOT NULL,
  `type_main_group` varchar(45) COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`idmain_group`),
  UNIQUE KEY `name_main_group_UNIQUE` (`name_main_group`),
  UNIQUE KEY `type_main_group_UNIQUE` (`type_main_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_group`
--

LOCK TABLES `main_group` WRITE;
/*!40000 ALTER TABLE `main_group` DISABLE KEYS */;
INSERT INTO `main_group` VALUES ('SMG-0001','Apple','Fruits');
/*!40000 ALTER TABLE `main_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `master_group`
--

DROP TABLE IF EXISTS `master_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `master_group` (
  `idmaster_group` varchar(45) COLLATE utf8_bin NOT NULL,
  `name_master_group` varchar(45) COLLATE utf8_bin NOT NULL,
  `sell_uom_master_group` varchar(45) COLLATE utf8_bin DEFAULT NULL,
  `sell_uom_type_main_group` varchar(45) COLLATE utf8_bin DEFAULT NULL,
  `sell_uom_avg_wt_per_uom_master_group` double DEFAULT NULL,
  `packaging_cost_master_group` double DEFAULT NULL,
  `loading_percent_master_group` double DEFAULT NULL,
  `idparent_group` varchar(45) COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`idmaster_group`),
  UNIQUE KEY `idmaster_group_UNIQUE` (`idmaster_group`),
  UNIQUE KEY `name_master_group_UNIQUE` (`name_master_group`),
  KEY `idparent_group` (`idparent_group`),
  CONSTRAINT `idparent_group` FOREIGN KEY (`idparent_group`) REFERENCES `parent_group` (`idparent_group`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `master_group`
--

LOCK TABLES `master_group` WRITE;
/*!40000 ALTER TABLE `master_group` DISABLE KEYS */;
INSERT INTO `master_group` VALUES ('RO-300007','Apple-Fuji Loose','Loose','kg',1,0,25,'RI-50008'),('RO-300008','Apple-Fuji Loose (500 gm)','Loose','kg',1,0,40,'RI-50008');
/*!40000 ALTER TABLE `master_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `parent_group`
--

DROP TABLE IF EXISTS `parent_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `parent_group` (
  `idparent_group` varchar(45) COLLATE utf8_bin NOT NULL,
  `name_parent_group` varchar(45) COLLATE utf8_bin NOT NULL,
  `purchase_type_parent_group` varchar(45) COLLATE utf8_bin DEFAULT NULL,
  `uom_parent_group` varchar(45) COLLATE utf8_bin DEFAULT NULL,
  `weight_per_uom_parent_group` double DEFAULT NULL,
  `recovery_parent_group` double DEFAULT NULL,
  `group_parent_group` varchar(45) COLLATE utf8_bin DEFAULT NULL,
  `idmain_group` varchar(45) COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`idparent_group`),
  UNIQUE KEY `idparent_group_UNIQUE` (`idparent_group`),
  UNIQUE KEY `name_parent_group_UNIQUE` (`name_parent_group`),
  KEY `idmain_group` (`idmain_group`),
  CONSTRAINT `idmain_group` FOREIGN KEY (`idmain_group`) REFERENCES `main_group` (`idmain_group`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `parent_group`
--

LOCK TABLES `parent_group` WRITE;
/*!40000 ALTER TABLE `parent_group` DISABLE KEYS */;
INSERT INTO `parent_group` VALUES ('RI-50008','Apple-Fuji','Loose','kg',1,100,'Apple','SMG-0001');
/*!40000 ALTER TABLE `parent_group` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-10-21 13:48:13
