-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 13, 2024 at 02:00 AM
-- Server version: 10.4.21-MariaDB
-- PHP Version: 8.0.11

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `driving_success_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `appointments`
--

CREATE TABLE `appointments` (
  `id` int(11) NOT NULL,
  `learner_id` int(11) NOT NULL,
  `instructor_id` int(11) NOT NULL,
  `appointment_date_time` datetime NOT NULL,
  `status` int(11) NOT NULL DEFAULT 0,
  `created_at` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `appointments`
--

INSERT INTO `appointments` (`id`, `learner_id`, `instructor_id`, `appointment_date_time`, `status`, `created_at`) VALUES
(14, 20, 22, '2024-01-17 10:00:00', 2, '2024-01-16 07:21:53'),
(15, 20, 23, '2024-01-26 20:00:00', 2, '2024-01-16 16:00:09'),
(16, 20, 21, '2024-01-16 20:30:00', 0, '2024-01-16 16:07:32'),
(17, 20, 21, '2024-01-26 20:17:00', 0, '2024-01-16 16:13:16'),
(18, 20, 21, '2024-01-27 14:00:00', 1, '2024-01-24 00:56:22'),
(19, 20, 24, '2024-03-16 13:00:00', 0, '2024-03-13 00:22:02');

-- --------------------------------------------------------

--
-- Table structure for table `captured_learner_traits`
--

CREATE TABLE `captured_learner_traits` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `trait_category_id` int(11) NOT NULL,
  `captured_trait` int(11) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `captured_learner_traits`
--

INSERT INTO `captured_learner_traits` (`id`, `user_id`, `trait_category_id`, `captured_trait`, `created_at`) VALUES
(27, 20, 1, 3, '2024-01-16 06:05:31'),
(28, 20, 2, 5, '2024-01-16 06:05:31'),
(29, 20, 3, 7, '2024-01-16 06:05:31'),
(30, 20, 4, 10, '2024-01-16 06:05:31'),
(31, 20, 5, 11, '2024-01-16 06:05:31'),
(32, 20, 6, 13, '2024-01-16 06:05:31'),
(33, 20, 7, 15, '2024-01-16 06:05:31'),
(34, 20, 8, 17, '2024-01-16 06:05:31'),
(35, 20, 9, 19, '2024-01-16 06:05:31'),
(36, 20, 10, 22, '2024-01-16 06:05:31'),
(37, 20, 11, 23, '2024-01-16 06:05:31'),
(38, 20, 12, 26, '2024-01-16 06:05:31'),
(39, 20, 13, 1, '2024-01-16 06:05:31');

-- --------------------------------------------------------

--
-- Table structure for table `captured_traits`
--

CREATE TABLE `captured_traits` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `trait_category_id` int(11) NOT NULL,
  `captured_trait` int(11) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `captured_traits`
--

INSERT INTO `captured_traits` (`id`, `user_id`, `trait_category_id`, `captured_trait`, `created_at`) VALUES
(42, 21, 1, 3, '2024-01-16 07:01:29'),
(43, 21, 2, 6, '2024-01-16 07:01:29'),
(44, 21, 3, 7, '2024-01-16 07:01:29'),
(45, 21, 4, 9, '2024-01-16 07:01:29'),
(46, 21, 5, 11, '2024-01-16 07:01:29'),
(47, 21, 6, 13, '2024-01-16 07:01:29'),
(48, 21, 7, 15, '2024-01-16 07:01:29'),
(49, 21, 8, 17, '2024-01-16 07:01:29'),
(50, 21, 9, 19, '2024-01-16 07:01:29'),
(51, 21, 10, 21, '2024-01-16 07:01:29'),
(52, 21, 11, 23, '2024-01-16 07:01:29'),
(53, 21, 12, 25, '2024-01-16 07:01:29'),
(54, 21, 13, 1, '2024-01-16 07:01:29'),
(55, 22, 1, 3, '2024-01-16 07:10:46'),
(56, 22, 2, 5, '2024-01-16 07:10:46'),
(57, 22, 3, 7, '2024-01-16 07:10:46'),
(58, 22, 4, 9, '2024-01-16 07:10:46'),
(59, 22, 5, 11, '2024-01-16 07:10:46'),
(60, 22, 6, 13, '2024-01-16 07:10:46'),
(61, 22, 7, 15, '2024-01-16 07:10:46'),
(62, 22, 8, 17, '2024-01-16 07:10:46'),
(63, 22, 9, 19, '2024-01-16 07:10:46'),
(64, 22, 10, 21, '2024-01-16 07:10:46'),
(65, 22, 11, 23, '2024-01-16 07:10:46'),
(66, 22, 12, 25, '2024-01-16 07:10:46'),
(67, 22, 13, 1, '2024-01-16 07:10:46'),
(68, 23, 1, 3, '2024-01-16 07:16:56'),
(69, 23, 2, 5, '2024-01-16 07:16:56'),
(70, 23, 3, 7, '2024-01-16 07:16:56'),
(71, 23, 4, 9, '2024-01-16 07:16:56'),
(72, 23, 5, 12, '2024-01-16 07:16:56'),
(73, 23, 6, 13, '2024-01-16 07:16:56'),
(74, 23, 7, 15, '2024-01-16 07:16:56'),
(75, 23, 8, 17, '2024-01-16 07:16:56'),
(76, 23, 9, 20, '2024-01-16 07:16:56'),
(77, 23, 10, 22, '2024-01-16 07:16:56'),
(78, 23, 11, 23, '2024-01-16 07:16:56'),
(79, 23, 12, 25, '2024-01-16 07:16:56'),
(80, 23, 13, 2, '2024-01-16 07:16:56'),
(81, 24, 1, 3, '2024-03-12 23:45:16'),
(82, 24, 2, 5, '2024-03-12 23:45:16'),
(83, 24, 3, 7, '2024-03-12 23:45:16'),
(84, 24, 4, 9, '2024-03-12 23:45:16'),
(85, 24, 5, 11, '2024-03-12 23:45:16'),
(86, 24, 6, 13, '2024-03-12 23:45:16'),
(87, 24, 7, 15, '2024-03-12 23:45:16'),
(88, 24, 8, 17, '2024-03-12 23:45:16'),
(89, 24, 9, 19, '2024-03-12 23:45:16'),
(90, 24, 10, 21, '2024-03-12 23:45:16'),
(91, 24, 11, 23, '2024-03-12 23:45:16'),
(92, 24, 12, 25, '2024-03-12 23:45:16'),
(93, 24, 13, 2, '2024-03-12 23:45:16');

-- --------------------------------------------------------

--
-- Table structure for table `instructor_details`
--

CREATE TABLE `instructor_details` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `instructor_experience` int(11) NOT NULL,
  `instructor_charges` double NOT NULL,
  `instructor_vehicle_transmission_type` varchar(255) NOT NULL,
  `instructor_vehicle_category` varchar(255) NOT NULL,
  `instructor_vehicle_model` varchar(255) NOT NULL,
  `instructor_description` varchar(255) NOT NULL,
  `instructor_mins_per_session` int(11) NOT NULL,
  `instructor_rating` int(11) NOT NULL DEFAULT 0,
  `created_at` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `instructor_details`
--

INSERT INTO `instructor_details` (`id`, `user_id`, `instructor_experience`, `instructor_charges`, `instructor_vehicle_transmission_type`, `instructor_vehicle_category`, `instructor_vehicle_model`, `instructor_description`, `instructor_mins_per_session`, `instructor_rating`, `created_at`) VALUES
(3, 21, 10, 250, 'manual', 'sedan', 'Toyota Corolla', ' \r\nWelcome to the profile of an experienced and dedicated driving instructor, committed to shaping confident and responsible drivers for a safer road experience. With a passion for teaching and a focus on fostering good driving habits, I provide comprehen', 120, 0, '2024-01-16 07:01:29'),
(4, 22, 5, 300, 'automatic', 'suv', 'Nissan Rogue', ' As a certified driving instructor, I bring a wealth of knowledge and expertise to the table. I stay updated on the latest traffic laws, safety regulations, and teaching methodologies to ensure that my students receive the most relevant and effective inst', 120, 0, '2024-01-16 07:10:46'),
(5, 23, 6, 200, 'manual', 'sedan', ' BMW ALPINA', ' My teaching philosophy revolves around creating a positive and supportive learning environment. I understand that each student is unique, and I tailor my instruction to suit individual learning styles. Whether you\'re a nervous beginner or looking to enha', 120, 0, '2024-01-16 07:16:56'),
(6, 24, 5, 350, 'manual', 'sedan', 'Volkswagen Jetta SE', ' With over 5 years of dedicated experience in teaching individuals of all ages how to drive safely and confidently, I am passionate about empowering students to become competent and responsible drivers. My comprehensive approach combines practical instruc', 60, 0, '2024-03-12 23:45:14');

-- --------------------------------------------------------

--
-- Table structure for table `instructor_reviews`
--

CREATE TABLE `instructor_reviews` (
  `id` int(11) NOT NULL,
  `comment` varchar(255) DEFAULT NULL,
  `commenter_id` int(11) NOT NULL,
  `instructor_id` int(11) NOT NULL,
  `rating` int(11) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `in_built_instructor_traits`
--

CREATE TABLE `in_built_instructor_traits` (
  `id` int(11) NOT NULL,
  `trait_name` varchar(255) NOT NULL,
  `trait_category` int(11) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `in_built_instructor_traits`
--

INSERT INTO `in_built_instructor_traits` (`id`, `trait_name`, `trait_category`, `created_at`) VALUES
(1, 'Introverted', 13, '2024-01-11 12:04:39'),
(2, 'Extroverted', 13, '2024-01-11 12:04:39'),
(3, 'Tolerant', 1, '2024-01-11 12:06:21'),
(4, 'Intolerant', 1, '2024-01-11 12:06:21'),
(5, 'Clear Communicator', 2, '2024-01-11 12:08:05'),
(6, 'Unclear Communicator', 2, '2024-01-11 12:08:05'),
(7, 'Adaptable', 3, '2024-01-11 12:09:23'),
(8, 'Resistant to Change', 3, '2024-01-11 12:09:23'),
(9, 'Time-Conscious', 4, '2024-01-11 12:10:40'),
(10, 'Time-Relaxed', 4, '2024-01-11 12:10:40'),
(11, 'Structured Teacher ', 5, '2024-01-11 12:11:49'),
(12, 'Free-Form Teacher', 5, '2024-01-11 12:11:49'),
(13, 'Compassionate', 6, '2024-01-11 12:16:31'),
(14, 'Unsympathetic', 6, '2024-01-11 12:16:31'),
(15, 'Organized', 7, '2024-01-11 12:18:43'),
(16, 'Disorganized', 7, '2024-01-11 12:18:43'),
(17, 'Composed', 8, '2024-01-11 12:20:10'),
(18, 'Anxious', 8, '2024-01-11 12:20:10'),
(19, 'Receptive to Suggestions ', 9, '2024-01-11 12:27:19'),
(20, 'Resistant to Suggestions', 9, '2024-01-11 12:27:19'),
(21, 'Approachable', 10, '2024-01-11 12:29:12'),
(22, 'Reserved', 10, '2024-01-11 12:29:12'),
(23, 'Supportive ', 11, '2024-01-11 12:30:29'),
(24, 'Discouraging', 11, '2024-01-11 12:30:29'),
(25, 'Observant', 12, '2024-01-11 12:31:56'),
(26, 'Inattentive', 12, '2024-01-11 12:31:56');

-- --------------------------------------------------------

--
-- Table structure for table `in_built_learner_traits`
--

CREATE TABLE `in_built_learner_traits` (
  `id` int(11) NOT NULL,
  `trait_name` varchar(255) NOT NULL,
  `trait_category` int(11) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `in_built_learner_traits`
--

INSERT INTO `in_built_learner_traits` (`id`, `trait_name`, `trait_category`, `created_at`) VALUES
(1, 'Introverted', 13, '2024-01-11 09:04:39'),
(2, 'Extroverted', 13, '2024-01-11 09:04:39'),
(3, 'Very patient', 1, '2024-01-11 09:06:21'),
(4, 'Somewhat Impatient', 1, '2024-01-11 09:06:21'),
(5, 'Very well', 2, '2024-01-11 09:08:05'),
(6, 'Not well at all', 2, '2024-01-11 09:08:05'),
(7, 'I thrive in these situations', 3, '2024-01-11 09:09:23'),
(8, 'I prefer things to be predictable', 3, '2024-01-11 09:09:23'),
(9, 'Always on time', 4, '2024-01-11 09:10:40'),
(10, 'Often late', 4, '2024-01-11 09:10:40'),
(11, 'Structured Learning', 5, '2024-01-11 09:11:49'),
(12, 'Free-Form Learning', 5, '2024-01-11 09:11:49'),
(13, 'Yes', 6, '2024-01-11 09:16:31'),
(14, 'No', 6, '2024-01-11 09:16:31'),
(15, ' Meticulously plan', 7, '2024-01-11 09:18:43'),
(16, 'Go with the flow', 7, '2024-01-11 09:18:43'),
(17, 'Composed', 8, '2024-01-11 09:20:10'),
(18, 'Anxious', 8, '2024-01-11 09:20:10'),
(19, 'Yes', 9, '2024-01-11 09:27:19'),
(20, 'No', 9, '2024-01-11 09:27:19'),
(21, 'I enjoy initiating conversations', 10, '2024-01-11 09:29:12'),
(22, 'I prefer to wait for others to approach me', 10, '2024-01-11 09:29:12'),
(23, 'Yes', 11, '2024-01-11 09:30:29'),
(24, 'No', 11, '2024-01-11 09:30:29'),
(25, 'Yes', 12, '2024-01-11 09:31:56'),
(26, 'No', 12, '2024-01-11 09:31:56');

-- --------------------------------------------------------

--
-- Table structure for table `in_built_traits`
--

CREATE TABLE `in_built_traits` (
  `id` int(11) NOT NULL,
  `trait_name` varchar(255) NOT NULL,
  `trait_category` int(11) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `in_built_traits`
--

INSERT INTO `in_built_traits` (`id`, `trait_name`, `trait_category`, `created_at`) VALUES
(1, 'introverted', 0, '2024-01-04 01:41:49'),
(2, 'extrovert', 0, '2024-01-04 01:41:49'),
(3, 'Serious', 0, '2024-01-04 01:42:53'),
(4, 'Lively', 0, '2024-01-04 01:42:53');

-- --------------------------------------------------------

--
-- Table structure for table `password_reset`
--

CREATE TABLE `password_reset` (
  `id` int(11) NOT NULL,
  `email` varchar(255) NOT NULL,
  `token` varchar(255) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `password_reset`
--

INSERT INTO `password_reset` (`id`, `email`, `token`, `created_at`) VALUES
(1, 'johndoe@test.com', 'eqkkd_mPAz-2hKjXV49gAlRyeGI', '2024-02-28 02:20:18'),
(2, 'joebloggs@gmail.com', 'Xme4E8gHDLAu8D_HGrZgCGv1NhE', '2024-02-28 02:24:45'),
(3, 'janedoe@test.com', 'q-5qIH5NHRP42a6N0ypB9wvwf1M', '2024-02-28 02:29:16'),
(4, 'tommy@test.com', '2-RE6jObyV_Lir3m-0G6kA1RzUg', '2024-02-28 02:39:46'),
(5, 'johndoe@test.com', 'Ypzd-leZlPdmOg_L0bFerJRtpVM', '2024-02-28 11:25:56'),
(6, 'johndoe@test.com', 'OfgaxwGiO3FFKpu6SSudiGLBCfU', '2024-02-28 12:13:46');

-- --------------------------------------------------------

--
-- Table structure for table `trait_categories`
--

CREATE TABLE `trait_categories` (
  `id` int(11) NOT NULL,
  `trait_category_name` varchar(255) NOT NULL,
  `instructor_q` varchar(255) DEFAULT NULL,
  `learner_q` varchar(255) DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `trait_categories`
--

INSERT INTO `trait_categories` (`id`, `trait_category_name`, `instructor_q`, `learner_q`, `created_at`) VALUES
(1, 'Patience', 'Are you generally tolerant or intolerant?', 'How patient would you say you are when anticipating results or dealing with slow processes?', '2024-01-11 14:51:27'),
(2, 'Communication Style', 'Are you a clear or unclear communicator?', 'How well do you think you adapt to communication style from different individuals?', '2024-01-11 14:51:27'),
(3, 'Adaptability', 'Would you describe yourself as flexible and adaptable, or more set in your ways?', 'How well do you handle unexpected situations or challenges?', '2024-01-11 14:53:43'),
(4, 'Punctuality', 'How strict are you with time?', 'Would you describe yourself as someone who is always on time, or often running late?', '2024-01-11 14:53:43'),
(5, 'Teaching Style', 'How would you describe your teaching style?', 'Do you thrive in learning environments with clear goals, defined steps, and regular feedback, or do you prefer more open-ended exploration and independent problem-solving?', '2024-01-11 14:55:22'),
(6, 'Empathy', 'Do you often put yourself in other people\'s shoes to understand their perspective?(Yes - Compassionate, No - Unsymphathetic)', 'Do you easily find yourself feeling what others are feeling? ', '2024-01-11 14:55:22'),
(7, 'Organizational Skills', 'On a scale of 1 to 10 how organized are you? (1-5: disorganized, 6-10: organized)', 'How important is planning and scheduling for you? Do you meticulously plan your day, or go with the flow?', '2024-01-11 14:57:26'),
(8, 'Calmness under Pressure', 'When faced with a challenging situation, do you stay cool(composed) and collected or get easily flustered(anxious)\n? ', 'When faced with a challenging situation, do you stay cool(composed) and collected or get easily flustered(anxious)\n? ', '2024-01-11 14:57:26'),
(9, 'Openness to Feedback', 'Do you appreciate receiving feedback on your work, even if it\'s critical?', 'Do you feel compelled to share feedback to help others improve, even if it might be critical?', '2024-01-11 14:58:13'),
(10, 'Friendliness', 'How friendly are you?', 'Do you generally enjoy initiating conversations and meeting new people, or prefer to wait for others to approach you?', '2024-01-11 14:58:13'),
(11, 'Encouragement Style', 'Imagine seeing someone struggling – would your first instinct be to offer a listening ear and words of encouragement? (Yes - supportive, No - Discouraging)', 'Do you find yourself drawn to uplifting stories and motivational quotes? ', '2024-01-11 14:58:47'),
(12, 'Attentiveness', 'On a scale of 1 to 5, how observant are you generally? (1 -2 being very inattentive, 3-5 being observant)', 'Do you enjoy activities like puzzles, crosswords, or detective stories that require close attention to detail?', '2024-01-11 14:58:47'),
(13, 'Introversion_extroversion', 'Would you describe yourself as being intro or extroverted?', 'Do you consider yourself intro or extroverted?', '2024-01-11 15:01:47');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `username` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `phone` varchar(255) DEFAULT NULL,
  `role` varchar(255) NOT NULL,
  `profile_pic_url` varchar(255) DEFAULT NULL,
  `age` int(11) DEFAULT NULL,
  `gender` varchar(255) DEFAULT NULL,
  `language` varchar(255) DEFAULT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `first_name`, `last_name`, `username`, `email`, `phone`, `role`, `profile_pic_url`, `age`, `gender`, `language`, `password`) VALUES
(20, 'John', 'Doe', 'John_Doe', 'johndoe@test.com', '555-255554', 'learner', 'user_1.jpg', 25, 'M', 'English', '$5$rounds=535000$pxse1H.bM/3BSGTj$DQTBikh5onItYjE.5Yh3UaeRphC7lpfxMeGy.lJhyu8'),
(21, 'Joe', ' Bloggs ', ' Joe_Bloggs ', 'joebloggs@gmail.com', '89908787774', 'instructor', 'user_2.jpg', 35, 'M', 'English', '$5$rounds=535000$lI.4vwCJh8K3.dVK$jdhDnFPSEuGYM0ZoYNYzOXGUjJOz8i62njzxl/Feb./'),
(22, 'Jane', 'Doe', 'jane', 'janedoe@test.com', '897489555', 'instructor', 'user_3.jpg', 25, 'F', 'English', '$5$rounds=535000$/QBTn13GW1rFTYKs$KteSoVSlOP7BPZ92LhFHj0BgE27vK7.gLQp6bTVi0u2'),
(23, 'Tommy', 'Atkins', 'tommy', 'tommy@test.com', '855552222', 'instructor', 'user_4.jpg', 30, 'M', 'English', '$5$rounds=535000$pvUm7NCpttFLRTNf$QDM6IeK5ngYspfM4gGj8vXR.s9Ofz.RvGgMAMuEbQn7'),
(24, 'William', 'Saliba', 'williamsaliba', 'williamsaliba@gmail.cm', '222222222', 'instructor', 'pexels-nguyen-gia-huy-tran-2285991.jpg', 35, 'M', 'English', '$5$rounds=535000$UHu4VDu5lhnGulBh$UoyXgvlvJ84X3ZZRJ5eHtS8wR9Ii11289xEu6cxRG9B');

-- --------------------------------------------------------

--
-- Table structure for table `user_traits`
--

CREATE TABLE `user_traits` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `trait_id` int(11) DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `appointments`
--
ALTER TABLE `appointments`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `captured_learner_traits`
--
ALTER TABLE `captured_learner_traits`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `captured_traits`
--
ALTER TABLE `captured_traits`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `instructor_details`
--
ALTER TABLE `instructor_details`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- Indexes for table `instructor_reviews`
--
ALTER TABLE `instructor_reviews`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `in_built_instructor_traits`
--
ALTER TABLE `in_built_instructor_traits`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `in_built_learner_traits`
--
ALTER TABLE `in_built_learner_traits`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `in_built_traits`
--
ALTER TABLE `in_built_traits`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `password_reset`
--
ALTER TABLE `password_reset`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `trait_categories`
--
ALTER TABLE `trait_categories`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user_traits`
--
ALTER TABLE `user_traits`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `appointments`
--
ALTER TABLE `appointments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT for table `captured_learner_traits`
--
ALTER TABLE `captured_learner_traits`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=40;

--
-- AUTO_INCREMENT for table `captured_traits`
--
ALTER TABLE `captured_traits`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=94;

--
-- AUTO_INCREMENT for table `instructor_details`
--
ALTER TABLE `instructor_details`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `instructor_reviews`
--
ALTER TABLE `instructor_reviews`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `in_built_instructor_traits`
--
ALTER TABLE `in_built_instructor_traits`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- AUTO_INCREMENT for table `in_built_learner_traits`
--
ALTER TABLE `in_built_learner_traits`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- AUTO_INCREMENT for table `in_built_traits`
--
ALTER TABLE `in_built_traits`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `password_reset`
--
ALTER TABLE `password_reset`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `trait_categories`
--
ALTER TABLE `trait_categories`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT for table `user_traits`
--
ALTER TABLE `user_traits`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `user_traits`
--
ALTER TABLE `user_traits`
  ADD CONSTRAINT `user_traits_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
