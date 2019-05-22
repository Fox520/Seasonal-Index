__author__ = "Lone Wolf"

# accuracy of this is program not tested
import csv
import datetime
# ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']

filename = "nmref.csv"
dates = []
closing_prices = []
quater_specific_closing = [] #y
quater_specific_time = []
end_quarter_dates = []
quartile_moving_average = []
centered_avg = []
percent_avg = []
mean_row = []
seasonal_index = []
merged_date_closing = {}
moving_average_amount = 4
ADJ_VAL = moving_average_amount * 100

#####DATE##########
counter_dates = 0
total_dates = 0
quarter_dates = []
all_quarters_dates = []

#####CLOSING###<- what we're interested in for now
counter_closing = 0
total_closing = 0
quarter_closing = []
all_quarters_closing = []

def get_data(filename):
    with open(filename, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader) # skipping column names
        for row in csv_reader:
            dates.append(row[0])
            closing_prices.append(row[4])


def set_dates():
    global total_dates
    global quarter_dates
    global all_quarters_dates
    global counter_dates
    for d in dates:
        # moving by 4 quarters
        if counter_dates == moving_average_amount:
            counter_dates = 0
            total_dates += 1
            all_quarters_dates.append(quarter_dates)
            quarter_dates = []
        else:
            counter_dates += 1
            datee = datetime.datetime.strptime(d, "%Y-%m-%d")
            quarter_dates.append(datee)

def set_closing_prices():
    global counter_closing
    global total_closing
    global quarter_closing
    global all_quarters_closing

    for c in closing_prices:
        if counter_closing == moving_average_amount:
            counter_closing = 0
            total_closing += 1
            all_quarters_closing.append(c)
            quarter_closing = []
        else:
            counter_closing += 1
            quarter_closing.append(c)

    set_closing_for_quarters()

def set_closing_for_quarters():
    global quater_specific_closing
    # get the quartile average closing price
    temp_counter = 0
    q_total = 0
    for c in closing_prices:
        if temp_counter == moving_average_amount:
            # get the average closing price
            quater_specific_closing.append(q_total/moving_average_amount)
            temp_counter = 0
            q_total = 0
        else:
            q_total += float(c)
            temp_counter += 1

def set_time_period():
    global quater_specific_time
    # organises the time to match the quarter closing price
    temp_counter = 0
    for d in dates:
        if temp_counter == moving_average_amount:
            # add only the last date
            quater_specific_time.append(d)
            temp_counter = 0
        else:
            temp_counter += 1

def set_end_quarter_period():
    global end_quarter_dates
    count = 0
    for i in quater_specific_time:
        if count == moving_average_amount-1:
            end_quarter_dates.append(i)
            count = 0
        else:
            count += 1

def merge_the_date_and_closing():
    global merged_date_closing
    for n,j in zip(dates, closing_prices):
        merged_date_closing[n] = j

def get_moving_average():
    global quartile_moving_average
    temp_total = 0
    origin = 0
    i = 0
    while i < len(quater_specific_closing):
        if (i != 0) and ((i % moving_average_amount) == 0):
            if (temp_total / moving_average_amount) != 0:
                # so we don't add zero's
                quartile_moving_average.append(temp_total / moving_average_amount)
            temp_total = 0
            i = origin + 1
            origin += 1
        else:
            temp_total += quater_specific_closing[i]
            i += 1

def get_centered_average():
    global centered_avg
    temp_total = 0
    origin = 0 # the one before
    i = 1
    while i < len(quartile_moving_average):
        centered_avg.append((quartile_moving_average[i] + quartile_moving_average[i-1]) / 2)
        i += 1

    return centered_avg

def get_percent_of_avg():
    global percent_avg
    origin = moving_average_amount - int(moving_average_amount/2) # the a pattern
    count = 0 # for the smaller list
    for i in range(len(quater_specific_closing)-moving_average_amount):
        # y/cent_ma * 100
        
        try:
            percent_avg.append((quater_specific_closing[origin] / centered_avg[count]) * 100)
        except:
            # count is out of bounds
            pass
        origin += 1
        count += 1

def get_mean_quarters():
    global mean_row
    # number in quarter (column)
    num = int(len(percent_avg) / moving_average_amount)
    count = 0
    for i in range(len(percent_avg)):
        # add the mean of current and previous
        if count == num-1:
            mean_row.append((percent_avg[i]+percent_avg[i-1]) / 2)
            count = 0
        else:
            count += 1

def do_adjustment():
    global seasonal_index
    x_adj_factor = ADJ_VAL/sum(mean_row)
    for i in mean_row:
        seasonal_index.append(i*x_adj_factor)

def print_nice():
    print('{:10s}'.format("Year/Month"), end="")
    for i in range(moving_average_amount):
        print('{:10s}'.format("Quarter "+str(i+1)), end="")
    print()
    for i in range(len(end_quarter_dates)):
        print('{:10s}'.format(end_quarter_dates[i]))
    
    print()
    for i in range(len(seasonal_index)):
        print('{:15f}'.format(seasonal_index[i]), end="")
    print()
get_data(filename)
set_dates()
set_closing_prices()
merge_the_date_and_closing()
set_time_period()
get_moving_average()
get_centered_average()
get_percent_of_avg()
get_mean_quarters()
do_adjustment()
set_end_quarter_period()
print_nice()