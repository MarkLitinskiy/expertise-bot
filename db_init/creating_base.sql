CREATE TABLE
    client_data (
        id SERIAL NOT NULL PRIMARY KEY,
        name TEXT NOT NULL,
        telegram_id BIGINT NOT NULL,
        telegram_username text NOT NULL,
        is_admin BOOLEAN NOT NULL DEFAULT FALSE
    );

CREATE TABLE
    meetings (
        id SERIAL NOT NULL PRIMARY KEY,
        expert_id BIGINT NOT NULL,
        client_id BIGINT NOT NULL,
        date DATE NOT NULL,
        time TIME NOT NULL,
        lat FLOAT NOT NULL,
        lng FLOAT NOT NULL,
        house TEXT NOT NULL,
        constraint fk_expert_meeting_id foreign key (expert_id) references client_data(id),
        constraint fk_client_meeting_id foreign key (client_id) references client_data(id)
    );