import os, sys, time
import argparse
from .yqd import YahooQuote

def main():
    p = argparse.ArgumentParser()
    p.add_argument('-H', '--no-header', action='store_false', default=True, dest='header')
    p.add_argument('-e', '--events', choices=('history','div','split'), default='history')
    x = p.add_mutually_exclusive_group()
    x.add_argument('-d', '--days', type=int, default=1, help='Number of days of results to return (default %(default)s)')
    x.add_argument('-L', '--latest', action='store_true', help='Just return the one most-recent row for each ticker')
    p.add_argument('-t', '--tsv', action='store_const', const='\t', dest='sep', default=',',
                   help='Output TSV (tab-separated) rather than CSV (comma-separated)')
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

    if args.latest:
        begindate, max_rows = None, 1
    else:
        max_rows, begindate = None, int(time.time()-86400*args.days)
    sys.stdout.writelines( yq.csv(args.ticker, events=args.events, headers=args.header, begindate=begindate, max_rows=max_rows, sep=args.sep) )

if __name__=='__main__':
    main()
