#!/usr/bin/env python3

import json
import urllib.request

# Weechat stuff
SCR_NAME    = "bash_search"
SCR_AUTHOR  = "David Trail <bash_search@vaunt.eu>"
SCR_VERSION = "0.0.1"
SCR_LICENSE = "BSD"
SCR_DESC    = "SCReddit EU Bash search script"
SCR_COMMAND = "bash"

_BASE_URL = "http://bash.vaunt.eu/"
_JSON_URL = "{base_url}?json".format(base_url=_BASE_URL)
_URL_FORMAT_STRING = "{base_url}?{id}"
_MAX_SEARCH_RESULTS = 3
quote_list = []

try:
    import weechat
    import_ok = True
except ImportError:
    import_ok = False


class Quote:
    """Base Quote class."""
    id = None
    text = None
    score = None

    def __init__(self, _hash):
        self.id = _hash['id']
        self.text = _hash['quote']
        self.score = _hash['popularity']

    def __str__(self):
        return """{id} ({score}): {url}""".format(
            id=self.id,
            score=self.score,
            url=_URL_FORMAT_STRING.format(base_url=_BASE_URL, id=self.id),
        )

response = urllib.request.urlopen(_JSON_URL)
json_quotes = json.loads(response.read().decode('utf-8'))

for j in json_quotes:
    quote = Quote(j)
    quote_list.append(quote)


def search_quotes(string):
    """List of quotes matching search string."""
    matches = []
    for quote in quote_list:
        if string in quote.text and len(matches) <= _MAX_SEARCH_RESULTS:
            matches.append(quote)
    return matches

if __name__ == "__main__" and import_ok:
    weechat.register(SCR_NAME, SCR_AUTHOR, SCR_VERSION, SCR_LICENSE, SCR_DESC, "", "UTF-8")
    buffer = buffer = weechat.info_get("irc_buffer", "quakenet,#nay")
    weechat.prnt(buffer, "Sup")
    dict = weechat.info_get_hashtable("irc_message_parse", {"message": ":nick!user@host PRIVMSG #weechat :message here"})
    weechat.prnt(buffer, dict)
