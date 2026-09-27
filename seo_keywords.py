#!/usr/bin/env python3
"""Command-line SEO keyword finder built on the Google autocomplete API.

Takes a seed query (e.g. "amazon"), asks Google autocomplete for suggestions
and prints them ordered by Google's relevance score. With --expand the query is
also combined with question prefixes ("how to", "best", ...) and a-z suffixes
to surface many more related keywords.

Usage examples:
    python seo_keywords.py amazon
    python seo_keywords.py amazon --expand --limit 50
    python seo_keywords.py "running shoes" --expand --format csv -o keywords.csv
"""

import argparse
import csv
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

SUGGEST_URL = "https://suggestqueries.google.com/complete/search"

EXPANDED_TERM_PREFIXES = ['who is *', 'what is *', 'where is *', 'when can *', 'why is *',
                          'how to *', 'best', 'cheap', 'worst', 'is', 'what', 'when', 'why',
                          'how', 'who']

EXPANDED_TERM_SUFFIXES = list('abcdefghijklmnopqrstuvwxyz')


def get_url(url, timeout=10):
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset, errors="replace")


def get_result(query, lang="en", country=None):
    params = {"output": "chrome", "hl": lang, "q": query}
    if country:
        params["gl"] = country
    url = SUGGEST_URL + "?" + urllib.parse.urlencode(params)
    return json.loads(get_url(url))


def order_result(result):
    terms = result[1]
    relevances = result[4].get('google:suggestrelevance', [0] * len(terms)) if len(result) > 4 else [0] * len(terms)
    return [{"term": term, "relevance": relevance} for term, relevance in zip(terms, relevances)]


def query_expansion(query):
    terms = [prefix + ' ' + query for prefix in EXPANDED_TERM_PREFIXES]
    terms += [query + ' ' + suffix for suffix in EXPANDED_TERM_SUFFIXES]
    return terms


def find_keywords(query, expand=False, lang="en", country=None, delay=0.0, verbose=False):
    terms = [query] + (query_expansion(query) if expand else [])
    best = {}
    for i, term in enumerate(terms):
        if verbose:
            print(f"[{i + 1}/{len(terms)}] {term}", file=sys.stderr)
        try:
            suggestions = order_result(get_result(term, lang, country))
        except (urllib.error.URLError, ValueError, IndexError, KeyError) as e:
            print(f"warning: failed to fetch suggestions for {term!r}: {e}", file=sys.stderr)
            continue
        # Keep each keyword once, with the highest relevance it was seen at.
        for item in suggestions:
            if item["relevance"] > best.get(item["term"], -1):
                best[item["term"]] = item["relevance"]
        if delay and i < len(terms) - 1:
            time.sleep(delay)
    results = [{"term": term, "relevance": relevance} for term, relevance in best.items()]
    return sorted(results, key=lambda k: k["relevance"], reverse=True)


def write_output(results, fmt, out):
    if fmt == "json":
        json.dump(results, out, indent=2, ensure_ascii=False)
        out.write("\n")
    elif fmt == "csv":
        writer = csv.DictWriter(out, fieldnames=["term", "relevance"])
        writer.writeheader()
        writer.writerows(results)
    else:
        out.write(f"{'RELEVANCE':>9}  KEYWORD\n")
        for r in results:
            out.write(f"{r['relevance']:>9}  {r['term']}\n")


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Find SEO keywords for a query using Google autocomplete suggestions.")
    parser.add_argument("query", help="seed search query, e.g. \"amazon\"")
    parser.add_argument("-e", "--expand", action="store_true",
                        help="expand the query with question prefixes and a-z suffixes (41 extra requests)")
    parser.add_argument("-n", "--limit", type=int, default=None,
                        help="show only the top N keywords")
    parser.add_argument("-f", "--format", choices=["table", "json", "csv"], default="table",
                        help="output format (default: table)")
    parser.add_argument("-o", "--output", help="write results to this file instead of stdout")
    parser.add_argument("-l", "--lang", default="en", help="interface language code (default: en)")
    parser.add_argument("-c", "--country", help="country code to localise results, e.g. us, in, uk")
    parser.add_argument("-d", "--delay", type=float, default=0.2,
                        help="seconds to wait between requests when expanding (default: 0.2)")
    parser.add_argument("-v", "--verbose", action="store_true", help="print progress to stderr")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    results = find_keywords(args.query, expand=args.expand, lang=args.lang,
                            country=args.country, delay=args.delay, verbose=args.verbose)
    if not results:
        print("No suggestions found.", file=sys.stderr)
        return 1
    if args.limit is not None:
        results = results[:args.limit]
    if args.output:
        with open(args.output, "w", newline="", encoding="utf-8") as f:
            write_output(results, args.format, f)
        print(f"Wrote {len(results)} keywords to {args.output}", file=sys.stderr)
    else:
        write_output(results, args.format, sys.stdout)
    return 0


if __name__ == "__main__":
    sys.exit(main())
