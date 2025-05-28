import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import streamlit as st

def apply_filters(df, district, vaccine, date_range, age_group, gender):
    """Apply selected filters to the dataframe."""
    try:
        filtered_df = df.copy()
        
        # District filter
        if district != 'All':
            filtered_df = filtered_df[filtered_df['district'] == district]
        
        # Vaccine filter
        if vaccine != 'All':
            filtered_df = filtered_df[filtered_df['vaccine_type'] == vaccine]
        
        # Date range filter
        if len(date_range) == 2:
            start_date, end_date = date_range
            filtered_df = filtered_df[
                (filtered_df['date'].dt.date >= start_date) & 
                (filtered_df['date'].dt.date <= end_date)
            ]
        
        # Age group filter
        if age_group != 'All':
            filtered_df = filtered_df[filtered_df['age_group'] == age_group]
        
        # Gender filter
        if gender != 'All':
            filtered_df = filtered_df[filtered_df['gender'] == gender]
        
        return filtered_df
        
    except Exception as e:
        st.error(f"Error applying filters: {str(e)}")
        return pd.DataFrame()

def get_low_coverage_areas(df, threshold=70):
    """Identify areas with coverage below the specified threshold."""
    try:
        district_coverage = df.groupby('district')['coverage_percentage'].mean().reset_index()
        low_coverage = district_coverage[district_coverage['coverage_percentage'] < threshold]
        return low_coverage.sort_values('coverage_percentage')
        
    except Exception as e:
        st.error(f"Error identifying low coverage areas: {str(e)}")
        return pd.DataFrame()

def get_district_summary(df):
    """Generate a summary table by district."""
    try:
        summary = df.groupby('district').agg({
            'coverage_percentage': ['mean', 'min', 'max', 'std'],
            'child_id': 'nunique',
            'vaccine_type': 'nunique',
            'village': 'nunique'
        }).round(2)
        
        # Flatten column names
        summary.columns = [
            'Avg Coverage (%)', 'Min Coverage (%)', 'Max Coverage (%)', 
            'Std Dev (%)', 'Children Tracked', 'Vaccines Administered', 'Villages Covered'
        ]
        
        summary = summary.reset_index()
        summary = summary.sort_values('Avg Coverage (%)', ascending=False)
        
        return summary
        
    except Exception as e:
        st.error(f"Error generating district summary: {str(e)}")
        return pd.DataFrame()

def get_demographic_analysis(df):
    """Generate demographic analysis table."""
    try:
        demographic_summary = df.groupby(['age_group', 'gender']).agg({
            'coverage_percentage': 'mean',
            'child_id': 'nunique',
            'fully_vaccinated': lambda x: (x == True).sum()
        }).round(2)
        
        demographic_summary.columns = ['Avg Coverage (%)', 'Children Count', 'Fully Vaccinated']
        demographic_summary = demographic_summary.reset_index()
        
        # Calculate fully vaccinated percentage
        demographic_summary['Fully Vaccinated (%)'] = (
            demographic_summary['Fully Vaccinated'] / demographic_summary['Children Count'] * 100
        ).round(2)
        
        return demographic_summary
        
    except Exception as e:
        st.error(f"Error generating demographic analysis: {str(e)}")
        return pd.DataFrame()

def get_summary_statistics(df):
    """Generate comprehensive summary statistics."""
    try:
        coverage_stats = {
            "overall_coverage": df['coverage_percentage'].mean(),
            "median_coverage": df['coverage_percentage'].median(),
            "min_coverage": df['coverage_percentage'].min(),
            "max_coverage": df['coverage_percentage'].max(),
            "std_coverage": df['coverage_percentage'].std(),
            "districts_above_90": len(df[df['coverage_percentage'] >= 90]['district'].unique()),
            "districts_below_70": len(df[df['coverage_percentage'] < 70]['district'].unique())
        }
        
        demographic_stats = {
            "total_children": df['child_id'].nunique(),
            "total_districts": df['district'].nunique(),
            "total_villages": df['village'].nunique(),
            "male_children": len(df[df['gender'] == 'Male']['child_id'].unique()),
            "female_children": len(df[df['gender'] == 'Female']['child_id'].unique()),
            "fully_vaccinated_count": len(df[df['fully_vaccinated'] == True]['child_id'].unique())
        }
        
        return {
            "coverage_stats": coverage_stats,
            "demographic_stats": demographic_stats
        }
        
    except Exception as e:
        st.error(f"Error generating summary statistics: {str(e)}")
        return {"coverage_stats": {}, "demographic_stats": {}}

