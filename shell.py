import cmd
import requests
import re
import webbrowser
from termcolor import colored
from colorama import Fore, Style


class Terminal(cmd.Cmd):
    intro = "Welcome to the molenaar shell. Type help or ? to list commands"
    prompt = '[$] '
    links = []

    def do_search(self, url):
        """search [url]
        Searches the given url for youtube links"""
        if url:
            if re.match(r"^(http|https)://", url):
                text = requests.get(url).text
                pattern = r"(http|https)://(www\.)?(youtube.com|youtu.be)/(watch)?(\?v=)?(\S+)?/"
                matches = re.finditer(pattern, text, re.MULTILINE | re.IGNORECASE)
                for num, match in enumerate(matches, start=1):
                    print(colored("Match {num} was found at {start}--{end}: {match}".format(num=num, start=match.start(),
                                                                                    end=match.end(),
                                                                                    match=match.group(0)), "green", attrs=["bold"]))
                    self.links.append(match.group())
            else:
                print(colored("Please enter a valid url starting with http:// or https://", "red", attrs=["bold"]))
        else:
            print(colored("Please enter a url", "red", attrs=["bold"]))

    def do_open(self, url):
        """open [url]
        Opens the given url in the default browser"""
        if url:
            if re.match(r"^(http|https)://", url):
                webbrowser.open(url, new=2)
            else:
                print(colored("Please enter a valid url starting with http:// or https://", "red", attrs=["bold"]))
        else:
            print(colored("Please enter a url", "red", attrs=["bold"]))

    def do_openall(self, arg):
        """Opens all youtube links found by the search command. Empties stored urls after."""
        if len(self.links) == 0:
            print(colored("No links to open", "red", attrs=["bold"]))
            return
        for link in self.links:
            webbrowser.open(link, new=2)
            self.links.remove(link)

    def do_EOF(self, arg):
        """Quits the shell"""
        print(f"{Fore.RED}Goodbye{Style.RESET_ALL}")
        return True


if __name__ == '__main__':
    Terminal().cmdloop()
