-- Below is our database for Ecommerce management project.
create database `Ecommerce_Management` ; 
-- to enter in database
use `Ecommerce_Management`;
-- --------------------------------------------- Category --------------------------------------------------------------
-- for creating table for category
create table `Category`(
`Category_Id` int primary key ,
`Category_Name` varchar(50) not null);

-- to view category
select * from `Category`;
show create table category;

-- --------------------------------------------- Product --------------------------------------------------------------

-- for creating product.
create table `Product`(
`Product_Id` int primary key ,
`Product_Name` varchar(50) not null,
`Category_Id` int not null,
`Price` decimal(10,2) not null check (`Price`>0),
foreign key (`Category_id`) references `Category`(`Category_id`)
);

-- to view product table
select * from `product`;

-- to change data type of Price double to float. 
alter table `Product`
change column `Price` `Price` float(7,2); 

-- --------------------------------------------- Account --------------------------------------------------------------

create table `Admin`(
`User_Id` int unique,
`Password` varchar (15) not null,
`Confirm_Password` varchar (15) not null,
`Role` varchar (10) not null,
key (`User_Id`));

select * from Account;

-- Rename Admin table to Account
Alter table `admin` rename `Account`;

-- Rename column confirm password to old password
Alter table `Account` change column `Confirm_Password` `Old_Password` varchar (200) ;

-- Change properties of column Password
Alter table `Account` change column `Password` `Password` varchar (200);

-- Add primary Key to User_Id
alter table `Account` add constraint primary key (`User_Id`);

-- changes by akshay --
-- Add column User_Name
alter table `Account` add column `User_Name` varchar(200) after `User_Id`;

-- Change properties of User_id
alter table `Account` modify column `User_id` int auto_increment, auto_increment = 1000;

-- Adding new column
ALTER TABLE `Account` ADD COLUMN `Status` ENUM('Active', 'Deleted') DEFAULT 'Active';

-- --------------------------------------------- Customer --------------------------------------------------------------

-- for creating customer table
create table `Customers`(
`Customer_Id` int not null,
`Customer_Name` varchar (50) not null,
`Customer_Number` int(10) unique,
`Customer_Email` varchar (70) not null,
primary key (`Customer_Id`))auto_increment = 1000;

select * from `customers`;

-- Change column name customers id to user id
Alter table `Customers` change column `Customer_Id` `User_Id` varchar (50) not null;
Alter table `Customers` change column `User_Id` `User_Id` int not null;

-- Change column constraints P.K to F.K.
alter table `customers` drop primary key;
alter table `customers` add constraint foreign key (`User_Id`) references `account` (`User_Id`) ;

-- Add New column 
alter table `Customers` add column `Coustomer_Address` varchar (100) not null;

-- changes by akshay --
-- Change column name and Add new column
alter table `Customers` change column `Customer_Name` `Customer_First_Name` varchar (50) not null;
alter table `Customers` add column `Customer_Last_Name` varchar(50) not null after `Customer_First_Name`;

-- changing the Coustomer_Address column
alter table `Customers` change column `Coustomer_Address` `Customer_Address` varchar(100);

-- Modify column
alter table `Customers` modify column `Customer_Number` char(10) unique;

desc customers;
show create table `customers`;

-- --------------------------------------------- Order --------------------------------------------------------------

/*-- for creating orders table
create table `Orders` (
`Order_Id` int ,
`Customer_Id` int not null,
`Product_Id` int not null,
`Total_price` decimal(10,2),
primary key (`Order_Id`),
foreign key (`Customer_Id`) references `Customers`(`Customer_Id`),
foreign key (`Product_Id`) references `Product`(`Product_Id`));
-- Above table is deleted.*/

-- Delete Order table
drop table `orders`;

-- ---------------------------------------------  --------------------------------------------------------------
-- for creating account table
/*create table `Account`(
`User_Id` int unique,
`Password` varchar (15) not null,
`Confirm_Password` varchar (15) not null,
`Role` varchar (10) not null,
key (`User_Id`));*/ 

-- table added by akshay
-- --------------------------------------------- order_status --------------------------------------------------------------
create table `order_status` (
`status_id` int unique not null,
`status_name` varchar(50),
primary key  `order_status`(`status_id`)
);

-- --------------------------------------------- Orders_History --------------------------------------------------------------

