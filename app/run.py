from flask import Flask, render_template, request
from geopy.distance import geodesic
import folium
import pandas as pd

app = Flask(__name__)


color_grad = ['darkgreen', 'green', 'lightgreen', 'orange', 'pink', 'lightred', 'red', 'darkred']
parking_df = pd.read_csv('../filtered_data/Parking_Spots_Data.csv')
# %%
def create_and_save_map(coordinates, bound=100):
    folium_map = folium.Map(location=coordinates, zoom_start=14)
    folium.map.Marker(coordinates, popup=f'({coordinates[0]},{coordinates[1]})').add_to(folium_map)
    dist = lambda row: geodesic(coordinates, (row.Latitude, row.Longitude)).meters
    parking_df['distance'] = parking_df.apply(dist, axis=1)
    for _, spot in parking_df[parking_df['distance']<bound].iterrows():
        folium.map.Marker((spot.Latitude, spot.Longitude), popup='distance: {} m\nsafety-index: %, meter-id:'.format(spot.distance),
         icon=folium.Icon(color=color_grad[0], icon='car', prefix='fa')).add_to(folium_map)
    folium_map.save('templates/map.html')

# %%

@app.route('/', methods=['GET', 'POST'])
def find_parking():
    if request.method == 'GET':
        coordinates = (37.76, -122.44)
        folium_map = folium.Map(location=coordinates, zoom_start=14)
        folium_map.save('templates/map.html')
    else:
        coordinates = (request.form['latitude'], request.form['longitude'])
        create_and_save_map(coordinates, 500)
    return render_template('index.html')

if __name__=='__main__':
    app.run(debug=True)