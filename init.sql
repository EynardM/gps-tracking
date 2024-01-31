-- Drop the table if it exists
DROP TABLE IF EXISTS coordinates;

-- Create the coordinates table
CREATE TABLE coordinates (
    id SERIAL PRIMARY KEY,
    ip VARCHAR(100),
    lat DOUBLE PRECISION,
    lon DOUBLE PRECISION,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create trigger function to send notification
CREATE OR REPLACE FUNCTION notify_coordinates_insert()
RETURNS TRIGGER AS
$$
BEGIN
    -- Send a notification when a new row is inserted into the coordinates table
    PERFORM pg_notify('coordinates_insert', json_build_object('ip', NEW.ip, 'lat', NEW.lat, 'lon', NEW.lon, 'date', NEW.date)::text);
    RETURN NEW;
END;
$$
LANGUAGE plpgsql;

-- Attach the trigger function to your table
CREATE TRIGGER coordinates_insert_trigger
AFTER INSERT ON coordinates
FOR EACH ROW
EXECUTE FUNCTION notify_coordinates_insert();
