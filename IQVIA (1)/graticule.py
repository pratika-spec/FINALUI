import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
import hydralit_components as hc
import datetime
#  from snowflake_sqlalchemy import create_snowflake_engine
st.set_page_config(layout="wide")

IC_conditions_synthetic_data = pd.read_csv("IC Sub Cohort Distribution  (1).csv")
ISPREP_indicator=pd.read_excel("AZD7442CE_COHORTS_ALL_COHORT_ENCOUNTERS_ISPREP.xlsx")
case_encounter=pd.read_excel("AZD7442CE_COHORTS_CASE_COHORT_INDEX_ENCOUNTER.xlsx")
cohorts_demographics=pd.read_excel("AZD7442CE_COHORTS_COHORT_DEMOGRAPHICS.xlsx")
control_encounters=pd.read_excel("AZD7442CE_COHORTS_CONTROL_COHORT_ENCOUNTERS.xlsx")
unexposed_demo=pd.read_excel("DEID_GRATICULE.SOW3EVUSHELD.VW_DEID_PATIENTS.xlsx")

ISPREP_indicator.columns=ISPREP_indicator.columns.str.lower() 
case_encounter.columns=case_encounter.columns.str.lower() 
cohorts_demographics.columns=cohorts_demographics.columns.str.lower() 
control_encounters.columns=control_encounters.columns.str.lower() 
unexposed_demo.columns=unexposed_demo.columns.str.lower()



df_display = IC_conditions_synthetic_data.copy()
df_display.index = [''] * len(df_display)  # Replace index with empty strings
df_display.index.name = ''  # Remove index name

# Set page configuration

# st.write(ISPREP_indicator.columns)
# st.write(case_encounter.columns)
# st.write(cohorts_demographics.columns)
# st.write(control_encounters.columns)


st.markdown(
        """
     <style>
    .main {
        padding-top: 8px !important; /* Adjust the padding value as needed */
    }
    .block-container {
        padding-top: 0 !important;
    }
    .block-content {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }
    .stMarkdown {
        margin-bottom: 0px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Rest of your code



# Hide Menu - Top Right Corner -  Three Doted Lines
hidden_menu = """
<style>
#MainMenu {
    visibility: hidden;
}
<style>"""

# Your menu_data and hc.nav_bar code here...
menu_data = [
    {'label':"Global Evidence Hub"},
    {'icon': "fa fa-home",'label':"Home"},
    {'icon': "far fa-copy", 'label':"FAQ"},
    {'icon': "fa fa-user", 'label':"My Account"}]

# Render the navigation bar

menu_id = hc.nav_bar(
    menu_definition=menu_data,
    override_theme={'txc_inactive': 'white','menu_background':'lightslategrey','txc_active':'black','option_active':None},
    hide_streamlit_markers=False, #will show the st hamburger as well as the navbar now!
    sticky_mode='pinned'#jumpy or not-jumpy, but sticky or pinned
)


# #------------------------------------------------------------------------------------------------------------------------------------------------------





filtered_cohorts = cohorts_demographics[cohorts_demographics['isexposed'] ==True]

overall = pd.merge(case_encounter, filtered_cohorts, on='masterpatientid', how='inner')

exposed_combined_df = pd.merge(overall, ISPREP_indicator, left_on='encounterid', right_on='encounterid', how='left')





control_encounters['indexdate'] = pd.to_datetime(control_encounters['indexdate'])
cohorts_demographics['birthdate'] = pd.to_datetime(cohorts_demographics['birthdate'])

filtered_encounters = control_encounters[control_encounters['evusheldexposure'] ==False]


ranked_encounters = filtered_encounters.groupby('masterpatientid').apply(lambda group: group.sort_values(['indexdate'], ascending=True)).reset_index(drop=True)


ranked_encounters['rank'] = ranked_encounters.groupby('masterpatientid').cumcount() + 1


filtered_ranked_encounters = ranked_encounters[ranked_encounters['rank'] == 1]



merged_data = pd.merge(filtered_ranked_encounters, unexposed_demo, on='masterpatientid', how='inner')


final_result = merged_data[merged_data['birthdate'].notnull()]
selected_columns = [
    'masterpatientid', 'indexdate', 'birthdate', 'gender', 'hispanic', 'race','rank']
unexposed_combined_df = final_result[selected_columns]















# Data Preprocessing

# Calculate Age
date_columns = ['birthdate', 'indexdate']
exposed_combined_df[date_columns] = exposed_combined_df[date_columns].apply(pd.to_datetime)
exposed_combined_df['age'] = (exposed_combined_df['indexdate'] - exposed_combined_df['birthdate']) / pd.Timedelta(days=365.25)
exposed_combined_df['age'] = exposed_combined_df['age'].round().astype(int)

unexposed_combined_df[date_columns] = unexposed_combined_df[date_columns].apply(pd.to_datetime)
unexposed_combined_df['age'] = (unexposed_combined_df['indexdate'] - unexposed_combined_df['birthdate']) /pd.Timedelta(days=365.25)
unexposed_combined_df['age'] = unexposed_combined_df['age'].round().astype(int)


# Rename Field Values
field_mappings = {
    'race': {'2': 'Asian', '3': 'Black or African American', '5': 'White', 'OT': 'Others'},
    'gender': {'M': 'Male', 'F': 'Female', 'OT': 'Others'},
    'hispanic': {'Y': 'Hispanic', 'N': 'Not Hispanic', 'R': 'Refuse to Answer', 'NI': 'No Information', 'UN': 'Unknown', 'OT': 'Other'},
    'encountertype': {'AV': 'Ambulatory Visit', 'ED': 'Emergency Department', 'EI': 'Emergency Department Admit to Inpatient Hospital Stay (permissible substitution)',
                      'IP': 'Inpatient Hospital Stay', 'IS': 'Non-Acute Institutional Stay', 'OS': 'Observation Stay',
                      'IC': 'Institutional Professional Consult (permissible substitution)', 'OA': 'Other Ambulatory Visit',
                      'NI': 'No Information', 'UN': 'Unknown', 'OT': 'Other', 'TH': 'Telehealth'}
}

exposed_combined_df.replace(field_mappings, inplace=True)
unexposed_combined_df.replace(field_mappings, inplace=True)


# # #---------------------------------------------------------------------------------------------------------------------------------------------

# Define Filters and Sidebars

@st.cache_data # Use caching to speed up data loading
def apply_filters(df, options1, options2, options3,options4):
    if 'All' in options1:
        filtered_df = df
    else:
        filtered_df = df[(df['age'] >= options1[0]) & (df['age'] <= options1[1])]

    if 'All' not in options2:
        filtered_df = filtered_df[filtered_df['gender'].isin(options2)]

    if 'All' not in options3:
        filtered_df = filtered_df[filtered_df['race'].isin(options3)]
        
    if 'All' not in options4:
        filtered_df = filtered_df[filtered_df['state'].isin(options4)]

    return filtered_df

# ------------------------------------------------------------------------------------------------------------------------------------------------
def show_intro():
    
    st.markdown("""
    <style>
        .left-margin {
            margin-left: 0px; /* Adjust the value as needed */
        }
    </style>

    <div class="left-margin">
        <strong>Definitions -</strong>
        <ul>
            <li>Exposed cohort is built using the medication administration table, where index date and dosage information is closest to ground truth and the unique patients are selected with a full dose (600mg) administration within the inclusion period, or 2 half dose (300mg) administrations in which the 2nd ("catchup") dose is within the inclusion period</li>
            <li>MEDADMINSTARTDATE is used as the index date for exposed cohort</li>
            <li>Unexposed cohort is built by selecting unique patients with at least one immunocompromised conditions and have at least one encounter within the inclusion period</li>
        </ul>
        <strong>Inclusion Criteria -</strong>
        <ul>
            <li>Inclusion Period - BA.2 Period
                <ul>
                    <li>Start Date - 01/24/2022</li>
                    <li>End Date - 06/19/2022</li>
                </ul>
            </li>
            <li>Age >= 12 years as of index date</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
