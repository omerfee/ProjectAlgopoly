import plotly.graph_objects as go
import pandas as pd
import streamlit as st


st.set_page_config(
    page_title= 'Inputs',
    page_icon='📊'
)


# Transforming txt data to data frame for inputs

ic_safety_factor = pd.read_table('inputs/' + 'ic-safety-factor.txt', delim_whitespace=True, index_col = 'ic_name')
arc_distance = pd.read_table('inputs/' + 'arc-distance.txt', delim_whitespace=True, index_col = 'ic_name')
ic_ramp = pd.read_table('inputs/' + 'ic-ramp.txt', delim_whitespace=True, index_col = 'ic_name')
ic_init = pd.read_table('inputs/' + 'ic-init.txt', delim_whitespace=True, index_col = 'ic_name')
ic_prod_per_line = pd.read_table('inputs/' + 'ic-prod-per-line.txt', delim_whitespace=True, index_col = 'ic_name')
hub_demand = pd.read_table('inputs/' + 'hub-demand.txt', delim_whitespace=True, index_col='hub_name')
ic_coordinates = pd.read_table('inputs/' + 'ic_coordinates.txt', sep=',', index_col = 'ic_name')
hub_coordinates = pd.read_table('inputs/' + 'hub_coordinates.txt', sep=',', index_col = 'hub_name')


IC_NUMBER = len(ic_init.index)
HUB_NUMBER = len(hub_demand.index)
PERIOD_NUMBER = len((ic_prod_per_line.T).index)



st.header('2 - Inputs')
st.markdown("""
The MIP model uses five data tables as inputs. The tabs below shows the inputed data of the problem instance reported in this document and the formats of the data tables in general. [All data tables can also be accessed as a spreadsheet file here. ](https://docs.google.com/spreadsheets/d/1iAUJlXSaR1SQZ7LDzb9cMgDL4sSq-5KJ/edit?usp=sharing&ouid=102054403470164424175&rtpof=true&sd=true)
""")
st.sidebar.markdown("# 2 - Inputs 📊")





distance_tab, ic_prod_per_line_tab, allowed_ramping_tab, hub_demand_tab, ic_init_tab = st.tabs(['Table 1 - Distances','Table 2 - Production-Per-Line at ICs','Table 3 - Allowed Ramping', 'Table 4 - Demand at Hubs', 'Table 5 - IC Init'])

with distance_tab:
  st.markdown('### Distances')
  st.dataframe(arc_distance)


with ic_init_tab:
  st.markdown('### Inital Attributes of ICs')
  st.dataframe(ic_init)


large_rockwell_template = dict(
    layout=go.Layout(title_font=dict(family="Rockwell", size=24))
)

with ic_prod_per_line_tab:
  ic_prod_per_line_fig = go.Figure()

  for i in range(1,IC_NUMBER + 1):
    ic_prod_per_line_fig.add_trace(go.Line(
      x = ['t_{}'.format(i) for i in range(1,PERIOD_NUMBER + 1)],
      y = [x for x in ic_prod_per_line.loc['ic_{}'.format(i)]],
      name = 'ic_{}'.format(i),
      mode = 'lines+markers'
    ))

    ic_prod_per_line_fig.update_layout(
    title = 'production-per-line of ICs over periods',
    xaxis_title = 'Period',
    yaxis_title = 'production-per-line',
    template = large_rockwell_template,
    plot_bgcolor="white"
  )
  st.plotly_chart(ic_prod_per_line_fig)


  total_prod_per_line_fig = go.Figure()
  total_prod_per_line_fig.add_trace(go.Line(

    x = ['t_{}'.format(i) for i in range(1,PERIOD_NUMBER + 1)],
    y = ic_prod_per_line.sum(),
    name = 'total production',
    mode = 'lines+markers'

  ))

  total_prod_per_line_fig.update_layout(
    title = 'total production-per-line of ICs over periods',
    xaxis_title = 'Period',
    yaxis_title = 'production-per-line',
    template = large_rockwell_template,
    plot_bgcolor="white"
    
  )
  

  st.plotly_chart(total_prod_per_line_fig)
  
  st.dataframe(ic_prod_per_line)


with allowed_ramping_tab:
  st.header('Allowed Ramping at ICs')
  st.dataframe(ic_ramp)

with hub_demand_tab:
  hub_demand_fig = go.Figure()

  for i in range(1,HUB_NUMBER +1):
    hub_demand_fig.add_trace(go.Line(
      x = ['t_{}'.format(i) for i in range(1,PERIOD_NUMBER + 1)],
      y = [x for x in hub_demand.loc['hub_{}'.format(i)]],
      name = 'hub_{}'.format(i),
      mode = 'lines+markers'
    ))

    hub_demand_fig.update_layout(
    title = 'Demand at Hubs',
    xaxis_title = 'Period',
    yaxis_title = 'Hub Demand',
    template = large_rockwell_template,
    plot_bgcolor="white"
  )

  st.plotly_chart(hub_demand_fig)

  total_demand_at_hubs_fig = go.Figure()
  total_demand_at_hubs_fig.add_trace(go.Line(

  x = ['t_{}'.format(i) for i in range(1,PERIOD_NUMBER + 1)],
  y = hub_demand.sum(),
  name = 'total demand at hubs over period',
  mode = 'lines+markers'

))

  total_demand_at_hubs_fig.update_layout(
    title = 'total demand at hubs over period',
    xaxis_title = 'Period',
    yaxis_title = 'total hub demand',
    template = large_rockwell_template,
    plot_bgcolor="white"
    
  )
  

  st.plotly_chart(total_demand_at_hubs_fig)

  st.dataframe(hub_demand)
