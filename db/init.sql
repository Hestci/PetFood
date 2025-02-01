-- Создаем тип ENUM
CREATE TYPE feeding_type AS ENUM ('daily', 'special');

-- Создаем таблицу chat
CREATE TABLE chat (
    user_id BIGINT PRIMARY KEY
);

-- Создаем таблицу food
CREATE TABLE food (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT,
    name VARCHAR(255),
    type feeding_type,
    past_feeding TIMESTAMP,
    future_feeding TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES chat(user_id) ON DELETE CASCADE
);

-- Создаем индексы
CREATE INDEX idx_food_user_id ON food(user_id);
CREATE INDEX idx_food_type ON food(type);