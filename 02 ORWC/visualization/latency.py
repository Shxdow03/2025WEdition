import pandas as pd
import scipy.stats as st
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import os

base = Path(__file__).resolve().parent
paths=[base.parent/'Results'/'latencyWinAPIc.csv', base.parent/'Results'/'latencyWinAPIc++.csv', base.parent/'Results'/'latencyFstream.csv']

try:
    for i in paths:
        data = pd.read_csv(i)
        current_file = os.path.splitext(os.path.basename(i.name))[0]

        data_stats = pd.DataFrame(columns=['Operation', 'Max', 'Min', 'Mean', 'Median', 'Std Dev', 'Lower 95%', 'Upper 95%', 'Lower 99%', 'Upper 99%', 'LBound 95% ConfI', 'UBound 95% ConfI', 'LBound 99% ConfI', 'UBound 99% ConfI'])
        data_stats['Operation'] = data.columns[1:]
        data_stats['Max'] = data_stats['Operation'].apply(lambda x: data[x].max())
        data_stats['Min'] = data_stats['Operation'].apply(lambda x: data[x].min())
        data_stats['Mean'] = data_stats['Operation'].apply(lambda x: data[x].mean())
        data_stats['Median'] = data_stats['Operation'].apply(lambda x: data[x].median())
        data_stats['Std Dev'] = data_stats['Operation'].apply(lambda x: data[x].std())
        data_stats['Upper 95%'] = data_stats['Operation'].apply(lambda x: st.scoreatpercentile(data[x], 95))
        data_stats['Lower 95%'] = data_stats['Operation'].apply(lambda x: st.scoreatpercentile(data[x], 5))
        data_stats['Upper 99%'] = data_stats['Operation'].apply(lambda x: st.scoreatpercentile(data[x], 99))
        data_stats['Lower 99%'] = data_stats['Operation'].apply(lambda x: st.scoreatpercentile(data[x], 1))
        data_stats['UBound 95% ConfI'] = data_stats['Operation'].apply(lambda x: pd.Series(st.t.interval(0.95, len(data[x])-1, loc=data[x].mean(), scale=data[x].sem()), index=['Lower Bound', 'Upper Bound'])["Upper Bound"])
        data_stats['LBound 95% ConfI'] = data_stats['Operation'].apply(lambda x: pd.Series(st.t.interval(0.95, len(data[x])-1, loc=data[x].mean(), scale=data[x].sem()), index=['Lower Bound', 'Upper Bound'])["Lower Bound"])
        data_stats['UBound 99% ConfI'] = data_stats['Operation'].apply(lambda x: pd.Series(st.t.interval(0.99, len(data[x])-1, loc=data[x].mean(), scale=data[x].sem()), index=['Lower Bound', 'Upper Bound'])["Upper Bound"])
        data_stats['LBound 99% ConfI'] = data_stats['Operation'].apply(lambda x: pd.Series(st.t.interval(0.99, len(data[x])-1, loc=data[x].mean(), scale=data[x].sem()), index=['Lower Bound', 'Upper Bound'])["Lower Bound"])

        bins=200
        percent=98
        percentile_open = np.percentile(data['Open'], percent)
        filtered_open = data['Open'][data['Open'] <= percentile_open]
        percentile_read = np.percentile(data['Read'], percent)
        filtered_read = data['Read'][data['Read'] <= percentile_read]
        percentile_write = np.percentile(data['Write'], percent)
        filtered_write = data['Write'][data['Write'] <= percentile_write]
        percentile_close = np.percentile(data['Close'], percent)
        filtered_close = data['Close'][data['Close'] <= percentile_close]

        fig1, axs = plt.subplots(2,2, figsize=(12,10))
        fig1.suptitle(f"Latency in µs ({percent}th Percentile) for {current_file}")

        axs[0,0].hist(filtered_open, bins=bins)
        axs[0,0].set_title('Open')
        axs[0,0].axvline(data_stats.iloc[0, 3], color='r', linestyle='dashed', linewidth=2, label='Mean')
        axs[0,1].hist(filtered_read, bins=bins)
        axs[0,1].set_title('Read')
        axs[0,1].axvline(data_stats.iloc[2, 3], color='r', linestyle='dashed', linewidth=2, label='Mean')
        axs[1,0].hist(filtered_write, bins=bins)
        axs[1,0].set_title('Write')
        axs[1,0].axvline(data_stats.iloc[1, 3], color='r', linestyle='dashed', linewidth=2, label='Mean')
        axs[1,1].hist(filtered_close, bins=bins)
        axs[1,1].set_title('Close')
        axs[1,1].axvline(data_stats.iloc[3, 3], color='r', linestyle='dashed', linewidth=2, label='Mean')

        axs[0,0].set_ylabel('Frequency')
        axs[1,0].set_ylabel('Frequency')
        axs[1,0].set_xlabel('Latency')
        axs[1,1].set_xlabel('Latency')
        fig1.savefig(base.parent/'images'/f"subplots_{current_file}.png")
        #plt.show()

        stats = data_stats.set_index('Operation')
        columns = [i for i in stats.columns if i != 'Operation']
        table_data = stats[columns].apply(pd.to_numeric, errors='coerce').round(2)

        fig2, ax = plt.subplots(figsize=(18, 6))
        ax.axis('off')

        table = ax.table(cellText=table_data.values,
                        rowLabels=table_data.index,
                        colLabels=table_data.columns,
                        cellLoc='center',
                        loc='center')

        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1.25,3)
        
        ax.set_title(f'Latency Statistics in µs ({current_file})', fontsize=30, fontweight='bold', pad=15)
        fig2.savefig(base.parent/'images'/f"stats_{current_file}.png")
        plt.show()

except FileNotFoundError as ex:
    print(f"File {i} not found: {ex}")