import pandas as pd
from matplotlib import pyplot as plt

# import dataframe
df = pd.read_csv("./Dataset/energy_consuption.csv")

# |--- FEATURE SELECTION - SCRUBBING ---|

# filters out every country but Australia using boolean indexing
# filters out YEAR 2011 to 2021 - YEAR >= 2011 and <= 2021
# remove irrelevant features as vectors

df = df[df["COUNTRY"] == "Australia"]  # using logical operators in pandas df functions
df = df[(df["YEAR"] >= 2011) & (df["YEAR"] <= 2021)]  # using pandas operators within a boolean index
del df["DISPLAY_ORDER"]
del df["CODE_TIME"]
del df["TIME"]
del df["share"]
del df["COUNTRY"]

# remove any unuseful variable features that could hinder the expected prediction
# we do not want to include "Stored" or "Lost" or "Produced" energy. Even any duplicates.
# create a list of irrelevant variable features

exclude = ["Distribution losses",
           "Used for pumped storage",
           "Electricity supplied",
           "Net electricity production",
           "Total combustible fuels",
           "Final consumption",
           "Others",  # vague feature
           "Low carbon",  # Same as renewables
           "Non-renewables"  # Same as Fossil Fuels
           ]

# drop rows containing variables listed in "exclude"
# Tilde is a negation operator. This will exclude rows containing variables in "exclude" from PRODUCT
# isin() check if the df has a particular value - so make FALSE IF exclude IS IN PRODUCT
df = df[~df["PRODUCT"].isin(exclude)]


# aggregate feature variables into two relevant categories; Renewables and Fossil Fuels
# aggregation will essentially combine related variables, apply them to a single category, then find the sum.
map_features = {
    "Hydro": "Renewables",
    "Wind": "Renewables",
    "Solar": "Renewables",
    "Geothermal": "Renewables",
    "Combustible renewables": "Renewables",
    "Other renewables aggregated": "Renewables",
    "Coal": "Fossil Fuels",
    "Oil": "Fossil Fuels",
    "Natural Gas": "Fossil Fuels",
}

# Mapping variables into "PRODUCT"
# map() will transform variables within the PRODUCT feature to align with "map_features"
# df["TYPE"] is creating a new feature with these variables, it removes "PRODUCT" entirely
df["TYPE"] = df["PRODUCT"].map(map_features)


# prepare for aggregation by defining aggregation rules
aggregation = {
    "VALUE": "sum",     # The values in the "VALUE" feature should be summed up  (e.g. Coal + Oil + Natural Gas)
    "yearToDate": "last",  # "last" will take the known value of the previous month and add as a cumulative sum
    "previousYearToDate": "sum"  # The values in the "previousYearToDate" feature should be summed up
}

# group non-aggregated features and aggregate then apply aggregation to perform operations (sums, last)
# Aggregation is applied to the remaining features in "aggregation" above
df = df.groupby(["YEAR", "MONTH", "MONTH_NAME", "TYPE"]).agg(aggregation)

# group data by each combination of  "YEAR" and "TYPE"
# e.g. Group 1: 2011, Fossil Fuels, Group 2: 2011, Renewables, Group 3: 2012, Fossil Fuels etc...
# .cumsum() iterates over "VALUE" rows of each group and applies the cumulative some to each row of df["yearToDate"]
# check the onenote file for a better understanding
df["yearToDate"] = df.groupby(["YEAR", "TYPE"])["VALUE"].cumsum()

# clean data by resetting the data frame indexing.
# this will remove any groupings or aggregated data and reset to default index value "0"
# inplace="True will modify the df rather than creating a new one.
df.reset_index(inplace=True)  # resting the index to columns

# drop missing data
df.dropna(axis=0, thresh=len(df.columns), subset=None, inplace=True)


# |--- MATPLOTLIB VISUALISATION --|

# first, configure plot
plt.figure(figsize=(14, 6))     # figure size by width x height in inches
plt.grid(True)       # shows plot gridlines
plt.xlabel("Month")     # x-axis label
plt.xticks(rotation=45)     # rotates x-labels by 45 degrees
plt.ylabel("Consumption (GWh)")       # y-axis label
plt.title("Australia Energy Consumption between 2011 to 2021")      # figure title

# extract frames from existing dataset. X = TYPE and MONTH over a YEAR
df_fossilfuels = df[df["TYPE"] == "Fossil Fuels"]
df_renewables = df[df["TYPE"] == "Renewables"]

# iterate over the df_fossilfuels dataframe, grouping it by the "YEAR" feature.
# this will extract every year for fossil fuels
for YEAR, feature in df_fossilfuels.groupby("YEAR"):
    # plot the first X and y values. feature(X) being MONTH and feature(y) being VALUE
    # Set X-axis label.
    plt.plot(feature["MONTH_NAME"], feature["VALUE"], label=f"Fossil Fuels - {YEAR}")

# iterate over the df_renewables dataframe, grouping it by the "YEAR" feature.
# this will extract every year for renewables
for YEAR, feature in df_renewables.groupby("YEAR"):
    # plot the second X and y values. feature[X] being MONTH_NAME and feature[y] being VALUE
    # then set a label for the X axis.
    plt.plot(feature["MONTH_NAME"], feature["VALUE"], label=f"Renewables - {YEAR}")

# show plotted data
plt.legend(loc="center left", bbox_to_anchor=(1.05, 0.5))   # plot legend - bbox sets legend to outside the plot
plt.tight_layout()      # prevents clipping of data
plt.show()      # show figure
