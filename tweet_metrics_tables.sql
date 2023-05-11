CREATE TABLE `twitter` (
  `tweet_id` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `timestamp` timestamp NULL DEFAULT NULL,
  `author` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `tweet_type` varchar(15) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `replied_to_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `replied_to_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `quoted_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `retweet_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `message` text COLLATE utf8mb4_general_ci,
  `likes` int UNSIGNED DEFAULT NULL,
  `retweets` int UNSIGNED DEFAULT NULL,
  `replies` int UNSIGNED DEFAULT NULL,
  `quotes` int UNSIGNED DEFAULT NULL,
  `impressions` int UNSIGNED DEFAULT NULL,
  `updated` tinyint(1) NOT NULL DEFAULT '0',
  `updated_time` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
