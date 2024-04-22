#%%

#############
# IMPORTS #
#############
import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
from scipy.stats import norm

################
# RESULTS FILE #
################

# results = "./2024-04-15-results.csv"
results = "/home/mooney/exjobb/layer-performance/analysis/2024-04-15-results.csv"
df = pd.read_csv(results)

print(df)

#######################################
# Array of all the names of the tests #
#######################################
test_array = [
    "javascript-mysql-app-adprocedure-1",
    "javascript-mysql-app-adprocedure-2",
    "javascript-mysql-app-adprocedure-3",
    "javascript-mysql-app-aggre-1",
    "javascript-mysql-app-aggre-2",
    "javascript-mysql-app-aggre-3",
    "javascript-mysql-app-filter-1",
    "javascript-mysql-app-filter-2",
    "javascript-mysql-app-filter-3",
    "javascript-mysql-app-procedure-1",
    "javascript-mysql-app-procedure-2",
    "javascript-mysql-app-procedure-3",
    "javascript-mysql-app-sort-1",
    "javascript-mysql-app-sort-2",
    "javascript-mysql-app-sort-3",
    "javascript-mysql-data-adprocedure-1",
    "javascript-mysql-data-adprocedure-2",
    "javascript-mysql-data-adprocedure-3",
    "javascript-mysql-data-aggre-1",
    "javascript-mysql-data-aggre-2",
    "javascript-mysql-data-aggre-3",
    "javascript-mysql-data-filter-1",
    "javascript-mysql-data-filter-2",
    "javascript-mysql-data-filter-3",
    "javascript-mysql-data-procedure-1",
    "javascript-mysql-data-procedure-2",
    "javascript-mysql-data-procedure-3",
    "javascript-mysql-data-sort-1",
    "javascript-mysql-data-sort-2",
    "javascript-mysql-data-sort-3",
    "php-mysql-app-adprocedure-1",
    "php-mysql-app-adprocedure-2",
    "php-mysql-app-adprocedure-3",
    "php-mysql-app-aggre-1",
    "php-mysql-app-aggre-2",
    "php-mysql-app-aggre-3",
    "php-mysql-app-filter-1",
    "php-mysql-app-filter-2",
    "php-mysql-app-filter-3",
    "php-mysql-app-procedure-1",
    "php-mysql-app-procedure-2",
    "php-mysql-app-procedure-3",
    "php-mysql-app-sort-1",
    "php-mysql-app-sort-2",
    "php-mysql-app-sort-3",
    "php-mysql-data-adprocedure-1",
    "php-mysql-data-adprocedure-2",
    "php-mysql-data-adprocedure-3",
    "php-mysql-data-aggre-1",
    "php-mysql-data-aggre-2",
    "php-mysql-data-aggre-3",
    "php-mysql-data-filter-1",
    "php-mysql-data-filter-2",
    "php-mysql-data-filter-3",
    "php-mysql-data-procedure-1",
    "php-mysql-data-procedure-2",
    "php-mysql-data-procedure-3",
    "php-mysql-data-sort-1",
    "php-mysql-data-sort-2",
    "php-mysql-data-sort-3",
    "python-mysql-app-adprocedure-1",
    "python-mysql-app-adprocedure-2",
    "python-mysql-app-adprocedure-3",
    "python-mysql-app-aggre-1",
    "python-mysql-app-aggre-2",
    "python-mysql-app-aggre-3",
    "python-mysql-app-filter-1",
    "python-mysql-app-filter-2",
    "python-mysql-app-filter-3",
    "python-mysql-app-procedure-1",
    "python-mysql-app-procedure-2",
    "python-mysql-app-procedure-3",
    "python-mysql-app-sort-1",
    "python-mysql-app-sort-2",
    "python-mysql-app-sort-3",
    "python-mysql-data-adprocedure-1",
    "python-mysql-data-adprocedure-2",
    "python-mysql-data-adprocedure-3",
    "python-mysql-data-aggre-1",
    "python-mysql-data-aggre-2",
    "python-mysql-data-aggre-3",
    "python-mysql-data-filter-1",
    "python-mysql-data-filter-2",
    "python-mysql-data-filter-3",
    "python-mysql-data-procedure-1",
    "python-mysql-data-procedure-2",
    "python-mysql-data-procedure-3",
    "python-mysql-data-sort-1",
    "python-mysql-data-sort-2",
    "python-mysql-data-sort-3"
]

#######################################
# Create CSV Reports                  #
#######################################

def create_report_csv(dataframe, name):

    # Extract data from the DataFrame
    test_names = dataframe.index.tolist()
    avg_times = dataframe.tolist()

    # Separate test names into components
    languages = []
    data_layers = []
    test_types = []
    datasets = []

    for test_name in test_names:
        parts = test_name.split("-")
        languages.append(parts[0])
        data_layers.append(parts[2])
        test_types.append(parts[3])
        datasets.append(int(parts[4]))

    # Group results by language and test type
    final_data = {}
    for i, test_name in enumerate(test_names): 
        language = languages[i]
        data_layer = data_layers[i]
        test_type = test_types[i]
        dataset = datasets[i]
        avg_time = avg_times[i]
        if (language, test_type) not in final_data:
            final_data[(language, test_type)] = {"data": [None] * 3, "app": [None] * 3}
        final_data[(language, test_type)][data_layer][dataset - 1] = avg_time

    # Unpack data for each language and test type
    csv_data = []
    for (language, test_type), results in final_data.items():
        #   test_name = test_names[languages.index(language) and test_types.index(test_type)]  # Find corresponding test name
        test_name = test_type
        data_layer_results = results["data"]
        app_layer_results = results["app"]
        csv_data.append([language, test_name, *data_layer_results, *app_layer_results])

    # Write data to CSV file
    with open(f'{name}.csv', "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Language", "Test Name", "Data Layer (Dataset 1)", "Data Layer (Dataset 2)", "Data Layer (Dataset 3)", "Application Layer (Dataset 1)", "Application Layer (Dataset 2)", "Application Layer (Dataset 3)"])
        writer.writerows(csv_data)

    print("CSV file created successfully!")

