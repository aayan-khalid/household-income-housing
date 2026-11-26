'''
q2.py
  Author(s): Aayan Yousuf, Evren Suer, Carl Asojo, Raaif Rizwan

  Project: Milestone III - Household income and housing costs
  Question 2: Which provinces have the highest median monthly housing costs?

  Functional Summary
      Reads the housing cost CSV file, finds the median monthly shelter
      cost for the chosen tenure (total, owner or renter) in one province
      or in all provinces/territories, ranks them from highest to lowest,
      prints the ranking and shows it as a bar chart.

     Commandline Parameters: 3  (or --help / interactive)
        argv[1] = housing cost CSV file
        argv[2] = tenure: total, owner or renter
        argv[3] = province name, or "all"

  Design note (from the original author):
      A --help option and an "interactive" mode were added so that a user
      who is not a computer expert can still use the software.
'''
import csv
import sys
import matplotlib.pyplot as plt

# List of Canadian provinces and territories so the user can select one
PROVINCES = [
    "Newfoundland and Labrador",
    "Prince Edward Island",
    "Nova Scotia",
    "New Brunswick",
    "Quebec",
    "Ontario",
    "Manitoba",
    "Saskatchewan",
    "Alberta",
    "British Columbia",
    "Yukon",
    "Northwest Territories",
    "Nunavut"
]

TENURES = ["total", "owner", "renter"]


def print_help():
    print("Housing Cost Comparison")
    print("Normal mode:      python3 q2.py housing_cost.csv total all")
    print("Interactive mode: python3 q2.py interactive")


def find_province(province_choice):
    '''Match the province ignoring case; exit with an error if not found'''

    for province in PROVINCES:
        if province.lower() == province_choice.lower():
            return province

    print("Invalid province name '{}'.  Choose one of:".format(province_choice),
            file=sys.stderr)
    print("   ", "\n    ".join(PROVINCES), file=sys.stderr)
    sys.exit(1)


def read_costs(filename, tenure, province_choice):
    '''
    Return a list of (province, median monthly shelter cost) for the
    chosen tenure.  The file has three rows we care about:
        "Geography"           province names (merged cells, so blanks follow)
        "Tenure ..."          Total / Owner / Renter for each province
        "Median shelter cost" the number we want
    '''

    try:
        with open(filename, "r", encoding="utf-8-sig", newline="") as file:
            rows = list(csv.reader(file))
    except IOError as err:
        print("Unable to open '{}' : {}".format(filename, err), file=sys.stderr)
        sys.exit(1)

    # Find the three rows by the label in their first column
    geography_row = []
    tenure_row = []
    median_row = []

    for row in rows:
        if len(row) > 0:
            if row[0] == "Geography" and geography_row == []:
                geography_row = row
            elif row[0].startswith("Tenure") and tenure_row == []:
                tenure_row = row
            elif row[0] == "Median shelter cost" and median_row == []:
                median_row = row

    if len(geography_row) == 0 or len(tenure_row) == 0 or len(median_row) == 0:
        print("Could not find the required data in '{}'.".format(filename),
                file=sys.stderr)
        sys.exit(1)

    province_costs = []
    geography = ""

    # column 0 only has row labels, so start at column 1
    for column in range(1, len(geography_row)):

        # province names are merged cells: keep the last one we saw
        if geography_row[column].strip() != "":
            geography = geography_row[column].strip()

            # Remove the Statistics Canada footnote marker, e.g. "Canada i1"
            geography = geography.rsplit(" i", 1)[0]

        # Only look at provinces/territories
        if geography not in PROVINCES:
            continue

        # Only look at the province the user asked for
        if province_choice != "all" and geography != province_choice:
            continue

        # Only look at the column for the chosen tenure
        if not tenure_row[column].strip().lower().startswith(tenure):
            continue

        try:
            cost = median_row[column].replace(",", "").replace("$", "")
            province_costs.append((geography, float(cost)))
        except (ValueError, IndexError):
            continue

    return province_costs


def get_cost(item):
    return item[1]


def show_chart(province_costs, tenure):
    '''Bar chart of the ranked shelter costs'''

    names = [item[0] for item in province_costs]
    costs = [item[1] for item in province_costs]

    plt.figure()
    bars = plt.bar(names, costs, color="#3DB9D3")
    plt.bar_label(bars, labels=["${:,.0f}".format(c) for c in costs], fontsize=7)

    plt.suptitle("Median Monthly Shelter Cost by Province/Territory ({})".format(
            tenure.title()), weight="bold", fontsize=12)
    plt.xlabel("Province/Territory", weight="bold", fontsize=10)
    plt.ylabel("Median monthly shelter cost (CAD $)", weight="bold", fontsize=10)
    plt.grid(axis="y", color="#cccbcb97")
    plt.gca().set_axisbelow(True)
    plt.xticks(rotation=30, ha="right", fontsize=7)
    plt.tight_layout()
    plt.show()


def main(argv):

    # Work out the three parameters: file, tenure, province
    if len(argv) == 2 and argv[1] in ("--help", "-h"):
        print_help()
        return

    if len(argv) == 2 and argv[1].lower() == "interactive":
        filename = input("Enter CSV filename: ")
        tenure = input("Choose tenure (total, owner, renter): ").lower()
        province_choice = input("Choose province or all: ").lower()

    elif len(argv) == 4:
        filename = argv[1]
        tenure = argv[2].lower()
        province_choice = argv[3].lower()

    else:
        print("Usage: q2.py <housing file> <tenure> <province or all>",
                file=sys.stderr)
        print("Invalid command.  Use --help for help.", file=sys.stderr)
        sys.exit(1)

    if tenure not in TENURES:
        print("Invalid tenure.  Choose total, owner or renter.", file=sys.stderr)
        sys.exit(1)

    if province_choice != "all":
        province_choice = find_province(province_choice)

    print("=" * 56)
    print("Question selected : Q2 - Highest monthly housing costs")
    print("Parameters        : file = {}, tenure = {}, province = {}".format(
            filename, tenure, province_choice))
    print("=" * 56)

    province_costs = read_costs(filename, tenure, province_choice)

    # Sort provinces from highest to lowest shelter cost
    province_costs.sort(key=get_cost, reverse=True)

    if len(province_costs) == 0:
        print("No data found.", file=sys.stderr)
        sys.exit(1)

    print("\nMedian Monthly Shelter Costs")
    print("Tenure:", tenure.title())
    print("--------------------------------")

    for rank, item in enumerate(province_costs, start=1):
        print(rank, item[0], "$" + format(item[1], ",.0f"))

    show_chart(province_costs, tenure)


if __name__ == "__main__":
    main(sys.argv)
