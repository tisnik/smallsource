from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit import print_formatted_text as print, HTML

from storage_interface import create_connection, select_all_ecosystems

connection = create_connection("../workdir/smallsource.db")


def welcome_message():
    print()
    print(HTML('<ansired>Smallsource version 0.1</ansired>'))
    print()
    print(HTML('type <blue>quit</blue> or <blue>exit</blue> to exit'))
    print(HTML('type <blue>help</blue> for on-line help'))
    print(HTML('type <blue>info</blue> for the current configuration'))
    print(HTML('type <blue>version</blue> for information about the current ' +
               '<ansired>Smallsource</ansired> version'))
    print()


def show_help():
    print("""Help
--------
quit - quit this application
exit - exit from this application
eval - evaluate
""")


def repl():
    c = WordCompleter(["quit", "exit", "help", "ecosystems"], ignore_case=True)
    s = PromptSession(completer=c)

    while True:
        cmd = s.prompt("> ")
        if cmd in {"q", "quit", "Quit", "exit", "Exit"}:
            break
        elif cmd in {"help", "Help", "?"}:
            show_help()
        elif cmd == "ecosystems":
            ecosystems = select_all_ecosystems(connection)
            print(HTML('<ansired>List of ecosystems</ansired>'))
            for ecosystem in ecosystems:
                print(HTML('<darkblue>{}</darkblue>').format(ecosystem))


welcome_message()
repl()
