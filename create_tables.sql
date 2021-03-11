 CREATE TABLE  IF NOT EXISTS products
    (
        id SERIAL NOT NULL,
        Asin character varying(16) NULL,
        Title text NULL,
        created_at timestamp without time zone default (now() at time zone 'utc'),
        updated_at timestamp without time zone default (now() at time zone 'utc'),
        PRIMARY KEY (id),
        UNIQUE(asin)
    );

 CREATE TABLE  IF NOT EXISTS reviews
    (
        id SERIAL NOT NULL,
        Asin_id int NOT NULL,
        Title text NULL,
		Review text NULL,
        created_at timestamp without time zone default (now() at time zone 'utc'),
        updated_at timestamp without time zone default (now() at time zone 'utc'),
        PRIMARY KEY (id),
		FOREIGN KEY (asin_id) REFERENCES products(id) ON DELETE CASCADE
    );

 CREATE TABLE  IF NOT EXISTS reviews_temp
    (
        Asin character varying(16) NULL,
        Title text NULL,
		Review text NULL
    );

COPY public.products (Title, Asin) FROM '/tmp/Products.csv' DELIMITER ',' CSV HEADER;
COPY public.reviews_temp (Asin,Title,Review) FROM '/tmp/Reviews.csv' DELIMITER ',' CSV HEADER;

insert into public.reviews (Asin_id, Title, Review) select p.id,t.Title,t.Review from public.reviews_temp t join public.products p on t.Asin=p.Asin;

DROP TABLE reviews_temp;