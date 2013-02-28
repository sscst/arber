CREATE DATABASE arber;

use arber;

DROP TABLE IF EXISTS mession;
CREATE TABLE mession(
       user_name varchar(500) not null,
       target_name varchar(500) not null,
       status varchar(10) not null
)DEFAULT charset=utf8;

DROP TABLE IF EXISTS context;
CREATE TABLE context(
       id bigint not null,
       content varchar(500) not null,
       create_time datetime not null,
       pic_url varchar(500) not null,
       own int not null,
       other_context varchar(500) not null,
       target_name varchar(50) not null,
       user_name varchar(100) not null,
       hot int not null
)CHARACTER SET utf8 COLLATE utf8_general_ci ;

ALTER TABLE arber.context MODIFY COLUMN other_context VARCHAR(500) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL;

ALTER TABLE arber.context MODIFY COLUMN content VARCHAR(500) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL;