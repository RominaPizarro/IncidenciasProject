alter session set "_ORACLE_SCRIPT" = TRUE;

create user db_control_incidencias IDENTIFIED BY incidencias_123;
alter user db_control_incidencias default TABLESPACE users quota UNLIMITED on users;

grant connect to db_control_incidencias;
grant all privileges to db_control_incidencias;