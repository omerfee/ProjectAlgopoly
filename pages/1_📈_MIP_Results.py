import plotly.graph_objects as go
import numpy as np
import pandas as pd
import glob
import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(
    page_title= 'MIP Results',
    page_icon='📈'
)


#accessing the names of txt files in the inputs and outputs folder.
input_path = 'inputs/*.txt'
input_files = glob.glob(input_path)

input_file_names = []

for i in input_files:
  input_file_names.append(i.split('\\')[1])

output_path = 'outputs/*.txt'
output_files = glob.glob(output_path)

output_file_names = []
for i in output_files:
  output_file_names.append(i.split('\\')[1])

epsilon_list = []
for i in output_file_names:
  if i.startswith("flow"):
    epsilon_list.append((i.split('_')[3]).split('.txt')[0])
    
st.markdown('\n**Given Epsilon**')
given_epsilon = st.selectbox('Please select given epsilon for the results.', options=epsilon_list)



# Transforming txt data to data frame for inputs

ic_safety_factor = pd.read_table('inputs/' + 'ic-safety-factor.txt', delim_whitespace=True, index_col = 'ic_name')
arc_distance = pd.read_table('inputs/' + 'arc-distance.txt', delim_whitespace=True, index_col = 'ic_name')
ic_ramp = pd.read_table('inputs/' + 'ic-ramp.txt', delim_whitespace=True, index_col = 'ic_name')
ic_init = pd.read_table('inputs/' + 'ic-init.txt', delim_whitespace=True, index_col = 'ic_name')
ic_prod_per_line = pd.read_table('inputs/' + 'ic-prod-per-line.txt', delim_whitespace=True, index_col = 'ic_name')
hub_demand = pd.read_table('inputs/' + 'hub-demand.txt', delim_whitespace=True, index_col='hub_name')
ic_coordinates = pd.read_table('inputs/' + 'ic_coordinates.txt', sep=',', index_col = 'ic_name')
hub_coordinates = pd.read_table('inputs/' + 'hub_coordinates.txt', sep=',', index_col = 'hub_name')


# Transforming txt data to data frame for outputs

selected_ic_solution = pd.read_table('outputs/' + 'ic_results_eps_{}.txt'.format(given_epsilon), sep=',', index_col = 'ic_name')
safety_results = pd.read_table('outputs/' + 'safety_results_eps_{}.txt'.format(given_epsilon), sep=',')
flow_results = pd.read_table('outputs/' + 'flow_results_eps_{}.txt'.format(given_epsilon), sep = ',')
pareto_frontier_results = pd.read_table('outputs/' + 'pareto-frontier-results.txt',sep=',')

IC_NUMBER = len(ic_init.index)
HUB_NUMBER = len(hub_demand.index)
PERIOD_NUMBER = len((ic_prod_per_line.T).index)



st.header('3 - MIP Results')
st.sidebar.markdown("# 3 - MIP Results 📈")
st.markdown(""" 
We here take a closer look at the decision space in 3.2. In this experiment, we define safety factor for inventory / outflow ratio as 1.5.

The problem can be considered with two objectives:

1. minimize the total costs
2. minimize the maximum deviations from the desired safety factor at the end of time periods.

""")



st.markdown('### 3.1 - Pareto Optimal Solutions')

large_rockwell_template = dict(
    layout=go.Layout(title_font=dict(family="Rockwell", size=24))
)

pareto_frontier_results_fig = go.Figure()
pareto_frontier_results_fig.add_trace(go.Scatter(
  x = pareto_frontier_results['maximum_deviation'],
  y = pareto_frontier_results['total_cost'],
  mode = 'markers'
))

pareto_frontier_results_fig.update_layout(
  title = 'pareto-optimal frontier of bi-objective case',
  xaxis_title = 'largest deviation from the desired inventory/sales ratio',
  yaxis_title = 'cost',
  template = large_rockwell_template,
  plot_bgcolor="white"
)

st.plotly_chart(pareto_frontier_results_fig)






st.markdown('### 3.2 - IC-based results of the selected solution')



number_of_lines_tab, period_production_tab, flow_tab, final_inventory_tab, ic_safety_tab = st.tabs(['Table 1 - Number of Lines', 'Table 2 - Period Production','Table 3 - Flow', 'Table 4 - Final Inventory', 'Table 5 - IC Safety' ])

with number_of_lines_tab:
  number_of_lines_fig = go.Figure()

  for i in range(1,IC_NUMBER + 1):
    number_of_lines_fig.add_trace(go.Line(
      x = ['t_{}'.format(i) for i in range(1,PERIOD_NUMBER + 1)],
      y = [x for x in selected_ic_solution.loc['ic_{}'.format(i)]['numberoflines']],
      name = 'ic_{}'.format(i),
      mode = 'lines+markers'
      
      
    ))

  number_of_lines_fig.update_layout(
    title = 'Number of Lines',
    xaxis_title = 'Period',
    yaxis_title = 'Number of Lines',
    template = large_rockwell_template,
    plot_bgcolor="white"
  )
  st.plotly_chart(number_of_lines_fig)