# #-------------------------------------------------------- Demographic Distribution - Tab/Page 1 ------------------------------------------------

def show_demographics_anaysis(filtered_exposed_combined_df,filtered_unexposed_combined_df):
    
    
    # Statistics - Total Number of Imuunocompromised Patients
    
    ## Calculate Total Number of IC/eligible Patients
    total_patients = filtered_exposed_combined_df['masterpatientid'].nunique() + filtered_unexposed_combined_df['masterpatientid'].nunique()
    total_patients_formatted = "{:,}".format(total_patients)
    
    ## Calculate Total Number of Exposed Patients
    total_exposed_patients = len(filtered_exposed_combined_df['masterpatientid'].unique())
    total_exposed_patients_formatted = "{:,}".format(total_exposed_patients)
    
    ## Calculate Total Number of Unexposed Patients
    total_unexposed_patients = len(filtered_unexposed_combined_df['masterpatientid'].unique())
    total_unexposed_patients_formatted = "{:,}".format(total_unexposed_patients)
    
    ## Define custom CSS styles  
    ## Define custom CSS styles  
    style = """
    .metric-container {
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 0.7em;
        width: 800px;
    }
    .metric-container.total-immunocompromised {
    background-color: #c9c5c5; /* Color for total immunocompromised patients */
    width: 1500px;
    color: black;
    margin-bottom: 0;
    
    }

    .metric-container.total-exposed {
        background-color: none; /* Color for total immunocompromised patients */
        color: black;
        
    }

    .metric-container.total-unexposed {
        background-color: none; /* Color for total exposed patients */
        color: black;
    }

    .metric-label {
        font-size: 18px;
        margin-right: 1em;
        text-align: center;
        
    }

    .metric-value {
        font-size: 25px;
        font-weight: bold;
        text-align: center;
        
    }

    .container {
        display: flex;
        gap: 0;
    }
    """
    
    ## Render the custom styles  
    st.write('<style>{}</style>'.format(style), unsafe_allow_html=True)
    
    ## Display Total Number of Exposed Patients
    st.markdown(
    f'<div class="container">'
    f'<div class="metric-container total-immunocompromised">'
    f'<div class="metric-label"><center>Total Number of Immunocompromised Patients</center></div>'
    f'<div class="metric-value"><center>{total_patients_formatted}</center></div>'
    f'</div>'
    f'</div>',
    unsafe_allow_html=True
)
    st.write("")  # Blank line for spacing
    
    st.markdown(
    f'<div class="container">'
    f'<div class="metric-container total-exposed">'
    f'<div class="metric-label"><center>Patients who received AZD 7442 </center></div>'
    f'<div class="metric-value"><center>{total_exposed_patients_formatted}</center></div>'
    f'</div>'
    f'<div style="width: 50px;"></div>'  # Add space between the two boxes
    f'<div class="metric-container total-unexposed">'
    f'<div class="metric-label"><center>Patients who did not receive AZD 7442</center></div>'
    f'<div class="metric-value"><center>{total_unexposed_patients_formatted}</center></div>'
    f'</div>'
    f'</div>',
    unsafe_allow_html=True
)
    
    # Individual Graphs
    
    ## IC Patient Distribution by EVUSHELD Status
    colors = ["green","#4F81BD"]
    total_unique_patients = filtered_exposed_combined_df['masterpatientid'].nunique() + filtered_unexposed_combined_df['masterpatientid'].nunique()
    percent_exposed = filtered_exposed_combined_df['masterpatientid'].nunique() / total_unique_patients * 100
    percent_unexposed = filtered_unexposed_combined_df['masterpatientid'].nunique() / total_unique_patients * 100
    labels = ['Patients who received AZD 7442', 'Patients who did not receive AZD 7442']
    values = [filtered_exposed_combined_df['masterpatientid'].nunique(), filtered_unexposed_combined_df['masterpatientid'].nunique()]
    hover_data = {
        'label': labels,
        'percent': [f'{percent_exposed:.2f}%', f'{percent_unexposed:.2f}%'],
        'value': values
    }
    fig = px.pie(values=values, names=labels, hover_data=hover_data,
             title='IC Patient Distribution by EVUSHELD Status',
             labels={'label': 'Dataframe', 'value': 'Count', 'percent': 'Percentage'},color_discrete_sequence=colors)
    fig.update_traces(textinfo='percent', textposition='inside')
    fig.update_layout(legend={'font': {'size': 14}},legend_x=0.6,width=500, height=400,title_x=0.35)
    st.plotly_chart(fig, use_container_width=True) 
    
    ## Define numner of columns
    col1, col2 = st.columns(2)
    
    ## Column 1 Graphs
    with col1:
        
        st.markdown('<h3 style="font-size: 20px;font-weight: bold;">Demographic Distribution of Patients who received AZD 7442</h3>', unsafe_allow_html=True)

        ### Age Distribution of Exposed Population    
        age_counts = filtered_exposed_combined_df.groupby('age')['masterpatientid'].nunique().reset_index(name='unique_counts')
        total_patients = age_counts['unique_counts'].sum()
        age_counts['percentage'] = ((100 * age_counts['unique_counts'] / total_patients).round(1))
        fig1 = px.bar(
            age_counts,
            x='age',
            y='percentage',
            text='percentage', # Show percentage on bars
            hover_data={'age': True, 'unique_counts': True, 'percentage': True}, # Show age, counts, and percentage on hover
            title="Age Distribution of Patients who received AZD 7442",
            width=500,
            height=400,
        )
        fig1.update_traces(texttemplate='%{text:.1f} %')
        fig1.update_layout(xaxis_title=None, yaxis_title='% of Patients',xaxis=dict(showgrid=False),yaxis=dict(showgrid=False))
        st.plotly_chart(fig1)
         
        ### Gender Distribution of Exposed Population   
        colors = ["#365E8D","#8CB4E8","#A5C6E0"]
        unique_counts = filtered_exposed_combined_df.groupby('gender')['masterpatientid'].nunique()
        total_unique_patients = unique_counts.sum()
        percentage_unique_patients = (unique_counts / total_unique_patients) * 100
        fig3 = px.pie(percentage_unique_patients, values=percentage_unique_patients.values, names=percentage_unique_patients.index, 
                     labels={'names': 'gender', 'values': 'Percentage of Patients'}, title = 'Gender Distribution of Patients who received AZD 7442',color_discrete_sequence=colors)
        fig3.update_traces(hovertemplate='<b>%{label}</b><br>%{value:.1f}%<br>Count: %{text}<extra></extra>',
                           text=unique_counts,
                           textinfo= 'percent'
                           )
        fig3.update_layout(legend={'font': {'size': 14}},legend_x=0.9,width=500, height=400)
        st.plotly_chart(fig3, use_container_width=True)
        
        ### Race Distribution of Exposed Population   
        unique_counts = filtered_exposed_combined_df.groupby('race')['masterpatientid'].nunique()
        total_unique_patients = unique_counts.sum()
        percentage_unique_patients = (unique_counts / total_unique_patients) * 100
        sorted_value_counts = unique_counts.sort_values(ascending=True)
        sorted_percentages = percentage_unique_patients.loc[sorted_value_counts.index]
        fig2 = px.bar(y=sorted_value_counts.index, x=sorted_percentages.values,
                     text=sorted_percentages.apply(lambda x: f'{x:.1f}%'))
        fig2.update_traces(texttemplate='%{text}', textposition='auto')
        fig2.update_layout(title='Race Distribution of Patients who received AZD 7442',
                          yaxis_title=None, xaxis_title='% of Patients',width=500, height=400)
        st.plotly_chart(fig2)
        
        ### Hispanic Distribution of Exposed Population   
        unique_counts = filtered_exposed_combined_df.groupby('hispanic')['masterpatientid'].nunique()
        total_unique_patients = unique_counts.sum()
        percentage_unique_patients = (unique_counts / total_unique_patients) * 100
        sorted_value_counts = unique_counts.sort_values(ascending=True)
        sorted_percentages = percentage_unique_patients.loc[sorted_value_counts.index]
        fig4 = px.bar(y=sorted_value_counts.index, x=sorted_percentages.values,
                     text=sorted_percentages.apply(lambda x: f'{x:.1f}%'))
        fig4.update_traces(texttemplate='%{text}', textposition='auto')
        fig4.update_layout(title='Ethnicity Distribution of Patients who received AZD 7442',
                          yaxis_title=None, xaxis_title='% of Patients',width=500, height=400)
        st.plotly_chart(fig4)
        
    ## Column 2 Graphs
    with col2:
        
        st.markdown('<h3 style="font-size: 20px;font-weight: bold;">Demographic Distribution of Patients who did not receive AZD 7442</h3>', unsafe_allow_html=True)
        
        ### Age Distribution of Unexposed Population
        age_counts = filtered_unexposed_combined_df.groupby('age')['masterpatientid'].nunique().reset_index(name='unique_counts')
        total_patients = age_counts['unique_counts'].sum()
        age_counts['percentage'] = ((100 * age_counts['unique_counts'] / total_patients).round(1))
        fig5 = px.bar(
            age_counts,
            x='age',
            y='percentage',
            text='percentage', # Show percentage on bars
            hover_data={'age': True, 'unique_counts': True, 'percentage': True}, # Show age, counts, and percentage on hover
            title="Age Distribution of Patients who did not receive AZD 7442",
            width=500,
            height=400, 
            color_discrete_sequence=['green']
        )
        fig5.update_traces(texttemplate='%{text:.1f} %')
        fig5.update_layout(xaxis_title=None, yaxis_title='% of Patients',xaxis=dict(showgrid=False),yaxis=dict(showgrid=False))
        st.plotly_chart(fig5)
        
        ### Gender Distribution of Unexposed Population   
        colors = ["#254117", "#548235"]
        unique_counts = filtered_unexposed_combined_df.groupby('gender')['masterpatientid'].nunique()
        total_unique_patients = unique_counts.sum()
        percentage_unique_patients = (unique_counts / total_unique_patients) * 100
        fig6 = px.pie(percentage_unique_patients, values=percentage_unique_patients.values, names=percentage_unique_patients.index, 
                     labels={'names': 'gender', 'values': 'Percentage of Patients'}, title = 'Gender Distribution of Patients who did not receive AZD 7442',color_discrete_sequence=colors)
        fig6.update_traces(hovertemplate='<b>%{label}</b><br>%{value:.1f}%<br>Count: %{text}<extra></extra>',
                           text=unique_counts,
                           textinfo= 'percent'
                           )
        fig6.update_layout(legend={'font': {'size': 14}},legend_x=0.9,width=500, height=400)
        st.plotly_chart(fig6, use_container_width=True)  
        
        ### Race Distribution of Unexposed Population
        unique_counts = filtered_unexposed_combined_df.groupby('race')['masterpatientid'].nunique()
        total_unique_patients = unique_counts.sum()
        percentage_unique_patients = (unique_counts / total_unique_patients) * 100
        sorted_value_counts = unique_counts.sort_values(ascending=True)
        sorted_percentages = percentage_unique_patients.loc[sorted_value_counts.index]
        fig7 = px.bar(y=sorted_value_counts.index, x=sorted_percentages.values,
                     text=sorted_percentages.apply(lambda x: f'{x:.1f}%'),color_discrete_sequence=['green'])
        fig7.update_traces(texttemplate='%{text}', textposition='auto')
        fig7.update_layout(title='Race Distribution of Patients who did not receive AZD 7442',
                          yaxis_title=None, xaxis_title='% of Patients',width=500, height=400)
        st.plotly_chart(fig7)
        
        
        ### Hispanic Distribution of Unexposed Population   
        unique_counts = filtered_unexposed_combined_df.groupby('hispanic')['masterpatientid'].nunique()
        total_unique_patients = unique_counts.sum()
        percentage_unique_patients = (unique_counts / total_unique_patients) * 100
        sorted_value_counts = unique_counts.sort_values(ascending=True)
        sorted_percentages = percentage_unique_patients.loc[sorted_value_counts.index]
        fig8 = px.bar(y=sorted_value_counts.index, x=sorted_percentages.values,
                     text=sorted_percentages.apply(lambda x: f'{x:.1f}%'),color_discrete_sequence=['green'])
        fig8.update_traces(texttemplate='%{text}', textposition='auto')
        fig8.update_layout(title='Ethnicity Distribution of Patients who did not receive AZD 7442',
                          yaxis_title=None, xaxis_title='% of Patients',width=500, height=400)
        st.plotly_chart(fig8)
        
    st.markdown("""
 **Source:** The data presented above sourced from the Loopback US Datasource, involving data from 11 Health Systems or Data Partners. This data is not a comprehensive representation of the entire United States; it represents a subset of US.

 **Notes:**
 - The numbers are subject to change with successive iterations and inputs from additional sources/workstreams
 - Total patient volume in Loopback is xx
 - Out of total number of immunocompromised patients, the proportion of exposed vs unexposed is presented in this tab along with the Demographic distribution of both the cohorts
 - The parent cohorts of the following immunocompromised conditions have been considered for the analysis
      - Recipients of solid organ or islet cell transplant
      - Recipients of hematopoietic or stem cell transplant
      - Moderate or severe primary immunodeficiency
      - End Stage Renal Disease (ESRD) or on dialysis treatment
      - Solid tumors/ hematological malignancies on treatment (chemotherapy)
      - Solid tumors/ hematological malignancies on treatment (not on chemotherapy)
      - Active treatment with high dose corticosteroid, immunosuppressive or immunomodulatory treatment
      - Advanced or untreated human immunodeficiency virus (HIV) infection
 
""")

#-------------------------------------------------------------------------------------------------------------------------------------------------

def show_utilization_by_locations(filtered_exposed_combined_df,filtered_unexposed_combined_df):

    
    # Statistics - Total Number of Imuunocompromised Patients
    
     ## Calculate Total Number of Exposed Patients
    total_patients = filtered_exposed_combined_df['masterpatientid'].nunique() + filtered_unexposed_combined_df['masterpatientid'].nunique()
    total_patients_formatted = "{:,}".format(total_patients)
    
    total_exposed_patients = len(filtered_exposed_combined_df['masterpatientid'].unique())
    total_exposed_patients_formatted = "{:,}".format(total_exposed_patients)
    
    total_unexposed_patients = len(filtered_unexposed_combined_df['masterpatientid'].unique())
    total_unexposed_patients_formatted = "{:,}".format(total_unexposed_patients)
    
    ## Define custom CSS styles  
    ## Define custom CSS styles  
    style = """
    .metric-container {
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 0.7em;
        width: 800px;
    }
    .metric-container.total-immunocompromised {
    background-color: #c9c5c5; /* Color for total immunocompromised patients */
    width: 1500px;
    color: black;
    margin-bottom: 0;
    
    }

    .metric-container.total-exposed {
        background-color: none; /* Color for total immunocompromised patients */
        color: black;
        
    }

    .metric-container.total-unexposed {
        background-color: none; /* Color for total exposed patients */
        color: black;
    }

    .metric-label {
        font-size: 18px;
        margin-right: 1em;
        text-align: center;
        
    }

    .metric-value {
        font-size: 25px;
        font-weight: bold;
        text-align: center;
        
    }

    .container {
        display: flex;
        gap: 0;
    }
    """
    
    ## Render the custom styles  
    st.write('<style>{}</style>'.format(style), unsafe_allow_html=True)
    
    ## Display Total Number of Exposed Patients
    st.markdown(
    f'<div class="container">'
    f'<div class="metric-container total-immunocompromised">'
    f'<div class="metric-label"><center>Total Number of Immunocompromised Patients</center></div>'
    f'<div class="metric-value"><center>{total_patients_formatted}</center></div>'
    f'</div>'
    f'</div>',
    unsafe_allow_html=True
)
    st.write("")  # Blank line for spacing
    
    st.markdown(
    f'<div class="container">'
    f'<div class="metric-container total-exposed">'
    f'<div class="metric-label"><center>Patients who received AZD 7442 </center></div>'
    f'<div class="metric-value"><center>{total_exposed_patients_formatted}</center></div>'
    f'</div>'
    f'<div style="width: 50px;"></div>'  # Add space between the two boxes
    f'<div class="metric-container total-unexposed">'
    f'<div class="metric-label"><center>Patients who did not receive AZD 7442</center></div>'
    f'<div class="metric-value"><center>{total_unexposed_patients_formatted}</center></div>'
    f'</div>'
    f'</div>',
    unsafe_allow_html=True
)
    
    
    # Individual Graphs
        
   # Map - Patient Distribution by States

    ## Calculate the number of unique exposed patients per state
    patient_distribution = filtered_exposed_combined_df.groupby('state')['masterpatientid'].nunique().reset_index()

    ## Create hover text for each state
    patient_distribution['hover_text'] = 'Number of Exposed Patients: ' + patient_distribution['masterpatientid'].astype(str)

    ## Create the choropleth map
    fig = go.Figure(data=go.Choropleth(
        locations=patient_distribution['state'],  # DataFrame column with locations
        z=patient_distribution['masterpatientid'],  # DataFrame column with color values
        locationmode='USA-states',  # set of locations match entries in `locations`
        colorscale='Blues',
        colorbar_title="Number of Patients",
        marker_line_color='darkgray',
        marker_line_width=0.5,
        showscale=True,
        text=patient_distribution['hover_text'],
        hoverinfo='text'
    ))

    ## Update the layout of the map
    fig.update_layout(
        title_text='Number of Exposed Patients in Each State',
        title_x=0.3,
        geo_scope='usa',  # limit map scope to USA
        autosize=False,
        width=1000,  # width in pixels
        height=500,  # height in pixels
    )

    ## Define the threshold for text color differentiation
    threshold = 1000

    ## Add state labels to the map
    for _, row in patient_distribution.iterrows():
        if row['masterpatientid'] > threshold:
            text_color = 'white'  # Use white color for states with a higher number of patients
        else:
            text_color = 'black'  # Use black color for states with a lower number of patients

        fig.add_trace(
            go.Scattergeo(
                locations=[row['state']],
                locationmode='USA-states',
                text=[row['state']],
                mode='text',
                textfont=dict(
                    color=text_color,
                    size=10
                ),
                showlegend=False,
                hoverinfo='skip'  # Skip the hover for this trace
            )
        )
    
    ## Display Map
    st.plotly_chart(fig)
       
    
    st.markdown("""
 **Source:** The data presented above sourced from the Loopback US Datasource, involving data from 11 Health Systems or Data Partners. This data is not a comprehensive representation of the entire United States; it represents a subset of US.

 **Notes:**
 - The numbers are subject to change with successive iterations and inputs from additional sources/workstreams
 - Utilization tab/page focuses on the EVUSHELD administration across different locations
 
""")

#-------------------------------------------------------- Utilization Analysis Over Time ------------------------------------------------------

def show_utilization_over_time(filtered_exposed_combined_df,filtered_unexposed_combined_df):
    
    # Statistics - Total Number of Imuunocompromised Patients
    
     ## Calculate Total Number of Exposed Patients
    total_patients = filtered_exposed_combined_df['masterpatientid'].nunique() + filtered_unexposed_combined_df['masterpatientid'].nunique()
    total_patients_formatted = "{:,}".format(total_patients)
    
    total_exposed_patients = len(filtered_exposed_combined_df['masterpatientid'].unique())
    total_exposed_patients_formatted = "{:,}".format(total_exposed_patients)
    
    total_unexposed_patients = len(filtered_unexposed_combined_df['masterpatientid'].unique())
    total_unexposed_patients_formatted = "{:,}".format(total_unexposed_patients)
    
    ## Define custom CSS styles  
    style = """
    .metric-container {
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 0.7em;
        width: 800px;
    }
    .metric-container.total-immunocompromised {
    background-color: #c9c5c5; /* Color for total immunocompromised patients */
    width: 1500px;
    color: black;
    margin-bottom: 0;
    
    }

    .metric-container.total-exposed {
        background-color: none; /* Color for total immunocompromised patients */
        color: black;
        
    }

    .metric-container.total-unexposed {
        background-color: none; /* Color for total exposed patients */
        color: black;
    }

    .metric-label {
        font-size: 18px;
        margin-right: 1em;
        text-align: center;
        
    }

    .metric-value {
        font-size: 25px;
        font-weight: bold;
        text-align: center;
        
    }

    .container {
        display: flex;
        gap: 0;
    }
    """
    
    ## Render the custom styles  
    st.write('<style>{}</style>'.format(style), unsafe_allow_html=True)
    
    ## Display Total Number of Exposed Patients
    st.markdown(
    f'<div class="container">'
    f'<div class="metric-container total-immunocompromised">'
    f'<div class="metric-label"><center>Total Number of Immunocompromised Patients</center></div>'
    f'<div class="metric-value"><center>{total_patients_formatted}</center></div>'
    f'</div>'
    f'</div>',
    unsafe_allow_html=True
)
    st.write("")  # Blank line for spacing
    
    st.markdown(
    f'<div class="container">'
    f'<div class="metric-container total-exposed">'
    f'<div class="metric-label"><center>Patients who received AZD 7442 </center></div>'
    f'<div class="metric-value"><center>{total_exposed_patients_formatted}</center></div>'
    f'</div>'
    f'<div style="width: 50px;"></div>'  # Add space between the two boxes
    f'<div class="metric-container total-unexposed">'
    f'<div class="metric-label"><center>Patients who did not receive AZD 7442</center></div>'
    f'<div class="metric-value"><center>{total_unexposed_patients_formatted}</center></div>'
    f'</div>'
    f'</div>',
    unsafe_allow_html=True
)
    
    
    # Individual Graphs
    
    ## Define numner of columns
    col1, col2 = st.columns(2)
    
    ## Column 1 Graphs
    with col1:
        
        ### Utilization Over Time
        filtered_exposed_combined_df['indexdate'] = pd.to_datetime(filtered_exposed_combined_df['indexdate'])
        utilization_counts = filtered_exposed_combined_df.groupby(filtered_exposed_combined_df['indexdate'].dt.to_period('M'))['masterpatientid'].nunique().reset_index(name='unique_counts')
        utilization_counts['indexdate'] = utilization_counts['indexdate'].astype(str)
        fig = px.bar(
            utilization_counts,
            x='indexdate',
            y='unique_counts',
            text='unique_counts',
            hover_data={'indexdate': True, 'unique_counts': True},
            title='EVUSHELD Utilization Over Time',
            width=500,
            height=400,
        )
        fig.update_traces(texttemplate='%{text:.0f}')
        fig.update_layout(xaxis_title='Month', yaxis_title='Number of Patients', xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))
        st.plotly_chart(fig)
        

    with col2: 
    
    ### PrEP vs Other Expsoure Types Distribution
        colors = ["#365E8D","#8CB4E8"]
        filtered_exposed_combined_df['isprep'] = filtered_exposed_combined_df['isprep'].map({True: 'PrEP', False: 'Non-PrEP'})
        unique_counts = filtered_exposed_combined_df.groupby('isprep')['masterpatientid'].nunique()
        total_unique_patients = unique_counts.sum()
        percentage_unique_patients = (unique_counts / total_unique_patients) * 100
        fig3 = px.pie(percentage_unique_patients, values=percentage_unique_patients.values, names=percentage_unique_patients.index, 
                      labels={'names': 'exposure types', 'values': 'Percentage of Patients'}, title = 'PrEP vs Other Exposure Types Distribution',color_discrete_sequence=colors)
        fig3.update_traces(hovertemplate='<b>%{label}</b><br>%{value:.1f}%<br>Count: %{text}<extra></extra>',
                               text=unique_counts,
                               textinfo= 'percent'
                               )
        fig3.update_layout(legend={'font': {'size': 14}},legend_x=0.7,width=500, height=400)
        st.plotly_chart(fig3, use_container_width=True)
        
        
    # ### Full Dose vs Catch Up Dose Distribution
    #     colors = ["#365E8D","#8CB4E8"]
    #     filtered_exposed_combined_df['iscatchupdose'] = filtered_exposed_combined_df['iscatchupdose'].map({True: 'Catch Up Dose', False: 'Full Dose'})
    #     unique_counts = filtered_exposed_combined_df.groupby('iscatchupdose')['masterpatientid'].nunique()
    #     total_unique_patients = unique_counts.sum()
    #     percentage_unique_patients = (unique_counts / total_unique_patients) * 100
    #     fig4 = px.pie(percentage_unique_patients, values=percentage_unique_patients.values, names=percentage_unique_patients.index, 
    #                   labels={'names': 'Dose Type', 'values': 'Percentage of Patients'}, 
    #                   title = 'Full Dose vs Catch Up Dose Distribution',color_discrete_sequence=colors)
    #     fig4.update_traces(hovertemplate='<b>%{label}</b><br>%{value:.1f}%<br>Count: %{text}<extra></extra>',
    #                            text=unique_counts,
    #                            textinfo= 'percent'
    #                            )
    #     fig4.update_layout(legend={'font': {'size': 14}},legend_x=0.7,width=500, height=400)
    #     st.plotly_chart(fig4, use_container_width=True)
    
    st.markdown("""
 **Source:** The data presented above sourced from the Loopback US Datasource, involving data from 11 Health Systems or Data Partners. This data is not a comprehensive representation of the entire United States; it represents a subset of US.

 **Notes:**
 - The numbers are subject to change with successive iterations and inputs from additional sources/workstreams
 - Utilization tab/page focuses on the trend in EVUSHELD utilization over inclusion period and distribution of EVUSHLED exposure as PrEP vs other types of exposures
 
""")
    