-- create Order history table

create table `Orders_History` (
`Order_Id` int ,
`User_Id` int not null,
`Product_Id` int not null,
`Order_Date` date not null,
`Order_Status`  varchar(10) not null,
foreign key (`User_Id`) references `Customers`(`User_Id`),
foreign key (`Product_ID`) references `Product`(`Product_Id`)
);

desc `Orders_History`;

-- Drop foreign key user id
alter table `Orders_History`
drop foreign key `FK_User_Id`; 

ALTER TABLE `orders_history` 
DROP FOREIGN KEY `orders_history_ibfk_1`;

-- Add new foregin key
alter table `orders_history` Add constraint foreign key (`User_Id`) references `Customers`(`User_Id`);

-- changes by akshay
-- add new column Qty
alter table `orders_history` add column `Qty` int after `Product_id`;
-- modify column
alter table `orders_history` modify column `order_status` int not null;
-- add foreign key
alter table `orders_history` add foreign key (`order_status`) references `order_status`(`status_id`);
-- modify column
alter table `orders_history` modify column `order_id` int not null;
-- add primary key 
alter table `orders_history` add primary key (`order_id`);
-- modify column
alter table `orders_history` modify column `order_id` int auto_increment, auto_increment = 111111;

show create table  `orders_history`;

-- --------------------------------------------- Admin --------------------------------------------------------------

create table `admin`(
`User_Id` int unique,
`phone_number` int unique not null,
`mail_id` varchar (20) unique not null,
`address` varchar (100) not null,
foreign key (`User_Id`) references `Customers`(`User_Id`)  
);
 
 select * from `admin`;
 
 -- Add column after user id
alter table `admin` add column `admin_username` varchar (20) after `User_Id`;

-- Add new foregin key
alter table `admin` Add constraint foreign key (`User_Id`) references `Account`(`User_Id`);

-- drop foregin key
ALTER TABLE `admin` 
DROP FOREIGN KEY `admin_ibfk_1`;

-- changes by akshay
-- Modifying columnn
alter table `admin` modify column `address` varchar(100);

alter table `admin` modify column `admin_username` varchar(20) not null;

-- changing primary key
alter table `admin` add primary key (`user_id`);
-- drop primary key
alter table `admin` drop primary key;
-- modify column
alter table `admin` modify `phone_number` char(10) unique not null;

desc admin;
show create table admin;

-- Data Inserting Queries

insert into `Category`(`Category_id`,`Category_name`)
values
(201,'Health'),
(202,'Skincare'),
(203,'Cosmetics'),
(204,'Vegetables'),
(205,'Fruits'),
(206,'Dairy'),
(207,'Bakery'),
(208,'Cleaning_Essentials'),
(209,'Baby_Care');

insert into `Product`(`Product_Id`,`Product_Name`,`Category_Id`,`Price`)
values
(1101,'Electric_Philips_Toothbruch',201,2500), # Health Product start from 1101
(1102,'Omron_Blood_Pressure',201,2000),
(1201,'Mamaearth_Face_Wash',202,219), # Skincare product Start from 1201
(1202,'Dettol_soap',202,280),
(1301,'Fair_and_Lovely',203,90), # Cosmetics product Start from 1301
(1401,'Tomato_1KG',204,18), # Vegetables product Start from 1401
(1402,'Onion_1KG',204,33),
(1501,'Apple_1KG',205,150), # Fruits product Start from 1501
(1502,'Tender_Coconut',205,50),
(1601,'Milk_1L',206,50), # Dairy product Start from 1601
(1602,'Shrikhand_1KG',206,140),
(1701,'Amul_Butter_100G',207,60), # Bakery product Start from 1701
(1702,'Amul_Cheese',207,124),
(1801,'Milton_Spin_Mop',208,1399), # Cleaning_Essentials product Start from 1801
(1802,'Scotch_Brite',208,195),
(1901,'Cetaphil_Baby_Shampoo',209,625); # Baby_Care Start from 1901insert into Category(Category_id,Category_name)

-- data added by akshay
insert into `order_status`(`status_id`, `status_name`)
values
(11, 'Not Dispatched'),
(21, 'Dispatched'),
(31, 'Delivered'),
(41, 'Not Delivered'),
(51, 'Returned'),
(61, 'Cancelled');