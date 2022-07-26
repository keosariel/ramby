# ramby.py
# Ramby is a simple way to setup a webscraper, also making
# it easy to update without having to touch your code or add more
# if-statements

from bs4 import BeautifulSoup
from collections import defaultdict
import requests
from urllib.parse import urlparse
from werkzeug.routing import Map, Rule, NotFound
import yaml

__version__ = "0.0.1"
__author__ = "keosariel"

class Ramby:
    def __init__(self, config_file):
        with open(config_file) as stream:
            config = yaml.safe_load(stream)

        valid_keys = ("headers", "host", "rules")

        if set(valid_keys).intersection(set(config.keys())) != set(valid_keys):
            raise ValueError("Expected: %s" % (', '.join(valid_keys)))
        
        self._host = config["host"]
        self._rules = config["rules"]

        self.headers = config["headers"]
        self.rule_map = Map()

        self._add_patterns()

    def _add_patterns(self):
        """Stores a pattern for later matching
        """

        for rule, values in self._rules.items():
            pattern = values.get("pattern")
            if pattern:
                self.rule_map.add(Rule(pattern, defaults=values, endpoint=rule))
        
    def match(self, url):
        """Matches a url with a pattern

        Args:
            url (str): web location to scrape 
        
        Returns:
            matched (tuple): a tuple containg the rule name and it's
                             config data
        """

        rules = self.rule_map.bind(self._host, "/")

        try:
            upd = urlparse(url)
            
            if upd.netloc != self._host:
                raise ValueError("Unsupported Host")
            return rules.match( upd.path+"/" )

        except NotFound:
            raise ValueError("Unknown pattern")

    def _get_request_func(self, method):
        """Gets the requests function associated
        with `method`

        Args:
            method (str): a HTTP request method i.e GET

        Exceptions:
            ValueError: Throws this if method not in (GET, POST)
        
        Returns: a requests function
        """

        method = method.lower()

        if method == "get":
            return requests.get
        elif method == "post":
            return requests.post
        else:
            raise ValueError("Method not allowed")

    def scrape(self, url, method="GET", headers={}):
        """Scrapes `url` based on the data given in
        the rule which it matches.

        Args:
            url (str): web location to scrape
            method (str): HTTP request method (either GET or POST)
            headers (dict): HTTP headers for request

        Returns: None or a Dictionary
        """

        rule_name, values = self.match(url)

        res = requests.get(url, headers=headers or self.headers)

        if res.status_code == 200:
            return self._scrape(res.text, values)
        
    
    def _scrape(self, text, rules):
        """Extracts data from `text` based on the `rules`
        
        Args:  
            text (str): html string
            rules (dict): selectors to query
        
        Returns: dict
        """

        soup = BeautifulSoup(text, features="html.parser")
        
        rules.pop("pattern")

        object_data = {}

        for object_name, props in rules.items():
            data = dict()

            for prop_name, p_prop in props.items():
                prop_data = defaultdict(dict)

                selector = p_prop.get('selector')

                if selector:
                    count = p_prop.get('count', 1)
                    if count > 1:
                        selected = soup.select(selector)[:count]
                    else:
                        selected = [soup.select_one(selector)]
                        
                    if selected:
                        for i, item in enumerate(selected):
                            if item:
                                if p_prop.get('text'):
                                    prop_data[i]["text"] = item.text
                                
                                if p_prop.get('html'):
                                    prop_data[i]["html"] = str(item)
                                
                                for attr in p_prop.get("attrs", []):
                                    if not prop_data[i].get("attrs"):
                                        prop_data[i]["attrs"] = dict()

                                    prop_data[i]["attrs"][attr] = item.attrs.get(attr)


                data[prop_name] = dict(prop_data)
            object_data[object_name] = dict(data)

        return object_data