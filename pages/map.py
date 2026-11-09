from dash import register_page, html, dcc, callback, Input, Output
import plotly.express as px

from src.data import load_data

register_page(__name__, path="/map", name="Carte", order=1)

df = load_data()
df = df.sort_values("Year")  # so the animation slider goes 2000 -> 2015

COLOR_RANGE = (df["Life expectancy"].min(), df["Life expectancy"].max())  # same scale every year


def make_map(data, zoom=False):
    fig = px.choropleth(
        data,
        locations="Country",
        locationmode="country names",
        color="Life expectancy",
        hover_name="Country",
        animation_frame="Year",
        color_continuous_scale="Viridis",
        range_color=COLOR_RANGE,
        projection="natural earth",
    )
    fig.update_layout(height=600, margin=dict(l=0, r=0, t=30, b=0))
    if zoom:
        fig.update_geos(fitbounds="locations")  # zoom in on the selected countries
    return fig


layout = html.Div([
    html.H1("Map Page"),
    dcc.Dropdown(
        id="country-search",
        options=sorted(df["Country"].unique()),
        multi=True,            # pick several countries
        searchable=True,       # type to search
        placeholder="Search countries...",
    ),
    dcc.Graph(id="world-map", figure=make_map(df)),
])


@callback(
    Output("world-map", "figure"),
    Input("country-search", "value"),
)
def update_map(selected_countries):
    if not selected_countries:  # nothing selected -> whole world
        return make_map(df)
    filtered = df[df["Country"].isin(selected_countries)]
    return make_map(filtered, zoom=True)