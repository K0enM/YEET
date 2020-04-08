import cmd
import requests
import re


class Terminal(cmd.Cmd):
    intro = 'Welcome to the molenaar shell. Type help or ? to list commands'
    prompt = '[$] '

    def do_search(self, url):
        """search [url]
        search the given url for youtube links"""
        if url:
            prog = re.compile('^(http|https)://')
            if prog.match(url):
                text = requests.get(url).text
                matches = re.finditer(
                    r"(?:https?://)?(?:www\.)?youtu\.?be(?:\.com)?/?.*(?:watch|embed)?(?:.*v=|v/|/)([\w-]+)", text,
                    re.MULTILINE | re.IGNORECASE)
                for num, match in enumerate(matches, start=1):
                    print("Match {num} was found at {start}--{end}: {match}".format(num=num, start=match.start(),
                                                                                    end=match.end(), match=match))
            else:
                print("please enter a valid url starting with http:// or https://")
        else:
            print("please enter a url")

    def do_EOF(self, arg):
        """quits the shell"""
        return True


if __name__ == '__main__':
    Terminal().cmdloop()
