#!/usr/bin/env python3

'''
question1.py
  Author(s): Aayan Yousuf, Evren Suer, Carl Asojo, Raaif Rizwan

  Project: Milestone II - Household income and housing costs
  Question 1: Do households with more people have higher incomes?

  Functional Summary
      Reads the household income CSV, finds the median income for
      1-4 person households in ONE province, and prints how much the
      income changes with each extra person.  Optionally saves a bar
      chart of the result.

     Commandline Parameters: 2 or 3
        argv[1] = household income CSV file
        argv[2] = province name
        argv[3] = (optional) graphics file to create, e.g. q1.png
'''

import sys
import csv
from matplotlib import pyplot as plt

# rows of the file: province names, household sizes, incomes
PROVINCE_ROW, SIZE_ROW, INCOME_ROW = 0, 1, 2


def read_income_file(filename):
    '''Return { province: { household size: median income } }'''

    try:
        income_fh = open(filename, encoding="utf-8-sig")
    except IOError as err:
        print("Unable to open '{}' : {}".format(filename, err), file=sys.stderr)
        sys.exit(1)

    rows = list(csv.reader(income_fh))
    income_fh.close()

    if len(rows) <= INCOME_ROW:
        print("'{}' needs at least 3 rows".format(filename), file=sys.stderr)
        sys.exit(1)

    income_by_province = {}
    province = ""

    # column 0 only has row labels, so start at column 1
    for col in range(1, len(rows[INCOME_ROW])):

        # province names are merged cells: only the first column of each
        # group has a name, so keep the last one we saw
        if rows[PROVINCE_ROW][col] != "":
            province = rows[PROVINCE_ROW][col]

        first_word = rows[SIZE_ROW][col].split()[0] if rows[SIZE_ROW][col] else ""

        # each province also has a "Total" (all sizes) column, not used for Q1
        if first_word == "Total":
            continue

        try:
            size = int(first_word)                        # "2 persons" -> 2
            income = int(rows[INCOME_ROW][col])
        except ValueError as err:
            print("Bad value in column {}: {}".format(col, err), file=sys.stderr)
            sys.exit(1)

        income_by_province.setdefault(province, {})[size] = income

    return income_by_province


def find_province(requested, income_by_province):
    '''Match the province ignoring case; exit with a list if not found'''

    for name in income_by_province:
        if name.lower() == requested.lower():
            return name

    print("Unknown province '{}'.  Choose one of:".format(requested),
            file=sys.stderr)
    print("   ", "\n    ".join(income_by_province), file=sys.stderr)
    sys.exit(1)


def calculate_changes(income_by_size):
    '''Return (size, income, $ change, % change) for each household size'''

    results = []
    previous = None

    for size in sorted(income_by_size):
        income = income_by_size[size]
        if previous is None:
            results.append((size, income, None, None))
        else:
            results.append((size, income, income - previous,
                            100.0 * (income - previous) / previous))
        previous = income

    return results


def print_table(province, results):
    '''Print the results as a table'''

    print("\nMedian household income by household size: " + province + "\n")
    print("{:<12}{:>12}{:>12}{:>10}".format(
            "Size", "Income ($)", "Change ($)", "Change %"))

    for size, income, dollars, percent in results:
        if dollars is None:
            change = "{:>12}{:>10}".format("-", "-")
        else:
            change = "{:>12,}{:>9.0f}%".format(dollars, percent)
        print("{:<12}{:>12,}{}".format("{} person(s)".format(size), income, change))


def create_plot(province, results, graphics_filename):
    '''Save a bar chart of income vs. household size'''

    fig = plt.figure()
    plt.bar([str(r[0]) for r in results], [r[1] for r in results],
            color="#3DB9D3")
    plt.title("Median household income by household size: " + province)
    plt.xlabel("Number of people in household")
    plt.ylabel("Median income ($)")
    fig.savefig(graphics_filename, bbox_inches="tight")
    plt.close(fig)


def main(argv):

    if len(argv) not in (3, 4):
        print("Usage: question1.py <income file> <province> [graphics file]",
                file=sys.stderr)
        sys.exit(1)

    graphics_filename = argv[3] if len(argv) == 4 else None

    print("=" * 56)
    print("Question selected : Q1 - Household size and income")
    print("Parameters        : file = {}, province = {}, chart = {}".format(
            argv[1], argv[2], graphics_filename))
    print("=" * 56)

    print("Step 1: reading", argv[1])
    income_by_province = read_income_file(argv[1])

    province = find_province(argv[2], income_by_province)
    print("Step 2: using province '{}'".format(province))

    print("Step 3: calculating income change per extra person")
    results = calculate_changes(income_by_province[province])
    print_table(province, results)

    if graphics_filename is not None:
        print("\nStep 4: saving chart to", graphics_filename)
        create_plot(province, results, graphics_filename)


if __name__ == "__main__":
    main(sys.argv)
