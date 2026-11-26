'''
q3.py
  Author(s): Aayan Yousuf, Evren Suer, Carl Asojo, Raaif Rizwan

  Project: Milestone III - Household income and housing costs
  Question 3: Do provinces with higher incomes also have higher housing costs?

  Functional Summary
      Reads the household income and housing cost CSV files, 
      finds the total median income and total median housing 
      cost for all inputed provinces, and graphs the 
      percentage of income going to housing in each province.

  Formula
    percentage = ((monthly_housing_cost * 12) / (yearly_income)) * 100

     Commandline Parameters: <=13
        argv[x] = names of provinces
'''
import sys
import csv
import matplotlib.pyplot as plt

# rows of the both files: province names, household sizes / tenant type, incomes / shelter cost
PROVINCE_ROW, SIZE_ROW, INCOME_ROW = 0, 1, 2

INCOME_FILENAME = "household_income.csv"
HOUSING_FILENAME = "housing_cost.csv"


def read_file(filename):
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

        try:
            size = rows[SIZE_ROW][col].split()[0]    # "2 persons" -> 2
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


def main(argv):

    if len(argv) < 2:
        print("Usage: q3.py <province> [<province> ...]", file=sys.stderr)
        sys.exit(1)

    if len(argv)>14:    # 13 provinces and territories + 1 for program
        print("Too many arguments (only 13 provinces): q3.py <province>", file=sys.stderr)
        sys.exit(1)

    print("=" * 56)
    print("Question selected : Q3 - Income vs housing costs")
    print("Parameters        : provinces = {}".format(", ".join(argv[1:])))
    print("=" * 56)

    #opening and parsing both files
    income_list = read_file(INCOME_FILENAME)
    housing_list = read_file(HOUSING_FILENAME)

    q3(income_list,housing_list,argv)


def print_table(provinces, incomes, costs, percentages):
    '''Print the matched data from both files'''

    print("\n{:<28}{:>14}{:>16}{:>12}".format(
            "Province", "Income ($/yr)", "Housing ($/mo)", "% of income"))
    for i in range(len(provinces)):
        print("{:<28}{:>14,}{:>16,}{:>11.1f}%".format(
                provinces[i], incomes[i], costs[i], percentages[i]))
    print()


#question 3 method
def q3(i_list, h_list, argv):
    percentages=[]#list for graphing percentages
    province_list=[]
    incomes=[]      #yearly median income of each province
    costs=[]        #monthly median housing cost of each province

    for i in range(1,len(argv)):
        province=""
        province = find_province(argv[i], i_list)
        find_province(argv[i], h_list)

        try:
            # median % of yearly income going towards yearly housing costs
            #((monthly_housing_cost * 12) / (yearly_income)) * 100
            delta = (100 * int(h_list[province]["Total"]) * 12) / (int(i_list[province]["Total"])) 

            percentages.append(delta)
            province_list.append(province)
            incomes.append(int(i_list[province]["Total"]))
            costs.append(int(h_list[province]["Total"]))

        except ZeroDivisionError as err:    #if division by zero
            print("Income cannot be 0 : {}".format(err), file=sys.stderr)
            sys.exit(1)


    print_table(province_list, incomes, costs, percentages)

    #adding title and labels to graph
    plt.suptitle("Percentage of Total Yearly Median Income Spent On Housing Costs In Canadian Provinces and Territories, 2020",weight='bold',wrap=True,fontsize=12)
    plt.xlabel("Selected Provinces and Territories",weight='bold',fontsize=10)
    plt.ylabel("(%) of income spent on housing",weight='bold',fontsize=10)


    #adding horizontal lines to the graph
    plt.grid(axis='y',color="#cccbcb97",)
    plt.gca().set_axisbelow(True)
    plt.ylim(6,20)  #vertically scaling the graph


    #adding data into graph
    plt.bar(province_list, percentages, width=0.4, color=["#246ec2"])

    #rotating and shrinking text to fit graph
    plt.xticks(rotation=30, ha="right",fontsize=6)  
    plt.yticks(fontsize=8)
    plt.tight_layout()

    plt.show()  #display graph
    

if __name__ == "__main__":
    main(sys.argv)
```[cite: 4]
