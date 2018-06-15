CREATE TABLE keys(
	hash char(64) PRIMARY KEY NOT NULL,
	public_key varchar(300) NOT NULL,
	active boolean DEFAULT FALSE NOT NULL,
	name varchar(50) NOT NULL,
	description varchar(300)
);

CREATE TABLE transactions(
	hash char(64) PRIMARY KEY NOT NULL,
	transmitter char(64) REFERENCES keys NOT NULL,
	receiver char(64) REFERENCES keys,
	server_timestamp timestamp DEFAULT NOW() NOT NULL,
	client_timestamp timestamp NOT NULL,
	transaction_data json NOT NULL,
	sign char(256) NOT NULL
);