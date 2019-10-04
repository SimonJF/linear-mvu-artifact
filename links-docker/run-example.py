#!/usr/bin/env python3
import sys
import subprocess

# List of examples

# Examples from the paper
paper_examples = \
    [
        ("examples/paper-examples/label.links",
         "Box and label"),
        ("examples/paper-examples/mouse.links",
         "Subscriptions (mouse movements)"),
        ("examples/paper-examples/commands.links",
         "Commands (long-running computations)")
    ]

caught_errors = \
    [
        ("examples/caught-errors/communication-mismatch.links",
         "Communication mismatch"),
        ("examples/caught-errors/linearity-violation.links",
         "Linearity violation"),
        ("examples/caught-errors/erroneous-discard.links",
         "Erroneously discarding a linear channel")
    ]

examples = \
    [
        (paper_examples, "Examples from the paper"),
        (caught_errors, "Errors caught by session types"),
    ]

all_examples = \
    [ (filename, description)
        for (example_list, description) in examples
            for (filename, description) in example_list]

def show_examples():
    index = 1
    for example_list, list_description in examples:
        print("=== %s ===" % (list_description))
        for (filename, example_description) in example_list:
            print("%s. %s" %(index, example_description))
            index = index + 1
        print()

def run_example(filename):
    print("File contents:")
    subprocess.call(["cat", filename])
    subprocess.call(["./links/links", "--config=config", filename])

def get_filename():
    while True:
        idx = input("Enter example number > ")
        try:
            index = int(idx)
            list_index = index - 1
            if list_index < 0 or list_index > (len(all_examples) - 1):
                print("Invalid example ID.")
            else:
                return all_examples[list_index][0]
        except ValueError:
            print("Invalid index.")

def main():
    # Example file: run directly
    if len(sys.argv) > 1:
        run_example(sys.argv[1])
        sys.exit(0)

    # Otherwise, interactive mode
    show_examples()
    print("Note that for the paper examples, you must " + \
          "navigate to http://localhost:8080 in your browser, and press Ctrl-C to exit.")
    filename = get_filename()
    run_example(filename)


if __name__ == "__main__":
    main()
