create table if not exists user (
    user_id int not null,
    tg_id int not null,
    message_format varchar(5),
    include_banks varchar(200),
    deleted_flg char(1) not null,
    processed_dttm timestamp not null
);
