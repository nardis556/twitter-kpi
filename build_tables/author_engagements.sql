CREATE TABLE author_daily_engagements (
    date DATE NOT NULL,
    engagements INT,
    PRIMARY KEY (date)
);

CREATE TABLE author_weekly_engagements (
    date DATE NOT NULL,
    engagements INT,
    PRIMARY KEY (date)
);

CREATE TABLE author_monthly_engagements (
    date DATE NOT NULL,
    engagements INT,
    PRIMARY KEY (date)
);
