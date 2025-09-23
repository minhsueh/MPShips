__description__ = "This module provides elemental distribution visualization of MP API endpoints."
__author__ = "Min-Hsueh Chiu"


from dash import Dash, html, dcc, callback, Output, Input, MATCH, State, ctx
import plotly.express as px
import pandas as pd
import json
from ptable_plotly import ptable_heatmap_plotly
from ptable_info import elements_dict, empty_element_count
import sys
import uuid
from collections import defaultdict

from mp_api.client import MPRester
# import crystal_toolkit.helpers.layouts as ctl

API_KEY = "HPnhjtiVgcMGwniGlFFtr877nVA7skf6"

class MPDistAIO(html.Div):
    class ids:
        header = lambda aio:{
            "component": "MPDistAIO",
            "aio": aio,
            "subcomponents": "header"
        } 

        api_endpoint_dropdown = lambda aio:{
            "component": "MPDistAIO",
            "aio": aio,
            "subcomponents": "api_endpoint_dropdown"
        } 

        api_endpoint_histogram = lambda aio:{
            "component": "MPDistAIO",
            "aio": aio,
            "subcomponents": "api_endpoint_histogram"
        } 

        api_endpoint_div = lambda aio:{
            "component": "MPDistAIO",
            "aio": aio,
            "subcomponents": "api_endpoint_div"
        } 

        elemental_search_bar = lambda aio:{
            "component": "MPDistAIO",
            "aio": aio,
            "subcomponents": "elemental_search_bar"
        } 

        ptable_search_bar = lambda aio:{
            "component": "MPDistAIO",
            "aio": aio,
            "subcomponents": "ptable_search_bar"
        }

        ptable_search_button = lambda aio:{
            "component": "MPDistAIO",
            "aio": aio,
            "subcomponents": "ptable_search_button"
        }

        ptable_search_reset_button = lambda aio:{
            "component": "MPDistAIO",
            "aio": aio,
            "subcomponents": "ptable_search_reset_button"
        }

        ptable = lambda aio:{
            "component": "MPDistAIO",
            "aio": aio,
            "subcomponents": "ptable"
        } 

        ptable_div = lambda aio:{
            "component": "MPDistAIO",
            "aio": aio,
            "subcomponents": "ptable_div"
        } 

        ptable_title = lambda aio:{
            "component": "MPDistAIO",
            "aio": aio,
            "subcomponents": "ptable_title"
        } 

        ptable_loader = lambda aio:{
            "component": "MPDistAIO",
            "aio": aio,
            "subcomponents": "ptable_loader"
        } 

        whole_graph = lambda aio:{
            "component": "MPDistAIO",
            "aio": aio,
            "subcomponents": "whole_graph"
        } 


    ids = ids 

    def __init__(self, id=None, aio=None, **kwargs):

        if sys.version_info < (3, 10):
            # this is require for pymatgen
            raise RuntimeError("Python 3.10 or higher is required.")

        aio_id = aio
        if aio is None:
            # Otherwise use a uuid that has virtually no chance of collision.
            # Uuids are safe in dash deployments with processes
            # because this component's callbacks
            # use a stateless pattern-matching callback:
            # The actual ID does not matter as long as its unique and matches
            # the PMC `MATCH` pattern..
            aio_id = str(uuid.uuid4())
        self.aio = aio_id
        self.kwargs = kwargs

        # put your layout here 
        # header
        header = html.H1(
            children='Materials Project Elemental Data Statistics', 
            style={'textAlign':'center'},
            id=self.ids.header(aio_id)
        )

        # api_endpoint_dropdown
        endpoint_list = [
            'absorption',
            'bonds',
            'dielectric',
            'elasticity',
            # 'electronic_structure_bandstructure', 
            # 'electronic_structure_dos',
            'electronic_structure',
            # 'insertion_electrodes',
            'magnetism',
            'oxidation_states',
            'piezoelectric',
            'summary', 
            'thermo',
        ]
        api_endpoint_dropdown = dcc.Dropdown(
            options=endpoint_list, 
            value='absorption', 
            id=self.ids.api_endpoint_dropdown(aio_id),
            style={
                'flex': '1',
                # 'width': '10%'
            }
        )

        # histogram
        api_endpoint_histogram = html.Div(
            [
            dcc.Graph(id=self.ids.api_endpoint_histogram(aio_id))
            ], 
            style={
                'flex': '1',
                # 'width': '10%'
            }
        )

        # api_endpoint_div
        api_endpoint_div = html.Div([
                api_endpoint_dropdown,
                api_endpoint_histogram
            ], 
            style={
                # 'flex': '2',
                'display': 'flex',
                "border":"2px black solid",
                'width': '40%',
                'flexDirection': 'column',
                'padding': '10px'
            },
            id=self.ids.api_endpoint_div(aio_id)
        )

        # ptable_title
        ptable_title = html.H3(
            children=f'Elemental distribution', 
            style={'textAlign':'center'},
            id=self.ids.ptable_title(aio_id)
        )

        # ptable_search_bar
        ptable_search_bar = dcc.Input(
            id=self.ids.ptable_search_bar(aio_id),
            placeholder="e.g. Al-O",
            debounce=True
        )

        # ptable_search_button
        ptable_search_button = html.Button(
            'Search',
            id=self.ids.ptable_search_button(aio_id),
            n_clicks=0
        )

        # ptable_search_reset_button
        ptable_search_reset_button = html.Button(
            'Reset',
            id=self.ids.ptable_search_reset_button(aio_id),
            n_clicks=0
        )

        # p_table
        ptable = dcc.Graph(
            id=self.ids.ptable(aio_id)
        )

        # loader
        ptable_loader = dcc.Loading(
            id=self.ids.ptable_loader(aio_id),
            type="circle",  # options: "default", "circle", "dot", "cube"
            children=ptable
        )

        # ptable_div
        ptable_div = html.Div([
                # ptable_title,
                ptable_search_bar,
                ptable_search_button,
                ptable_search_reset_button,
                ptable_loader
            ], 
            style={
                'flex': '2',
                'width': '80%',
                'padding': '10px'
            },
            id=self.ids.ptable_div(aio_id)
        )

    

        whole_graph = html.Div([
                api_endpoint_div,
                ptable_div
            ], 
            style={
                'display': 'flex',
                'width': '100vw'
            },
            id=self.ids.whole_graph(aio_id)
            )
        


        super().__init__(children=[
            whole_graph

        ], **kwargs)


    # put all your callbacks here   
    @callback(
        Output(ids.api_endpoint_histogram(MATCH), 'figure'),
        Input(ids.api_endpoint_dropdown(MATCH), 'value')
    )
    def update_fig_enpoint(end_point):
        

        
        # histogram
        with open(f"./data/count.json", 'r') as json_file:
            endpoint_material_count = json.load(json_file)
        endpoint_count_df = pd.DataFrame(endpoint_material_count, index=[0]).T.reset_index()
        endpoint_count_df.columns = ['endpoint', 'count']
        endpoint_count_df.sort_values('count', inplace=True)
        colors = ['blue' if endpoint != end_point else 'red' for endpoint in endpoint_count_df['endpoint']]
        fig_hist = px.bar(
            endpoint_count_df, 
            x='endpoint', 
            y='count', 
            color=colors
        )
        fig_hist.update_layout(
            showlegend=False,
            margin=dict(l=0, r=0, t=20, b=20),
            yaxis=dict(type='log')
        )

        return(fig_hist)

    @callback(
        Output(ids.ptable_search_bar(MATCH), 'value'),
        Input(ids.ptable_search_reset_button(MATCH), 'n_clicks'),
        State(ids.ptable_search_bar(MATCH), 'value')
        # prevent_initial_call=True  # Optional: avoids resetting on page load
    )
    def reset_input(n_clicks, current_value):
        return ''

    @callback(
        Output(ids.ptable(MATCH), 'figure'),
        Input(ids.api_endpoint_dropdown(MATCH), 'value'),
        Input(ids.ptable_search_button(MATCH), 'n_clicks'),
        Input(ids.ptable_search_reset_button(MATCH), 'n_clicks'),
        Input(ids.ptable_search_bar(MATCH), 'value'),
    )
    def update_ptable(end_point, n_clicks, reset, elements_raw):
        triggered = ctx.triggered_id
        if n_clicks == 0 or not elements_raw or triggered == MPDistAIO.ids.ptable_search_reset_button(MATCH):
            with open(f"./data/count_ele_{end_point}.json", 'r') as json_file:
                element_count = json.load(json_file)
            ptable = ptable_heatmap_plotly(
                    element_count,
                    # hover_props=["atomic_number", "type"],
                    hover_props=["name"],
                    scaling_factor=0.7,
                )
            return ptable
        
        ptable = None
        element_list = elements_raw.split('-')

        if len(element_list) == 1:
            symbol = element_list[0]
            with open(f"./data/elemental/count_ele_ele_{end_point}.json", 'r') as json_file:
                    element_element_count = json.load(json_file)
                
            if symbol in element_element_count:
            
                # chemical elements distribution on specific element-based
                ptable = ptable_heatmap_plotly(
                        element_element_count[symbol],
                        hover_props=["name"],
                        scaling_factor=0.7
                    )
        else:
            with MPRester(API_KEY) as mpr:
                # get all materials id that contatins quired elements
                summaries = mpr.materials.summary.search(elements=element_list)
                mat_ids = [doc.material_id for doc in summaries]

            
                api_class = getattr(mpr.materials, end_point)
                docs = api_class.search(
                    # chemsys=elements_raw,
                    material_ids=mat_ids,
                    fields=['elements']
                )
                """
                docs = api_class.search(
                    # chemsys=elements_raw,
                    elements=element_list,
                    fields=['elements']
                )
                """
                print('---')
                print(len(mat_ids))
                print(len(docs))


                element_dict = defaultdict(int)

                for doc in docs:
                    for element in doc.elements:
                        element_dict[element.name] += 1
                
            ptable = ptable_heatmap_plotly(
                element_dict, 
                scaling_factor=0.7
            )


        if not ptable:
            ptable = ptable_heatmap_plotly(
                empty_element_count, 
                scaling_factor=0.7
            )
        return(ptable)
    

    


if __name__ == "__main__":
    app = Dash(__name__, suppress_callback_exceptions=True, use_pages=False)
    app.layout = html.Div(MPDistAIO(aio="test"))
    app.run_server(debug=True)