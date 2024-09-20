-- MySQL dump 10.13  Distrib 8.0.35, for macos13 (arm64)
--
-- Host: 127.0.0.1    Database: navalweb
-- ------------------------------------------------------
-- Server version	8.0.35

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
-- Table structure for table `pelanggaran`
--

DROP TABLE IF EXISTS `pelanggaran`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pelanggaran` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tgl_pelanggaran` date DEFAULT NULL,
  `jenis_pelanggaran` varchar(255) DEFAULT NULL,
  `nomor_plat` varchar(255) DEFAULT NULL,
  `gambar_pelanggaran` varchar(255) DEFAULT NULL,
  `gambar_plat_nomor` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pelanggaran`
--

LOCK TABLES `pelanggaran` WRITE;
/*!40000 ALTER TABLE `pelanggaran` DISABLE KEYS */;
INSERT INTO `pelanggaran` VALUES (1,'2024-02-28','Penumpang Tidak ada','N 2345 GR','assets/logo.png','assets/logo.png'),(2,'2024-02-29','Penumpang Bunuh Diri','M 3 LI','assets/logo.png','assets/logo.png'),(3,'2024-03-01','Penumpang Bootlop','M 3 LI','assets/logo.png','assets/logo.png'),(4,'2024-02-27','Penumpang coli','M 3 M 3 K','assets/logo.png','assets/logo.png'),(5,'2024-02-24','Pengendara berimajinasi','N 90C0 K','assets/logo.png','assets/logo.png');
/*!40000 ALTER TABLE `pelanggaran` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-03-25 13:50:28
