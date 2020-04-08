import cmd


class Terminal(cmd.Cmd):
    intro = 'Welcome to the molenaar shell. Type help or ? to list commands'
    prompt = '[$] '

    def do_test(self, arg):
        'Prints test'
        print("Test")


if __name__ == '__main__':
    Terminal().cmdloop()
