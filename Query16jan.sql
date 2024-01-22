-- Create the User table
CREATE SEQUENCE user_id_sequence START 1;

CREATE TABLE Users (
    userid integer PRIMARY KEY DEFAULT nextval('user_id_sequence'),
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    password VARCHAR(255),
    admin BOOLEAN DEFAULT FALSE
);

-- Create the Bookings table
CREATE TABLE bookings (
    booking_id SERIAL PRIMARY KEY,
    user_id integer REFERENCES users(userid),
    classroom VARCHAR(255),
    title VARCHAR(255),
    date TIMESTAMP,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    status VARCHAR(50),
    created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cancelled_on TIMESTAMP
);


SELECT *
FROM pg_settings
WHERE name = 'port';

select * from users;


drop TABLE users;

select * from Bookings;

drop TABLE Bookings

INSERT INTO users (UserName, Email, Password, Admin)
VALUES ('Chester Green', 'greenc@wellingtoncollege.org.uk', 'password1', true);
INSERT INTO users (UserName, Email, Password, Admin)
VALUES ('Alfred Watson', 'watsona@wellingtoncollege.org.uk', 'password2', true);