#-------------------------------------------------------- Utilization Analysis by IC conditions  -------------------------------------------------

def show_utilization_by_ic_sub_cohorts(filtered_exposed_combined_df,filtered_unexposed_combined_df):

    
    # Statistics - Total Number of Imuunocompromised Patients
    
     ## Calculate Total Number of Exposed Patients
    total_patients = filtered_exposed_combined_df['masterpatientid'].nunique() + filtered_unexposed_combined_df['masterpatientid'].nunique()
    total_patients_formatted = "{:,}".format(total_patients)
    
    total_exposed_patients = len(filtered_exposed_combined_df['masterpatientid'].unique())
    total_exposed_patients_formatted = "{:,}".format(total_exposed_patients)
    
    total_unexposed_patients = len(filtered_unexposed_combined_df['masterpatientid'].unique())
    total_unexposed_patients_formatted = "{:,}".format(total_unexposed_patients)
    
    ## Define custom CSS styles  
    style = """
    .metric-container {
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 0.7em;
        width: 800px;
    }
    .metric-container.total-immunocompromised {
    background-color: #c9c5c5; /* Color for total immunocompromised patients */
    width: 1500px;
    color: black;
    margin-bottom: 0;
    
    }

    .metric-container.total-exposed {
        background-color: none; /* Color for total immunocompromised patients */
        color: black;
        
    }

    .metric-container.total-unexposed {
        background-color: none; /* Color for total exposed patients */
        color: black;
    }

    .metric-label {
        font-size: 18px;
        margin-right: 1em;
        text-align: center;
        
    }

    .metric-value {
        font-size: 25px;
        font-weight: bold;
        text-align: center;
        
    }

    .container {
        display: flex;
        gap: 0;
    }
    """
    
    ## Render the custom styles  
    st.write('<style>{}</style>'.format(style), unsafe_allow_html=True)
    
    ## Display Total Number of Exposed Patients
    st.markdown(
    f'<div class="container">'
    f'<div class="metric-container total-immunocompromised">'
    f'<div class="metric-label"><center>Total Number of Immunocompromised Patients</center></div>'
    f'<div class="metric-value"><center>{total_patients_formatted}</center></div>'
    f'</div>'
    f'</div>',
    unsafe_allow_html=True
)
    st.write("")  # Blank line for spacing
    
    st.markdown(
    f'<div class="container">'
    f'<div class="metric-container total-exposed">'
    f'<div class="metric-label"><center>Patients who received AZD 7442 </center></div>'
    f'<div class="metric-value"><center>{total_exposed_patients_formatted}</center></div>'
    f'</div>'
    f'<div style="width: 50px;"></div>'  # Add space between the two boxes
    f'<div class="metric-container total-unexposed">'
    f'<div class="metric-label"><center>Patients who did not receive AZD 7442</center></div>'
    f'<div class="metric-value"><center>{total_unexposed_patients_formatted}</center></div>'
    f'</div>'
    f'</div>',
    unsafe_allow_html=True
)
    
    
    # Format the numeric columns in the DataFrame to have comma separators for thousands
    numeric_columns = df_display.select_dtypes(include=[int, float]).columns
    df_display[numeric_columns] = df_display[numeric_columns].applymap('{:,.0f}'.format)
    st.write(" ")
    st.table(df_display)

#     formatted_table1 = df_display.style.set_properties(**{'text-align': 'center'}).set_table_styles([
#     {'selector': 'th:not(:first-child)', 'props': [('text-align', 'center')]},
#     {'selector': 'td:(:first-child)', 'props': [('text-align', 'center')]},
#     {'selector': 'th:nth-child(1), td:nth-child(1)', 'props': [('text-align', 'left')]} 
# ])
    st.write(" ")
    
    # styled_table_html = formatted_table1.to_html()
    # st.write(formatted_table1, unsafe_allow_html=True)
    
    st.write(" ")
    st.write(" ")
    st.markdown("""
 **Source:** The data presented above comes from the Loopback Datasource with 11 Health Systems or Data Partners
 
 **Notes:**
 - The numbers presented in the above table is synthetic; it is subject to change as analysis progresses
 - In this tab/page, exploratory analysis is done to understand the distribution of IC sub conditions within exposed & unexposed cohorts
 - The parent cohorts of the following immunocompromised conditions have been considered for the analysis
      - Recipients of solid organ or islet cell transplant
      - Recipients of hematopoietic or stem cell transplant
      - Moderate or severe primary immunodeficiency
      - End Stage Renal Disease (ESRD) or on dialysis treatment
      - Solid tumors/ hematological malignancies on treatment (chemotherapy)
      - Solid tumors/ hematological malignancies on treatment (not on chemotherapy)
      - Active treatment with high dose corticosteroid, immunosuppressive or immunomodulatory treatment
      - Advanced or untreated human immunodeficiency virus (HIV) infection
""")
    
