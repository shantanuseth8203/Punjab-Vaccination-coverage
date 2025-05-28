import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import folium
import streamlit as st
import numpy as np
from datetime import datetime

def create_coverage_map(df):
    """Create a folium map showing vaccination coverage by geographic area."""
    try:
        if df.empty:
            return None
        
        # Calculate average coverage by district
        district_coverage = df.groupby('district').agg({
            'coverage_percentage': 'mean',
            'village': 'first'  # Get a representative village name
        }).reset_index()
        
        # Create base map centered on Punjab
        punjab_coords = [30.7333, 76.7794]  # Approximate center of Punjab
        m = folium.Map(location=punjab_coords, zoom_start=8, tiles='OpenStreetMap')
        
        # Add markers for each district
        for _, row in district_coverage.iterrows():
            # Generate approximate coordinates for demonstration
            # In production, you would have actual geographic coordinates
            lat = punjab_coords[0] + np.random.uniform(-1, 1)
            lon = punjab_coords[1] + np.random.uniform(-1, 1)
            
            coverage = row['coverage_percentage']
            
            # Color code based on coverage percentage
            if coverage >= 90:
                color = 'green'
                icon = 'ok-sign'
            elif coverage >= 75:
                color = 'orange'
                icon = 'warning-sign'
            else:
                color = 'red'
                icon = 'remove-sign'
            
            folium.Marker(
                location=[lat, lon],
                popup=f"""
                <b>{row['district']}</b><br>
                Coverage: {coverage:.1f}%<br>
                Status: {'Good' if coverage >= 90 else 'Needs Attention' if coverage >= 75 else 'Critical'}
                """,
                tooltip=f"{row['district']}: {coverage:.1f}%",
                icon=folium.Icon(color=color, icon=icon)
            ).add_to(m)
        
        # Add legend
        legend_html = """
        <div style="position: fixed; 
                    bottom: 50px; left: 50px; width: 150px; height: 90px; 
                    background-color: white; border:2px solid grey; z-index:9999; 
                    font-size:14px; font-weight: bold;
                    ">
        <p style="margin: 10px;"><i class="fa fa-circle" style="color:green"></i> ≥90% Coverage</p>
        <p style="margin: 10px;"><i class="fa fa-circle" style="color:orange"></i> 75-89% Coverage</p>
        <p style="margin: 10px;"><i class="fa fa-circle" style="color:red"></i> <75% Coverage</p>
        </div>
        """
        # Add legend using a simpler method
        try:
            m.get_root().html.add_child(folium.Element(legend_html))
        except:
            # Fallback if legend fails
            pass
        
        return m
        
    except Exception as e:
        st.error(f"Error creating map: {str(e)}")
        return None

