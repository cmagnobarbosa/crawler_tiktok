## Crawler TikTok
[![Pylint](https://github.com/cmagnobarbosa/crawler_tiktok/actions/workflows/pylint.yml/badge.svg)](https://github.com/cmagnobarbosa/crawler_tiktok/actions/workflows/pylint.yml)

* Desenvolvido com objetivos educacionais

Crawler simples para recuperar metadados de videos no Tiktok.

Simple crawler to retrieve video metadata related to a search on the TikTok website.

``` console
run main.py [subject_to_search]
```


### Output

JSON:
``` JSON

{
   "title": "str",
   "username": "str",
   "views": "str",
   "url": "str",
   "date": "str",
   "hashtags": "List",
   "created_at": "str",
   "shares": "number",
   "comments": "number",
   "likes": "number"
}
```

### Constants

Constants file:
- [Link](core/constants.py)

``` sheel
TIKTOK_URL = "https://www.tiktok.com/"
MAX_PAGINATION = 20 # Max scrools on Tiktok page
SLEEP_TIME = 3 # Time to await
LANG = "pt-BR"
```
