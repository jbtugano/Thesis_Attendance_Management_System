name = input("Please enter your name: ")
std_number = input("Please enter your student number: ")
x = std_number.split("-")[-1]
y = name.split(" ")[-1]

print(f"{y}{x}")

#input
# andrew tapawan escandor
# 2015 - 2 - 01350

#expected output
#escandor01350
