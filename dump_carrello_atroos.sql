-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Creato il: Apr 07, 2023 alle 02:08
-- Versione del server: 10.4.27-MariaDB
-- Versione PHP: 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `carrello atroos`
--
CREATE DATABASE IF NOT EXISTS `carrello atroos` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `carrello atroos`;

-- --------------------------------------------------------

--
-- Struttura della tabella `articles`
--

CREATE TABLE `articles` (
  `Nome` varchar(30) NOT NULL,
  `Prezzo` decimal(12,2) UNSIGNED NOT NULL,
  `Quantita_disponibile` int(10) UNSIGNED NOT NULL,
  `Foto` varchar(500) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dump dei dati per la tabella `articles`
--

INSERT INTO `articles` (`Nome`, `Prezzo`, `Quantita_disponibile`, `Foto`) VALUES
('Pane', '2.00', 30, 'https://dietapaleo.it/wp-content/uploads/pane-bianco.jpg'),
('Pasta', '5.00', 20, 'https://fthmb.tqn.com/pPeGs_p0LNCDzfh6Afh5VRgVCFg=/5472x3648/filters:fill(auto,1)/close-up-of-penne-arabiata-in-bowl-683842303-587e99035f9b584db3432942.jpg'),
('Pizza', '10.00', 50, 'https://gdsit.cdn-immedia.net/2016/03/Pizza-Margherita.jpg');

-- --------------------------------------------------------

--
-- Struttura della tabella `contiene`
--

CREATE TABLE `contiene` (
  `Ordine` int(10) UNSIGNED NOT NULL,
  `Articolo` varchar(30) NOT NULL,
  `Quantità` int(10) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dump dei dati per la tabella `contiene`
--

INSERT INTO `contiene` (`Ordine`, `Articolo`, `Quantità`) VALUES
(1, 'Pane', 7),
(1, 'Pasta', 5),
(1, 'Pizza', 3);

-- --------------------------------------------------------

--
-- Struttura della tabella `orders`
--

CREATE TABLE `orders` (
  `ID` int(11) UNSIGNED NOT NULL,
  `Utente` int(11) UNSIGNED NOT NULL,
  `Stato` enum('Pending','Settled') NOT NULL DEFAULT 'Pending'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dump dei dati per la tabella `orders`
--

INSERT INTO `orders` (`ID`, `Utente`, `Stato`) VALUES
(1, 1, 'Pending');

-- --------------------------------------------------------

--
-- Struttura della tabella `users`
--

CREATE TABLE `users` (
  `ID` int(11) UNSIGNED NOT NULL,
  `Nome` varchar(20) NOT NULL,
  `Cognome` varchar(20) NOT NULL,
  `CF` char(16) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dump dei dati per la tabella `users`
--

INSERT INTO `users` (`ID`, `Nome`, `Cognome`, `CF`) VALUES
(1, 'Marco', 'Zennaro', 'ZNNMRC01E07L736W'),
(2, 'Mario', 'Rossi', 'RSSMRA03C03L736W');

--
-- Indici per le tabelle scaricate
--

--
-- Indici per le tabelle `articles`
--
ALTER TABLE `articles`
  ADD PRIMARY KEY (`Nome`);

--
-- Indici per le tabelle `contiene`
--
ALTER TABLE `contiene`
  ADD UNIQUE KEY `Ordine_2` (`Ordine`,`Articolo`),
  ADD KEY `ordine` (`Ordine`),
  ADD KEY `articolo` (`Articolo`);

--
-- Indici per le tabelle `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `users ID` (`Utente`);

--
-- Indici per le tabelle `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`ID`);

--
-- AUTO_INCREMENT per le tabelle scaricate
--

--
-- AUTO_INCREMENT per la tabella `orders`
--
ALTER TABLE `orders`
  MODIFY `ID` int(11) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT per la tabella `users`
--
ALTER TABLE `users`
  MODIFY `ID` int(11) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Limiti per le tabelle scaricate
--

--
-- Limiti per la tabella `contiene`
--
ALTER TABLE `contiene`
  ADD CONSTRAINT `contiene_ibfk_1` FOREIGN KEY (`Articolo`) REFERENCES `articles` (`Nome`),
  ADD CONSTRAINT `contiene_ibfk_2` FOREIGN KEY (`Ordine`) REFERENCES `orders` (`ID`),
  ADD CONSTRAINT `contiene_ibfk_3` FOREIGN KEY (`Ordine`) REFERENCES `orders` (`ID`);

--
-- Limiti per la tabella `orders`
--
ALTER TABLE `orders`
  ADD CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`Utente`) REFERENCES `users` (`ID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
