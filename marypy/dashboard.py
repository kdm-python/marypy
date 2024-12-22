import pandas as pd
from dash import Dash, Input, Output, State, callback, callback_context, html, dcc
from dash.dash_table import DataTable

import data_operations as dt

df: pd.DataFrame = dt.get_strain_data().sort_values(by="Name")
tbl_data = dt.get_table_data(df)

app = Dash(__name__)
app.title = "MaryPy Cannabis Directory"

app.layout = html.Div(
    [
        html.Div(
            children=app.title,
            className="title",
        ),
        DataTable(
            id="data-table",
            data=df.to_dict(
                orient="records"
            ),  # Convert DataFrame rows to a list of dictionaries
            style_table={"overflowX": "auto"},
            style_cell={"textAlign": "left", "padding": "10px", "minWidth": "100px"},
            style_header={
                "backgroundColor": "rgb(230, 230, 230)",
                "fontWeight": "bold",
            },
            page_size=10,
            columns=[
                {"name": "Name", "id": "Name"},  # Match DataFrame columns
                {"name": "Rating", "id": "Rating"},
                {"name": "THC%", "id": "THC%"},
                {"name": "Type", "id": "Type"},
            ],
        ),
        dcc.RadioItems(
            options=[
                {"label": "Sort by Name", "value": "Name"},
                {"label": "Sort by Rating", "value": "Rating"},
            ],
            value="Name",  # Default value for sort order
            id="controls-and-radio-item",
            style={"marginBottom": "20px"},
        ),
        dcc.Dropdown(
            options=[
                {"label": "Ascending", "value": "asc"},
                {"label": "Descending", "value": "desc"},
            ],
            value="asc",  # Default sorting order
            id="sort-order-dropdown",
            style={"marginBottom": "20px", "width": "200px"},
        ),
        html.Div(
            [
                dcc.Input(
                    id="search-input",
                    type="text",
                    placeholder="Enter strain name",
                ),
                html.Button(
                    "Search",
                    id="search-button",
                    className="standard-button",
                    n_clicks=0,
                ),
            ],
            style={"margin": "20px 0"},
        ),
    ]
)


@callback(
    Output(component_id="data-table", component_property="data"),
    [
        Input(component_id="controls-and-radio-item", component_property="value"),
        Input(component_id="sort-order-dropdown", component_property="value"),
        Input("search-button", "n_clicks"),
    ],
    [State("search-input", "value")],
)
def update_table(sort_by, sort_order, search_clicks, search_term):
    ctx = callback_context
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0] if ctx.triggered else None
    current_data = tbl_data

    if trigger_id == "search-button" and search_term:
        current_data = df[df["Name"].str.contains(search_term, case=False, na=False)]

    valid_columns = ["Name", "Rating", "THC%", "Type"]
    if sort_by not in valid_columns:
        sort_by = "Name"
    ascending = sort_order == "asc"

    try:
        sorted_data = sorted(
            current_data,
            key=lambda x: x[sort_by],
            reverse=not ascending,
        )
        return sorted_data
    except Exception as e:
        print(f"Error in sorting: {e}")

    return current_data.to_dict("records")


# @callback(
#     Output("data-table", "data"),
#     Input("search-button", "n_clicks"),
#     State("search-input", "value"),
# )
# def update_search(n_clicks: int, search_term: str):
#     if not search_term:
#         return df.to_dict("records")
#     filtered_df = df[
#         df['Name'].str.contains(search_term, case=False, na=False)
#     ]

#     return filtered_df.to_dict("records")

if __name__ == "__main__":
    app.run(debug=True)
