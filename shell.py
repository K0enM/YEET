import cmd
import requests
import re
import webbrowser


class Terminal(cmd.Cmd):
    intro = "Welcome to the molenaar shell. Type help or ? to list commands"
    prompt = '[$] '
    links =[]

    def do_search(self, url):
        """search [url]
        Searches the given url for youtube links"""
        if url:
            if re.match(r"^(http|https)://", url):
                text = requests.get(url).text
                # matches = re.finditer(
                #     r"(?:https?://)?(?:www\.)?youtu\.?be(?:\.com)?/?.*(?:watch|embed)?(?:.*v=|v/|/)([\w-]{1,12})", text,
                #     re.MULTILINE | re.IGNORECASE)
                pattern = r"(http|https)://(www.youtube.com/watch[?]v=)(.{1,11})"
                matches = re.finditer(pattern, text)
                for num, match in enumerate(matches, start=1):
                    print("Match {num} was found at {start}--{end}: {match}".format(num=num, start=match.start(),
                                                                                    end=match.end(), match=match.group(0)))
                    self.links.append(match.group())
            else:
                print("Please enter a valid url starting with http:// or https://")
        else:
            print("Please enter a url")

    def do_open(self, url):
        """open [url]
        Opens the given url in the default browser"""
        if url:
            if re.match(r"^(http|https)://", url):
                webbrowser.open(url, new=2)
            else:
                print("Please enter a valid url starting with http:// or https://")
        else:
            print("Please enter a url")

    def do_openall(self, arg):
        """Opens all youtube links found by the search command. Empties stored urls after."""
        if len(self.links) == 0:
            print("No stored links to open")
            return
        for link in self.links:
            webbrowser.open(link, new=2)
            self.links.remove(link)

    def do_EOF(self, arg):
        """Quits the shell"""
        return True


if __name__ == '__main__':
    Terminal().cmdloop()
