import streamlit as st
import plotly.graph_objects as go
import json

geojson_file_path = r"alenashar057/course_project/Russia_regions.geojson"

with open(geojson_file_path, "r", encoding="utf-8") as file:
    geojson_content = json.load(file)

def create_map(data_frame, color_palette, map_title):
    figure = go.Figure(
        go.Choroplethmapbox(
            geojson=geojson_content,
            featureidkey="properties.region",
            locations=data_frame['region_name'],
            z=data_frame['count'],
            colorscale=color_palette,
            zmin=data_frame['count'].min(),
            zmax=data_frame['count'].max(),
            marker_opacity=0.7,
            marker_line_width=0.5,
            hovertemplate="<b>%{location}</b><br>Value: %{z}<extra></extra>",
            colorbar_title="Value",
        )
    )

    figure.update_layout(
        mapbox_style="carto-positron",
        mapbox_zoom=3,
        mapbox_center={"lat": 65, "lon": 100},
        title_text=map_title,
        title_x=0.5,
        margin={"r": 0, "t": 40, "l": 0, "b": 0},
        height=350,
    )

    st.plotly_chart(figure, use_container_width=True)