def generate_recommendations(df):
    """Generate actionable recommendations based on data analysis."""
    try:
        recommendations = []
        
        # Analyze overall coverage
        avg_coverage = df['coverage_percentage'].mean()
        if avg_coverage < 75:
            recommendations.append(
                f"🚨 **Critical**: Overall coverage is {avg_coverage:.1f}%. Immediate intervention required across all districts."
            )
        elif avg_coverage < 90:
            recommendations.append(
                f"⚠️ **Action Needed**: Overall coverage is {avg_coverage:.1f}%. Focus on improving coverage to reach WHO targets."
            )
        
        # Identify low-performing districts
        low_coverage_districts = get_low_coverage_areas(df, 70)
        if not low_coverage_districts.empty:
            district_list = ", ".join(low_coverage_districts['district'].head(3).tolist())
            recommendations.append(
                f"📍 **Priority Districts**: Focus resources on {district_list} - these areas have critically low coverage."
            )
        
        # Gender disparities
        gender_analysis = df.groupby('gender')['coverage_percentage'].mean()
        if len(gender_analysis) >= 2:
            gender_diff = abs(gender_analysis.iloc[0] - gender_analysis.iloc[1])
            if gender_diff > 10:
                recommendations.append(
                    f"👥 **Gender Equity**: Address {gender_diff:.1f}% coverage gap between genders through targeted outreach."
                )
        
        # Vaccine-specific issues
        vaccine_coverage = df.groupby('vaccine_type')['coverage_percentage'].mean()
        low_vaccine = vaccine_coverage[vaccine_coverage < 75]
        if not low_vaccine.empty:
            vaccine_list = ", ".join(low_vaccine.index.tolist())
            recommendations.append(
                f"💉 **Vaccine Focus**: Strengthen campaigns for {vaccine_list} - these have below-target coverage."
            )
        
        # Seasonal patterns
        monthly_coverage = df.groupby('month')['coverage_percentage'].mean()
        if len(monthly_coverage) > 1:
            low_months = monthly_coverage[monthly_coverage < monthly_coverage.mean() - 5]
            if not low_months.empty:
                month_names = [datetime(2000, month, 1).strftime('%B') for month in low_months.index]
                recommendations.append(
                    f"📅 **Seasonal Planning**: Plan intensive campaigns during {', '.join(month_names)} - historically low coverage months."
                )
        
        # Age group analysis
        age_coverage = df.groupby('age_group')['coverage_percentage'].mean()
        low_age_groups = age_coverage[age_coverage < 80]
        if not low_age_groups.empty:
            age_list = ", ".join(low_age_groups.index.tolist())
            recommendations.append(
                f"👶 **Age-Specific Outreach**: Design targeted programs for {age_list} age groups with lower coverage."
            )
        
        if not recommendations:
            recommendations.append("✅ **Good Performance**: Current vaccination coverage is meeting targets. Continue monitoring and maintain quality standards.")
        
        return recommendations
        
    except Exception as e:
        st.error(f"Error generating recommendations: {str(e)}")
        return ["Unable to generate recommendations due to data processing error."]

def prepare_csv_export(df):
    """Prepare filtered data for CSV export."""
    try:
        # Select relevant columns for export
        export_columns = [
            'district', 'village', 'child_id', 'vaccine_type', 'date',
            'age_group', 'gender', 'coverage_percentage', 'fully_vaccinated'
        ]
        
        export_df = df[export_columns].copy()
        export_df['date'] = export_df['date'].dt.strftime('%Y-%m-%d')
        
        return export_df.to_csv(index=False)
        
    except Exception as e:
        st.error(f"Error preparing CSV export: {str(e)}")
        return ""

def prepare_excel_export(df):
    """Prepare filtered data for Excel export with multiple sheets."""
    try:
        from io import BytesIO
        import xlsxwriter
        
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output)
        
        # Main data sheet
        worksheet1 = workbook.add_worksheet('Vaccination Data')
        export_columns = [
            'district', 'village', 'child_id', 'vaccine_type', 'date',
            'age_group', 'gender', 'coverage_percentage', 'fully_vaccinated'
        ]
        
        export_df = df[export_columns].copy()
        export_df['date'] = export_df['date'].dt.strftime('%Y-%m-%d')
        
        # Write headers
        for col, header in enumerate(export_df.columns):
            worksheet1.write(0, col, header)
        
        # Write data
        for row, data in enumerate(export_df.values, 1):
            for col, value in enumerate(data):
                worksheet1.write(row, col, value)
        
        # Summary sheet
        worksheet2 = workbook.add_worksheet('Summary Statistics')
        summary_stats = get_summary_statistics(df)
        
        row = 0
        worksheet2.write(row, 0, "Coverage Statistics")
        row += 1
        for key, value in summary_stats['coverage_stats'].items():
            worksheet2.write(row, 0, key)
            worksheet2.write(row, 1, value)
            row += 1
        
        row += 1
        worksheet2.write(row, 0, "Demographic Statistics")
        row += 1
        for key, value in summary_stats['demographic_stats'].items():
            worksheet2.write(row, 0, key)
            worksheet2.write(row, 1, value)
            row += 1
        
        # District summary sheet
        worksheet3 = workbook.add_worksheet('District Summary')
        district_summary = get_district_summary(df)
        
        # Write headers
        for col, header in enumerate(district_summary.columns):
            worksheet3.write(0, col, header)
        
        # Write data
        for row, data in enumerate(district_summary.values, 1):
            for col, value in enumerate(data):
                worksheet3.write(row, col, value)
        
        workbook.close()
        output.seek(0)
        
        return output.getvalue()
        
    except Exception as e:
        st.error(f"Error preparing Excel export: {str(e)}")
        return None

