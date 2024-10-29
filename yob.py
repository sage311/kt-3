import pandas as pd
import matplotlib.pyplot as plt
import os

def read_yob_file(filename):
    df = pd.read_csv(filename, names=['Name', 'Sex', 'Count'])
    df['Year'] = int(filename.split('.')[0][-4:])
    return df

def combine_yob_files(directory):
    all_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.txt')]
    df_list = [read_yob_file(f) for f in all_files]
    combined_df = pd.concat(df_list, ignore_index=True)
    return combined_df

def validate_year_input(year_input):
    try:
        year = int(year_input)
        if year < 1880 or year > 2010:
            raise ValueError(f"Ошибка: год {year} вне диапазона (1880-2010). Пожалуйста, введите корректный год.")
        return year
    except ValueError:
        raise ValueError(f"Ошибка: '{year_input}' не является корректным годом. Пожалуйста, введите числовое значение.")

def plot_charts(df, year):
    data_for_year = df[df['Year'] == year]

    sex_counts = data_for_year.groupby('Sex')['Count'].sum()
    plt.subplot(1, 2, 1)
    plt.pie(sex_counts, labels=sex_counts.index, autopct='%1.1f%%', colors=['#ff9999', '#66b3ff'])
    plt.title(f"Распределение по полу в {year} году")

    top_names = data_for_year.groupby('Name')['Count'].sum().nlargest(10)
    plt.subplot(1, 2, 2)
    plt.pie(top_names, labels=top_names.index, autopct='%1.1f%%', colors=['#ffcc99', '#99ff99', '#66b3ff'])
    plt.title(f"Топ-10 имен в {year} году")

    plt.tight_layout()
    plt.show()

def plot_names(df, names):
    filtered_df = df[df['Name'].isin(names)]
    total_counts = filtered_df.groupby('Name')['Count'].sum()

    plt.figure(figsize=(8, 6))
    plt.pie(total_counts, labels=total_counts.index, autopct='%1.1f%%', colors=['#ffb3e6', '#cceeff', '#ffcc99'])
    plt.title("Общее количество младенцев с выбранными именами")
    plt.tight_layout()
    plt.show()

def plot_trend(df, names):
    filtered_df = df[df['Name'].isin(names)]
    years_range = pd.Series(range(1880, 2011))
    counts_per_name_year = filtered_df.groupby(['Year', 'Name'])['Count'].sum().unstack(fill_value=0)
    counts_per_name_year = counts_per_name_year.reindex(years_range, fill_value=0)

    plt.figure(figsize=(18, 6))

    plt.subplot(1, 2, 1)
    for name in names:
        plt.plot(counts_per_name_year.index, counts_per_name_year[name], label=name)
    plt.title("Количество младенцев с указанными именами")
    plt.xlabel('Год')
    plt.ylabel('Количество')
    plt.legend()

    plt.subplot(1, 2, 2)
    total_name_counts = counts_per_name_year.sum(axis=1)
    plt.plot(total_name_counts.index, total_name_counts, label="Общее количество", color="darkorange")
    plt.title("Общее количество младенцев с выбранными именами (1880-2010)")
    plt.xlabel('Год')
    plt.ylabel('Общее количество')
    plt.legend()

    plt.tight_layout()
    plt.show()

def plot_selected_names_trend(df, names):
    filtered_df = df[df['Name'].isin(names)]
    years_range = pd.Series(range(1880, 2011))
    counts_per_name_year = filtered_df.groupby(['Year', 'Name'])['Count'].sum().unstack(fill_value=0)
    counts_per_name_year = counts_per_name_year.reindex(years_range, fill_value=0)

    plt.figure(figsize=(10, 6))
    plt.title("Динамика имен с 1880 по 2010 год")
    plt.xlabel('Год')
    plt.ylabel('Количество')
    plt.grid()
    for name in names:
        plt.plot(counts_per_name_year.index, counts_per_name_year[name], label=name)
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_top_names(df, top_n=10):
    name_counts = df.groupby('Name')['Count'].sum().sort_values(ascending=False)
    top_names = name_counts.head(top_n)

    plt.figure(figsize=(10, 6))
    plt.barh(top_names.index, top_names.values, color='lightcoral')
    plt.gca().invert_yaxis()
    plt.title(f"Топ-{top_n} самых популярных имен (1880-2010)")
    plt.xlabel("Количество младенцев")
    plt.ylabel("Имя")
    plt.tight_layout()
    plt.show()

directory = 'yob'
df = combine_yob_files(directory)

while True:
    print('Введите год (1880-2010):')
    year_input = input()
    try:
        year_to_plot = validate_year_input(year_input)
        break
    except ValueError as e:
        print(e)

plot_charts(df, year_to_plot)

names_to_plot = ['Michael', 'Jessica', 'James']
plot_names(df, names_to_plot)
plot_trend(df, names_to_plot)
plot_selected_names_trend(df, names_to_plot)
plot_top_names(df)
