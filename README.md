# Inventory Hunter

Hopefully this helps you get the gift you want this year! My only request is that you do not use this for scalping (buying an in-demand item and selling it for a profit). I originally forked this repository from [EricJMarti](https://github.com/EricJMarti/inventory-hunter) and modified it to fit my needs.

## Requirements

- [Python](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)

## Quick Start

1. First, open your command prompt program of choice (I prefer using [Windows Terminal](https://www.microsoft.com/en-us/p/windows-terminal/9n0dx20hk701) but feel free to use PowerShell or Command Prompt).

2. Navigate to the folder you want to keep this program in using your Command Prompt program

3. Clone the repository.
```
$ git clone https://github.com/austinbaccus/inventory-hunter.git
```

4. Navigate into the newly created inventory-hunter folder, and run the program.
```
$ cd inventory-hunter
```

5. Run the program
```
$ python src.run.py -c <config_file>
```

Here is the exact line I use to run this program:
```
$ python src/run.py -c config/main.yaml
```

You can use any of the pre-made YAML files in the /config folder or make your own. 

## How it works

The general idea is if you can get notified as soon as a product becomes in stock, you might have a chance to purchase it before scalpers clear out inventory. This script continually refreshes a set of URLs, looking for the "add to cart" phrase. Once detected, the program will automatically open the webpage, allowing you as much time as possible to snag it before it's out of stock again.

## FAQ

### How is this different from existing online inventory trackers?

Before developing inventory-hunter, I used several existing services without any luck. By the time I received an alert, the product had already been scalped. This bot alerts faster than existing trackers for several reasons:
- it runs on your own hardware, so no processing time is spent servicing other users
- you get to choose which products you want to track
- you are in control of the refresh frequency

### What if inventory-hunter gets used by scalpers?

I sure hope this doesn't happen... 2020 is bad enough already. My hope is that inventory-hunter levels the playing field a bit by giving real customers a better opportunity than they had previously. Serious scalpers will continue using automated checkout bots, and it is up to online retailers to combat this malarkey.

### What did Austin (me) add to the original code?

I removed the email notification feature, added an alarm sound when the program detects an item is in stock, and added a feature that automatically opens the browser to that item's webpage when program detects that item is in stock.
