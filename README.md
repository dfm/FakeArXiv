This code generates *nearly* believable titles for scientific papers based on
a smoothed trigram model of all of the titles ever published on
[arxiv.org](http://arxiv.org).

Usage
-----

First download and unzip the [text file containing the list of
titles](http://bbq.dfm.io/~dfm/data/titles.txt.gz). Then run:

```
python ngram.py --build
```

After this first run, you only have to run

```
python ngram.py
```

and it will use the cached N-gram dictionary.

If you want to post to Twitter, register an app on the developer site (making
sure that it has write access) and save a file called `local.cfg` with the
format:

```
[twitter]
consumer_key: ...
consumer_secret: ...
user_key: ...
user_secret: ...
```

replacing the `...` with the obvious things. Then call

```
python ngram.py --tweet
```


Licence
-------

Licensed under the MIT license.

Copyright 2014 Dan Foreman-Mackey
