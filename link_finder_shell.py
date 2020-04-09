import cmd
import requests
import re
import webbrowser
from colorama import Fore, Style
import validators


class Terminal(cmd.Cmd):
    intro = "Welcome to the molenaar shell. Type help or ? to list commands"
    prompt = f'{Fore.MAGENTA}[$] {Style.RESET_ALL}'
    links = []

    def do_search_channel(self, url):
        """search [url]
        Searches the given url for youtube channel links"""
        if url:
            if re.match(r"^(http|https)://", url):
                text = requests.get(url).text
                pattern = r"(?:https?://)?(?:www\.)?youtu\.?be(?:\.com)?/?(.{1,7})(?:watch|embed)?(?:.*v=|v/|/)([\w-]{1,24})"
                matches = re.finditer(pattern, text, re.MULTILINE | re.IGNORECASE)
                for num, match in enumerate(matches, start=1):
                    print("{green} Match {num} was found at {start}--{end}: {match} {reset}".format(green=Fore.GREEN,
                                                                                                    num=num,
                                                                                                    start=match.start(),
                                                                                                    end=match.end(),
                                                                                                    match=match.group(
                                                                                                        0),
                                                                                                    reset=Style.RESET_ALL))
                    self.links.append(match.group())
                    self.links = [i for n, i in enumerate(self.links) if i not in self.links[:n]]
            else:
                print(f"{Fore.RED}Please enter a valid url starting with http:// or https://{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Please enter a url{Style.RESET_ALL}")

    def do_search_video(self, url):
        """search [url]
        Searches the given url for youtube channel links"""
        if url:
            if re.match(r"^(http|https)://", url):
                text = requests.get(url).text
                pattern = r"(?:https?://)?(?:www\.)?youtu\.?be(?:\.com)?/(?:watch|embed)?(?:.*v=|v/|/)([\w-]{1,11})"
                matches = re.finditer(pattern, text, re.MULTILINE | re.IGNORECASE)
                for num, match in enumerate(matches, start=1):
                    print("{green} Match {num} was found at {start}--{end}: {match} {reset}".format(green=Fore.GREEN,
                                                                                                    num=num,
                                                                                                    start=match.start(),
                                                                                                    end=match.end(),
                                                                                                    match=match.group(
                                                                                                    ),
                                                                                                    reset=Style.RESET_ALL))
                    self.links.append(match.group())
                    self.links = [i for n, i in enumerate(self.links) if i not in self.links[:n]]
            else:
                print(f"{Fore.RED}Please enter a valid url starting with http:// or https://{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Please enter a url{Style.RESET_ALL}")

    def do_open(self, url):
        """open [url]
        Opens the given url in the default browser"""
        if url:
            if re.match(r"^(http|https)://", url):
                webbrowser.open(url, new=2)
            else:
                print(f"{Fore.RED}Please enter a valid url starting with http:// or https://{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Please enter a url{Style.RESET_ALL}")

    def do_openall(self, arg):
        """Opens all youtube links found by the search command. Empties stored urls after."""
        if len(self.links) == 0:
            print(f"{Fore.YELLOW}No links to open{Style.RESET_ALL}")
            return
        for link in self.links:
            webbrowser.open(link, new=2)
            self.links.remove(link)

    def do_show(self, arg):
        """Shows all stored matches"""
        if len(self.links) == 0:
            print(f"{Fore.BLUE}No matches stored{Style.RESET_ALL}")
        for link in self.links:
            print(f"{Fore.BLUE}Match: {link} - ID: {self.links.index(link)}{Style.RESET_ALL}")

    def do_delete_match(self, arg):
        """Deletes a certain match from the stored list of matches"""
        if arg:
            for link in self.links:
                if self.links.index(link) == int(arg):
                    print(f"{Fore.CYAN}Deleting match {link} with ID {arg}{Style.RESET_ALL}")
                    self.links.remove(link)
        else:
            print(f"{Fore.RED}Please enter a match{Style.RESET_ALL}")

    def do_clean(self, arg):
        """Cleans stored list of matches by removing non url matches"""
        for link in self.links:
            if not validators.url(link):
                self.do_delete_match(self.links.index(link))
        print(f"{Fore.GREEN}Done cleaning list{Style.RESET_ALL}")

    def do_EOF(self, arg):
        """Quits the shell"""
        print(f"{Fore.RED}Goodbye{Style.RESET_ALL}")
        return True


if __name__ == '__main__':
    Terminal().cmdloop()
