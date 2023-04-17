import pandas as pd

log_filename = 'LOG_2023-03-26.log'
col = ['date', 'time', 'coin', 'stratname', 'price(ask)', 'depth (%)', 'rollback (R)(%)', 'delta (d)', 'dBTC (%)',
       'dBTC5m (%)', 'dBTC1m (%)', '24hBTC1m (%)', '72hBTC1m (%)', 'dMarkets: (%)', 'dMarkets24 (%)', '24vol (m)',
       'hvol(k)', 'h3vol(k)', 'Delta24h(%)', 'Delta3h(%)', 'd1h (%)', 'd15m (%)', 'PumpD (%)', 'PumpHDelta (%)',
       'DumpHDelta (%)', 'Min(5min, 1sec)', 'Max(5min, 1sec)', 'Min(15min, 1sec)', 'Max(15min, 1sec)', 'Min(30min, 1sec)',
       'Max(30min, 1sec)', 'Min(60min, 1sec)', 'Max(60min, 1sec)', 'Min(1hours, 1sec)', 'Max(1hours, 1sec)',
       'Min(2hours, 1sec)', 'Max(2hours, 1sec)', 'Min(3hours, 1sec)', 'Max(3hours, 1sec)', 'Min(4hours, 1sec)',
       'Max(4hours, 1sec)', 'Min(6hours, 1sec)', 'Max(6hours, 1sec)', 'Min(12hours, 1sec)', 'Max(12hours, 1sec)',
       'Min(24hours, 1sec)', 'Max(24hours, 1sec)']

template_signal = [('Signal', 'coin'), ('Ask', 'price(ask)'), ('dBTC', 'dBTC (%)'), ('dBTC5m', 'dBTC5m (%)'), ('dBTC1m', 'dBTC1m (%)'),
                   ('24hBTC','24hBTC1m (%)'), ('72hBTC', '72hBTC1m (%)'), ('dMarkets','dMarkets: (%)'), ('dMarkets24','dMarkets24 (%)'),
                   ('(strategy','stratname'), ('Depth','depth (%)'), ('R','rollback (R)(%)'), ('d','delta (d)')]

template_pumpq = [('24vol','24vol (m)'), ('hvol','hvol(k)'), ('h3vol','h3vol(k)'), ('Delta24h','Delta24h(%)'),
                  ('Delta3h','Delta3h(%)'), ('d1h', 'd1h (%)'), ('d15m','d15m (%)'), ('PumpD','PumpD (%)'),
                  ('PumpHDelta','PumpHDelta (%)'), ('DumpHDelta','DumpHDelta (%)')]

template_emafilter = [('Min(5min,','Min(5min, 1sec)'), ('Max(5min,','Max(5min, 1sec)'),
                      ('Min(15min,','Min(15min, 1sec)'), ('Max(15min,','Max(15min, 1sec)'),
                      ('Min(30min,','Min(30min, 1sec)'), ('Max(30min,','Max(30min, 1sec)'),
                      ('Min(60min,','Min(60min, 1sec)'), ('Max(60min,','Max(60min, 1sec)'),
                      ('Min(1hours,','Min(1hours, 1sec)'), ('Max(1hours,','Max(1hours, 1sec)'),
                      ('Min(2hours,','Min(2hours, 1sec)'), ('Max(2hours,','Max(2hours, 1sec)'),
                      ('Min(3hours,','Min(3hours, 1sec)'), ('Max(3hours,','Max(3hours, 1sec)'),
                      ('Min(4hours,','Min(4hours, 1sec)'), ('Max(4hours,','Max(4hours, 1sec)'),
                      ('Min(6hours,','Min(6hours, 1sec)'), ('Max(6hours,','Max(6hours, 1sec)'),
                      ('Min(12hours,','Min(12hours, 1sec)'), ('Max(12hours,','Max(12hours, 1sec)'),
                      ('Min(24hours,','Min(24hours, 1sec)'), ('Max(24hours,','Max(24hours, 1sec)')]


new_data = pd.DataFrame(columns=col)
row_in_dataframe = 0

date = log_filename.split('.')[0][4:]


def fill_df_with_data(template, row):
    global splitted_line
    global new_data
    for i in template:
        if i[0] in splitted_line:
            tick_position = splitted_line.index(i[0])
            new_data.at[row, i[1]] = splitted_line[tick_position + 1]
        else:
            print(f'НЕТ ТАКОЙ ИНФОРМАЦИИ! {i[0]}')


with open(log_filename, 'r') as myfile:
    for line in myfile:

        if 'Signal' in line:
            new_data.at[row_in_dataframe, 'date'] = date

            first_space_position = line.index(' ')
            new_data.at[row_in_dataframe, 'time'] = line[:first_space_position]

            new_line = line.replace(':', ' ')
            splitted_line = new_line.split()

            print(splitted_line)

            fill_df_with_data(template_signal, row_in_dataframe)

        if 'PumpQ' in line:
            new_line = line.replace('=', ' ')
            new_line2 = new_line.replace(':', ' ')

            splitted_line = new_line2.split()
            print(splitted_line)

            fill_df_with_data(template_pumpq, row_in_dataframe)

        if 'EMAFilter' in line:
            new_line = line.replace('=', ' ')
            new_line = new_line.replace(('1sec)'), ' ')
            splitted_line = new_line.split()
            print(splitted_line)

            fill_df_with_data(template_emafilter, row_in_dataframe)

            row_in_dataframe +=1

new_data['24vol (m)'] = new_data['24vol (m)'].str.replace('m', '')
new_data['stratname'] = new_data['stratname'].str.replace(')', '')
new_data['coin'] = new_data['coin'].str.replace('USDT-', '')
new_data = new_data.replace('%', '', regex=True)
new_data.iloc[:, 4:] = new_data.iloc[:, 4:].astype('float64')

print(new_data.to_string())

xlsx_filename = log_filename[:-3] + 'xlsx'
new_data.to_excel(xlsx_filename, index=False)