with period_production_tab:
  period_production_fig = go.Figure()

  for i in range(1,IC_NUMBER + 1):
    period_production_fig.add_trace(go.Line(
      x = ['t_{}'.format(i) for i in range(1,PERIOD_NUMBER + 1)],
      y = [x for x in selected_ic_solution.loc['ic_{}'.format(i)]['periodproduction']],
      name = 'ic_{}'.format(i),
      mode = 'lines+markers'
      
      
    ))

  period_production_fig.update_layout(
    title = 'Period Production',
    xaxis_title = 'Period',
    yaxis_title = 'Production',
    template = large_rockwell_template,
    plot_bgcolor="white"
  )
  st.plotly_chart(period_production_fig)


with flow_tab:
  flow_fig = go.Figure()

  for i in range(1,IC_NUMBER + 1):
    flow_fig.add_trace(go.Line(
      x = ['t_{}'.format(i) for i in range(1,PERIOD_NUMBER + 1)],
      y = [x for x in selected_ic_solution.loc['ic_{}'.format(i)]['flow']],
      name = 'ic_{}'.format(i),
      mode = 'lines+markers'
    ))

  flow_fig.update_layout(
    title = 'Flow',
    xaxis_title = 'Period',
    yaxis_title = 'Flow',
    template = large_rockwell_template,
    plot_bgcolor="white"
  )
  st.plotly_chart(flow_fig)


with final_inventory_tab:
  final_inventory_fig = go.Figure()

  for i in range(1,IC_NUMBER + 1):
    final_inventory_fig.add_trace(go.Line(
      x = ['t_{}'.format(i) for i in range(1,PERIOD_NUMBER + 1)],
      y = [x for x in selected_ic_solution.loc['ic_{}'.format(i)]['finalinventory']],
      name = 'ic_{}'.format(i),
      mode = 'lines+markers'
      
      
    ))

  final_inventory_fig.update_layout(
    title = 'Final Inventory',
    xaxis_title = 'Period',
    yaxis_title = 'Final Inventory',
    template = large_rockwell_template,
    plot_bgcolor="white"
  )
  st.plotly_chart(final_inventory_fig)



with ic_safety_tab:
  ic_safety_fig = go.Figure()

  for i in range(1, IC_NUMBER + 1):
    ic_safety_fig.add_trace(go.Line(
      x = ['t_{}'.format(i) for i in range(1,PERIOD_NUMBER + 1)],
      y = [x for x in (selected_ic_solution.loc['ic_{}'.format(i)]['finalinventory'] / selected_ic_solution.loc['ic_{}'.format(i)]['flow'])],
      name = 'ic_{}'.format(i),
      mode = 'lines+markers'
      
        
      ))

  ic_safety_fig.update_layout(
    title = 'IC Safety',
    xaxis_title = 'Period',
    yaxis_title = 'Final Inventory / Flow',
    template = large_rockwell_template,
    plot_bgcolor="white"
  )
  st.plotly_chart(ic_safety_fig)
  







st.markdown('### 3.3 - Global Results of the Selected Solution (period-based)')
total_demand_tab, total_period_production_tab, total_flow_tab, total_final_inventory_tab, safety_ratio_tab = st.tabs(['Table 1 - Total Demand', 'Table 2 - Total Production', 'Table 3 - Total Flow', 'Table 4 - Total Final Inventory', 'Table 5 - Safety Ratio'])


with total_demand_tab:
  total_hub_demand = []
  for i in range(1,PERIOD_NUMBER + 1):
    total_hub_demand.append(hub_demand['t_{}'.format(i)].sum())

  total_hub_demand_fig = go.Figure()
  total_hub_demand_fig.add_trace(go.Line(
    x = ['t_{}'.format(i) for i in range(1,PERIOD_NUMBER + 1)],
    y = total_hub_demand,
    mode = 'lines+markers'
  ))

  total_hub_demand_fig.update_layout(
  title = 'Total Demand',
  xaxis_title = 'Period',
  yaxis_title = 'Demand',
  template = large_rockwell_template,
  plot_bgcolor="white"
 )
  st.plotly_chart(total_hub_demand_fig)



with total_period_production_tab:
  total_period_production = []
  for i in range(1, PERIOD_NUMBER + 1):
    total_period_production.append(selected_ic_solution.loc[selected_ic_solution['period'] == 't_{}'.format(i)]['periodproduction'].sum())

  total_period_production_fig = go.Figure()
  total_period_production_fig.add_trace(go.Line(
    x = ['t_{}'.format(i) for i in range(1,PERIOD_NUMBER + 1)],
    y = total_period_production,
    mode = 'lines+markers'))

  total_period_production_fig.update_layout(
  title = 'Total Period Production',
  xaxis_title = 'Period',
  yaxis_title = 'Production',
  template = large_rockwell_template,
  plot_bgcolor="white"
  )
  st.plotly_chart(total_period_production_fig)

