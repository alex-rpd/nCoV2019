df2 = df.copy()
df2['Date_1'] = df2['Date'] + pd.Timedelta(days=1)
df2.rename(columns={'Confirmed': 'Confirmed_1',
                    'Deaths': 'Deaths_1',
                    'Recovered': 'Recovered_1',
                    'Date': 'Date_Minus_1'}, inplace=True)
df3 = df.merge(df2[['Province_State',
                    'Country_Region',
                    'Confirmed_1',
                    'Deaths_1',
                    'Recovered_1',
                    'Date_1',
                    'Date_Minus_1']], how='left',
               left_on=['Province_State', 'Country_Region', 'Date'],
               right_on=['Province_State', 'Country_Region', 'Date_1'])
df3['MonthYear'] = df3['Date'].dt.strftime('%b-%Y')
df3['ConfirmedDaily'] = df3['Confirmed'] - df3['Confirmed_1']
df3['DeathsDaily'] = df3['Deaths'] - df3['Deaths_1']
df3['RecoveredDaily'] = df3['Recovered'] - df3['Recovered_1']
df3['Continent'] = df3['Country_Region'].map(country_continent)
df3['ConfirmedDaily'].loc[df3['Date'] == '2020-01-22'] = df3['Confirmed']
df3['DeathsDaily'].loc[df3['Date'] == '2020-01-22'] = df3['Deaths']
df3['RecoveredDaily'].loc[df3['Date'] == '2020-01-22'] = df3['Recovered']

del df3['Confirmed_1']
del df3['Deaths_1']
del df3['Recovered_1']
del df3['Date_1']
del df3['Date_Minus_1']

if len(df3[df3['Continent'].isna()]) == 0:
    print(30*'+'+' All good ' + 30*'+')
else:
    print(30*'-'+' Check ' + 30*'-')

print(f'Deaths:\t\t{df3.DeathsDaily.sum()}\nConfirmed:\t{df3.ConfirmedDaily.sum()}\nRecovered:\t{df3.RecoveredDaily.sum()}\nCountries:\t{len(df3["Country_Region"].unique())}')
df3['DeathRate'] = df3['Deaths'] / df3['Confirmed']
df3['RecoveredRate'] = df3['Recovered'] / df3['Confirmed']
df3['MonthYear'] = df3['Date'].dt.strftime('%b-%Y')
df3.to_csv(f'data_{datetime.date.today()}.csv')
df3.groupby(['Country_Region']).sum()[['DeathsDaily']
                                      ].sort_values(ascending=False,
                                                    by='DeathsDaily').reset_index().head(10)