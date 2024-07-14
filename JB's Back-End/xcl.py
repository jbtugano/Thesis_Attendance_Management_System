import pandas as pd


excel_path = "PATHFIT4-SCHEDULE-2ND-SEM-AY-2023-2024.xlsx"

df = pd.read_excel(excel_path)
column_length = len(df.columns)

#col 0 = Faculty
#col 1 = Day
#col 2 = Time
#col 3 = Section
#col 4 = Subject Code
#col 5 = Activity
#col 6 = Room


def process_time(trange):
    fixed_time = []
    separate_time = trange.split("-")

    start_time = separate_time[0].split(":")[0]
    if 7 <= int(start_time) <= 11:
        fixed_time.append(f"{separate_time[0]}AM")
    else:
        fixed_time.append(f"{separate_time[0]}PM")

    end_time = separate_time[1].split(":")[0]

    if 1 <= int(end_time) <= 8 or int(end_time) == 12:
        fixed_time.append(f"{separate_time[1]}PM")
    else:
        fixed_time.append(f"{separate_time[1]}AM")

    final_time = "-".join(fixed_time)
    return [final_time, separate_time[0], separate_time[1]]


#for i in range(len(df)):

    #for column in range(column_length):
        #print(df.iloc[i, column], end=" ")



    # if prof not in faculty db, ask admin to register them first
    # add
    # if activity not in activity db, add it

sections = {
    'section' : []
}
for index, row in df.iterrows():

    print(process_time(row["TIME"]))
    x = row["SECTION"].split("/")
    for sec in x:
        if sec.lstrip() not in sections['section']:
            sections['section'].append(sec.lstrip())

print(sections)