def create_vaccine_coverage_chart(df):
    """Create a bar chart showing coverage by vaccine type."""
    try:
        vaccine_coverage = df.groupby('vaccine_type')['coverage_percentage'].mean().reset_index()
        vaccine_coverage = vaccine_coverage.sort_values('coverage_percentage', ascending=True)
        
        fig = px.bar(
            vaccine_coverage,
            x='coverage_percentage',
            y='vaccine_type',
            orientation='h',
            title='Average Vaccination Coverage by Vaccine Type',
            labels={'coverage_percentage': 'Coverage Percentage (%)', 'vaccine_type': 'Vaccine Type'},
            color='coverage_percentage',
            color_continuous_scale='RdYlGn',
            range_color=[0, 100]
        )
        
        # Add target line at 90%
        fig.add_vline(
            x=90, 
            line_dash="dash", 
            line_color="red",
            annotation_text="WHO Target (90%)",
            annotation_position="top"
        )
        
        fig.update_layout(
            height=400,
            showlegend=False,
            xaxis=dict(range=[0, 100]),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig
        
    except Exception as e:
        st.error(f"Error creating vaccine coverage chart: {str(e)}")
        return go.Figure()

def create_coverage_distribution(df):
    """Create a histogram showing distribution of coverage percentages."""
    try:
        fig = px.histogram(
            df,
            x='coverage_percentage',
            nbins=20,
            title='Distribution of Vaccination Coverage Percentages',
            labels={'coverage_percentage': 'Coverage Percentage (%)', 'count': 'Number of Records'},
            color_discrete_sequence=['#1f77b4']
        )
        
        # Add target lines
        fig.add_vline(x=90, line_dash="dash", line_color="green", annotation_text="WHO Target")
        fig.add_vline(x=75, line_dash="dash", line_color="orange", annotation_text="Minimum Target")
        
        fig.update_layout(height=400)
        
        return fig
        
    except Exception as e:
        st.error(f"Error creating coverage distribution: {str(e)}")
        return go.Figure()

def create_vaccine_comparison_chart(df):
    """Create a detailed comparison chart of all vaccines."""
    try:
        # Calculate statistics by vaccine
        vaccine_stats = df.groupby('vaccine_type').agg({
            'coverage_percentage': ['mean', 'std', 'min', 'max', 'count']
        }).round(2)
        
        vaccine_stats.columns = ['mean', 'std', 'min', 'max', 'count']
        vaccine_stats = vaccine_stats.reset_index()
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Average Coverage', 'Coverage Range', 'Standard Deviation', 'Sample Size'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Average coverage
        fig.add_trace(
            go.Bar(x=vaccine_stats['vaccine_type'], y=vaccine_stats['mean'], name='Average'),
            row=1, col=1
        )
        
        # Coverage range (min-max)
        fig.add_trace(
            go.Scatter(
                x=vaccine_stats['vaccine_type'], 
                y=vaccine_stats['max'], 
                mode='markers', 
                name='Max',
                marker=dict(color='green', size=8)
            ),
            row=1, col=2
        )
        fig.add_trace(
            go.Scatter(
                x=vaccine_stats['vaccine_type'], 
                y=vaccine_stats['min'], 
                mode='markers', 
                name='Min',
                marker=dict(color='red', size=8)
            ),
            row=1, col=2
        )
        
        # Standard deviation
        fig.add_trace(
            go.Bar(x=vaccine_stats['vaccine_type'], y=vaccine_stats['std'], name='Std Dev'),
            row=2, col=1
        )
        
        # Sample size
        fig.add_trace(
            go.Bar(x=vaccine_stats['vaccine_type'], y=vaccine_stats['count'], name='Count'),
            row=2, col=2
        )
        
        fig.update_layout(height=600, showlegend=False, title_text="Comprehensive Vaccine Analysis")
        
        return fig
        
    except Exception as e:
        st.error(f"Error creating vaccine comparison chart: {str(e)}")
        return go.Figure()

def create_timeline_chart(df):
    """Create a timeline chart showing coverage trends over time."""
    try:
        # Group by date and calculate average coverage
        timeline_data = df.groupby(['date', 'vaccine_type'])['coverage_percentage'].mean().reset_index()
        
        fig = px.line(
            timeline_data,
            x='date',
            y='coverage_percentage',
            color='vaccine_type',
            title='Vaccination Coverage Trends Over Time',
            labels={'coverage_percentage': 'Coverage Percentage (%)', 'date': 'Date'}
        )
        
        # Add target line
        fig.add_hline(
            y=90, 
            line_dash="dash", 
            line_color="red",
            annotation_text="WHO Target (90%)"
        )
        
        fig.update_layout(height=500, hovermode='x unified')
        
        return fig
        
    except Exception as e:
        st.error(f"Error creating timeline chart: {str(e)}")
        return go.Figure()

def create_monthly_activity_chart(df):
    """Create a chart showing monthly vaccination activity."""
    try:
        monthly_data = df.groupby(['year', 'month']).size().reset_index(name='vaccinations')
        monthly_data['date_str'] = monthly_data['year'].astype(str) + '-' + monthly_data['month'].astype(str).str.zfill(2)
        
        fig = px.bar(
            monthly_data,
            x='date_str',
            y='vaccinations',
            title='Monthly Vaccination Activity',
            labels={'vaccinations': 'Number of Vaccinations', 'date_str': 'Month'}
        )
        
        fig.update_layout(height=400, xaxis={'tickangle': 45})
        
        return fig
        
    except Exception as e:
        st.error(f"Error creating monthly activity chart: {str(e)}")
        return go.Figure()

def create_seasonal_pattern_chart(df):
    """Create a chart showing seasonal vaccination patterns."""
    try:
        seasonal_data = df.groupby('month')['coverage_percentage'].mean().reset_index()
        seasonal_data['month_name'] = pd.to_datetime(seasonal_data['month'], format='%m').dt.strftime('%B')
        
        fig = px.line(
            seasonal_data,
            x='month_name',
            y='coverage_percentage',
            title='Seasonal Vaccination Patterns',
            labels={'coverage_percentage': 'Average Coverage (%)', 'month_name': 'Month'},
            markers=True
        )
        
        fig.update_layout(height=400, xaxis={'tickangle': 45})
        
        return fig
        
    except Exception as e:
        st.error(f"Error creating seasonal pattern chart: {str(e)}")
        return go.Figure()

def create_age_group_chart(df):
    """Create a chart showing coverage by age group."""
    try:
        age_data = df.groupby('age_group')['coverage_percentage'].mean().reset_index()
        age_data = age_data.sort_values('coverage_percentage', ascending=False)
        
        fig = px.bar(
            age_data,
            x='age_group',
            y='coverage_percentage',
            title='Vaccination Coverage by Age Group',
            labels={'coverage_percentage': 'Coverage Percentage (%)', 'age_group': 'Age Group'},
            color='coverage_percentage',
            color_continuous_scale='Viridis'
        )
        
        fig.add_hline(y=90, line_dash="dash", line_color="red")
        fig.update_layout(height=400, showlegend=False)
        
        return fig
        
    except Exception as e:
        st.error(f"Error creating age group chart: {str(e)}")
        return go.Figure()

def create_gender_chart(df):
    """Create a chart showing coverage by gender."""
    try:
        gender_data = df.groupby(['gender', 'vaccine_type'])['coverage_percentage'].mean().reset_index()
        
        fig = px.bar(
            gender_data,
            x='vaccine_type',
            y='coverage_percentage',
            color='gender',
            barmode='group',
            title='Vaccination Coverage by Gender',
            labels={'coverage_percentage': 'Coverage Percentage (%)', 'vaccine_type': 'Vaccine Type'}
        )
        
        fig.add_hline(y=90, line_dash="dash", line_color="red")
        fig.update_layout(
            height=400,
            xaxis={'tickangle': 45}
        )
        
        return fig
        
    except Exception as e:
        st.error(f"Error creating gender chart: {str(e)}")
        return go.Figure()
