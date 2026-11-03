from dash import Dash, html, dcc
import dash_ag_grid as dag
import pandas as pd
import plotly.express as px

df = pd.read_csv("dazzle_dash/data/life_expectancy_data.csv")

moyenne = df.groupby('Country', as_index=False)['Adult Mortality'].mean()
moyenne = moyenne.sort_values('Adult Mortality', ascending=False).head(5)

fig = px.bar(
    moyenne,
    x='Adult Mortality',
    y='Country',
    orientation='h',
    title="5 pays avec la mortalité adulte la plus élevée",
)

fig.update_layout(
    yaxis={'categoryorder': 'total ascending'},
    height=700,
    )
fig.update_yaxes(dtick=1)


app = Dash()

app.layout = [
    html.Div(children='My first app with Data'),
    dag.AgGrid(
        rowData=df.astype(object).where(df.notna(), None).to_dict('records'),
        columnDefs=[{"field": i} for i in df.columns],
        style={"height": "600px"}
    ),
    dcc.Graph(figure=fig)
]

if __name__ == '__main__':
    app.run(debug=True)