#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 17:56:11 2024

@author: rafaelom
"""

from data_manipulation import *
from graphing import *

app = Dash(__name__, url_base_pathname='/endangered-species/', external_stylesheets=[
    "https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&family=Lato:wght@400;700&display=swap"
])

app.layout = html.Div([
    html.Div([
    	html.Div([
		html.H1("Interactive Dashboards for Species Analysis", className="h1Title"),
		html.Button("Species Use Chart", id="btn-species-use", className="btnMenu", n_clicks=0),
		html.Button("Risk of Extinction Chart", id="btn-risk", className="btnMenu", n_clicks=0),
		html.Button("Species Distribution Map", id="btn-map", className="btnMenu", n_clicks=0),
	], id="sidebar-content")
    ], id="sidebar"),
    
    html.Div([
        html.Div("Interactive Species Use Chart", className="title_div"),
        html.Div([
            html.Div([
		    html.Div([
			    html.H3("Filters and Options", className="h3Filters"),
			    html.Div([
				html.H4("Filtering by Country", style={
				"color": "#AD180D"
				}),
				dcc.Dropdown(
				    id="country-dropdown",
				    options=[{"label": c, "value": c} for c in countries],
				    placeholder="Select a country",
				    multi=True,
				    className="dropdown"
				)
			    ], style={"margin-bottom": "20px"}),

			    html.Div([
				html.H4("Filtering by Taxonomy", style={"color": "#AD180D"}),
				dcc.Dropdown(id="kingdom-dropdown", placeholder="Select a kingdom", className="dropdown"),
				dcc.Dropdown(id="phylum-dropdown", placeholder="Select a phylum", className="dropdown"),
				dcc.Dropdown(id="class-dropdown", placeholder="Select a class", className="dropdown"),
				dcc.Dropdown(id="order-dropdown", placeholder="Select an order", className="dropdown"),
				dcc.Dropdown(id="family-dropdown", placeholder="Select a family", className="dropdown"),
				dcc.Dropdown(id="specie-dropdown", placeholder="Select a species", className="dropdown"),
			    ], style={"margin-bottom": "20px"}),

			    html.Div([
				html.H4("Filtering by Year", style={"color": "#AD180D"}),
				dcc.Dropdown(
				    id="year-dropdown",
				    options=[{"label": year, "value": year} for year in unique_years],
				    placeholder="Select one or more years",
				    multi=True,
				    className="dropdown"
				)
			    ]),

			    html.Div([
				html.H4("View Options", style={"color": "#AD180D"}),
				dcc.Checklist(
				    id="default-mode-checklist",
				    options=[{"label": "Accumulated graph", "value": "default_mode"}],
				    value=["default_mode"],
				    labelStyle={'display': 'block', "margin-bottom": "5px"}
				),
				dcc.Checklist(
				    id="country-mode-checklist",
				    options=[{"label": "Stacked chart by country", "value": "country_mode"}],
				    labelStyle={"display": "block", "margin-bottom": "5px"}
				),
				dcc.Checklist(
				    id="year-mode-checklist",
				    options=[{"label": "Stacked chart by year", "value": "year_mode"}],
				    labelStyle={"display": "block", "margin-bottom": "5px"}
				),
				dcc.Checklist(
				    id="category-checklist",
				    options=[{"label": "Stacked chart by risk category", "value": "category_mode"}],
				    labelStyle={"display": "block", "margin-bottom": "5px"}
				),
				html.H4("Value Options", style={"color": "#AD180D"}),
				dcc.Checklist(
				    id="absolute-mode-checklist",
				    options=[{"label": "Absolute Values", "value": "absolute_mode"}],
				    value=["absolute_mode"],
				    labelStyle={'display': 'block', "margin-bottom": "5px"}
				),
				dcc.Checklist(
				    id="percentage-mode-checklist",
				    options=[{"label": "Percentage Values", "value": "percentage_mode"}],
				    labelStyle={"display": "block", "margin-bottom": "5px"}
				)
			    ])
			], id="use_chart_div")
		], className="div_filters"),

        html.Div([
		dcc.Graph(
		    id="stacked-bar-chart")
		 ], className="use_div")
	   
	], className="content_div", id="content_uses"),
    ], id="main-container1", className="main-container"),
    
    html.Div([
        html.Div("Risk of Extinction of Species Over the Years", className="title_div"),
        html.Div([
        	html.Div([
			html.Div([
				html.H4("Search for a Species", className="h4Title"),
				dcc.Input(
				    id="species-input",
				    className="search-input",
				    type="text",
				    placeholder="Type a scientific species name",
				),
				html.Button(
				    "Submit",
				    id="submit-button",
				    className="submitButton"
				),
				html.Div(
				    id="error-message",
				    className="error-message",
				)
			    ], className="search_div")],
			className="div_forms"),

		    html.Div([
			    dcc.Graph(
				id="risk-graph"
			    )], className="graph")
		    ], className="content_div"),
    ], id="main-container2", className="main-container"),
    
    html.Div([
        html.Div("Species Distribution Map", className="title_div"),
        html.Div([
        	html.Div([
			html.Div([
				html.H4("Search for a Species", className="h4Title"),
				dcc.Input(
				    id="species-input2",
				    className="search-input",
				    type="text",
				    placeholder="Type a scientific species name",
				),
				html.Button(
				    "Submit",
				    id="submit-button2",
				    className="submitButton"
				),
				html.Div(
				    id="error-message2",
				    className="error-message",
				)
			    ], className="search_div")],
			className="div_forms"),

		    html.Div([
			    dcc.Graph(
				id="distribution-map"
			    )], className="graph")
		    ], className="content_div"),
    ], id="main-container3", className="main-container"),
], id="div_body")

@app.callback(
    [Output("main-container1", "style"),
     Output("main-container2", "style"),
     Output("main-container3", "style")],
    [Input("btn-species-use", "n_clicks"),
     Input("btn-risk", "n_clicks"),
     Input("btn-map", "n_clicks")]
)
def toggle_content(btn_species_use, btn_risk, btn_maps):
    """
        Toggles style of page according to which graph (species usage, status progression or map distribution) is chosen

    """

    ctx = dash.callback_context
    if not ctx.triggered:
        button_id = "btn-species-use"  # Default
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    styles = {
        "btn-species-use": [
            {"display": "flex"}, 
            {"display": "none"},
            {"display": "none"}
        ],
        "btn-risk": [
            {"display": "none"},
            {"display": "flex"},  
            {"display": "none"}
        ],
        "btn-map": [
            {"display": "none"},
            {"display": "none"},
            {"display": "flex"}  
        ],
    }

    return styles.get(button_id, [{"display": "flex"}, {"display": "none"}, {"display": "none"}])



@app.callback(
    [Output("risk-graph", "figure"), Output("error-message", "children")],
    [Input("submit-button", "n_clicks"), Input("species-input", "n_submit")],
    State("species-input", "value")
)
def update_status_graph(n_clicks, n_submit, input_value):
    """
    Updates graph of status evolution according to a scientific name

    Args:
        input_value (str): possible species' scientific name

    Returns:
        go.Figure | dash.NoUpdate: figure containing status evolution of the given species
        string: containing possible error message
    
    """
    if input_value is None or input_value.strip() == "":
        return dash.no_update, ""
        
    input_value = clean_input(input_value)

    if input_value not in species:
        return dash.no_update, f"Error: '{input_value}' is not a valid species."

    status_enum = {'No Risk Data': 0,
            'Least Concern': 1,
            'Little Threatened': 2,
            'Vulnerable': 3,
            'Endangered': 4,
            'Critically Endangered': 5,
            'Regionally Extinct': 6,
            'Extinct in the Wild': 7,
            'Extinct': 8}
    fig = go.Figure()
    df_plot = filter_dataframe_by_specie(dataframe, input_value)
    fig.add_trace(go.Scatter(x=df_plot['Years'], y=df_plot['categoriaOrdem'],
                             mode='lines',
                             line=dict(color='darkred'),
                             name=input_value))
    fig.update_layout(autosize=True,
    	              xaxis_title='Years',
                      yaxis_title='Risk Category',
                      yaxis_range=[0,8],
                      yaxis=dict(tickmode='array',
                                 tickvals=list(status_enum.values()),
                                 ticktext=list(status_enum.keys())),
                      xaxis_showgrid=False,
                      yaxis_showgrid=False)
    
    return fig, ""
    
@app.callback(
    [Output("distribution-map", "figure"), Output("error-message2", "children")],
    [Input("submit-button2", "n_clicks"), Input("species-input2", "n_submit")],
    State("species-input2", "value")
)
def update_map(n_clicks, n_submit, input_value):
    """
    Updates habitat map according to a scientific name

    Args:
        input_value (str): possible species' scientific name

    Returns:
        go.Figure | dash.NoUpdate: map figure highlighting the areas inhabited by the given species
        string: containing possible error message
    
    """
    if input_value is None or input_value.strip() == "":
        return dash.no_update, ""
        
    input_value = clean_input(input_value)

    if input_value not in species:
        return dash.no_update, f"Error: '{input_value}' is not a valid species."

    filtered_gdf = gdf[gdf['sci_name'] == input_value]
    filtered_gdf['id'] = filtered_gdf.index
    
    fig = px.choropleth(
        filtered_gdf,
        geojson=filtered_gdf.__geo_interface__,
        locations='id',
        color_discrete_map= {input_value:'#871108'},
        color='sci_name',
    )
    fig.update_layout(
    	autosize=True,
        showlegend = False,
        margin=dict(l=0, r=0, t=0, b=0),
        geo=dict(
            showframe=False,
            showcoastlines=False,
            showcountries=True,
            projection_type='equirectangular',
            fitbounds="geojson",
        ),
        annotations = []
    )
    return fig, ""

@app.callback(
    [Output("default-mode-checklist", "value"), Output("country-mode-checklist", "value"), Output("year-mode-checklist", "value"), Output("category-checklist", "value")],
    [Input("default-mode-checklist", "value"), Input("country-mode-checklist", "value"), Input("year-mode-checklist", "value"), Input("category-checklist", "value")],
)
def update_mode_checklists(selected_default_mode, selected_country_mode, selected_year_mode, selected_category_mode):
    ctx = dash.callback_context  # contexto do callback para identificar o acionador

    triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]

    # Se o checklist de país foi acionado, ajusta para "stacked_country" e limpa o de ano
    if triggered_id == "country-mode-checklist" and selected_country_mode:  # se estiver selecionado, aplica "stacked_country"
        return [], ["country_mode"], [], []

    # Se o checklist de ano foi acionado, ajusta para "stacked_year" e limpa o de país
    elif triggered_id == "year-mode-checklist" and selected_year_mode:  # se estiver selecionado, aplica "stacked_year"
        return [], [], ["year_mode"], []

        
    elif triggered_id == "category-checklist" and selected_category_mode:  # se estiver selecionado, aplica "stacked_year"
        return [], [], [], ["category_mode"]
    return ["default_mode"], [], [], []

@app.callback(
    [Output("absolute-mode-checklist", "value"),
     Output("percentage-mode-checklist", "value")],
    [Input("absolute-mode-checklist", "value"),
     Input("percentage-mode-checklist", "value")]
)
def update_values_mode_checklists(absolute_value, percentage_value):
    ctx = dash.callback_context
    
    if not ctx.triggered:
        # Inicia com o modo padrão marcado
        return ["absolute_mode"], []

    triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if triggered_id == "absolute-mode-checklist" and absolute_value:
        return ["absolute_mode"], []

    elif triggered_id == "percentage-mode-checklist" and percentage_value:
        return [], ["percentage_mode"]

    return ["absolute_mode"], []  # Caso todos sejam desmarcados
        
# Callback para atualizar o dropdown de reino baseado no país selecionado
@app.callback(
    Output("kingdom-dropdown", "options"),
    [Input("country-dropdown", "value")]
)
def update_kingdom_options(selected_countries):
    #if not selected_countries:
        #return []
    kingdoms = dataframe["taxon.kingdom_name"].unique()
    return [{"label": k, "value": k} for k in kingdoms]

# Callbacks para atualizar os dropdowns sequencialmente (reino, filo, classe, ordem, família)
@app.callback(
    Output("phylum-dropdown", "options"),
    [Input("kingdom-dropdown", "value"), Input("country-dropdown", "value")]
)
def update_phylum_options(selected_kingdom, selected_countries):
    if not selected_kingdom:
        return []
    phyla = dataframe[dataframe["taxon.kingdom_name"] == selected_kingdom]["taxon.phylum_name"].unique()
    return [{"label": p, "value": p} for p in phyla]

@app.callback(
    Output("class-dropdown", "options"),
    [Input("phylum-dropdown", "value"), Input("kingdom-dropdown", "value")]
)
def update_class_options(selected_phylum, selected_kingdom):
    if selected_phylum is None:
        return []
    classes = dataframe[(dataframe["taxon.kingdom_name"] == selected_kingdom) & 
                 (dataframe["taxon.phylum_name"] == selected_phylum)]["taxon.class_name"].unique()
    return [{"label": c, "value": c} for c in classes]

@app.callback(
    Output("order-dropdown", "options"),
    [Input("class-dropdown", "value"), Input("phylum-dropdown", "value"), Input("kingdom-dropdown", "value")]
)
def update_order_options(selected_class, selected_phylum, selected_kingdom):
    if selected_class is None:
        return []
    orders = dataframe[(dataframe["taxon.kingdom_name"] == selected_kingdom) & 
                (dataframe["taxon.phylum_name"] == selected_phylum) &
                (dataframe["taxon.class_name"] == selected_class)]["taxon.order_name"].unique()
    return [{"label": o, "value": o} for o in orders]

@app.callback(
    Output("family-dropdown", "options"),
    [Input("order-dropdown", "value"), Input("class-dropdown", "value"), Input("phylum-dropdown", "value"), Input("kingdom-dropdown", "value")]
)
def update_family_options(selected_order, selected_class, selected_phylum, selected_kingdom):
    if selected_order is None:
        return []
    families = dataframe[(dataframe["taxon.kingdom_name"] == selected_kingdom) & 
                  (dataframe["taxon.phylum_name"] == selected_phylum) &
                  (dataframe["taxon.class_name"] == selected_class) &
                  (dataframe["taxon.order_name"] == selected_order)]["taxon.family_name"].unique()
    return [{"label": f, "value": f} for f in families]

@app.callback(
    Output("specie-dropdown", "options"),
    [Input("family-dropdown", "value"), Input("order-dropdown", "value"), Input("class-dropdown", "value"), Input("phylum-dropdown", "value"), Input("kingdom-dropdown", "value")]
)
def update_specie_options(selected_family, selected_order, selected_class, selected_phylum, selected_kingdom):
    if selected_family is None:
        return []
    species = dataframe[(dataframe["taxon.kingdom_name"] == selected_kingdom) & 
                  (dataframe["taxon.phylum_name"] == selected_phylum) &
                  (dataframe["taxon.class_name"] == selected_class) &
                  (dataframe["taxon.order_name"] == selected_order) &
                  (dataframe["taxon.family_name"] == selected_family)]["taxon.scientific_name"].unique()
    return [{"label": f, "value": f} for f in species]

@app.callback(
    Output("year-dropdown", "options"),
    [Input("specie-dropdown", "value"),
     Input("family-dropdown", "value"), Input("order-dropdown", "value"),
     Input("class-dropdown", "value"), Input("phylum-dropdown", "value"),
     Input("kingdom-dropdown", "value"), Input("country-dropdown", "value")]
)
def update_years_options(selected_specie, selected_family, selected_order, selected_class, selected_phylum, selected_kingdom, selected_countries):
    years = filter_years(dataframe, countries_dataframe, selected_specie, selected_family, selected_order, selected_class, selected_phylum, selected_kingdom, selected_countries)
    return [{"label": f, "value": f} for f in years]


# Callback para atualizar o gráfico de barras
@app.callback(
    Output("stacked-bar-chart", "figure"),
    [Input("specie-dropdown", "value"),
     Input("family-dropdown", "value"), Input("order-dropdown", "value"),
     Input("class-dropdown", "value"), Input("phylum-dropdown", "value"),
     Input("kingdom-dropdown", "value"), Input("country-dropdown", "value"),
     Input("year-dropdown", "value"), 
     Input("country-mode-checklist", "value"), Input("year-mode-checklist", "value"), 
     Input("percentage-mode-checklist", "value"), Input("category-checklist", "value")]
)
def update_graph(selected_specie, selected_family, selected_order, selected_class, selected_phylum, 
                 selected_kingdom, selected_countries, selected_years, country_mode, year_mode, percentage_mode, category_mode):
    """
        Updates barplot according to a selection of years, countries and species (or other taxonomic rank - see parameters)

    """
    
    filtered_df = dataframe.copy()
    fig = go.Figure()
    total_by_use = {'Food': 0,
                    'Pets/display animals, horticulture': 0,
                    'Medicine - human & veterinary': 0,
                    'Others': 0,
                    'Sport hunting/specimen collecting': 0,
                    'Construction or structural materials': 0,
                    'Fuels': 0,
                    'Handicrafts, jewellery, etc.': 0,
                    'Chemicals': 0,
                    'Wearing apparel, accessories': 0,
                    'Research': 0}
    total = 0
    all_uses = list(total_by_use.keys())
    if country_mode:
        selected_countries, dict_country_uses, total = update_graph_country(selected_specie, selected_family, selected_order, selected_class, selected_phylum, 
                                                 selected_kingdom, selected_countries, selected_years, filtered_df, total_by_use)
        # Calcular os percentuais para cada país
        create_bars(fig, all_uses, dict_country_uses, selected_countries, total, percentage_mode)
        if percentage_mode:
            update_fig_layout(fig, "Species Use by Country", "Percentage (%)", "Categories")
        else:
            update_fig_layout(fig, "Species Use by Country", "Count", "Categories")

    elif year_mode:
        selected_years, dict_year_uses, total = update_graph_year(selected_specie, selected_family, selected_order, selected_class, selected_phylum, selected_kingdom, selected_countries, selected_years, filtered_df, total_by_use)
        create_bars(fig, all_uses, dict_year_uses, selected_years, total, percentage_mode, years_mode=True)

        if percentage_mode:
            update_fig_layout(fig, "Species Use by Year", "Percentage (%)", "Categories")
        else:
            update_fig_layout(fig, "Species Use by Year", "Count", "Categories")
    elif category_mode:
        dict_categories, total = update_graph_risk(selected_specie, selected_family, selected_order, selected_class, selected_phylum, 
                 selected_kingdom, selected_countries, selected_years, filtered_df, total_by_use)
        create_bars(fig, all_uses, dict_categories, unique_categories, total, percentage_mode)
        if percentage_mode:
            update_fig_layout(fig, "Use of Species by Risk Category", "Percentage (%)", "Categories")
        else:
            update_fig_layout(fig, "Use of Species by Risk Category", "Count", "Categories")
        
    else:   
        if selected_countries:
            ids = list(countries_dataframe[countries_dataframe['Country'].isin(selected_countries)]['ID'].unique())
            filtered_df = filtered_df[filtered_df["taxon.sis_id"].isin(ids)]
        filtered_df = filter_taxonomy(filtered_df, selected_kingdom, selected_phylum, selected_class, selected_order, selected_family, selected_specie)
        if selected_years:
            years_dataframe = filter_some_years(filtered_df, selected_years)
            ids = list(years_dataframe['taxon.sis_id'].unique())
            filtered_df = filtered_df[filtered_df['taxon.sis_id'].isin(ids)]

        # Contar o número de espécies por categoria de uso
        usage_counts = generate_uses_count(filtered_df, uses_dataframe)
        for use in usage_counts.keys():
            total_by_use[use] += usage_counts[use]
            total += usage_counts[use]

        fig = create_figure_with_bar(total_by_use, percentage_mode)
        
        if percentage_mode:
            update_fig_layout(fig, "Use of Species", "Percentage (%)", "Categories")
        else:
            update_fig_layout(fig, "Use of Species", "Count", "Categories")
    
    return fig

if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8040)
