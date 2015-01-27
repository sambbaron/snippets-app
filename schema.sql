
-- Create snippets table
create table snippets (
keyword text primary key,
message text not null default ''
);

-- Insert row examples
insert into snippets values ('insert', 'Add new rows to a table');
insert into snippets (message, keyword) values ('Add new rows to a table', 'insert');

-- Select row examples
select * from snippets;
select message from snippets;
select keyword, message from snippets where keyword='insert';

-- Update row examples
update snippets set keyword='insert into', message='Insert new rows into a table' where keyword='insert';

-- Delete row examples
delete from snippets where keyword='insert into';
