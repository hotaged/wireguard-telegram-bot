-- upgrade --
CREATE TABLE IF NOT EXISTS "telegramuser" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "telegram_id" INT NOT NULL UNIQUE,
    "is_admin" BOOL NOT NULL  DEFAULT False
);
CREATE TABLE IF NOT EXISTS "wireguardserver" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "webhook_url" VARCHAR(128) NOT NULL,
    "server_key" VARCHAR(256) NOT NULL,
    "country" VARCHAR(256) NOT NULL
);
CREATE TABLE IF NOT EXISTS "wireguardpeer" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "peer_name" VARCHAR(32) NOT NULL,
    "tg_user_id" INT REFERENCES "telegramuser" ("id") ON DELETE CASCADE,
    "wg_server_id" INT NOT NULL REFERENCES "wireguardserver" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