# # Compute average total time for each test
avg_total_time = df.groupby('Test')['Total Time'].mean()
avg_total_time.to_csv('total_time.csv')

std_total_time = df.groupby('Test')['Total Time'].std()
std_total_time.to_csv('std_total_time.csv')

print(avg_total_time)

avg_start_transfer = df.groupby('Test')['Start Transfer'].mean()
avg_start_transfer.to_csv('start_transfer.csv')

print(avg_start_transfer)

create_report_csv(avg_total_time, "total_time_table")
create_report_csv(avg_start_transfer, "start_transfer_table")
create_report_csv(std_total_time, "std_total_time_table")

#####################
# Graphs and Charts #
#####################

def create_charts(language, test):
    csv_results = pd.read_csv("./total_time.csv")

    # Filter the DataFrame for JavaScript data and app results for adprocedure
    data_test = csv_results[csv_results['Test'].str.contains(f'{language}-mysql-data-{test}')]
    app_test = csv_results[csv_results['Test'].str.contains(f'{language}-mysql-app-{test}')]

    # Extract the relevant data for plotting for test
    data_test_1 = data_test[data_test['Test'].str.endswith('-1')]
    app_test_1 = app_test[app_test['Test'].str.endswith('-1')]
    data_test_2 = data_test[data_test['Test'].str.endswith('-2')]
    app_test_2 = app_test[app_test['Test'].str.endswith('-2')]
    data_test_3 = data_test[data_test['Test'].str.endswith('-3')]
    app_test_3 = app_test[app_test['Test'].str.endswith('-3')]

    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))

    # Bar graph for data vs app - adprocedure Test 1
    ax.bar([1, 2], [data_test_1['Total Time'].iloc[0], app_test_1['Total Time'].iloc[0]], width=1, tick_label=['Data', 'App'], color=['blue', 'red'], alpha=0.7, label=f'{test} Test 1')

    # Bar graph for data vs app - adprocedure Test 2
    ax.bar([4, 5], [data_test_2['Total Time'].iloc[0], app_test_2['Total Time'].iloc[0]], width=1, tick_label=['Data', 'App'], color=['blue', 'red'], alpha=0.7, label=f'{test} Test 2')

    # Bar graph for data vs app - adprocedure Test 3
    ax.bar([7, 8], [data_test_3['Total Time'].iloc[0], app_test_3['Total Time'].iloc[0]], width=1, tick_label=['Data', 'App'], color=['blue', 'red'], alpha=0.7, label=f'{test} Test 3')

    # Superimposed lines for data and app results for adprocedure
    ax.plot([1.2, 4.2], [data_test_1['Total Time'].iloc[0], data_test_2['Total Time'].iloc[0]], color='blue', linestyle='-', label='Line Data 1 to Data 2')
    ax.plot([1.4, 4.4], [app_test_1['Total Time'].iloc[0], app_test_2['Total Time'].iloc[0]], color='red', linestyle='-', label='Line App 1 to App 2')

    ax.plot([4.2, 7.2], [data_test_2['Total Time'].iloc[0], data_test_3['Total Time'].iloc[0]], color='blue', linestyle='-', label='Line Data 2 to Data 3')
    ax.plot([4.4, 7.4], [app_test_2['Total Time'].iloc[0], app_test_3['Total Time'].iloc[0]], color='red', linestyle='-', label='Line App 2 to App 3')

    # Show legend
    # ax.legend()

    # Set labels and title
    ax.set_ylabel('Total Time (s)')
    ax.set_title(f'Performance Comparison between Data and App Layers for {test} in {language}')

    plt.xticks([1.5, 4.5, 7.5], ['Dataset 1', 'Dataset 2', 'Dataset 3'])

    plt.tight_layout()
    plt.show()

languages = ['javascript', 'python', 'php']
tests = ['adprocedure', 'aggre', 'filter', 'procedure', 'sort']

for test in tests:
    for language in languages:
        create_charts(language, test)

#####################
# COMPARE LANGUAGES #
#####################



# # Select data for one test (for example, test number 1)
# test_data = df[df['Test'] == test_array[8]]['Total Time']
# print(test_data)
# # Calculate mean and standard deviation
# mean = test_data.mean()
# std_dev = test_data.std()

# # Plot histogram
# plt.hist(test_data, bins=15, density=True, alpha=0.6, color='g', edgecolor='black')

# # Plot normal distribution curve
# xmin, xmax = plt.xlim()
# x = np.linspace(xmin, xmax, 100)
# p = norm.pdf(x, mean, std_dev)
# plt.plot(x, p, 'k', linewidth=2)

# # Add labels and title
# plt.xlabel('Total Time')
# plt.ylabel('Frequency')
# plt.title('Normal Distribution for Test 1')

# # Show plot
# plt.show()