def prepare_pdf_report(df):
    """Generate comprehensive PDF report."""
    try:
        from reportlab.lib.pagesizes import letter, A4
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.lib import colors
        from io import BytesIO
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            textColor=colors.darkblue,
            alignment=1  # Center alignment
        )
        story.append(Paragraph("Punjab Vaccination Coverage Report", title_style))
        story.append(Spacer(1, 20))
        
        # Executive Summary
        story.append(Paragraph("Executive Summary", styles['Heading2']))
        
        summary_stats = get_summary_statistics(df)
        summary_text = f"""
        This report analyzes vaccination coverage data for {summary_stats['demographic_stats']['total_children']} children 
        across {summary_stats['demographic_stats']['total_districts']} districts in Punjab. 
        The overall coverage rate is {summary_stats['coverage_stats']['overall_coverage']:.1f}%.
        """
        story.append(Paragraph(summary_text, styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Key Metrics Table
        story.append(Paragraph("Key Performance Indicators", styles['Heading2']))
        
        metrics_data = [
            ['Metric', 'Value'],
            ['Total Children', f"{summary_stats['demographic_stats']['total_children']:,}"],
            ['Districts Covered', summary_stats['demographic_stats']['total_districts']],
            ['Villages Covered', summary_stats['demographic_stats']['total_villages']],
            ['Average Coverage', f"{summary_stats['coverage_stats']['overall_coverage']:.1f}%"],
            ['Fully Vaccinated', summary_stats['demographic_stats']['fully_vaccinated_count']]
        ]
        
        metrics_table = Table(metrics_data)
        metrics_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(metrics_table)
        story.append(Spacer(1, 20))
        
        # District Performance
        story.append(Paragraph("District Performance Summary", styles['Heading2']))
        
        district_summary = get_district_summary(df)
        district_data = [['District', 'Avg Coverage (%)', 'Children Tracked', 'Villages']]
        
        for _, row in district_summary.head(10).iterrows():
            district_data.append([
                row['district'],
                f"{row['Avg Coverage (%)']:.1f}%",
                str(row['Children Tracked']),
                str(row['Villages Covered'])
            ])
        
        district_table = Table(district_data)
        district_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(district_table)
        story.append(Spacer(1, 20))
        
        # Recommendations
        story.append(Paragraph("Recommendations", styles['Heading2']))
        recommendations = generate_recommendations(df)
        
        for i, rec in enumerate(recommendations, 1):
            clean_rec = rec.replace("**", "").replace("🚨", "").replace("⚠️", "").replace("📍", "").replace("👥", "").replace("💉", "").replace("📅", "").replace("👶", "").replace("✅", "")
            story.append(Paragraph(f"{i}. {clean_rec}", styles['Normal']))
            story.append(Spacer(1, 10))
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        
        return buffer.getvalue()
        
    except Exception as e:
        st.error(f"Error generating PDF report: {str(e)}")
        return None

def generate_summary_report(df):
    """Generate a text-based summary report."""
    try:
        report_lines = []
        report_lines.append("VACCINATION COVERAGE SUMMARY REPORT")
        report_lines.append("=" * 50)
        report_lines.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append("")
        
        # Overall statistics
        report_lines.append("OVERALL STATISTICS")
        report_lines.append("-" * 20)
        report_lines.append(f"Total children tracked: {df['child_id'].nunique():,}")
        report_lines.append(f"Districts covered: {df['district'].nunique()}")
        report_lines.append(f"Villages covered: {df['village'].nunique()}")
        report_lines.append(f"Average coverage: {df['coverage_percentage'].mean():.1f}%")
        report_lines.append("")
        
        # District performance
        report_lines.append("DISTRICT PERFORMANCE")
        report_lines.append("-" * 20)
        district_summary = df.groupby('district')['coverage_percentage'].mean().sort_values(ascending=False)
        for district, coverage in district_summary.head(10).items():
            report_lines.append(f"{district}: {coverage:.1f}%")
        report_lines.append("")
        
        # Recommendations
        report_lines.append("KEY RECOMMENDATIONS")
        report_lines.append("-" * 20)
        recommendations = generate_recommendations(df)
        for i, rec in enumerate(recommendations, 1):
            # Remove markdown formatting for text report
            clean_rec = rec.replace("**", "").replace("🚨", "").replace("⚠️", "").replace("📍", "").replace("👥", "").replace("💉", "").replace("📅", "").replace("👶", "").replace("✅", "")
            report_lines.append(f"{i}. {clean_rec}")
        
        return "\n".join(report_lines)
        
    except Exception as e:
        st.error(f"Error generating summary report: {str(e)}")
        return "Error generating report."
