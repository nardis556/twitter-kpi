CREATE TABLE `followers` (
  `id` int NOT NULL,
  `timestamp` timestamp NULL DEFAULT NULL,
  `twitter_id` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `username` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `followers_count` int DEFAULT NULL,
  `following_count` int DEFAULT NULL,
  `tweet_count` int DEFAULT NULL,
  `listed_count` int DEFAULT NULL,
  `user_followers_count` int DEFAULT NULL,
  `pagination_token` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
