import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

columns = ['region_ID', 'Country/Region', 'Year', 'Note', 'Emission_Value']
df_emission = pd.read_csv("SYB64_310_202110_Carbon Dioxide Emission Estimates.csv",
header = 1, names = columns, thousands = ",", encoding = "iso-8859-1")

df_emission_per_capita = df_emission.loc[df_emission['Note'].str.contains("Emissions per capita")]
df_emission_total = df_emission.loc[~df_emission['Note'].str.contains("Emissions per capita")]

df_merged = pd.merge(df_emission_per_capita, df_emission_total, how = "left",
left_on = ['Country/Region', 'Year'], right_on = ['Country/Region', 'Year'],
suffixes = ('_per_capita', '_total'))

df_final = df_merged[['Country/Region', "Year", 'Emission_Value_per_capita',
"Emission_Value_total"]]

print(df_final.head(10))

# create a category chart: bar chart
df_emission_2018 = df_final[df_final["Year"] == 2018].sort_values('Emission_Value_total',
ascending = False).head(10)
print(df_emission_2018)

#======================plotting===================================
# bar chart
sns.catplot(x = "Country/Region", y = "Emission_Value_total", data = df_emission_2018,
kind = 'bar')
plt.ylabel("Total Emission 2018 (thousand metric tons)")
plt.title("Top 10 Carbon Dioxide Emission Countries in 2018")
plt.xticks(rotation = 90)
plt.show()

# same as above, but use plt directly.
plt.bar(df_emission_2018["Country/Region"], df_emission_2018["Emission_Value_total"],
color ='maroon',width = 0.6)
plt.ylabel("Total Emission 2018 (thousand metric tons)")
plt.title("Top 10 Carbon Dioxide Emission Countries in 2018")
plt.xticks(rotation = 90)
plt.show()

sns.barplot(x = "Emission_Value_total", y = "Country/Region", data= df_emission_2018)
plt.show()

# create the line chart for the top 10 emission countries
top_emission_countries = df_emission_2018['Country/Region'].tolist()
df_emission_top_countries = df_final[df_final['Country/Region'].isin(top_emission_countries)]
sns.relplot(x = "Year", y = "Emission_Value_total", data = df_emission_top_countries,
kind = "line", hue = "Country/Region")
plt.xticks(rotation = 90)
plt.title("Top 10 Carbon Dioxide Emission Countries Trending")
plt.show()

# use matplotlib to draw side-by-side bars
df_china_emission = df_emission_top_countries.loc[df_emission_top_countries['Country/Region'] == 'China']
df_usa_emission = df_emission_top_countries.loc[df_emission_top_countries['Country/Region'] == 'United States of America']
plt.bar(df_china_emission["Year"]-1, df_china_emission["Emission_Value_total"],
color ='r', width = 0.5)
plt.bar(df_usa_emission["Year"], df_usa_emission["Emission_Value_total"],
color ='b', width = 0.5)
plt.title("China vs. USA Carbon Dioxide Emission Comparison")
plt.legend(loc="lower left")
plt.show()

# create scatter chart
sns.relplot(x = "Emission_Value_per_capita", y = "Emission_Value_total",
data = df_emission_top_countries, kind ="scatter")
plt.xticks(rotation = 90)
plt.xlabel("Emission Per Capita")
plt.ylabel("Total Emission Annually (thousand metric tons)")
plt.title("Carbon Dioxide Emission Total vs. Per-capita Relation")
plt.legend(loc="lower left")
plt.show()
