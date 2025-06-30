from bs4 import BeautifulSoup
import requests
import re
from collections import Counter
import argparse

print(r"""
 _____           _              __  __        __   _         _ _       
|_   _|__   ___ | |___    ___  / _| \ \      / /__| |__  ___(_) |_ ___ 
  | |/ _ \ / _ \| / __|  / _ \| |_   \ \ /\ / / _ \ '_ \/ __| | __/ _ \
  | | (_) | (_) | \__ \ | (_) |  _|   \ V  V /  __/ |_) \__ \ | ||  __/
  |_|\___/ \___/|_|___/  \___/|_|      \_/\_/ \___|_.__/|___/_|\__\___|
                                                                    by P""")

def search_link(website):
    print(f"[+] Starting search link from {website}...")
    r = requests.get(website)
    soup = BeautifulSoup(r.text, "html.parser")
    src = [tag['src'] for tag in soup.find_all('script', src=True) if tag['src'].strip()]
    href = [tag['href'] for tag in soup.find_all('link', href=True) if tag['href'].strip()]
    links = [link for link in src+href if link.startswith("http://") or link.startswith("https://")]
    if links:
        for link in links:
            print(link)
    else:
        print("[-] Not found")

def count_letter(website):
    print(f"[+] Starting count letter from {website}")
    r = requests.get(website)
    soup = BeautifulSoup(r.text, "html.parser")
    for tag in soup(["script", "style"]):
        tag.decompose()
    text = soup.get_text(separator=" ")
    words = re.findall(r"\b\w+\b", text.lower())
    word_count = Counter(words)
    for word, count in word_count.most_common():
        print(f"{word}: {count}")

def main():
    parser = argparse.ArgumentParser(prog="tools_of_website.py", description="Created by P")
    parser.add_argument("-u", "--url" , type=str, help="URL Target")
    parser.add_argument("-p", "--port", type=str, default="443", help="Port Target (default: 443)")
    parser.add_argument("-m", "--mode", type=str, default="sl", help="Mode: sl, cw (default: sl)")
    args = parser.parse_args()
    if args.url and args.port:
        if args.mode == "sl":
            search_link(args.url +":"+ args.port)
        elif args.mode == "cw":
            count_letter(args.url +":"+ args.port)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()