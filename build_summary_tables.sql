CREATE TABLE `daily_summary_mentions` (
  `date` date NOT NULL,
  `likes` decimal(32,0) DEFAULT NULL,
  `retweets` decimal(32,0) DEFAULT NULL,
  `replies` decimal(32,0) DEFAULT NULL,
  `quotes` decimal(32,0) DEFAULT NULL,
  `impressions` decimal(32,0) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `daily_summary_original` (
  `date` date NOT NULL,
  `likes` decimal(32,0) DEFAULT NULL,
  `retweets` decimal(32,0) DEFAULT NULL,
  `replies` decimal(32,0) DEFAULT NULL,
  `quotes` decimal(32,0) DEFAULT NULL,
  `impressions` decimal(32,0) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `daily_summary_reply` (
  `date` date NOT NULL,
  `likes` decimal(32,0) DEFAULT NULL,
  `retweets` decimal(32,0) DEFAULT NULL,
  `replies` decimal(32,0) DEFAULT NULL,
  `quotes` decimal(32,0) DEFAULT NULL,
  `impressions` decimal(32,0) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `daily_summary_retweet` (
  `date` date NOT NULL,
  `likes` decimal(32,0) DEFAULT NULL,
  `retweets` decimal(32,0) DEFAULT NULL,
  `replies` decimal(32,0) DEFAULT NULL,
  `quotes` decimal(32,0) DEFAULT NULL,
  `impressions` decimal(32,0) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `weekly_summary_mentions` (
  `date` date NOT NULL,
  `likes` decimal(32,0) DEFAULT NULL,
  `retweets` decimal(32,0) DEFAULT NULL,
  `replies` decimal(32,0) DEFAULT NULL,
  `quotes` decimal(32,0) DEFAULT NULL,
  `impressions` decimal(32,0) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `weekly_summary_original` (
  `date` date NOT NULL,
  `likes` decimal(32,0) DEFAULT NULL,
  `retweets` decimal(32,0) DEFAULT NULL,
  `replies` decimal(32,0) DEFAULT NULL,
  `quotes` decimal(32,0) DEFAULT NULL,
  `impressions` decimal(32,0) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `weekly_summary_reply` (
  `date` date NOT NULL,
  `likes` decimal(32,0) DEFAULT NULL,
  `retweets` decimal(32,0) DEFAULT NULL,
  `replies` decimal(32,0) DEFAULT NULL,
  `quotes` decimal(32,0) DEFAULT NULL,
  `impressions` decimal(32,0) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `weekly_summary_retweet` (
  `date` date NOT NULL,
  `likes` decimal(32,0) DEFAULT NULL,
  `retweets` decimal(32,0) DEFAULT NULL,
  `replies` decimal(32,0) DEFAULT NULL,
  `quotes` decimal(32,0) DEFAULT NULL,
  `impressions` decimal(32,0) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `monthly_summary_mentions` (
  `date` date NOT NULL,
  `likes` decimal(32,0) DEFAULT NULL,
  `retweets` decimal(32,0) DEFAULT NULL,
  `replies` decimal(32,0) DEFAULT NULL,
  `quotes` decimal(32,0) DEFAULT NULL,
  `impressions` decimal(32,0) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `monthly_summary_original` (
  `date` date NOT NULL,
  `likes` decimal(32,0) DEFAULT NULL,
  `retweets` decimal(32,0) DEFAULT NULL,
  `replies` decimal(32,0) DEFAULT NULL,
  `quotes` decimal(32,0) DEFAULT NULL,
  `impressions` decimal(32,0) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `monthly_summary_reply` (
  `date` date NOT NULL,
  `likes` decimal(32,0) DEFAULT NULL,
  `retweets` decimal(32,0) DEFAULT NULL,
  `replies` decimal(32,0) DEFAULT NULL,
  `quotes` decimal(32,0) DEFAULT NULL,
  `impressions` decimal(32,0) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `monthly_summary_retweet` (
  `date` date NOT NULL,
  `likes` decimal(32,0) DEFAULT NULL,
  `retweets` decimal(32,0) DEFAULT NULL,
  `replies` decimal(32,0) DEFAULT NULL,
  `quotes` decimal(32,0) DEFAULT NULL,
  `impressions` decimal(32,0) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
