-- upgrade --
CREATE TABLE IF NOT EXISTS "telegramuser" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "telegram_id" INT NOT NULL UNIQUE,
    "is_admin" INT NOT NULL  DEFAULT 0
);
CREATE TABLE IF NOT EXISTS "wireguardserver" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "webhook_url" VARCHAR(128) NOT NULL,
    "server_key" VARCHAR(256) NOT NULL,
    "country" VARCHAR(256) NOT NULL
);
CREATE TABLE IF NOT EXISTS "wireguardpeer" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "peer_name" VARCHAR(32) NOT NULL,
    "tg_user_id" INT REFERENCES "telegramuser" ("id") ON DELETE CASCADE,
    "wg_server_id" INT NOT NULL REFERENCES "wireguardserver" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSON NOT NULL
);