with total_flow_tab:
  total_flow = []
  for i in range(1,PERIOD_NUMBER + 1):
    total_flow.append(selected_ic_solution.loc[selected_ic_solution['period'] == 't_{}'.format(i)]['flow'].sum())

  total_flow_fig = go.Figure()
  total_flow_fig.add_trace(go.Line(
    x = ['t_{}'.format(i) for i in range(1,PERIOD_NUMBER + 1)],
    y = total_flow,
    mode = 'lines+markers'))

  total_flow_fig.update_layout(
  title = 'Total Flow',
  xaxis_title = 'Period',
  yaxis_title = 'Flow',
  template = large_rockwell_template,
  plot_bgcolor="white"
  )
  st.plotly_chart(total_flow_fig)



with total_final_inventory_tab:
  total_final_inventory = []
  for i in range(1,PERIOD_NUMBER + 1):
    total_final_inventory.append(selected_ic_solution.loc[selected_ic_solution['period'] == 't_{}'.format(i)]['finalinventory'].sum())
  
  total_final_inventory_fig = go.Figure()
  total_final_inventory_fig.add_trace(go.Line(
    x = ['t_{}'.format(i) for i in range(1,PERIOD_NUMBER + 1)],
    y = total_final_inventory,
    mode = 'lines+markers'))

  total_final_inventory_fig.update_layout(
  title = 'Total Final Inventory',
  xaxis_title = 'Period',
  yaxis_title = 'Inventory',
  template = large_rockwell_template,
  plot_bgcolor="white"
  )
  st.plotly_chart(total_final_inventory_fig)



with safety_ratio_tab:
  safety_ratio_fig = go.Figure()

  safety_ratio_fig.add_trace(go.Line(
    x = ['t_{}'.format(i) for i in range(1,PERIOD_NUMBER + 1)],
    y = [x for x in safety_results['safetyratio']],
    name = 'ic_{}'.format(i),
    mode = 'lines+markers'
    
      
    ))

  safety_ratio_fig.update_layout(
    title = 'Safety Ratio',
    xaxis_title = 'Period',
    yaxis_title = 'Safety Ratio',
    template = large_rockwell_template,
    plot_bgcolor="white"
  )
  st.plotly_chart(safety_ratio_fig)
  






st.markdown('### 3.4 - The IC-hub assignments and flows of the selected solution')


flow_map_fig = folium.Map(
location = [ic_coordinates.loc['ic_3']['ic_x'], ic_coordinates.loc['ic_3']['ic_y']],
zoom_start = 4)

for i in range(1, IC_NUMBER + 1):
  folium.Marker(
    [ic_coordinates.loc['ic_{}'.format(i)]['ic_x'], ic_coordinates.loc['ic_{}'.format(i)]['ic_y']],
    popup = 'IC {}'.format(i),
    tooltip = 'IC {}'.format(i),
    icon=folium.Icon(color="green", icon="info-sign")
  ).add_to(flow_map_fig)

for j in range(1, HUB_NUMBER + 1):
  folium.Marker(
    [hub_coordinates.loc['hub_{}'.format(j)]['hub_x'], hub_coordinates.loc['hub_{}'.format(j)]['hub_y']],
    popup = 'Hub {}'.format(j),
    tooltip = 'Hub {}'.format(j),
    icon=folium.Icon(color="blue", icon="info-sign")
  ).add_to(flow_map_fig)


selected_time_period = st.select_slider('Please select time period for result.', options=['t_{}'.format(period) for period in range(1, PERIOD_NUMBER +1)])


for j in range(1, IC_NUMBER + 1):
  temp_data = flow_results[(flow_results['period'] == str(selected_time_period)) & (flow_results['ic_name'] == 'ic_{}'.format(j)) & (flow_results['flow'] > 0)]
  
  temp_ic_name = 'ic_{}'.format(j)
  
  for temp_hub_name in (temp_data['hub_name']):
    temp_flow = [x for x in temp_data[temp_data['hub_name']=='{}'.format(temp_hub_name)]['flow']][0]

    flow_lines_for_map = folium.PolyLine(locations = [ [ic_coordinates.loc[temp_ic_name]['ic_x'], ic_coordinates.loc[temp_ic_name]['ic_y']], [ hub_coordinates.loc[str(temp_hub_name)]['hub_x'], hub_coordinates.loc[temp_hub_name]['hub_y']]],
                         popup = 'from {} to {}, flow = {}'.format(temp_ic_name, temp_hub_name, str(temp_flow)),
                         tooltip = 'from {} to {}, flow = {}'.format(temp_ic_name, temp_hub_name, str(temp_flow)),
                         weight = 5)
    flow_map_fig.add_child(flow_lines_for_map)




st_folium(flow_map_fig, width = 725)

