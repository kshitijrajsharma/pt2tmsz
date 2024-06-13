import leafmap.foliumap as leafmap
import mercantile
import requests
import streamlit as st

st.set_page_config(layout="wide")
m = leafmap.Map(center=[28, 84], zoom=3)


def get_max_zoom_level(tms_url, lat, lon):
    zoom_level = 1
    max_zoom_level = 0
    min_zoom_level = 1
    min_zoom_level_limit = 20
    while True:
        tile = mercantile.tile(lon, lat, zoom=zoom_level)
        tile_url = tms_url.format(x=tile.x, y=tile.y, z=zoom_level)
        response = requests.get(tile_url)
        if response.status_code == 200:
            max_zoom_level = zoom_level
            zoom_level += 1
        elif zoom_level <= min_zoom_level_limit:
            min_zoom_level = zoom_level
            zoom_level += 1
        else:
            break
    return max_zoom_level, min_zoom_level


def app():
    st.title("Query TMS Zoom Level")
    point_lat = st.text_input("Point Latitude (Y)", value=27.632669, key="lat")
    point_lon = st.text_input("Point Longitude (X)", value=85.5126, key="lon")
    tms_url = st.text_input(
        "TMS URL",
        value="https://tiles.openaerialmap.org/64c175a93473010001ab8bee/0/64c175a93473010001ab8bef/{z}/{x}/{y}",
    )
    if tms_url:
        try:
            m.add_tile_layer(tms_url, name="Your TMS", attribution="Your attribution")
        except Exception as e:
            st.error(f"Error adding TMS layer: {e}")
    if point_lat and point_lon:
        m.add_marker(location=[float(point_lat), float(point_lon)], draggable=True)
    if st.button("Calculate"):
        with st.spinner("Fetching zoom levels..."):
            max_zoom_level, min_zoom_level = get_max_zoom_level(
                tms_url, float(point_lat), float(point_lon)
            )

        st.success(
            f"Maximum available zoom level: {max_zoom_level}, Minimum available zoom level: {min_zoom_level}"
        )
        m.set_center(
            lat=float(point_lat), lon=float(point_lon), zoom=max_zoom_level - 2
        )

    m.to_streamlit(height=700)
    st.echo()


if __name__ == "__main__":
    app()
