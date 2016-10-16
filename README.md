# Pocket Stats

## Motivation

It's easy to get ever-growing [Pocket] reading lists and lose track of what is
actually in it. This script prints out useful stats and plots some graphs to
help you grok your reading list.

## Usage

Start by creating a virtualenv and install the necessary dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install --requirement requirements.txt
```

Authentication with Pocket's API is unfortunately difficult for a CLI script
because you must go through the web OAuth flow. Start by getting an access
token (you'll have to create a Pocket app to get a consumer key):

```bash
./pocket-stats.py --consumer-key="$consumer_key"
```

Copy and paste the URL into your web browser and authorize the login request.
Press enter to complete the login flow and generate an access token. Now, use
that access token to run the script to print out stats:

```bash
[N]> ./pocket-stats.py --consumer-key="$consumer_key" --access-token="$access_token"
Total: 1061
Total words: 1758033
Average words: 1656.9585296889727
Favorite: 0
Has image: 729
Has video: 82
Article: 986
Tags:
        ifttt: 404
        37signals: 128
        commonsware: 60
        fb code: 34
        fogcreek: 26
        optimizely: 20
        square: 19
        ifixit: 19
        wbw: 12
        stevenwilson: 10
        benmccormick: 10
        etsy: 9
        airbnb: 9
        github: 7
        xkcd: 6
        githubengineering: 6
        bolt: 5
        optimizely-engineers: 5
        optimizely-design: 4
        zachholman: 4
        davidzych: 3
        pocket: 3
        publicobject: 3
        clements: 1
        codinghorror: 1
```

This also launches a window to display a graph of dates to display when the
items were added to Pocket. Once that graph is closed, another graph is
displayed to show tags.

[Pocket]: https://getpocket.com/
