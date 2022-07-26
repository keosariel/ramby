from ramby import Ramby

g = Ramby("examples/hackernews.yaml")
print(g.scrape("https://news.ycombinator.com/", "GET"))
