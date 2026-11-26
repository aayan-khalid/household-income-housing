#!/usr/bin/env python3

'''
main.py
  Author(s): Aayan Yousuf, Evren Suer, Carl Asojo, Raaif Rizwan

  Project: Milestone III - Household income and housing costs
           across Canadian provinces

  Functional Summary
      Lets the user choose which of the three questions to run:

        Q1  Do households with more people have higher incomes?
              (question1.py - income file)
        Q2  Which provinces have the highest median monthly housing costs?
              (q2.py - housing cost file)
        Q3  Do provinces with higher incomes also have higher housing costs?
              (q3.py - BOTH files)

      Run with no arguments for a menu, or give the question on the
      command line:

        python3 main.py                              (menu)
        python3 main.py q1 Ontario [chart.png]
        python3 main.py q2 <total|owner|renter> <province|all>
        python3 main.py q3 <province> [<province> ...]
        python3 main.py q3 all
'''

import os
import sys

import question1
import q2
import q3

INCOME_FILE = "household_income.csv"
HOUSING_FILE = "housing_cost.csv"

ALL_PROVINCES = q2.PROVINCES


def run_q1(args):
    '''args = [province] or [province, chart file]'''

    if len(args) not in (1, 2):
        print("Usage: q1 <province> [chart file]", file=sys.stderr)
        sys.exit(1)
    question1.main(["question1.py", INCOME_FILE] + args)


def run_q2(args):
    '''args = [tenure, province or all]'''

    if len(args) != 2:
        print("Usage: q2 <total|owner|renter> <province|all>", file=sys.stderr)
        sys.exit(1)
    q2.main(["q2.py", HOUSING_FILE] + args)


def run_q3(args):
    '''args = list of provinces, or ["all"]'''

    if len(args) == 1 and args[0].lower() == "all":
        args = ALL_PROVINCES
    q3.main(["q3.py"] + args)


# menu choice -> (description, function)
QUESTIONS = {
    "1": ("Household size and income (one province)", run_q1),
    "2": ("Highest monthly housing costs (by tenure)", run_q2),
    "3": ("Income vs housing costs (uses BOTH files)", run_q3),
}


def get_question(text):
    '''Accept "1", "q1" or "Q1"; return "1", "2" or "3" (or None)'''

    text = text.strip().lower()
    if text.startswith("q"):
        text = text[1:]
    return text if text in QUESTIONS else None


def ask_for_arguments(choice):
    '''Menu mode: ask the user for the parameters of the chosen question'''

    if choice == "1":
        province = input("Province: ").strip()
        chart = input("Save a chart as (e.g. q1.png), or press Enter for none: ").strip()
        return [province] + ([chart] if chart else [])

    if choice == "2":
        tenure = input("Tenure (total, owner, renter): ").strip()
        province = input("Province, or all: ").strip()
        return [tenure, province]

    text = input("Provinces separated by commas, or all: ").strip()
    return [name.strip() for name in text.split(",") if name.strip()]


def run_menu():
    '''Keep showing the menu until the user quits'''

    while True:
        print()
        print("=" * 56)
        print(" Household income and housing costs - choose a question")
        print("=" * 56)
        for number in QUESTIONS:
            print("  {}  Q{}  {}".format(number, number, QUESTIONS[number][0]))
        print("  q  Quit")

        try:
            answer = input("\nYour choice: ").strip().lower()
        except EOFError:
            return

        if answer in ("q", "quit", "exit"):
            return

        choice = get_question(answer)
        if choice is None:
            print("Please enter 1, 2, 3 or q.", file=sys.stderr)
            continue

        try:
            QUESTIONS[choice][1](ask_for_arguments(choice))
        except SystemExit:
            # a question reported an error: go back to the menu instead of quitting
            print("\n(returning to the menu)")
        except EOFError:
            return


def main(argv):

    # the data files are looked up next to this script, wherever we run from
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    if len(argv) == 1:
        run_menu()
        return

    if argv[1] in ("--help", "-h"):
        print(__doc__)
        return

    choice = get_question(argv[1])
    if choice is None:
        print("Unknown question '{}'.  Use q1, q2 or q3.".format(argv[1]),
                file=sys.stderr)
        print("Run  python3 main.py --help  for examples.", file=sys.stderr)
        sys.exit(1)

    QUESTIONS[choice][1](argv[2:])


if __name__ == "__main__":
    main(sys.argv)
