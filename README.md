## Crawler TikTok

Retrieve video metadata related to a search on the TikTok website.

``` console
run main.py [subject_to_search]
```

### Return

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

