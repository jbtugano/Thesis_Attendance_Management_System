-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: 192.168.1.2    Database: thesis_system
-- ------------------------------------------------------
-- Server version	8.0.36

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `academicyear`
--

DROP TABLE IF EXISTS `academicyear`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `academicyear` (
  `id` int NOT NULL AUTO_INCREMENT,
  `year` varchar(50) NOT NULL,
  `start` datetime NOT NULL,
  `end` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `academicyear`
--

LOCK TABLES `academicyear` WRITE;
/*!40000 ALTER TABLE `academicyear` DISABLE KEYS */;
INSERT INTO `academicyear` VALUES (1,'2324','2024-01-24 00:00:00','2024-08-10 00:00:00');
/*!40000 ALTER TABLE `academicyear` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `activity`
--

DROP TABLE IF EXISTS `activity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `activity` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `description` varchar(100) DEFAULT NULL,
  `activity_img` varchar(50) DEFAULT NULL,
  `activity_limit` smallint DEFAULT NULL,
  `is_offered` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `activity`
--

LOCK TABLES `activity` WRITE;
/*!40000 ALTER TABLE `activity` DISABLE KEYS */;
INSERT INTO `activity` VALUES (1,'ACT0',NULL,NULL,NULL,1),(2,'ACT1',NULL,NULL,NULL,1),(3,'ACT2',NULL,NULL,NULL,1),(4,'FITNESS',NULL,NULL,NULL,1),(5,'VOLLEYBALL/BASKETBALL',NULL,NULL,NULL,1),(6,'DANCE',NULL,NULL,NULL,1),(7,'VOLLEYBALL',NULL,NULL,NULL,1),(8,'BASEBALL','Lorem Test','Some Link 2',40,1),(9,'BASKETBALL','Lorem Test','Some Link 2',40,1),(10,'testactivity','Lorem ipsum dolor sit',NULL,40,1),(11,'testlangule','Lorem ipsum dolor sit',NULL,40,1),(12,'testlangule3','Lorem ipsum dolor sit',NULL,40,1);
/*!40000 ALTER TABLE `activity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `classinfo`
--

DROP TABLE IF EXISTS `classinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `classinfo` (
  `id` int NOT NULL AUTO_INCREMENT,
  `room` varchar(50) DEFAULT NULL,
  `facultyid` int DEFAULT NULL,
  `activity_id` int DEFAULT NULL,
  `schedule_id` int DEFAULT NULL,
  `section_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `facultyid` (`facultyid`),
  KEY `activity_id` (`activity_id`),
  KEY `schedule_id` (`schedule_id`),
  KEY `section_id` (`section_id`),
  CONSTRAINT `classinfo_ibfk_1` FOREIGN KEY (`facultyid`) REFERENCES `faculty` (`id`),
  CONSTRAINT `classinfo_ibfk_2` FOREIGN KEY (`activity_id`) REFERENCES `activity` (`id`),
  CONSTRAINT `classinfo_ibfk_3` FOREIGN KEY (`schedule_id`) REFERENCES `schedule` (`id`),
  CONSTRAINT `classinfo_ibfk_4` FOREIGN KEY (`section_id`) REFERENCES `section` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `classinfo`
--

LOCK TABLES `classinfo` WRITE;
/*!40000 ALTER TABLE `classinfo` DISABLE KEYS */;
INSERT INTO `classinfo` VALUES (1,'SRDB',2,4,5,3),(2,'SRDB',2,8,5,4),(3,'SRDB',1,5,5,1),(4,'SRDB',2,9,6,5);
/*!40000 ALTER TABLE `classinfo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `daysummary`
--

DROP TABLE IF EXISTS `daysummary`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `daysummary` (
  `id` int NOT NULL AUTO_INCREMENT,
  `img_proof` varchar(100) NOT NULL,
  `date_time` datetime NOT NULL,
  `student_id` int DEFAULT NULL,
  `class_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `student_id` (`student_id`),
  KEY `class_id` (`class_id`),
  CONSTRAINT `daysummary_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`id`),
  CONSTRAINT `daysummary_ibfk_2` FOREIGN KEY (`class_id`) REFERENCES `classinfo` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=75 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `daysummary`
--

LOCK TABLES `daysummary` WRITE;
/*!40000 ALTER TABLE `daysummary` DISABLE KEYS */;
INSERT INTO `daysummary` VALUES (1,'','2024-04-01 16:24:30',11,2),(2,'','2024-04-01 16:25:05',11,1),(3,'','2024-04-01 16:28:15',14,1),(4,'','2024-04-01 16:28:18',14,2),(5,'','2024-04-01 17:52:24',5,3),(6,'','2024-04-01 17:52:30',7,3),(7,'static/uploads/ATTEMPTS/8.jpg','2024-05-16 17:34:32',23,1),(8,'static/uploads/ATTEMPTS/13.jpg','2024-05-16 18:02:08',24,2),(9,'static/uploads/ATTEMPTS/15.jpg','2024-05-17 14:23:00',24,1),(10,'static/uploads/ATTEMPTS/18.jpg','2024-05-17 14:31:26',24,1),(11,'static/uploads/ATTEMPTS/22.jpg','2024-05-18 15:27:32',24,1),(12,'static/uploads/ATTEMPTS/23.jpg','2024-05-18 15:29:19',24,1),(13,'static/uploads/ATTEMPTS/24.jpg','2024-05-18 15:29:41',23,1),(14,'static/uploads/ATTEMPTS/25.jpg','2024-05-18 15:30:02',23,1),(15,'static/uploads/ATTEMPTS/27.jpg','2024-05-18 15:40:06',24,1),(16,'static/uploads/ATTEMPTS/28.jpg','2024-05-18 15:40:31',24,1),(17,'static/uploads/ATTEMPTS/29.jpg','2024-05-18 16:01:54',24,1),(18,'static/uploads/ATTEMPTS/30.jpg','2024-05-18 16:34:58',26,1),(19,'static/uploads/ATTEMPTS/31.jpg','2024-05-18 16:37:09',26,1),(20,'static/uploads/ATTEMPTS/34.jpg','2024-05-18 16:50:11',24,1),(21,'static/uploads/ATTEMPTS/35.jpg','2024-05-18 16:50:24',27,1),(22,'static/uploads/ATTEMPTS/36.jpg','2024-05-18 16:50:34',26,1),(23,'static/uploads/ATTEMPTS/37.jpg','2024-05-18 16:50:44',26,1),(24,'static/uploads/ATTEMPTS/41.jpg','2024-05-18 20:16:44',26,1),(25,'static/uploads/ATTEMPTS/46.jpg','2024-05-18 20:18:18',26,1),(26,'static/uploads/ATTEMPTS/65.jpg','2024-05-18 20:19:20',24,1),(27,'static/uploads/ATTEMPTS/88.jpg','2024-05-18 20:26:09',26,1),(28,'static/uploads/ATTEMPTS/97.jpg','2024-05-18 20:32:52',26,1),(29,'static/uploads/ATTEMPTS/105.jpg','2024-05-18 20:37:05',26,1),(30,'static/uploads/ATTEMPTS/116.jpg','2024-05-18 20:38:03',26,2),(31,'static/uploads/ATTEMPTS/155.jpg','2024-05-18 20:41:58',27,1),(32,'static/uploads/ATTEMPTS/156.jpg','2024-05-22 07:58:02',24,1),(33,'static/uploads/ATTEMPTS/157.jpg','2024-05-22 07:58:49',24,2),(34,'static/uploads/ATTEMPTS/160.jpg','2024-05-22 07:59:59',24,1),(35,'static/uploads/ATTEMPTS/161.jpg','2024-05-22 08:00:23',24,1),(36,'static/uploads/ATTEMPTS/167.jpg','2024-05-22 08:05:28',28,1),(37,'static/uploads/ATTEMPTS/168.jpg','2024-05-22 08:05:37',28,1),(38,'static/uploads/ATTEMPTS/169.jpg','2024-05-22 08:06:04',28,1),(39,'static/uploads/ATTEMPTS/170.jpg','2024-05-22 08:06:24',28,1),(40,'static/uploads/ATTEMPTS/171.jpg','2024-05-22 08:06:40',28,1),(41,'static/uploads/ATTEMPTS/172.jpg','2024-05-22 08:07:00',28,1),(42,'static/uploads/ATTEMPTS/173.jpg','2024-05-22 08:07:57',24,1),(43,'static/uploads/ATTEMPTS/174.jpg','2024-05-22 08:17:12',24,1),(44,'static/uploads/ATTEMPTS/175.jpg','2024-05-22 08:17:37',24,1),(45,'static/uploads/ATTEMPTS/176.jpg','2024-05-22 08:17:52',24,1),(46,'static/uploads/ATTEMPTS/177.jpg','2024-05-22 08:18:40',24,1),(47,'static/uploads/ATTEMPTS/178.jpg','2024-05-22 08:19:02',24,1),(48,'static/uploads/ATTEMPTS/179.jpg','2024-05-22 08:19:25',24,2),(49,'static/uploads/ATTEMPTS/180.jpg','2024-05-22 08:34:45',24,1),(50,'static/uploads/ATTEMPTS/181.jpg','2024-05-22 08:37:45',24,1),(51,'static/uploads/ATTEMPTS/182.jpg','2024-05-22 08:38:08',28,1),(52,'static/uploads/ATTEMPTS/184.jpg','2024-05-22 08:44:06',24,2),(53,'static/uploads/ATTEMPTS/185.jpg','2024-05-24 14:25:16',24,1),(54,'static/uploads/ATTEMPTS/186.jpg','2024-05-24 14:25:25',26,1),(55,'static/uploads/ATTEMPTS/283.jpg','2024-05-24 14:41:47',26,3),(56,'static/uploads/ATTEMPTS/284.jpg','2024-05-24 16:00:51',26,1),(57,'static/uploads/ATTEMPTS/285.jpg','2024-05-24 16:02:47',24,2),(58,'static/uploads/ATTEMPTS/295.jpg','2024-05-24 16:24:37',24,3),(59,'static/uploads/ATTEMPTS/302.jpg','2024-05-24 16:25:41',24,1),(60,'static/uploads/ATTEMPTS/303.jpg','2024-05-30 14:26:50',23,1),(61,'static/uploads/ATTEMPTS/304.jpg','2024-05-30 14:27:16',28,2),(62,'static/uploads/ATTEMPTS/305.jpg','2024-05-30 14:33:02',24,1),(63,'static/uploads/ATTEMPTS/306.jpg','2024-05-30 14:33:13',28,2),(64,'static/uploads/ATTEMPTS/307.jpg','2024-05-30 14:45:03',23,1),(65,'static/uploads/ATTEMPTS/308.jpg','2024-05-30 15:02:39',23,1),(66,'static/uploads/ATTEMPTS/309.jpg','2024-05-30 15:03:43',24,2),(67,'static/uploads/ATTEMPTS/310.jpg','2024-05-30 15:12:23',29,1),(68,'static/uploads/ATTEMPTS/311.jpg','2024-05-31 00:43:09',24,1),(69,'static/uploads/ATTEMPTS/313.jpg','2024-05-31 00:45:37',24,1),(70,'static/uploads/ATTEMPTS/316.jpg','2024-05-31 00:46:57',24,1),(71,'static/uploads/ATTEMPTS/345.jpg','2024-05-31 00:55:52',26,1),(72,'static/uploads/ATTEMPTS/350.jpg','2024-05-31 01:03:09',24,1),(73,'static/uploads/ATTEMPTS/384.jpg','2024-05-31 01:04:22',24,1),(74,'static/uploads/ATTEMPTS/387.jpg','2024-05-31 01:52:13',24,1);
/*!40000 ALTER TABLE `daysummary` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `faceid`
--

DROP TABLE IF EXISTS `faceid`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `faceid` (
  `id` int NOT NULL AUTO_INCREMENT,
  `faceid` varchar(50) NOT NULL,
  `studentid` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `studentid` (`studentid`),
  CONSTRAINT `faceid_ibfk_1` FOREIGN KEY (`studentid`) REFERENCES `students` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `faceid`
--

LOCK TABLES `faceid` WRITE;
/*!40000 ALTER TABLE `faceid` DISABLE KEYS */;
/*!40000 ALTER TABLE `faceid` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `faculty`
--

DROP TABLE IF EXISTS `faculty`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `faculty` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `id_number` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `id_number` (`id_number`),
  CONSTRAINT `faculty_ibfk_1` FOREIGN KEY (`id_number`) REFERENCES `userrole` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `faculty`
--

LOCK TABLES `faculty` WRITE;
/*!40000 ALTER TABLE `faculty` DISABLE KEYS */;
INSERT INTO `faculty` VALUES (1,'Fors, Hans Eli T.','2013-1024E'),(2,'Lengyel, Felix X.','2013-1000E');
/*!40000 ALTER TABLE `faculty` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `logininfo`
--

DROP TABLE IF EXISTS `logininfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `logininfo` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` varchar(50) NOT NULL,
  `passwd` varchar(200) NOT NULL,
  `email` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `logininfo_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `userrole` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `logininfo`
--

LOCK TABLES `logininfo` WRITE;
/*!40000 ALTER TABLE `logininfo` DISABLE KEYS */;
INSERT INTO `logininfo` VALUES (1,'2013-1024E','scrypt:32768:8:1$RzzmDRnIXFBI3QyA$ba82ce0e92ef54d1418bab190ae712c65201672389bad11d8ff00d2a5750a8c9acc33fd9692878853715ec6f73e41d7cc051902cde5e119761baa0686976be72','prof1@gmail.com'),(2,'2013-1000E','scrypt:32768:8:1$F0B0N0xWii9bL7J7$bb1a33e77224fd6d082a27513243bd156de79cccb74dd349d0cd9e26fac100ccb787103ebc6578ac8ac2437e8ebab87c5a59b5a83832783eafb32b68fc510f05','testc@gmail.com'),(4,'2015-2-01351','scrypt:32768:8:1$p8ysVOGlD0pTz6Bs$9854ee45189fa7d653b1185490fbd653be0a0be6f65216e596c6b00c9390b9f29c0aaf9579dccf785ce2451c115414d8134274856ca1f958701f228879a5e569','testb74@gmail.com'),(5,'2015-2-01355','scrypt:32768:8:1$fqbKhEhHExjiszUC$9de5c4e01b5ab90af2e73993c15aaeabd9aac412db8bd81545f6f3ef4fcb3665d180b82b8a9f09cc017597d099988d02b4ec93a0558f283bd152c39961ee44dd','testb17@gmail.com'),(6,'2015-2-01322','scrypt:32768:8:1$dfj0GpEGMgSyQgDh$65fd9380c1aa8a0cad80293c9e83c668f0640a352471e7fedca5c26f0fec9ac86a050a7d8e32013027508ee2eec8ba10377a2a3610e75e53aabeefddc98185b9','testb66@gmail.com'),(7,'2015-2-08893','scrypt:32768:8:1$e42s5ZzQtyhvpphQ$8d22eac9e1bbb10f2cf1339e88608416418188d081f6a5ab9cc9745c684261f6366a91ae0ae26aab6e329f6a19f4f3ee73bb5766ebbb08edeb2adbd4b5b7df2a','testb91@gmail.com'),(8,'2019-2-91852','scrypt:32768:8:1$LiJnG7HmKR8iUJNa$4dde0ac4bebf7d0f43ff1a7bb558f019d2e5fab6c4cf9b268607bde6bbdffb83537e042173c3c8a21b230d223cf91d2a64fa4f55e965ecd9ebf6ff0a65f8ccbe','testb48@gmail.com'),(9,'2022-2-98315','scrypt:32768:8:1$XXgD7BJk4A6q0dGm$1cff8c664c70fa304277613542d67f2bb06440a0e51b5a9af8574c93a0bc982b2b677b7e7289e0eaf5dd07ed4ad28473743212664c7b98f58febe07a10351486','testb90@gmail.com'),(10,'2012-5-12352','scrypt:32768:8:1$Pq1UxEGwtcVNFeKf$23c414020fc5b1f432faef54034a3397b1574dc98dfdd39c03bac0bc1e9ad55701ae0de5fa5a9599276d5c13ef3ecd27fb3112cb557dd8b5e644cf925336ced9','testb8@gmail.com'),(11,'2022-2-95125','scrypt:32768:8:1$8mjZDKaRFGqGPO1f$db5bf1740ba8ee712b7edbff0a4b3dc8b3a9de42d7921d9eb6eb293708076daaf8457b9d2b68b6b033b7337a18e18fcae3be1467a34578bbbf091a54939385e6','testb60@gmail.com'),(12,'2015-2-90481','scrypt:32768:8:1$BKf6MIdiKVIihKdX$81269d1395a1d5fc88830c805d4e97588c894d53e0a984af26d918224343aa898ce184f36d9043b0ba28ac5ec96922067440dabd4ccca5ad08bc4820299b6d2c','testb84@gmail.com'),(13,'2023-2-73062','scrypt:32768:8:1$8j26HkHjOaootYfU$ce88cfdd7cb3d1db2189e4ba1f30b413f2c4bf131f43cb40787d329611e147d9dd65a5c4964587c4ce666c4c907209a6e0995ede89b33b677edc4710d4df090d','testb23@gmail.com'),(14,'2024-2-44267','scrypt:32768:8:1$00q9q2IxhLIAvQdx$46b8c7fea16a3b40e0bc1a90e0a3454eefee7cbad26554385fbef752c0a6cfa0bd663510a38511af77e144ea49deb495b26629a4c4568044fab9df77f0e6b105','testb27@gmail.com'),(15,'2024-2-18592','scrypt:32768:8:1$gDfWk6aV0wLzoCtL$b233275f516554289681bddc68148e0e329da0b1503350c50df5c2efdcd5f6e21f82b1ec87bdb99a509434d8bf9f1a7350a0a5c41f8866edc15e978a9afb152e','testb7249@gmail.com'),(16,'2024-2-85721','scrypt:32768:8:1$7sgni0XD4zTSWA9m$d376210c6e5900cef571ffd461dae6cfa4e5ebaa29e91b7c7f8f19476931e8cb6cfde9437bade4d92e7708d2aeed4bbb03f5af42cb57034f9af323b30775bb8b','testb26@gmail.com'),(17,'2024-2-29604','scrypt:32768:8:1$qi5AydIFYwpwNOtv$311f96e217c8de7711c80b90d704da0076a8073aafce6668e246eaef8e326b3844e3abcf6b0e0002b0541ada2398d4af293cf9a99015fdd3cde1a87792596fe6','testb10@gmail.com'),(18,'2024-2-99967','scrypt:32768:8:1$4hw0nzRYUPAKbBtN$6188c0a6f9504ef41f87223a25802d70c0fd8a0fb2a0da95af2cb64daa940c197bae87e2775c7931d4c12d7d692e4f8126c3664d7631e9100a4b44ce0ae755ba','testb42@gmail.com'),(19,'2024-2-76512','scrypt:32768:8:1$DyBQOwoEju0XvOVo$cdabe17a1b964eb813cc4f0dbd9db29bc3e23db24e90d7a5439895e76da819de1ffe502731d3b06476e8d448ce2915e26dfc1cd2dff83b7593bbc4523e5d43ed','testb66@gmail.com'),(20,'2024-2-66733','scrypt:32768:8:1$vqL3LieKfQjTOZSw$a4a304cb8082edfa22bb346949aba917dcd3948f14361f3c0d1ad8db48432684a573d2c838124dd90d4aa64cc4e6b01f83482e1f3fd8b886c4d41944a4c6cbed','testb16@gmail.com'),(21,'2024-2-26638','scrypt:32768:8:1$TB91J7xOXNrLkSAM$5390d647df27e362f569ac19f7dca45bb48500e36f34ed967a2abf63e6a7e740eab1a96a2a53aef2bcce0d67fa654f1cc73b4442f785c5e8556e597be7fbc69c','testb22@gmail.com'),(22,'2024-2-87658','scrypt:32768:8:1$YyWWzcu7lGzMYAwI$974fdd310e16c3eaae9258a02601dc840611c39b104a3ff2ac9be7e404bdb5975ec2fc09bfcdf9cd4439e5092f20129a2a88b4d03363529bd47f6ddd7abb9d23','testb29@gmail.com'),(23,'2024-2-39566','scrypt:32768:8:1$mFqh2nI9b4XaNFzr$4acea94d90295ca39e5b1f55178d26ff228b6f90cbc8d899cd23397ec93be185ca6dd4518e3d9e08088507892194660880f3118da818249f5f6bd27c77ffef3b','testb74@gmail.com'),(31,'2015-2-01350','scrypt:32768:8:1$2u6icVyuOgjFcIrw$5b3f7030436d78026912defcc733293d77bad1c83ade342a1ffbc58222dbc5c818d7a933851a700fda56fe61b3c0bf9d5edcb3921ffc3d56a0316c78c25416b9','andrewtapawan@yahoo.com'),(32,'1233333','scrypt:32768:8:1$ezCiDe3O1ldYmIre$91b538a2f4cdd6d354f02fe896f85d922f67630ef7d520a295da4e51935c159c49effd0a52c07e8e61cba9da289b50af0a7d31d2811ab65b64b01de5515eec15','seansean@test.com'),(33,'2019-2-2222','scrypt:32768:8:1$prmJ9URqmGb6fNGy$8ba9465802f59dd24b6278100ac9852b16f33ec3d4e9373a360987e7c3bbb335c9cadb00dc020f14b2176b48a1e288208b99a2c2a379e39ea4d283a6f8dba2f8','eli@test.com'),(34,'2019-2-01234','scrypt:32768:8:1$qshUSIf5KQZVWLI2$6ee112f9aaf8f5d5161f48cf1dae713321f7a1d346f02425cd1562df174df9a798b0a65eda5bcb9a676941e94178e6a65d328ebc1b55dcca9a848f6933dd4fda','jbtugs@gmail.com'),(35,'2019-2-78950','scrypt:32768:8:1$HgW8IsF5iFoKhyxS$8ad149ba235bc4eadc6aec2130c93ada13b523a0364bfeecbc922e5c6fdea75b0cfedf20186669faeb7d0ed6b43ee2600cb460be01d09dd4156d02dc9b3f96c5','denis1@test.com'),(36,'2019-2-02995','scrypt:32768:8:1$xcEvIiPMcNaTP2zo$df7f4fd254248e005a25623b1e4ccd77bb5b4b51d716366556778723fece4c1a4e3d64262be9600d41f9caf82f69e651b719e42afe375ed02582d6da99022e74','john.tugano@lpunetwork.edu.ph'),(37,'2029-0043','scrypt:32768:8:1$mQ8GOW0nTL3vzaaq$c471fb3b8cca65bc1ba3f4ae8d7f3678390c46cc850ece14ecce0af216a88c87734516fb2a1142114cccf5ed79a5a537388140b78625e7cd385f9a982690e289','jackielyn.hinacay@lpu.edu.ph'),(38,'2017-2-02350','scrypt:32768:8:1$vVyazjTxCzaCghUt$cc2cfa4dda8dbe99c0664eea5c81297024d30b43065da1a55113e23d084cad22d20a0cef0338e892de562da49e361a832f1c1b638975fd83b82c0d7076c0069d','jon.oco@lpunetwork.edu.ph'),(42,'20231456','scrypt:32768:8:1$aFGCjLMw8chlWT2Y$87e1a44fdddafd695a843c6873e045c4fc5b4ab28207d367eadb919242e958894aa392e3eb243fabfda8fb2b3a53a3d144b10ee3bf0e1a8c4cdcb6b7b3c99305','marriel.sofhi@test.com');
/*!40000 ALTER TABLE `logininfo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `schedule`
--

DROP TABLE IF EXISTS `schedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `schedule` (
  `id` int NOT NULL AUTO_INCREMENT,
  `day` varchar(5) NOT NULL,
  `time` varchar(15) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `schedule`
--

LOCK TABLES `schedule` WRITE;
/*!40000 ALTER TABLE `schedule` DISABLE KEYS */;
INSERT INTO `schedule` VALUES (1,'T','9-11'),(2,'F','9-11'),(3,'F','7-9'),(4,'M','8-7'),(5,'T','07:00AM-09:00AM'),(6,'F','02:00PM-04:00PM');
/*!40000 ALTER TABLE `schedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `section`
--

DROP TABLE IF EXISTS `section`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `section` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(15) NOT NULL,
  `course_code` varchar(50) NOT NULL,
  `facultyid` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `facultyid` (`facultyid`),
  CONSTRAINT `section_ibfk_1` FOREIGN KEY (`facultyid`) REFERENCES `faculty` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `section`
--

LOCK TABLES `section` WRITE;
/*!40000 ALTER TABLE `section` DISABLE KEYS */;
INSERT INTO `section` VALUES (1,'IT 201','PATHFIT 4',1),(2,'CS 201','PATHFIT 4',1),(3,'ARCH 201','PATHFIT 4',2),(4,'ME 201','PATHFIT 4',2),(5,'CE 201','PATHFIT4',2);
/*!40000 ALTER TABLE `section` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `semester`
--

DROP TABLE IF EXISTS `semester`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `semester` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `start` datetime NOT NULL,
  `end` datetime NOT NULL,
  `academic_year_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `academic_year_id` (`academic_year_id`),
  CONSTRAINT `semester_ibfk_1` FOREIGN KEY (`academic_year_id`) REFERENCES `academicyear` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `semester`
--

LOCK TABLES `semester` WRITE;
/*!40000 ALTER TABLE `semester` DISABLE KEYS */;
INSERT INTO `semester` VALUES (1,'1st Semester','2023-08-22 00:00:00','2024-01-24 00:00:00',1),(2,'2nd Semester','2024-02-12 00:00:00','2024-06-17 00:00:00',1),(3,'Special Semester','2024-07-01 00:00:00','2024-08-19 00:00:00',1);
/*!40000 ALTER TABLE `semester` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `student_cinfo`
--

DROP TABLE IF EXISTS `student_cinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `student_cinfo` (
  `classinfo_id` int DEFAULT NULL,
  `student_id` int DEFAULT NULL,
  KEY `classinfo_id` (`classinfo_id`),
  KEY `student_id` (`student_id`),
  CONSTRAINT `student_cinfo_ibfk_1` FOREIGN KEY (`classinfo_id`) REFERENCES `classinfo` (`id`),
  CONSTRAINT `student_cinfo_ibfk_2` FOREIGN KEY (`student_id`) REFERENCES `students` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student_cinfo`
--

LOCK TABLES `student_cinfo` WRITE;
/*!40000 ALTER TABLE `student_cinfo` DISABLE KEYS */;
/*!40000 ALTER TABLE `student_cinfo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `students`
--

DROP TABLE IF EXISTS `students`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `students` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `joindate` datetime NOT NULL,
  `progress` smallint DEFAULT NULL,
  `program` varchar(10) NOT NULL,
  `sectionid` int DEFAULT NULL,
  `id_number` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `sectionid` (`sectionid`),
  KEY `id_number` (`id_number`),
  CONSTRAINT `students_ibfk_1` FOREIGN KEY (`sectionid`) REFERENCES `section` (`id`),
  CONSTRAINT `students_ibfk_2` FOREIGN KEY (`id_number`) REFERENCES `userrole` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `students`
--

LOCK TABLES `students` WRITE;
/*!40000 ALTER TABLE `students` DISABLE KEYS */;
INSERT INTO `students` VALUES (1,'Escandor, Dummy Data W.','2024-04-01 12:04:48',0,'BS CpE',1,'2015-2-01351'),(2,'Escandor, Dummy Data B.','2024-04-01 12:04:48',0,'BS CpE',1,'2015-2-01355'),(3,'Escandor, Dummy Data C.','2024-04-01 12:04:48',0,'BS ECE',2,'2015-2-01322'),(4,'Escandor, Dummy Data D.','2024-04-01 12:04:48',0,'BS EE',4,'2015-2-08893'),(5,'Escandor, Dummy Data E.','2024-04-01 12:04:48',2,'BS ME',3,'2019-2-91852'),(6,'Escandor, Dummy Data F.','2024-04-01 12:04:48',0,'BS CpE',1,'2022-2-98315'),(7,'Escandor, Dummy Data G.','2024-04-01 12:04:48',2,'BS ME',2,'2012-5-12352'),(8,'Qwrgas, Drewwa H.','2024-04-01 12:04:48',0,'BS EE',3,'2022-2-95125'),(9,'Qwgqgas, Dtrqgh I.','2024-04-01 12:04:48',0,'BS ECE',2,'2015-2-90481'),(10,'Qwsahd, Dqwqwrg J.','2024-04-01 12:04:48',0,'BS ECE',3,'2023-2-73062'),(11,'Escandor, Dummy Data W.','2024-04-01 12:07:40',4,'BS IT',1,'2024-2-44267'),(12,'Esadqwwwe, Dummy Data W.','2024-04-01 12:07:40',0,'BS ECE',2,'2024-2-18592'),(13,'Gqgasd, Qweqwf D.','2024-04-01 12:07:40',0,'BS CpE',1,'2024-2-85721'),(14,'Escandow, Dummy Data G.','2024-04-01 12:07:40',4,'BS EE',4,'2024-2-29604'),(15,'Eqwdqwdwqdaz, Dummy Data Z.','2024-04-01 12:07:40',0,'BS CpE',1,'2024-2-99967'),(16,'Qwwgaedh, Wqtqwgqq T.','2024-04-01 12:07:40',0,'BS ME',4,'2024-2-76512'),(17,'Qwrqgbn, Rhqdahbds T.','2024-04-01 12:07:40',0,'BS IT',1,'2024-2-66733'),(18,'Qwfgasfg, Kuyafq W.','2024-04-01 12:07:40',0,'BS ME',3,'2024-2-26638'),(19,'Qdasg, Ateqqqwgb G.','2024-04-01 12:07:40',0,'BS CpE',4,'2024-2-87658'),(20,'Afqgaa, Gqhzhb N.','2024-04-01 12:07:40',0,'BS EE',1,'2024-2-39566'),(21,'Escandor, Andrew T.','2024-05-16 14:19:22',0,'BS CpE',3,'2015-2-01350'),(22,'Seantugano, Sean Z.','2024-05-16 15:34:39',0,'BS IT',2,'1233333'),(23,'Abucejo, Eleazar S.','2024-05-16 16:03:53',12,'BS CpE',3,'2019-2-2222'),(24,'Tugano, John Benedict Z.','2024-05-16 17:54:57',72,'BS ECE',2,'2019-2-01234'),(25,'Trillo, Dennis .','2024-05-17 14:28:44',0,'BS ECE',2,'2019-2-78950'),(26,'Tugs, Jb Z.','2024-05-18 16:31:37',28,'BS CpE',2,'2019-2-02995'),(27,'Hinacay, Jackielyn Larin.','2024-05-18 16:48:29',4,'BS ECE',2,'2029-0043'),(28,'Oco, Jon Robert R.','2024-05-22 08:04:18',18,'BS CpE',2,'2017-2-02350'),(29,'Sofhia, Marriel D.','2024-05-30 15:11:40',2,'BS IT',1,'20231456');
/*!40000 ALTER TABLE `students` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `term`
--

DROP TABLE IF EXISTS `term`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `term` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `start` datetime NOT NULL,
  `end` datetime NOT NULL,
  `semester_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `semester_id` (`semester_id`),
  CONSTRAINT `term_ibfk_1` FOREIGN KEY (`semester_id`) REFERENCES `semester` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `term`
--

LOCK TABLES `term` WRITE;
/*!40000 ALTER TABLE `term` DISABLE KEYS */;
INSERT INTO `term` VALUES (1,'Prelim','2023-08-22 00:00:00','2023-09-26 00:00:00',1),(2,'Midterm','2023-09-27 00:00:00','2023-11-14 00:00:00',1),(3,'Finals','2023-11-15 00:00:00','2024-01-09 00:00:00',1),(4,'Prelim','2024-02-12 00:00:00','2024-03-16 00:00:00',2),(5,'Midterm','2024-03-17 00:00:00','2024-04-27 00:00:00',2),(6,'Finals','2024-04-28 00:00:00','2024-06-15 00:00:00',2),(7,'Midterm','2024-07-01 00:00:00','2024-07-20 00:00:00',3),(8,'Finals','2024-07-21 00:00:00','2024-08-10 00:00:00',3);
/*!40000 ALTER TABLE `term` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `timeperiod`
--

DROP TABLE IF EXISTS `timeperiod`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `timeperiod` (
  `id` int NOT NULL AUTO_INCREMENT,
  `day` varchar(5) NOT NULL,
  `time` varchar(15) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `timeperiod`
--

LOCK TABLES `timeperiod` WRITE;
/*!40000 ALTER TABLE `timeperiod` DISABLE KEYS */;
/*!40000 ALTER TABLE `timeperiod` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `userrole`
--

DROP TABLE IF EXISTS `userrole`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `userrole` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` varchar(50) NOT NULL,
  `user_level` smallint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `userrole`
--

LOCK TABLES `userrole` WRITE;
/*!40000 ALTER TABLE `userrole` DISABLE KEYS */;
INSERT INTO `userrole` VALUES (1,'2013-1024E',1),(2,'2013-1000E',1),(4,'2015-2-01351',2),(5,'2015-2-01355',2),(6,'2015-2-01322',2),(7,'2015-2-08893',2),(8,'2019-2-91852',2),(9,'2022-2-98315',2),(10,'2012-5-12352',2),(11,'2022-2-95125',2),(12,'2015-2-90481',2),(13,'2023-2-73062',2),(14,'2024-2-44267',2),(15,'2024-2-18592',2),(16,'2024-2-85721',2),(17,'2024-2-29604',2),(18,'2024-2-99967',2),(19,'2024-2-76512',2),(20,'2024-2-66733',2),(21,'2024-2-26638',2),(22,'2024-2-87658',2),(23,'2024-2-39566',2),(31,'2015-2-01350',2),(33,'1233333',2),(34,'2019-2-2222',2),(35,'2019-2-01234',2),(36,'2019-2-78950',2),(37,'2019-2-02995',2),(38,'2029-0043',2),(39,'2017-2-02350',2),(44,'20231456',2);
/*!40000 ALTER TABLE `userrole` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-05-31 12:51:48
