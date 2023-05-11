CREATE TABLE user_daily_engagements (
    username VARCHAR(255),
    date DATE,
    engagements INT,
    PRIMARY KEY (username, date)
);

CREATE TABLE user_weekly_engagements (
    username VARCHAR(255),
    date DATE,
    engagements INT,
    PRIMARY KEY (username, date)
);

CREATE TABLE user_monthly_engagements (
    username VARCHAR(255),
    date DATE,
    engagements INT,
    PRIMARY KEY (username, date)
);
