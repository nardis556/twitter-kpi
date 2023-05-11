CREATE TABLE IF NOT EXISTS summary_original_daily (
    date DATE NOT NULL,
    likes INT DEFAULT 0,
    retweets INT DEFAULT 0,
    replies INT DEFAULT 0,
    quotes INT DEFAULT 0,
    impressions INT DEFAULT 0,
    PRIMARY KEY(date)
);

CREATE TABLE IF NOT EXISTS summary_original_weekly (
    date DATE NOT NULL,
    likes INT DEFAULT 0,
    retweets INT DEFAULT 0,
    replies INT DEFAULT 0,
    quotes INT DEFAULT 0,
    impressions INT DEFAULT 0,
    PRIMARY KEY(date)
);

CREATE TABLE IF NOT EXISTS summary_original_monthly (
    date DATE NOT NULL,
    likes INT DEFAULT 0,
    retweets INT DEFAULT 0,
    replies INT DEFAULT 0,
    quotes INT DEFAULT 0,
    impressions INT DEFAULT 0,
    PRIMARY KEY(date)
);

CREATE TABLE IF NOT EXISTS summary_retweet_daily (
    date DATE NOT NULL,
    likes INT DEFAULT 0,
    retweets INT DEFAULT 0,
    replies INT DEFAULT 0,
    quotes INT DEFAULT 0,
    impressions INT DEFAULT 0,
    PRIMARY KEY(date)
);

CREATE TABLE IF NOT EXISTS summary_retweet_weekly (
    date DATE NOT NULL,
    likes INT DEFAULT 0,
    retweets INT DEFAULT 0,
    replies INT DEFAULT 0,
    quotes INT DEFAULT 0,
    impressions INT DEFAULT 0,
    PRIMARY KEY(date)
);

CREATE TABLE IF NOT EXISTS summary_retweet_monthly (
    date DATE NOT NULL,
    likes INT DEFAULT 0,
    retweets INT DEFAULT 0,
    replies INT DEFAULT 0,
    quotes INT DEFAULT 0,
    impressions INT DEFAULT 0,
    PRIMARY KEY(date)
);

CREATE TABLE IF NOT EXISTS summary_reply_daily (
    date DATE NOT NULL,
    likes INT DEFAULT 0,
    retweets INT DEFAULT 0,
    replies INT DEFAULT 0,
    quotes INT DEFAULT 0,
    impressions INT DEFAULT 0,
    PRIMARY KEY(date)
);

CREATE TABLE IF NOT EXISTS summary_reply_weekly (
    date DATE NOT NULL,
    likes INT DEFAULT 0,
    retweets INT DEFAULT 0,
    replies INT DEFAULT 0,
    quotes INT DEFAULT 0,
    impressions INT DEFAULT 0,
    PRIMARY KEY(date)
);

CREATE TABLE IF NOT EXISTS summary_reply_monthly (
    date DATE NOT NULL,
    likes INT DEFAULT 0,
    retweets INT DEFAULT 0,
    replies INT DEFAULT 0,
    quotes INT DEFAULT 0,
    impressions INT DEFAULT 0,
    PRIMARY KEY(date)
);

CREATE TABLE IF NOT EXISTS summary_mentions_daily (
    date DATE NOT NULL,
    likes INT DEFAULT 0,
    retweets INT DEFAULT 0,
    replies INT DEFAULT 0,
    quotes INT DEFAULT 0,
    impressions INT DEFAULT 0,
    PRIMARY KEY(date)
);

CREATE TABLE IF NOT EXISTS summary_mentions_weekly (
    date DATE NOT NULL,
    likes INT DEFAULT 0,
    retweets INT DEFAULT 0,
    replies INT DEFAULT 0,
    quotes INT DEFAULT 0,
    impressions INT DEFAULT 0,
    PRIMARY KEY(date)
);

CREATE TABLE IF NOT EXISTS summary_mentions_monthly (
    date DATE NOT NULL,
    likes INT DEFAULT 0,
    retweets INT DEFAULT 0,
    replies INT DEFAULT 0,
    quotes INT DEFAULT 0,
    impressions INT DEFAULT 0,
    PRIMARY KEY(date)
);
