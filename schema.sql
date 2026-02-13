-- db e tabela do projeto

create database if not exists smartimg;
use smartimg;

create table if not exists images (
  id int auto_increment primary key,
  filename varchar(255) not null,   -- nome do arquivo
  sha256 char(64) not null,         -- hash de dedup
  description text not null,        -- descricao gerada
  category varchar(80) not null,    -- categoria
  created_at timestamp default current_timestamp
);

-- indice q acha dupe
create index idx_images_sha256 on images(sha256);
