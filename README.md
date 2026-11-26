Test Cases

Main Menu (main.py)

Help: python3 main.py --help -> Shows help text.

Menu: python3 main.py -> Opens the menu; typing q quits.

Invalid question: python3 main.py q9 -> Prints an unknown question error.

Question 1 (question1.py)

Valid province: python3 main.py q1 Ontario -> Prints Ontario's income table by household size.

Save chart: python3 main.py q1 Ontario q1.png -> Prints the table and saves q1.png.

Invalid province: python3 main.py q1 Gotham -> Prints an unknown province error.

Question 2 (q2.py)

All provinces (total): python3 main.py q2 total all -> Ranks all provinces and shows a bar chart.

Single province (renter): python3 main.py q2 renter Alberta -> Shows Alberta's renter housing cost and chart.

Invalid tenure: python3 main.py q2 mortgage all -> Prints an invalid tenure error.

Question 3 (q3.py)

All provinces: python3 main.py q3 all -> Prints income vs. housing cost table and chart for all provinces.

Selected provinces: python3 main.py q3 Ontario Quebec -> Prints comparison table and chart for Ontario and Quebec.

No provinces: python3 main.py q3 -> Prints a usage error.
