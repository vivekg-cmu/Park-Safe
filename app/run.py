from flask import Flask, render_template, request
import folium

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def find_parking():
    if request.method == 'GET':
        coordinates = (37.76, -122.44)
    else:
        coordinates = (request.form['latitude'], request.form['longitude'])
    print(coordinates)
    folium_map = folium.Map(location=coordinates, zoom_start=14)
    folium_map.save('templates/map.html')
    return render_template('index.html')

if __name__=='__main__':
    app.run(debug=True)