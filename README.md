If you are interested in using custom maps and/or custom landmarks, you may use
the instructions below to create them.  You are __not required__ to use custom
maps or landmarks.

## Creating a Custom Map

1. Use [BBBike Extract Service](https://extract.bbbike.org/?sw_lng=-77.69&sw_lat=43.077&ne_lng=-77.651&ne_lat=43.094&format=osm.pbf&coords=-77.69%2C43.077%7C-77.665%2C43.079%7C-77.662%2C43.082%7C-77.655%2C43.082%7C-77.653%2C43.086%7C-77.654%2C43.088%7C-77.652%2C43.092%7C-77.651%2C43.094%7C-77.682%2C43.094%7C-77.684%2C43.09%7C-77.688%2C43.085%7C-77.69%2C43.081&lang=en&city=RIT)
   to select and extract a geographic region.
   - Make sure to select the "Protocolbuffer (PBF)" format.
   - "Name of area to extract" can be an arbitrary description of the extracted
     map.
   - "Your email address" is the email address that will receive an email
     notification with the map's download link once extraction is complete.
2. Once extraction is complete, open the link in the notification email to
   download the map's `*.pbf` file, and place the file in the `data` directory.

### Adding Custom Landmarks

Landmark files have the following format:

```json
[
  {"landmark": "Golisano Hall", "amenity": "food", "geo": "43.08414155,-77.67989302038293"},
  {"landmark": "Slaughter Hall", "geo": "43.0849761,-77.68219844708884"},
  {"landmark": "Sustainability Institute", "geo": "43.085325600000004,-77.68132508662501"},
  {"landmark": "Wallace Library", "amenity": "food", "geo": "43.08391,-77.67634473251854"},
  {"landmark": "SHED", "geo": "43.08383285,-77.6757840091102"},
  ...
]
```
See `data/rit-landmarks.json` for an example. You can add your own landmark file
to a different file under the `data` directory.

To add a landmark:
1. Find it on [OpenStreetMap Nominatim](https://nominatim.openstreetmap.org/).
   - Tip: For landmarks on campus, you can narrow down your search by adding
     "Rochester" or "Henrietta" to your query.
2. Copy the "Centre Point (lat,lon)" from the details webpage
   (e.g. [Golisano Hall](https://nominatim.openstreetmap.org/ui/details.html?osmtype=W&osmid=24941723&class=building),
   and set that to be the value of `geo`.