#----------------------------------------
 
#-------------------------------------------------------------------------------------------------------------------------------------------------
def show_utilization_dashboard():
    # if st.button('Go Back to Select Data Source'):
    #     st.session_state.current_page = 'Utilization Analysis'
    #     st.experimental_rerun()
        
    
    # st.markdown('<h3 style="font-size: 30px;text-align: center;font-weight: bold;">Utilization Dashboard</h3>', unsafe_allow_html=True)
    col1, _, col2, _, col3 = st.columns([1.5, 0.1, 1.5, 0.01, 1.90])
    with col1:
        st.markdown(
            """
            <div style="margin-top: 10px; margin-bottom: 10px;">
                <span style="color: #337ab7; cursor: pointer;" onclick="window.location.href='./'">Global Evidence Hub</span> >
                <span style="color: #337ab7; cursor: pointer;" onclick="window.location.reload()">Descriptive</span> >
                Utilization Analysis
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.write("")
        interactive_box_content = """
                    <div style="{}">
                        <h2 style="margin-top: 10px;font-size: 16px;font-weight: bold; color: black;text-align: right;">Select a Data Source:</h2>
                    </div>
                """

        st.markdown(interactive_box_content, unsafe_allow_html=True)
    with col3:
        selected_option = st.selectbox("",["All", "US-Loopback (January 2022 to June 2022 -  BA.2 Period)", "US-Loopback (July 2022 to December 2022) ", "US-Loopback (January 2022 to June 2023)"],
            key="dropdown",index=1,
        )
    st.write("")
    col1, _, col2 = st.columns([0.4, 0.1, 1.5])
    
    with col1:
        st.markdown(
        '<div style="background-color: dimgrey; height: 40px; width: 300px; border-radius: 5px; display: flex; align-items: center; justify-content: center; margin-bottom: 10px;">'
        '<h2 style="color: white; font-size: 18px; text-align: center; margin: 0;">Filters</h2>'
        '</div>',
        unsafe_allow_html=True
    )
        st.markdown(
        '<h2 style="color: Black; font-size: 16px; font-weight: bold;margin: 0;">Demographic Filters</h2>'
        '</div>',
        unsafe_allow_html=True)
    
        State = ["All","AK","AZ","CA","CO","CT","DC","FL","GA","GU","HI","ID","IL","IN","KS","LA","MA","MD","ME","MI","MN","MO","MT","NC","NH","NI","NM","NV","NY","OH","OR","OT","PA","RI","SC","SD","TN","TX","UT","VA","WA","WI","WV","WY"]
        
    ## Define sidebar elements
        options11 = st.slider('Age', min_value=12, max_value=90, value=(11, 90))
        options12 = st.multiselect('Gender', options=['All'] + list(exposed_combined_df['gender'].unique().tolist()), default=['All'])
        options13 = st.multiselect('Race', options=['All'] + list(exposed_combined_df['race'].unique().tolist()), default=['All'])
        options14 = st.multiselect('State', options=State,default=State[0])

    ## Apply Filters on Data
        filtered_exposed_combined_df = apply_filters(exposed_combined_df, options11, options12, options13,options14)
        filtered_unexposed_combined_df = apply_filters(unexposed_combined_df, options11, options12, options13,options14)
        
    with col2:
        
    # Option menu for the descriptive analysis tab
        selected2 = option_menu(None, ["Introduction & Definitions", "Demographic Distribution of Unmatched Cohorts", "Utilization by Geographic Locations","Utilization Over Time and By Exposure Types", "Utilization by IC Sub Groups"],
        orientation="horizontal",styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon":{"display": "none"}, 
        "nav-link": {"font-size": "16px", "text-align": "center", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "lightcoral","font-weight": "inherit"},
    })
        
        if selected2 == "Demographic Distribution of Unmatched Cohorts":
            show_demographics_anaysis(filtered_exposed_combined_df,filtered_unexposed_combined_df)
        if selected2 == "Utilization by Geographic Locations":
            show_utilization_by_locations(filtered_exposed_combined_df,filtered_unexposed_combined_df)
        if selected2 == "Utilization Over Time and By Exposure Types":  
            show_utilization_over_time(filtered_exposed_combined_df,filtered_unexposed_combined_df)
        if selected2 == "Introduction & Definitions":
            show_intro()
        if selected2 == "Utilization by IC Sub Groups":
            show_utilization_by_ic_sub_cohorts(filtered_exposed_combined_df,filtered_unexposed_combined_df)
        st.markdown(hidden_menu, unsafe_allow_html=True)

def show_utilization_analysis():
    if st.button('Go Back to the Global Evidence Hub Page'):
        st.session_state.current_page = 'Global Evidence Hub'
        # st.experimental_rerun()
        
    descriptive_link = st.markdown('<a href="#">Descriptive</a>', unsafe_allow_html=True)
    
    if descriptive_link:
        st.session_state.current_page = "Global Evidence Hub"
    
    st.markdown(
        """
        <div style="margin-top: 10px; margin-bottom: 10px;">
            <span style="color: #337ab7; cursor: pointer;" onclick="window.location.href='./'">Global Evidence Hub</span> >
            <span style="color: #337ab7; cursor: pointer;" onclick="window.location.href='./descriptive'">Descriptive</span> >
            Utilization Analysis
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    # st.markdown('<h3 style="font-size: 30px;text-align: center;font-weight: bold;">Utilization Dashboard</h3>', unsafe_allow_html=True)
    st.markdown(
            """
            <p class='paragraph'>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Nam aliquam sem et tortor consequat id porta nibh venenatis. In nisl nisi scelerisque eu ultrices. Id venenatis a condimentum vitae sapien pellentesque. Etiam tempor orci eu lobortis elementum nibh tellus molestie. Viverra mauris in aliquam sem fringilla ut morbi tincidunt. Arcu felis bibendum ut tristique et egestas quis. Aenean sed adipiscing diam donec adipiscing tristique. Vel risus commodo viverra maecenas accumsan lacus vel facilisis volutpat. Id volutpat lacus laoreet non curabitur gravida arcu ac..
            </p>
            """,
            unsafe_allow_html=True,
        )
    col1,col2,col3 = st.columns(3)
    
    with col1: 
        st.write(" ")
        st.write(" ")
        interactive_box_content = """
                    <div style="{}">
                        <h2 style="margin-top: 10px;font-size: 16px;font-weight: bold; color: black;text-align: right;">Select a Data Source:</h2>
                    </div>
                """

        st.markdown(interactive_box_content, unsafe_allow_html=True)
    with col2:
        st.write(" ")
        selected_option = st.selectbox(
        "",
        ["All", "US-Loopback (January 2022 to June 2022 -  BA.2 Period)", "US-Loopback (July 2022 to December 2022) ", "US-Loopback (January 2022 to June 2023)"],
        key="dropdown"
    )

        if selected_option == "US-Loopback (January 2022 to June 2022 -  BA.2 Period)":
            st.session_state.current_page = 'Option 1 Analysis'
            # st.experimental_rerun()

    # Apply CSS styling to the dropdown to adjust its width and alignment
    st.markdown(
        f"""
        <style>
            .dropdown {{
                width: 200px; /* Adjust the width as needed */
                margin: 0 auto; /* Center-align the dropdown */
            }}
        </style>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown(hidden_menu, unsafe_allow_html=True)
    
    
def show_faq_analysis():
    st.markdown(hidden_menu,  unsafe_allow_html=True)
    st.header("FAQ Section")
    
# Function to show the home page
def show_home_page():  
        st.markdown(
            """
            <p class='paragraph'>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Nam aliquam sem et tortor consequat id porta nibh venenatis. In nisl nisi scelerisque eu ultrices. Id venenatis a condimentum vitae sapien pellentesque. Etiam tempor orci eu lobortis elementum nibh tellus molestie. Viverra mauris in aliquam sem fringilla ut morbi tincidunt. Arcu felis bibendum ut tristique et egestas quis. Aenean sed adipiscing diam donec adipiscing tristique. Vel risus commodo viverra maecenas accumsan lacus vel facilisis volutpat. Id volutpat lacus laoreet non curabitur gravida arcu ac..
            </p>
            """,
            unsafe_allow_html=True,
        )
        col1, _, col2, _, col3 = st.columns([1.5, 0.1, 1.5, 0.1, 1.4])

        with col1:
            container_style = """
                text-align: left;
                margin-top: 0px;
                margin-left: 10px;
            """

            interactive_box_content = """
                <div style="{}">
                    <h2 style="font-size: 23px;font-weight: bold; color: orange;text-align: center;">Descriptive</h2>
                    <p style="text-align: left;">
                        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
                    </p>
                    <p style="text-align: left;font-weight: bold;">
                       Choose the dashboard
                </div>
            """.format(container_style)

            st.markdown(interactive_box_content, unsafe_allow_html=True)
            
            if st.button('Utilization Analysis'):
                    st.session_state.current_page = 'Utilization Analysis'
                    st.experimental_rerun()

            if st.button('Variant Analysis'):
                    st.session_state.current_page = 'Variant Analysis'
                    st.experimental_rerun() 


        with col2:
                container_style = """
                    text-align: left;
                    margin-top: 0px;
                    margin-left: 10px;
                """

                interactive_box_content = """
                    <div style="{}">
                        <h2 style="font-size: 23px; color: #03870e;font-weight: bold;text-align: center;">Comparative Effectiveness</h2>
                        <p style="text-align: left;">
                            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
                        </p>
                        <p style="text-align: left;font-weight: bold;">
                           Choose the dashboard
                    </div>
                """.format(container_style)

                st.markdown(interactive_box_content, unsafe_allow_html=True)

                if st.button('Outcomes Analysis'):
                    st.session_state.current_page = 'Outcomes Analysis'
                    st.experimental_rerun()

                    

        with col3:
                container_style = """
                    text-align: left;
                    margin-top: 0px;
                    margin-left: 10px;
                """

                interactive_box_content = """
                    <div style="{}">
                        <h2 style="font-size: 23px;font-weight: bold; color: black;text-align: center;">News</h2>
                    </div>
                """.format(container_style)

                st.markdown(interactive_box_content, unsafe_allow_html=True)
                items = [
                    "July’23 version of comparative effectiveness analysis is now live",
                    "Next refresh for Italy scheduled on August 31st",
                    "Recent guideline change by FDA"
                ]

                # Define the big square symbol and space after the pointer
                square_pointer = '\u25A2&nbsp;&nbsp;'

                # Render the list items with the big square symbol using Streamlit markdown method
                for item in items:
                    st.markdown(f"{square_pointer}{item}", unsafe_allow_html=True)

                if st.button('See More',key='See More'):
                    st.session_state.current_page = 'See More'
                    st.experimental_rerun()
                
        st.write( """
                    <style>
                    .stButton>button {
                        background-color: white;
                        margin: 0 5px;
                        padding: 10;
                        font-size: 18px;
                        width: 425px;
                        color: black;
                        boarder: blue
                    }
                    </style>
                    """
                    , unsafe_allow_html=True
                )  
        st.markdown(hidden_menu,  unsafe_allow_html=True)

####################################################################################################################
###################################################################################################################3

def main():
    # Check if the "FAQ" item is selected and execute the faq_analysis function
    if menu_id == 'FAQ':
        show_faq_analysis()
    elif menu_id == 'Home':
        show_home_page()
    # Check if the "Global Evidence Hub" item is selected and execute the appropriate function based on the current page state
    elif menu_id == 'Global Evidence Hub':
        if 'current_page' not in st.session_state:
            st.session_state.current_page = 'Global Evidence Hub'

        # If the current page is 'Global Evidence Hub', display the home page
        if st.session_state.current_page == 'Global Evidence Hub':
            show_home_page()   

        # If the current page is 'Utilization Analysis', display the appropriate content
        elif st.session_state.current_page == 'Utilization Analysis':
            show_utilization_analysis()     

        elif st.session_state.current_page == 'Option 1 Analysis':
            show_utilization_dashboard()
# Run the app
if __name__ == "__main__":
    main()