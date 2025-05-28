import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import folium
from streamlit_folium import st_folium
import numpy as np
from datetime import datetime, timedelta
import data_loader
import visualization
import utils

# Page configuration
st.set_page_config(
    page_title="Punjab Vaccination Coverage Dashboard",
    page_icon="💉",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Theme selector in sidebar
def apply_theme():
    theme = st.sidebar.selectbox(
        "🎨 Choose Theme",
        ["Light Theme", "Dark Theme"],
        help="Select your preferred theme"
    )
    
    if theme == "Dark Theme":
        st.markdown("""
        <style>
        .stApp {
            background-color: #0e1117;
            color: #fafafa;
        }
        .stSidebar {
            background-color: #262730;
        }
        .metric-card {
            background-color: #262730 !important;
            border-left-color: #ff6b6b !important;
            color: #fafafa !important;
        }
        .alert-box {
            background-color: #3d4043 !important;
            border-color: #ff6b6b !important;
            color: #fafafa !important;
        }
        div[data-testid="stMetricValue"] {
            color: #fafafa;
        }
        div[data-testid="stMetricLabel"] {
            color: #fafafa;
        }
        </style>
        """, unsafe_allow_html=True)
    
    return theme

# Apply theme
current_theme = apply_theme()

# Custom CSS for better styling
st.markdown("""
<style>
.metric-card {
    background-color: #f8f9fa;
    padding: 1rem;
    border-radius: 0.5rem;
    border-left: 4px solid #1f77b4;
}
.alert-box {
    background-color: #fff3cd;
    border: 1px solid #ffeaa7;
    border-radius: 0.25rem;
    padding: 0.75rem;
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

def main():
    st.title("🏥 Childhood Vaccination Coverage Dashboard - Rural Punjab")
    st.markdown("### Comprehensive analysis and monitoring of vaccination coverage across rural districts")
    
    # Sidebar for filters
    st.sidebar.header("📊 Dashboard Filters")
    
    # Try to load data
    try:
        vaccination_data = data_loader.load_vaccination_data()
        
        if vaccination_data is None or vaccination_data.empty:
            st.error("❌ **No vaccination data available**")
            st.markdown("""
            **To connect to authentic vaccination data sources:**
            
            📊 **Option 1: Upload Your Dataset**
            - Use the file uploader below to upload your vaccination data (CSV, Excel)
            - Ensure your data includes: district, village, child_id, vaccine_type, date, age_group, gender, coverage_percentage
            
            📡 **Option 2: Connect to Official APIs**
            - WHO Global Health Observatory
            - India Government Open Data Platform
            - Punjab State Health Department
            
            🏥 **Option 3: Database Connection**
            - Connect to your health information system database
            """)
            
            # File uploader for user data
            uploaded_file = st.file_uploader(
                "Upload your vaccination dataset", 
                type=['csv', 'xlsx', 'xls'],
                help="Upload a CSV or Excel file with vaccination coverage data"
            )
            
            if uploaded_file is not None:
                try:
                    if uploaded_file.name.endswith('.csv'):
                        uploaded_data = pd.read_csv(uploaded_file)
                    else:
                        uploaded_data = pd.read_excel(uploaded_file)
                    
                    st.success(f"✅ Successfully loaded {len(uploaded_data)} records from {uploaded_file.name}")
                    
                    # Validate uploaded data
                    required_cols = ['district', 'vaccine_type', 'coverage_percentage']
                    missing_cols = [col for col in required_cols if col not in uploaded_data.columns]
                    
                    if missing_cols:
                        st.error(f"Missing required columns: {missing_cols}")
                        st.info("Please ensure your data includes at least: district, vaccine_type, coverage_percentage")
                    else:
                        # Save uploaded data and reload
                        uploaded_data.to_csv('vaccination_data.csv', index=False)
                        st.rerun()
                        
                except Exception as e:
                    st.error(f"Error processing uploaded file: {str(e)}")
            
            return
            
        # Data filters in sidebar
        districts = ['All'] + sorted(vaccination_data['district'].unique().tolist())
        selected_district = st.sidebar.selectbox("🏘️ Select District", districts)
        
        vaccines = ['All'] + sorted(vaccination_data['vaccine_type'].unique().tolist())
        selected_vaccine = st.sidebar.selectbox("💉 Select Vaccine Type", vaccines)
        
        # Date range filter
        min_date = vaccination_data['date'].min().date()
        max_date = vaccination_data['date'].max().date()
        
        date_range = st.sidebar.date_input(
            "📅 Select Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
        
        # Age group filter
        age_groups = ['All'] + sorted(vaccination_data['age_group'].unique().tolist())
        selected_age_group = st.sidebar.selectbox("👶 Select Age Group", age_groups)
        
        # Gender filter
        genders = ['All', 'Male', 'Female']
        selected_gender = st.sidebar.selectbox("👥 Select Gender", genders)
        
        # Apply filters
        filtered_data = utils.apply_filters(
            vaccination_data, 
            selected_district, 
            selected_vaccine, 
            date_range, 
            selected_age_group, 
            selected_gender
        )
        
        if filtered_data.empty:
            st.warning("⚠️ No data matches the selected filters. Please adjust your filter criteria.")
            return
        
        # Key Performance Indicators
        st.header("📈 Key Performance Indicators")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_children = len(filtered_data)
            st.metric(
                label="📊 Total Children Tracked",
                value=f"{total_children:,}",
                help="Total number of children in the filtered dataset"
            )
        
        with col2:
            avg_coverage = filtered_data.groupby('vaccine_type')['coverage_percentage'].mean().mean()
            st.metric(
                label="💉 Average Coverage",
                value=f"{avg_coverage:.1f}%",
                delta=f"{avg_coverage - 75:.1f}% vs target",
                help="Average vaccination coverage percentage across all vaccines"
            )
        
        with col3:
            fully_vaccinated = len(filtered_data[filtered_data['fully_vaccinated'] == True])
            fully_vaccinated_pct = (fully_vaccinated / total_children) * 100 if total_children > 0 else 0
            st.metric(
                label="✅ Fully Vaccinated",
                value=f"{fully_vaccinated_pct:.1f}%",
                delta=f"{fully_vaccinated_pct - 90:.1f}% vs WHO target",
                help="Percentage of children with complete vaccination schedule"
            )
        
        with col4:
            districts_covered = filtered_data['district'].nunique()
            st.metric(
                label="🏘️ Districts Covered",
                value=f"{districts_covered}",
                help="Number of districts included in current selection"
            )
        
        # Alert for low coverage areas
        low_coverage_threshold = 70
        low_coverage_districts = utils.get_low_coverage_areas(filtered_data, low_coverage_threshold)
        
        if not low_coverage_districts.empty:
            st.markdown("""
            <div class="alert-box">
            <strong>⚠️ Attention Required:</strong> The following areas have vaccination coverage below 70%:
            </div>
            """, unsafe_allow_html=True)
            
            for _, district in low_coverage_districts.iterrows():
                st.warning(f"📍 **{district['district']}**: {district['coverage_percentage']:.1f}% coverage")
        
        # Main dashboard content
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "🗺️ Geographic Overview", 
            "📊 Coverage Analysis", 
            "📈 Trends & Timeline", 
            "👥 Demographics", 
            "📋 Detailed Reports"
        ])
        
        with tab1:
            st.header("🗺️ Geographic Vaccination Coverage")
            
            # Create geographic visualization using charts instead of problematic map
            district_coverage = filtered_data.groupby('district')['coverage_percentage'].mean().reset_index()
            district_coverage = district_coverage.sort_values('coverage_percentage', ascending=True)
            
            # Create horizontal bar chart showing district coverage with color coding
            fig_geo = px.bar(
                district_coverage, 
                x='coverage_percentage', 
                y='district',
                orientation='h',
                title="📍 Vaccination Coverage by Punjab District",
                labels={'coverage_percentage': 'Coverage Percentage (%)', 'district': 'District'},
                color='coverage_percentage',
                color_continuous_scale=['#ff4444', '#ff8800', '#44ff44'],  # Red to green
                text='coverage_percentage'
            )
            fig_geo.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            fig_geo.update_layout(height=400, showlegend=False)
            fig_geo.update_coloraxes(showscale=False)
            st.plotly_chart(fig_geo, use_container_width=True)
            
            # Add coverage status indicators
            st.markdown("**🎯 Coverage Status Legend:**")
            col_legend1, col_legend2, col_legend3 = st.columns(3)
            with col_legend1:
                st.markdown("🟢 **Excellent (≥90%)**")
            with col_legend2:
                st.markdown("🟡 **Good (75-89%)**") 
            with col_legend3:
                st.markdown("🔴 **Needs Attention (<75%)**")
            
            # District-wise coverage table
            st.subheader("📋 District-wise Coverage Summary")
            district_summary = utils.get_district_summary(filtered_data)
            st.dataframe(
                district_summary,
                use_container_width=True,
                hide_index=True
            )
        
        with tab2:
            st.header("📊 Vaccination Coverage Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Vaccine-wise coverage chart
                st.subheader("💉 Coverage by Vaccine Type")
                vaccine_chart = visualization.create_vaccine_coverage_chart(filtered_data)
                st.plotly_chart(vaccine_chart, use_container_width=True, key="vaccine_coverage_chart")
            
            with col2:
                # Coverage distribution
                st.subheader("📈 Coverage Distribution")
                distribution_chart = visualization.create_coverage_distribution(filtered_data)
                st.plotly_chart(distribution_chart, use_container_width=True, key="coverage_distribution_chart")
            
            # Detailed vaccine comparison
            st.subheader("🔍 Detailed Vaccine Comparison")
            comparison_chart = visualization.create_vaccine_comparison_chart(filtered_data)
            st.plotly_chart(comparison_chart, use_container_width=True, key="vaccine_comparison_chart")
        
        with tab3:
            st.header("📈 Vaccination Trends & Timeline")
            
            # Time series analysis
            st.subheader("📅 Coverage Trends Over Time")
            timeline_chart = visualization.create_timeline_chart(filtered_data)
            st.plotly_chart(timeline_chart, use_container_width=True, key="timeline_chart")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Monthly vaccination counts
                st.subheader("📊 Monthly Vaccination Activity")
                monthly_chart = visualization.create_monthly_activity_chart(filtered_data)
                st.plotly_chart(monthly_chart, use_container_width=True, key="monthly_chart")
            
            with col2:
                # Seasonal patterns
                st.subheader("🌡️ Seasonal Vaccination Patterns")
                seasonal_chart = visualization.create_seasonal_pattern_chart(filtered_data)
                st.plotly_chart(seasonal_chart, use_container_width=True, key="seasonal_chart")
        
        with tab4:
            st.header("👥 Demographic Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Age group analysis
                st.subheader("👶 Coverage by Age Group")
                age_chart = visualization.create_age_group_chart(filtered_data)
                st.plotly_chart(age_chart, use_container_width=True, key="age_group_chart")
            
            with col2:
                # Gender analysis
                st.subheader("👦👧 Coverage by Gender")
                gender_chart = visualization.create_gender_chart(filtered_data)
                st.plotly_chart(gender_chart, use_container_width=True, key="gender_chart")
            
            # Combined demographic analysis
            st.subheader("🔍 Detailed Demographic Breakdown")
            demographic_table = utils.get_demographic_analysis(filtered_data)
            st.dataframe(demographic_table, use_container_width=True)
        
        with tab5:
            st.header("📋 Detailed Reports & Data Export")
            
            # Summary statistics
            st.subheader("📊 Summary Statistics")
            summary_stats = utils.get_summary_statistics(filtered_data)
            
            col1, col2 = st.columns(2)
            with col1:
                st.json(summary_stats['coverage_stats'])
            with col2:
                st.json(summary_stats['demographic_stats'])
            
            # Action items and recommendations
            st.subheader("🎯 Action Items & Recommendations")
            recommendations = utils.generate_recommendations(filtered_data)
            for i, rec in enumerate(recommendations, 1):
                st.markdown(f"**{i}.** {rec}")
            
            # Data export functionality
            st.subheader("💾 Export Data")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("**📥 CSV Export**")
                csv_data = utils.prepare_csv_export(filtered_data)
                st.download_button(
                    label="Download CSV Data",
                    data=csv_data,
                    file_name=f"vaccination_data_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    help="Download filtered vaccination data as CSV file"
                )
            
            with col2:
                st.markdown("**📊 Excel Export**")
                excel_data = utils.prepare_excel_export(filtered_data)
                if excel_data:
                    st.download_button(
                        label="Download Excel Report",
                        data=excel_data,
                        file_name=f"vaccination_report_{datetime.now().strftime('%Y%m%d')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        help="Download comprehensive report with multiple sheets in Excel format"
                    )
                else:
                    st.error("Failed to generate Excel file")
            
            with col3:
                st.markdown("**📄 PDF Report**")
                pdf_data = utils.prepare_pdf_report(filtered_data)
                if pdf_data:
                    st.download_button(
                        label="Download PDF Report",
                        data=pdf_data,
                        file_name=f"vaccination_report_{datetime.now().strftime('%Y%m%d')}.pdf",
                        mime="application/pdf",
                        help="Download professional PDF report with charts and analysis"
                    )
                else:
                    st.error("Failed to generate PDF report")
            
            # Additional export options
            st.markdown("---")
            st.subheader("📋 Text Summary")
            summary_report = utils.generate_summary_report(filtered_data)
            st.download_button(
                label="Download Text Summary",
                data=summary_report,
                file_name=f"vaccination_summary_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain",
                help="Download concise text summary report"
            )
    
    except Exception as e:
        st.error(f"❌ **Application Error**: {str(e)}")
        st.markdown("""
        **Troubleshooting Steps:**
        1. Check data source connectivity
        2. Verify required data columns are present
        3. Ensure proper data format and encoding
        4. Contact system administrator if the issue persists
        """)
        
        # Show technical details in expander
        with st.expander("🔧 Technical Details"):
            st.code(str(e))

if __name__ == "__main__":
    main()
