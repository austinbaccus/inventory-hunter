import logging
import sched
import smtplib
import sys
import winsound
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
            self.print_in_stock_alert(s.name)
            while True:
                winsound.PlaySound(".\\resources\\VenatorHangarHit.wav", winsound.SND_FILENAME)
                winsound.PlaySound(".\\resources\\yes.wav", winsound.SND_FILENAME)

        else:
            print(colored(s.name, 'white'), colored(' not in stock!', 'red'))

    def print_in_stock_alert(self, product_name):
        for i in range(0,20):
            print(colored('***********************************************************************************', 'red'))
        print()
        print()
        print()
        print(colored(product_name, 'red'), colored(' in stock!', 'green'))

    def send_alert(self, s, result, reason):
        logging.info(f'{s.name}: {reason}')
        self.alerter(result.alert_subject, result.alert_content)


def hunt(args, config):
    engine = Engine(args, config)
    engine.run()