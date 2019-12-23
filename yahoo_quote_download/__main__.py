import os, sys, time
import argparse
from .yqd import YahooQuote

def main():
    p = argparse.ArgumentParser()
    p.add_argument('-H', '--no-header', default=True, dest='header')
    p.add_argument('-e', '--events', choices=('history','div','split'), default='history')
    p.add_argument('-d', '--days', type=int, default=1)
    p.add_argument('ticker', nargs='+')
    args = p.parse_args()

    try:
        cookie_crumb = open(os.path.expanduser("~/.yahooquotes")).read().splitlines()
        print("Got cached cookie_crumb from ~/.yahooquotes", file=sys.stderr)
    except Exception:
        cookie_crumb = None
    yq = YahooQuote(cookie_crumb)
    if yq.cookie_crumb != cookie_crumb:
        open(os.path.expanduser("~/.yahooquotes"),'w').write('\n'.join(yq.cookie_crumb))
        print("Cached cookie_crumb in ~/.yahooquotes", file=sys.stderr)

    sys.stdout.writelines( yq.csv(args.ticker, events=args.events, headers=args.header, begindate=int(time.time()-86400*args.days)) )

if __name__=='__main__':
    main()
