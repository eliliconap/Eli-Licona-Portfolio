import folium
import pandas as pd

# Charlotte zip code data with readmission rates and zones
zip_data = {
    'zip': ['28216', '28208', '28205', '28212', 
            '28277', '28211', '28226', '28202'],
    'neighborhood': [
        'Beatties Ford Road / Northwest Charlotte',
        'Enderly Park / Brookhill',
        'Plaza Midwood / Eastside',
        'Hickory Grove / East Charlotte',
        'Ballantyne / South Charlotte',
        'Myers Park / Cotswold',
        'Pineville / South Charlotte',
        'Uptown Charlotte'
    ],
    'zone': ['Crescent', 'Crescent', 'Crescent', 'Crescent',
             'Wedge', 'Wedge', 'Wedge', 'Wedge'],
    'readmission_rate': [0.62, 0.61, 0.60, 0.63,
                         0.21, 0.22, 0.20, 0.23],
    'lat': [35.3127, 35.2087, 35.2271, 35.1982,
            35.0526, 35.1729, 35.0835, 35.2271],
    'lon': [-80.8817, -80.8897, -80.7854, -80.7432,
            -80.8418, -80.7981, -80.8407, -80.8432]
}

df = pd.DataFrame(zip_data)

# Create base map centered on Charlotte
m = folium.Map(
    location=[35.2271, -80.8431],
    zoom_start=11,
    tiles='CartoDB positron'
)

# Color function based on zone
def get_color(zone):
    if zone == 'Crescent':
        return '#3B1F5E'
    else:
        return '#C4A882'

# Add circles for each zip code
for _, row in df.iterrows():
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=18,
        color=get_color(row['zone']),
        fill=True,
        fill_color=get_color(row['zone']),
        fill_opacity=0.75,
        tooltip=folium.Tooltip(
            f"<div style='font-family: monospace; font-size: 13px; padding: 8px;'>"
            f"<strong>ZIP {row['zip']}</strong><br>"
            f"{row['neighborhood']}<br>"
            f"<span style='color: #888;'>{row['zone']} Corridor</span>"
            f"</div>"
        )
    ).add_to(m)

# Add legend
legend_html = '''
<div style="position: fixed; bottom: 40px; left: 40px; z-index: 1000;
     background: white; padding: 16px; border-radius: 4px;
     font-family: monospace; font-size: 12px; border: 1px solid #ccc;">
    <div style="margin-bottom: 8px; font-weight: bold;">Geographic Zone</div>
    <div style="margin-bottom: 6px;">
        <span style="background:#3B1F5E; 
        display:inline-block; width:14px; height:14px; 
        border-radius:50%; margin-right:8px;"></span>
        Crescent — High Readmission
    </div>
    <div>
        <span style="background:#C4A882; 
        display:inline-block; width:14px; height:14px; 
        border-radius:50%; margin-right:8px;"></span>
        Wedge — Low Readmission
    </div>
</div>
'''

m.get_root().html.add_child(folium.Element(legend_html))

# Save as HTML file
m.save('charlotte_readmission_map.html')

print("Map saved successfully as charlotte_readmission_map.html")