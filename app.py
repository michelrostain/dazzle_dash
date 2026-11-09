from dash import Dash, page_container, page_registry
import dash_bootstrap_components as dbc

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.FLATLY])

navbar = dbc.NavbarSimple(
    brand="Dazzle Dash",
    brand_href="/",
    children=[dbc.NavLink(page["name"], href=page["relative_path"]) for page in page_registry.values()],
    color="primary",
    dark=True,
    className="mb-4",
)

app.layout = [navbar, dbc.Container(page_container)]

if __name__ == "__main__":
    app.run(debug=True)
