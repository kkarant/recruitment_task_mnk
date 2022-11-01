CREATE TABLE public.data_ (
	part_number varchar(10) NOT NULL,
	manufacturer varchar(45) NOT NULL,
	main_part_number varchar(45) NOT NULL,
	category_ varchar(255) NOT NULL,
	origin varchar(10) NOT NULL
);

CREATE TABLE public.deposit_ (
	part_number varchar(10) NOT NULL,
	deposit varchar(10) NOT NULL
);

CREATE TABLE public.price_ (
	part_number varchar(10) NOT NULL,
	price varchar(10) NOT NULL
);

CREATE TABLE public.quantity_ (
	part_number varchar(10) NOT NULL,
	quantity varchar(10) NOT NULL,
	warehouse varchar(10) NOT NULL
);

CREATE TABLE public.report_ (
	part_number varchar(20) NOT NULL,
	main_part_number varchar(20) NOT NULL,
	manufacturer varchar(45) NOT NULL,
	category_ varchar(255) NOT NULL,
	origin varchar(10) NOT NULL,
	price numeric(10, 5) NOT NULL,
	deposit numeric(10, 5) NOT NULL,
	overall_price numeric(10, 5) NOT NULL,
	quantity int4 NOT NULL
);

CREATE TABLE public.weight_ (
	part_number varchar(10) NOT NULL,
	weight_unpacked varchar(10) NOT NULL,
	weight_packed varchar(10) NOT NULL
);

/*update and alter to make tables have right types of columns*/
UPDATE 
   price_ 
SET 
   price = REPLACE(price,',','.')

ALTER TABLE price_ 
ALTER COLUMN price TYPE DECIMAL using price::numeric;

UPDATE 
   quantity_ 
SET 
   quantity = REPLACE(quantity, '>', ' ' )
   
   
ALTER TABLE quantity_ 
ALTER COLUMN quantity TYPE integer USING quantity::integer;

UPDATE 
   deposit_
SET 
   deposit = REPLACE(deposit, ',', '.' ) where deposit like '%,%';
   
   
ALTER TABLE deposit_ 
ALTER COLUMN deposit TYPE decimal USING deposit::decimal;

/*insert into result table all values from join that pass all requirements*/
insert into report_ (part_number, main_part_number, manufacturer, category_, origin, price, deposit, overall_price, quantity)
select d.part_number, d.main_part_number, d.manufacturer, d.category_, d.origin, p.price, coalesce(d2.deposit, 0) as deposit, (p.price + d2.deposit) as overall_price, coalesce(q.quantity, 0) as quantity from data_ d
left join price_ p on d.part_number = p.part_number 
left join deposit_ d2 on d.part_number = d2.part_number 
left join quantity_ q on d.part_number = q.part_number
where q.warehouse in ('A', 'H', 'J', '3', '9') and q.quantity != 0 and p.price + d2.deposit >= 2;

/*final result rows*/
SELECT 
        main_part_number, manufacturer, category_, origin, price, deposit, overall_price, quantity
        FROM report_;