import logging
import sched
import smtplib
import sys
import winsound
import webbrowser
from scraper import Scraper
from termcolor import colored


class Engine:
    def __init__(self, args, config):
        self.refresh_interval = config.refresh_interval
        self.max_price = config.max_price
        self.scheduler = sched.scheduler()
        self.scrapers = [Scraper(url, self.refresh_interval) for url in config.urls]
        for s in self.scrapers:
            self.schedule(s)

    def run(self):
        self.scheduler.run(blocking=True)

    def schedule(self, s):
        if self.scheduler.queue:
            t = self.scheduler.queue[-1].time + self.refresh_interval
            self.scheduler.enterabs(t, 1, Engine.tick, (self, s))
        else:
            self.scheduler.enter(self.refresh_interval, 1, Engine.tick, (self, s))

    def tick(self, s):
        result = s.scrape()

        if result is None:
            logging.error(f'{s.name}: scrape failed')
        else:
            self.process_scrape_result(s, result)

        return self.schedule(s)

    def process_scrape_result(self, s, result):
        currently_in_stock = bool(result)

        if currently_in_stock:
            if self.max_price is not None and result.price <= self.max_price:
                self.in_stock_good_price(s.name, result.price, s.url)
            else:
                self.in_stock_bad_price(s.name, result.price)
        else:
            self.not_in_stock(s.name)

    def in_stock_good_price(self, product_name, price, url):
        for i in range(0,20):
            print(colored('***********************************************************************************', 'green'))
        print("\n\n\n", colored(product_name, 'white'), colored('in stock for', 'green'), colored(f'${price}', 'green'))

        # open the webpage for this item
        webbrowser.open(f'{url}', new=2)

        # play the alarm sound until the user ends the program
        print("Press Ctrl-C to end the program")
        while True:
            winsound.PlaySound(".\\resources\\VenatorHangarHit.wav", winsound.SND_FILENAME)
            winsound.PlaySound(".\\resources\\yes.wav", winsound.SND_FILENAME)

    def in_stock_bad_price(self, product_name, price):
        print(colored(product_name, 'white'), colored(f'in stock for bad price: ${price}', 'red'))

    def not_in_stock(self, product_name):
        print(colored(product_name, 'white'), colored('not in stock', 'red'))

    def send_alert(self, s, result, reason):
        logging.info(f'{s.name}: {reason}')
        self.alerter(result.alert_subject, result.alert_content)


def hunt(args, config):
    engine = Engine(args, config)
    engine.run()