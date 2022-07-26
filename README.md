# Ramby

Ramby is a simple way to setup a webscraper.

## Installation

`pip install ramby`

## Examples

```python
from ramby import Ramby

scraper = Ramby('./exapmles/hackernews.yaml')
data = scraper.scrape("https://news.ycombinator.com/item?id=32237445")
```

## Configuration

A configuration file needs two fields, `HOST` and `RULES`.

### HOST

The `HOST` holds the base domain of the site you which to scrape, also keep in mind an error would be thrown if you choose to scrape a `URL` with a different `HOST`.

So in practice the `HOST` would be added to the configuration like so:

```yaml
host: example.com
```

### RULES

A `RULE` is basically a way to target certain elements in a webpage. For example you want to select all the titles of the top posts in [hackernews](https://news.ycombinator.com) you'd select them like so:

```yaml
host: news.ycombinator.com

rules:
    hompage:
        pattern: '/' # The `/` path signifies we use the `homepage` rule 
        topics:    # This would denote a section in the homepage, making it easy to add other obejects if needed i.e all_authors
            title: # An object property
                selector: '.athing .title > a' # The title target
                text: true                     # We would want the text inside the target element
                # html: true is optional
                count: 2                       # The amount of elements to return
                attrs:                         # Specify the html attributes you'd want
                    - href                     # Also taking the link to the post
```

#### Sample returned Object based on the rules above

```python
{'topics': {'title': {0: {'attrs': {'href': 'https://paulbutler.org/2022/why-is-it-so-hard-to-give-google-money/'},
                          'text': 'Why is it so hard to give Google money?'},
                      1: {'attrs': {'href': 'https://mullvad.net/en/blog/2022/7/26/mullvad-is-now-available-on-amazon-us-se/'},
                          'text': 'Mullvad is now available on Amazon'}}}}
```

#### And if you choose to select comments

```yaml
host: news.ycombinator.com

rules:
    hompage:
        pattern: '/' # The `/` path signifies we use the `homepage` rule 
        topics:    # This would denote a section in the homepage, making it easy to add other obejects if needed i.e all_authors
            title: # An object property
                selector: '.athing .title > a' # The title target
                text: true                     # We would want the text inside the target element
                # html: true is optional
                count: 2                       # The amount of elements to return
                attrs:                         # Specify the html attributes you'd want
                    - href                     # Also taking the link to the post
                  
    posts:
        pattern: /item/
        post:
            title: 
                selector: '.fatitem:first-child .title > a'
                count: 1
                text: true
                attrs: 
                    - href 

        comments:
            texts:
                selector: '.comment .commtext'
                count: 2
                text: true

```


#### Sample returned Object based on the rules above

```python
{'topics': {'title': {0: {'attrs': {'href': 'https://paulbutler.org/2022/why-is-it-so-hard-to-give-google-money/'},
                          'text': 'Why is it so hard to give Google money?'},
                      1: {'attrs': {'href': 'https://mullvad.net/en/blog/2022/7/26/mullvad-is-now-available-on-amazon-us-se/'},
                          'text': 'Mullvad is now available on Amazon'}}}}
```


#### Sample returned Object based on the rules above

```python
{'comments': {'texts': {0: {'text': 'Wonder how much money & resources Shopify '
                                    'spent on all of their NFT features & '
                                    'integrations over the last months, how '
                                    'many people worked on it and how many of '
                                    "those are part of the lay-off now. I'd "
                                    "guess the support you'd need to provide "
                                    'for it and their tokengated commerce '
                                    "isn't little either.Tobi removed all the "
                                    'NFT stuff from his Twitter profile and '
                                    "didn't tweet much about it for months "
                                    'now, after being pretty vocal about it '
                                    'until earlier this year.Would love to '
                                    'hear his real thoughts on it and why '
                                    'he/they even (seemingly) invested so much '
                                    'into it. One of the few things I never '
                                    'got about Tobi / Shopify. Just seemed so '
                                    'late and weird to be so bullish there. '
                                    "Don't think he's the kind of person to "
                                    'push it just for personal gain, nor that '
                                    "he'd have to, but ..."},
                        1: {'text': 'I’m honestly still in disbelief at how '
                                    'many very smart people fell for the NFT '
                                    'trap. If you’ve spent even a single bull '
                                    'cycle in the crypto community you could '
                                    'tell right away NFTs we’re ICO level '
                                    'scams. The mental gymnastics very smart '
                                    'and technical people performed to '
                                    'rationalize paying for a jpeg still makes '
                                    'me question reality. I participate in '
                                    'crypto because I take a calculated risk, '
                                    'and I’m comfortable gambling. People who '
                                    'actually think something like an NFT has '
                                    'any real value still messes with my head. '
                                    'I really can’t grasp how they actually '
                                    'believe this. And yes, I understand '
                                    'technically how NFTs work.'}}},
 'post': {'title': {0: {'attrs': {'href': 'https://www.wsj.com/articles/shopify-to-lay-off-10-of-workers-in-broad-shake-up-11658839047'},
                        'text': 'Shopify to lay off 10% of workers in broad '
                                'shake-up'}}}}
```

### See more examples [here](https://github.com/keosariel/ramby/tree/master/examples)
