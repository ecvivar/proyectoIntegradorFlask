-- phpMyAdmin SQL Dump
-- version 4.9.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 24-07-2021 a las 04:59:58
-- Versión del servidor: 10.4.8-MariaDB
-- Versión de PHP: 7.3.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `final`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `carrito`
--

CREATE TABLE `carrito` (
  `id` int(10) NOT NULL,
  `username` varchar(50) NOT NULL,
  `codigo` int(10) NOT NULL,
  `descripcion` varchar(255) DEFAULT NULL,
  `precio` decimal(10,2) DEFAULT NULL,
  `cantidad` int(4) DEFAULT 0,
  `foto` varchar(500) DEFAULT NULL,
  `totalAbonar` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `carrito`
--

INSERT INTO `carrito` (`id`, `username`, `codigo`, `descripcion`, `precio`, `cantidad`, `foto`, `totalAbonar`) VALUES
(33, 'maria', 2, 'Remera Beastie Boys', '1890.00', 2, 'beastie-boys1.png', '3780.00'),
(34, 'maria', 4, 'Remera Parental Advisory', '1890.00', 2, 'parental-advisory1.png', '3780.00'),
(35, 'maria', 1, 'Remera Volver al Futuro', '1890.00', 2, 'back-to-the-future1.jpg', '3780.00'),
(40, 'maria', 3, 'Remera Beastie Boys', '1890.00', 2, 'beastie-boys2.png', '3780.00'),
(41, 'maria', 3, 'Remera Beastie Boys', '1890.00', 2, 'beastie-boys2.png', '3780.00'),
(42, 'maria', 3, 'Remera Beastie Boys', '1890.00', 2, 'beastie-boys2.png', '3780.00'),
(43, 'maria', 3, 'Remera Beastie Boys', '1890.00', 2, 'beastie-boys2.png', '3780.00'),
(44, 'maria', 3, 'Remera Beastie Boys', '1890.00', 2, 'beastie-boys2.png', '3780.00'),
(45, 'maria', 3, 'Remera Beastie Boys', '1890.00', 2, 'beastie-boys2.png', '3780.00'),
(46, 'maria', 3, 'Remera Beastie Boys', '1890.00', 2, 'beastie-boys2.png', '3780.00'),
(47, 'maria', 3, 'Remera Beastie Boys', '1890.00', 2, 'beastie-boys2.png', '3780.00'),
(48, 'maria', 3, 'Remera Beastie Boys', '1890.00', 2, 'beastie-boys2.png', '3780.00'),
(62, 'juan', 3, 'Remera Beastie Boys', '1890.00', 2, 'beastie-boys2.png', '3780.00'),
(63, 'juan', 2, 'Remera Beastie Boys', '1890.00', 2, 'beastie-boys1.png', '3780.00'),
(64, 'juan', 10, 'Remera Rammstein', '1890.00', 2, 'rammstein1.png', '3780.00'),
(133, 'pedro', 1, 'Remera Volver al Futuro', '1890.00', 1, 'back-to-the-future1.jpg', '1890.00');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `productos`
--

CREATE TABLE `productos` (
  `codigo` int(10) NOT NULL,
  `descripcion` varchar(255) DEFAULT NULL,
  `precio` decimal(10,2) DEFAULT NULL,
  `cantidad` int(4) DEFAULT NULL,
  `foto` varchar(500) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `productos`
--

INSERT INTO `productos` (`codigo`, `descripcion`, `precio`, `cantidad`, `foto`) VALUES
(1, 'Remera Volver al Futuro', '1890.00', 10, 'back-to-the-future1.jpg'),
(2, 'Remera Beastie Boys', '1890.00', 10, 'beastie-boys1.png'),
(3, 'Remera Beastie Boys', '1890.00', 10, 'beastie-boys2.png'),
(4, 'Remera Parental Advisory', '1890.00', 10, 'parental-advisory1.png'),
(5, 'Remera Parental Advisory', '1890.00', 10, 'parental-advisory2.png'),
(6, 'Remera Pink Floyd The Wall', '1890.00', 10, 'pink-floyd-the-wall1.png'),
(7, 'Remera Pink Floyd The Wall', '1890.00', 10, 'pink-floyd-the-wall2.png'),
(8, 'Remera Patricio Rey y sus Redonditos de Ricota Oktubre', '1890.00', 10, 'pr_oktubre1.png'),
(9, 'Remera Patricio Rey y sus Redonditos de Ricota Oktubre', '1890.00', 10, 'pr_oktubre2.png'),
(10, 'Remera Rammstein', '1890.00', 10, 'rammstein1.png'),
(11, 'Remera Rammstein', '1890.00', 10, 'rammstein2.png');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id`, `username`, `password`, `email`) VALUES
(2, 'pedro', '123456', 'pedro@gmail.com'),
(3, 'juan', '123456', 'juan@gmail.com'),
(4, 'jose', '123456', 'jose@gmail.com'),
(6, 'raul', '123456', 'raul@gmail.com'),
(7, 'maria', '123456', 'maria@gmail.com'),
(8, 'admin', '123456', 'admin@gmail.com');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `carrito`
--
ALTER TABLE `carrito`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `productos`
--
ALTER TABLE `productos`
  ADD PRIMARY KEY (`codigo`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `carrito`
--
ALTER TABLE `carrito`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=134;

--
-- AUTO_INCREMENT de la tabla `productos`
--
ALTER TABLE `productos`
  MODIFY `codigo` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
