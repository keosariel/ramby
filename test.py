from ramby import Ramby
import pprint
g = Ramby("examples/hackernews.yaml")
pprint.pprint(g.scrape("https://news.ycombinator.com/item?id=32237574", "GET"))
