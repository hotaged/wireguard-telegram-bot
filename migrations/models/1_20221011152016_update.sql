-- upgrade --
ALTER TABLE "telegramuser" ALTER COLUMN "telegram_id" TYPE BIGINT USING "telegram_id"::BIGINT;
-- downgrade --
ALTER TABLE "telegramuser" ALTER COLUMN "telegram_id" TYPE INT USING "telegram_id"::INT;
