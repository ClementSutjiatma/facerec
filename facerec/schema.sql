drop table if exists courses;
create table courses (
  id integer primary key autoincrement,
  coursename text not null,
  coursenum text not null,
  timestart TIMESTAMP,
  timeend TIMESTAMP,
  teacher_uniqname text not null
);
drop table if exists people;
create table people (
  uniqname text primary key not null,
  firstname text not null,
  lastname text not null
);
