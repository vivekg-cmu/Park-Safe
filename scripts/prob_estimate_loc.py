# %%
import pandas as pd
import numpy as np
import os
import math
from scipy.integrate import dblquad
from scipy.stats import multivariate_normal as mvn
from ast import literal_eval as make_tuple
from scipy.stats import median_test

# %%
gauss_df = pd.read_csv('../filtered_data/hotspot_gaussian.csv')
gauss_df = gauss_df[gauss_df['cluster_size'] >= 30]
gauss_df['mean'] = gauss_df['mean'].apply(make_tuple)
# %%

def prob_loc(lat, lon):
    # Calculate prob in 6x6 m box around spot
    lat_diff = 0.000027
    lon_diff = 0.000034

    prob = 0
    N = gauss_df['cluster_size'].sum()
    for idx, hotspot in gauss_df.iterrows():
        center = hotspot['mean']
        var_lat = hotspot['var_latitude']
        var_lon = hotspot['var_longitude']
        cov = hotspot['cov']

        var_mat = [[var_lat, cov], [cov, var_lon]]
        try:
            gauss_prob = dblquad(lambda y, x: mvn.pdf([x, y], center, var_mat), lat-lat_diff, lat+lat_diff, lambda x: lon-lon_diff, lambda x: lon+lon_diff)[0]
        except:
            continue
        prob += hotspot['cluster_size']*gauss_prob
    prob = prob/N
    return prob
# %%
'''
no_loc = 100
prob_random_list = list()
prob_incident_list = list()

for i in range(no_loc):
    rand_lat = np.random.uniform(37.708, 37.830)
    rand_lon = np.random.uniform(-122.511, -122.364)
    prob_random_list.append(prob_loc(rand_lat, rand_lon))
    if i%5==0:
        print(f'{i} locations completed')

incident_df = pd.read_csv('../filtered_data/Filtered_Incident_Report.csv')
incident_loc = np.random.randint(0, incident_df.shape[0], no_loc)
for i, (lat, lon) in enumerate(zip(incident_df['Latitude'][incident_loc], incident_df['Longitude'][incident_loc])):
    if not math.isnan(lon):
        prob_incident_list.append(prob_loc(lat, lon))
    if i%10==0:
        print(f'{i} locations completed')

stat, p, med, tbl = median_test(prob_incident_list, prob_random_list)
'''

# %%

prob_file = 'loc_prob.npy'
data_df = pd.read_csv('../filtered_data/Incident_2019_complete.csv')
start, end = 0, data_df.shape[0]    # CHANGE THIS LINE

prob = list()
if prob_file in os.listdir():
    prob = list(np.load(prob_file))
    start = len(prob)
    print(f'loaded {start} records')
    
# %%
for i in range(start, end):
    row = data_df.iloc[i]
    prob.append(prob_loc(row['latitude'], row['longitude']))
    if i % 50 == 0:
        print(f'saving {len(prob)} records')
        np.save(prob_file, np.array(prob))
