"""Main module with the implementation of Smallsource command-line console."""

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit import HTML, print_formatted_text
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory


from storage_interface import create_connection, select_all_ecosystems

connection = create_connection("../workdir/smallsource.db")


def welcome_message():
    """Print the welcome message to terminal."""
    print_formatted_text()
    print_formatted_text(HTML('<ansired>Smallsource version 0.1</ansired>'))
    print_formatted_text()
    print_formatted_text(HTML('type <blue>quit</blue> or <blue>exit</blue> to exit'))
    print_formatted_text(HTML('type <blue>help</blue> for on-line help'))
    print_formatted_text(HTML('type <blue>info</blue> for the current configuration'))
    print_formatted_text(HTML('type <blue>version</blue> for information about the current ' +
                              '<ansired>Smallsource</ansired> version'))
    print_formatted_text()


def show_help():
    """Show main help page."""
    print_formatted_text("""Help
--------
quit - quit this application
exit - exit from this application
eval - evaluate
""")


def bottom_toolbar():
    """Prepare a text that needs to be displayed on bottom toolbar (status line)."""
    return HTML("Storage: <ansired>none</ansired>   Message broker: <ansired>none</ansired>")


def repl():
    """Start an interactive REPL."""
    c = WordCompleter(["quit", "exit", "help", "ecosystems"], ignore_case=True)
    s = PromptSession(completer=c, auto_suggest=AutoSuggestFromHistory(),
                      bottom_toolbar=bottom_toolbar)

    while True:
        cmd = s.prompt("> ")
        if cmd in {"q", "quit", "Quit", "exit", "Exit"}:
            break
        elif cmd in {"help", "Help", "?"}:
            show_help()
        elif cmd == "ecosystems":
            ecosystems = select_all_ecosystems(connection)
            print_formatted_text(HTML('<ansired>List of ecosystems</ansired>'))
            for ecosystem in ecosystems:
                print_formatted_text(HTML('<darkblue>{}</darkblue>').format(ecosystem))


welcome_message()
repl()
