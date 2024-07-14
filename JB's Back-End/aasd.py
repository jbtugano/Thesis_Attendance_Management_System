file = "a.txt"
dicts = {
    "M": [],
    "T": [],
    "W": [],
    "TH": [],
    "F": [],
    "S": []
}
# planned processing, identifying if a class is AM/PM
with open(file, "r") as doc_file:
    next(doc_file) #skip header
    for line in doc_file:
        current_entry = line.strip().split(" ")
        timesched = current_entry[2].split("-")
        time_period = []
        for timea in timesched:
            #handle start time and end time differently.
            if 7 <= int(timea.split(":")[0]) <= 12:
                time_period.append(f"{timea}AM")
            else:
                time_period.append(f"{timea}PM")

        time_period = "-".join(time_period)
        print(time_period)

        dicts[current_entry[1]].append(f"{current_entry[0]} - {time_period}")
    #7-9
    #start time = 7 am
    #end time = 9am

    #5-7
    #start time = 5pm
    #end time = 7pm
for entry in dicts:
    print(f"{entry} - {dicts[entry]}")
    for indiv in dicts[entry]:
        if "GOYAL" in indiv:
            print("TRUE")