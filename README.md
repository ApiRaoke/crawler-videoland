# crawler-videoland

It's a crawler/spider to get karaoke list from <https://www.videoland.com.br/wwwroot/pesquisa.asp?artista=A&titulo=&letra=&categoria=33&pagina=1>

## Requirements

- python3
- scrapy

## How to run

### CSV

```shell
> cd crawler-path
> time scrapy runspider crawler.py -o file.csv -t csv
```

*Note.: * this CSV does not quote strings, so be careful.

### JSON

```shell
> cd crawler-path
> time scrapy runspider crawler.py -o file.csv -t csv
```
