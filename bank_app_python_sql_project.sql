create database new_bank;
use new_bank;
show tables;

create table customer_info
(
c_id int primary key auto_increment,
fname varchar(50),
mname varchar(50),
lname varchar(50),
phoneno varchar(10),
aadhaarno varchar(12),
date date,
username varchar(10),
password varchar(4),
balance int);

insert into customer_info values (10001,"Prakshi","Keshav","Karkera","9324205835","123456789101","2024-12-09","pkkk","2324",0);

select c_id from customer_info where username="pkkk";

select * from customer_info ;
select * from pkkk ;
update customer_info set balance=0 where c_id=10004;
truncate customer_info;
truncate pkkk;

drop table pkkk ;

-- create table kkrish
-- (Sr_no int primary key auto_increment,
-- Date date,
-- Transaction varchar(10),
-- Amount int);

create table admin_info(
ad_id int primary key auto_increment,
ad_name varchar(30),
ad_username varchar(10),
ad_passkey int);

insert into admin_info values
(1001,"Aayush","ayushak",181970),
(1002,"Samira","samthakur",261970),
(1003,"Priyanka","priyass",241982),
(1004,"Ankur","akmehta",221988),
(1005,"Shankar","shankarss",131190),
(1006,"Priyank","pikukumar",121994);

-- select*from admin_info;

-- drop database new_bank;