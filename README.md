# FacebookSearch
[![Downloads](https://pypip.in/d/FacebookSearch/badge.png)](https://crate.io/packages/FacebookSearch/) [![PyPI version](https://pypip.in/v/FacebookSearch/badge.png)](https://crate.io/packages/FacebookSearch/)

This library is in a very early stage of development and due to this there no documentation available (beside the source itself :p).

## Usage
However, if you would like to have a glimpse this is what you've got to do:
```python
from FacebookSearch import *
from pprint

fbo = FacebookSearchOrder()
fbo.setKeywords('NSA')

try:
    fb = FacebookSearch(client_id='123', client_secret='I_really_do_like_spiderman_undies')
    # or even: FacebookSearch(access_code='NoNeedToCreateOne')

    # don't worry if it takes its time - you'll get 500 records
    # (this is the maximum amount of recods you're able to get from the Graph API)
    for info in fb.searchGraphIterable(fbo):
        pprint.pprint(info)

except FacebookSearchException as e:
    print(e)
```
