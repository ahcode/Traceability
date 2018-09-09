CREATE TYPE status AS ENUM ('active', 'inactive', 'new');

CREATE TABLE keys(
	hash char(64) PRIMARY KEY NOT NULL,
	public_key varchar(300) NOT NULL,
	current_status status DEFAULT 'new' NOT NULL,
	name varchar(50) NOT NULL,
	description varchar(300)
);

CREATE TABLE transactions(
	hash char(64) PRIMARY KEY NOT NULL,
	type smallint NOT NULL,
	mode smallint NOT NULL,
	transmitter char(64) REFERENCES keys NOT NULL,
	receiver char(64) REFERENCES keys,
	server_timestamp timestamp DEFAULT NOW() NOT NULL,
	client_timestamp timestamp NOT NULL,
	raw_client_timestamp varchar(24) NOT NULL,
	transaction_data json NOT NULL,
	sign char(256) NOT NULL,
	updated_quantity json DEFAULT NULL,
	errors varchar(64)[] DEFAULT NULL
);

CREATE TABLE available_inputs(
	key_hash char(64) REFERENCES keys NOT NULL,
	product varchar(64) NOT NULL,
	inputs json[] NOT NULL,
	PRIMARY KEY(key_hash, product)
);

CREATE TABLE t_inputs(
	t_hash char(64) REFERENCES transactions NOT NULL,
	input char(64) REFERENCES transactions NOT NULL,
	product varchar(64) NOT NULL,
	PRIMARY KEY(t_hash, input, product)
);

CREATE TABLE product_id(
	id varchar(64) PRIMARY KEY NOT NULL,
	product varchar(64) NOT NULL,
	first_transaction char(64) REFERENCES transactions NOT NULL,
	last_transaction char(64) REFERENCES transactions NOT NULL,
	owner varchar(64) REFERENCES keys,
	destination varchar(64)
);

CREATE TABLE product_types(
	code varchar(64) PRIMARY KEY NOT NULL,
	name varchar(64) NOT NULL,
	measure_unit varchar(20) NOT NULL,
	multiplier int,
	description varchar(300)
);

CREATE TABLE origins(
	code varchar(64) PRIMARY KEY NOT NULL,
	name varchar(64) NOT NULL,
	description varchar(300)
);

CREATE TABLE destinations(
	code varchar(64) PRIMARY KEY NOT NULL,
	name varchar(64) NOT NULL,
	description varchar(300)
);