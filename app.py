import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import io
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from io import BytesIO
import base64

# Page config
st.set_page_config(
    page_title="LSI Coupon Statistics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 0.5rem 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Helper Functions
@st.cache_data
def load_data(file):
    """Load and process Excel data"""
    df = pd.read_excel(file)
    df['SaleDy'] = pd.to_datetime(df['SaleDy'].astype(str), format='%Y%m%d')
    return df

def filter_data(df, filter_stores, filter_mode, coupon_keywords, selected_coupons, date_range):
    """Apply filters to dataframe"""
    df_filtered = df.copy()
    
    # Filter by stores
    if filter_stores and len(filter_stores) > 0:
        df_filtered = df_filtered[df_filtered['StrNm'].isin(filter_stores)]
    
    # Filter by coupons
    if filter_mode == 'Keywords':
        pattern = '|'.join(coupon_keywords)
        df_filtered = df_filtered[df_filtered['CpnNm'].str.lower().str.contains(pattern, na=False, regex=True)]
    else:  # Specific
        if selected_coupons and len(selected_coupons) > 0:
            df_filtered = df_filtered[df_filtered['CpnNm'].isin(selected_coupons)]
    
    # Filter by date
    if date_range:
        df_filtered = df_filtered[
            (df_filtered['SaleDy'] >= pd.to_datetime(date_range[0])) &
            (df_filtered['SaleDy'] <= pd.to_datetime(date_range[1]))
        ]
    
    return df_filtered

def create_line_chart_plotly(df_filtered):
    """Create interactive Plotly line chart"""
    # Aggregate data
    daily_trend = df_filtered.groupby(['SaleDy', 'CpnNm'])['Qty'].sum().reset_index()
    daily_trend = daily_trend.sort_values(['SaleDy', 'CpnNm'])
    
    fig = go.Figure()
    
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', 
              '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
    
    max_qty = daily_trend['Qty'].max()
    y_range_max = max_qty * 1.2
    
    all_coupons = sorted(df_filtered['CpnNm'].unique())
    
    for i, coupon in enumerate(all_coupons):
        coupon_data = daily_trend[daily_trend['CpnNm'] == coupon]
        
        text_positions = []
        for idx, row in coupon_data.iterrows():
            if row['Qty'] > (max_qty * 0.7):
                text_positions.append('bottom center')
            else:
                text_positions.append('top center')
        
        fig.add_trace(go.Scatter(
            x=coupon_data['SaleDy'],
            y=coupon_data['Qty'],
            name=coupon,
            mode='lines+markers+text',
            line=dict(width=2.5, color=colors[i % len(colors)]),
            marker=dict(size=8),
            text=coupon_data['Qty'].astype(int),
            textposition=text_positions,
            textfont=dict(
                size=11,
                color=colors[i % len(colors)],
                family='Arial Black, sans-serif'
            ),
            hovertemplate='<b>%{fullData.name}</b><br>' +
                          'Date: %{x|%d-%b-%Y}<br>' +
                          'Quantity: %{y:,.0f}<br>' +
                          '<extra></extra>'
        ))
    
    fig.update_layout(
        title=dict(
            text='<b>RESULT PROMO NEW MEMBER & DORMANT</b><br><sub>BY COUPON USAGE (ALL STORE)</sub>',
            x=0.5,
            xanchor='center',
            font=dict(size=16)
        ),
        xaxis=dict(
            title='<b>Date</b>',
            tickformat='%d-%b',
            tickangle=-45,
            showgrid=True,
            gridcolor='lightgray',
            gridwidth=0.5
        ),
        yaxis=dict(
            title='<b>Quantity</b>',
            showgrid=True,
            gridcolor='lightgray',
            gridwidth=0.5,
            tickformat=',',
            range=[0, y_range_max]
        ),
        hovermode='x unified',
        height=600,
        showlegend=True,
        legend=dict(
            orientation='v',
            yanchor='top',
            y=1,
            xanchor='left',
            x=1.02,
            font=dict(size=9),
            bgcolor='rgba(255,255,255,0.9)',
            bordercolor='gray',
            borderwidth=1
        ),
        plot_bgcolor='white',
        font=dict(family='Arial', size=11),
        margin=dict(t=80, b=80, l=60, r=200)
    )
    
    return fig

def create_data_table_df(df_filtered):
    """Create data table as pandas DataFrame"""
    daily_trend = df_filtered.groupby(['SaleDy', 'CpnNm'])['Qty'].sum().reset_index()
    
    data_table = daily_trend.pivot_table(
        values='Qty', 
        index='CpnNm', 
        columns='SaleDy', 
        aggfunc='sum', 
        fill_value=0
    )
    
    data_table.columns = [col.strftime('%d-%b') for col in data_table.columns]
    data_table = data_table.reset_index()
    data_table.columns.name = None
    
    return data_table
    
def create_line_chart_matplotlib(df_filtered):
    """Create line chart with table using Matplotlib (perfect alignment)"""
    # Aggregate data
    daily_trend = df_filtered.groupby(['SaleDy', 'CpnNm'])['Qty'].sum().reset_index()
    daily_trend = daily_trend.sort_values(['SaleDy', 'CpnNm'])
    
    # Prepare table data
    data_table = daily_trend.pivot_table(
        values='Qty', 
        index='CpnNm', 
        columns='SaleDy', 
        aggfunc='sum', 
        fill_value=0
    )
    
    dates_list = sorted(data_table.columns)
    
    # Create figure with MORE vertical space
    fig = plt.figure(figsize=(16, 12))
    
    # Use GridSpec for better control
    import matplotlib.gridspec as gridspec
    gs = gridspec.GridSpec(2, 1, figure=fig, height_ratios=[2, 1], hspace=0.4)
    
    # Chart axes
    ax_chart = fig.add_subplot(gs[0])
    
    # Table axes
    ax_table = fig.add_subplot(gs[1])
    
    # Colors
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', 
              '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
    
    all_coupons = sorted(df_filtered['CpnNm'].unique())
    
    # Find max for Y range
    max_qty = daily_trend['Qty'].max()
    y_max = max_qty * 1.3  # Extra 30% space for labels
    
    # Plot lines
    for i, coupon in enumerate(all_coupons):
        coupon_data = daily_trend[daily_trend['CpnNm'] == coupon]
        
        # Plot line
        ax_chart.plot(
            coupon_data['SaleDy'], 
            coupon_data['Qty'],
            marker='o',
            linewidth=2.5,
            markersize=8,
            color=colors[i % len(colors)],
            label=coupon,
            zorder=3
        )
        
        # Add data labels with white background
        for idx, row in coupon_data.iterrows():
            # Smart positioning
            if row['Qty'] > (max_qty * 0.75):
                va = 'bottom'
                offset = 20
            elif row['Qty'] < (max_qty * 0.15):
                va = 'bottom'
                offset = 20
            else:
                va = 'top'
                offset = -20
            
            ax_chart.annotate(
                f"{int(row['Qty'])}", 
                xy=(row['SaleDy'], row['Qty']),
                xytext=(0, offset),
                textcoords='offset points',
                fontsize=9,
                fontweight='bold',
                color=colors[i % len(colors)],
                ha='center',
                va=va,
                bbox=dict(
                    boxstyle='round,pad=0.3',
                    facecolor='white',
                    edgecolor='lightgray',
                    alpha=0.9,
                    linewidth=0.5
                ),
                zorder=4
            )
    
    # Chart formatting
    ax_chart.set_title('RESULT PROMO NEW MEMBER & DORMANT\nBY COUPON USAGE (ALL STORE)', 
                       fontsize=16, fontweight='bold', pad=15)
    ax_chart.set_ylabel('Quantity', fontsize=13, fontweight='bold')
    ax_chart.set_ylim(0, y_max)
    ax_chart.grid(True, alpha=0.3, zorder=1, linestyle='--')
    ax_chart.legend(loc='upper left', bbox_to_anchor=(1.01, 1), fontsize=9, frameon=True, shadow=True)
    
    # Format x-axis
    ax_chart.xaxis.set_major_formatter(mdates.DateFormatter('%d-%b'))
    ax_chart.tick_params(axis='x', rotation=45, labelsize=10)
    ax_chart.set_xlabel('Date', fontsize=12, fontweight='bold', labelpad=10)
    
    # Add horizontal line at y=0
    ax_chart.axhline(y=0, color='black', linewidth=1, zorder=2)
    
    # Prepare table data
    table_data = []
    for coupon in all_coupons:
        row = [coupon]
        for date in dates_list:
            val = data_table.loc[coupon, date] if coupon in data_table.index else 0
            row.append(int(val))
        table_data.append(row)
    
    # Column labels
    col_labels = ['Coupon Name'] + [date.strftime('%d-%b') for date in dates_list]
    
    # Create table with adjusted width
    table = ax_table.table(
        cellText=table_data,
        colLabels=col_labels,
        cellLoc='center',
        loc='upper center',
        colWidths=[0.22] + [0.78/len(dates_list)] * len(dates_list)
    )
    
    # Style table
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 2.2)
    
    # Header styling
    for i in range(len(col_labels)):
        cell = table[(0, i)]
        cell.set_facecolor('#40E0D0')
        cell.set_text_props(weight='bold', fontsize=10)
        cell.set_edgecolor('white')
        cell.set_linewidth(2)
    
    # Row styling (alternating colors)
    for i in range(len(table_data)):
        for j in range(len(col_labels)):
            cell = table[(i+1, j)]
            if i % 2 == 0:
                cell.set_facecolor('#F0F8FF')
            else:
                cell.set_facecolor('#E0E0E0')
            cell.set_edgecolor('white')
            cell.set_linewidth(1)
    
    # Remove table axes
    ax_table.axis('off')
    ax_table.set_xlim(0, 1)
    ax_table.set_ylim(0, 1)
    
    # Adjust overall layout
    plt.subplots_adjust(left=0.05, right=0.88, top=0.95, bottom=0.05)
    
    # Save to BytesIO
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight', pad_inches=0.2)
    buf.seek(0)
    plt.close()
    
    return buf

def create_pivot_table(df_filtered):
    """Create pivot table: StrCd | StrNm | Coupon columns"""
    # Group by store and coupon
    pivot = df_filtered.groupby(['StrCd', 'StrNm', 'CpnNm'])['Qty'].sum().reset_index()
    
    # Pivot to wide format
    pivot_wide = pivot.pivot_table(
        values='Qty',
        index=['StrCd', 'StrNm'],
        columns='CpnNm',
        aggfunc='sum',
        fill_value=0
    ).reset_index()
    
    # Add total column
    coupon_cols = [col for col in pivot_wide.columns if col not in ['StrCd', 'StrNm']]
    pivot_wide['TOTAL'] = pivot_wide[coupon_cols].sum(axis=1)
    
    # Add grand total row
    total_row = pd.DataFrame({
        'StrCd': ['TOTAL'],
        'StrNm': [''],
        **{col: [pivot_wide[col].sum()] for col in coupon_cols},
        'TOTAL': [pivot_wide['TOTAL'].sum()]
    })
    
    pivot_final = pd.concat([pivot_wide, total_row], ignore_index=True)
    
    return pivot_final

# Main App
def main():
    # Header
    st.markdown('<div class="main-header">📊 LSI Coupon Statistics Dashboard</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Filter & Settings")
        
        # File uploader
        uploaded_file = st.file_uploader(
            "📂 Upload Excel File",
            type=['xlsx', 'xls'],
            help="Upload your LSI Coupon Statistics file"
        )
        
        if not uploaded_file:
            st.info("👆 Please upload an Excel file to begin")
            st.stop()
        
        # Load data
        df = load_data(uploaded_file)
        
        st.success(f"✅ Loaded {len(df):,} records")
        
        st.markdown("---")
        
        # Date range
        st.subheader("📅 Date Range")
        min_date = df['SaleDy'].min().date()
        max_date = df['SaleDy'].max().date()
        
        date_range = st.date_input(
            "Select Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
        
        st.markdown("---")
        
        # Store filter
        st.subheader("🏪 Store Filter")
        all_stores = sorted(df['StrNm'].unique())
        
        select_all_stores = st.checkbox("Select All Stores", value=True)
        
        if select_all_stores:
            filter_stores = all_stores
        else:
            filter_stores = st.multiselect(
                "Select Stores",
                options=all_stores,
                default=[]
            )
        
        st.markdown("---")
        
        # Coupon filter
        st.subheader("🎫 Coupon Filter")
        filter_mode = st.radio(
            "Filter Mode",
            options=['Keywords', 'Specific Coupons'],
            help="Choose how to filter coupons"
        )
        
        if filter_mode == 'Keywords':
            default_keywords = ['tm', 'new regis', 'dormant']
            coupon_keywords_input = st.text_input(
                "Enter keywords (comma-separated)",
                value=', '.join(default_keywords)
            )
            coupon_keywords = [kw.strip() for kw in coupon_keywords_input.split(',')]
            selected_coupons = None
        else:
            all_coupons = sorted(df['CpnNm'].unique())
            selected_coupons = st.multiselect(
                "Select Coupons",
                options=all_coupons,
                default=all_coupons[:3]
            )
            coupon_keywords = []
        
        st.markdown("---")
        st.markdown("### 📊 Dashboard Info")
        st.info("""
        **Features:**
        - Interactive line chart
        - Data table with daily values
        - Pivot table by store
        - Export to Excel/CSV
        """)
    
    # Apply filters
    df_filtered = filter_data(df, filter_stores, filter_mode, coupon_keywords, selected_coupons, date_range)
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Records",
            f"{len(df_filtered):,}",
            delta=f"{(len(df_filtered)/len(df)*100):.1f}% of total"
        )
    
    with col2:
        st.metric(
            "Total Quantity",
            f"{df_filtered['Qty'].sum():,.0f}"
        )
    
    with col3:
        st.metric(
            "Unique Stores",
            df_filtered['StrNm'].nunique()
        )
    
    with col4:
        st.metric(
            "Unique Coupons",
            df_filtered['CpnNm'].nunique()
        )
    
    st.markdown("---")
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 Line Chart & Table",
        "📊 Pivot Table (Store View)",
        "📋 Data Detail",
        "💾 Export"
    ])

    # Tab 1: Line Chart
    with tab1:
        st.subheader("📈 Daily Coupon Usage Trend")
        
        if len(df_filtered) == 0:
            st.warning("No data to display with current filters")
        else:
            # Choose visualization mode
            viz_mode = st.radio(
                "Visualization Mode:",
                options=["Interactive (Plotly)", "Static Perfect Alignment (Matplotlib)"],
                horizontal=True
            )
            
            if viz_mode == "Interactive (Plotly)":
                try:
                    # PLOTLY VERSION - Interactive
                    fig = create_line_chart_plotly(df_filtered)
                    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': True})
                    
                    st.markdown("---")
                    
                    # Data Table below
                    st.subheader("📊 Daily Data Table")
                    data_table = create_data_table_df(df_filtered)
                    
                    st.dataframe(
                        data_table.style.format({
                            col: '{:.0f}' for col in data_table.columns if col != 'CpnNm'
                        }),
                        use_container_width=True,
                        height=400
                    )
                    
                    # Download table
                    csv = data_table.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Download Data Table (CSV)",
                        data=csv,
                        file_name=f"daily_data_table_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                    
                except Exception as e:
                    st.error(f"Error creating chart: {str(e)}")
            
            else:  # Matplotlib
                try:
                    st.info("💡 This version has perfect chart-table alignment, ideal for reports and presentations.")
                    
                    # MATPLOTLIB VERSION - Perfect alignment
                    img_buf = create_line_chart_matplotlib(df_filtered)
                    
                    st.image(img_buf, use_column_width=True)
                    
                    # Download button
                    st.download_button(
                        label="📥 Download Chart + Table (PNG)",
                        data=img_buf,
                        file_name=f"coupon_chart_aligned_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                        mime="image/png"
                    )
                    
                except Exception as e:
                    st.error(f"Error creating chart: {str(e)}")
                    import traceback
                    st.code(traceback.format_exc())
    
    # Tab 2: Pivot Table
    with tab2:
        st.subheader("Pivot Table: Store × Coupon")
        st.markdown("**Structure:** StrCd | StrNm | [Coupon Columns] | TOTAL")
        
        if len(df_filtered) == 0:
            st.warning("No data to display with current filters")
        else:
            pivot_df = create_pivot_table(df_filtered)
            
            # Style the dataframe
            def highlight_total_row(row):
                if row['StrCd'] == 'TOTAL':
                    return ['background-color: #ffffcc; font-weight: bold'] * len(row)
                return [''] * len(row)
            
            styled_df = pivot_df.style.apply(highlight_total_row, axis=1).format({
                col: '{:,.0f}' for col in pivot_df.columns if col not in ['StrCd', 'StrNm']
            })
            
            st.dataframe(styled_df, use_container_width=True, height=600)
            
            # Download button
            csv = pivot_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Pivot Table (CSV)",
                data=csv,
                file_name=f"pivot_table_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    # Tab 3: Data Detail
    with tab3:
        st.subheader("Filtered Data Detail")
        
        if len(df_filtered) == 0:
            st.warning("No data to display with current filters")
        else:
            # Show summary
            st.markdown(f"**Showing {len(df_filtered):,} records**")
            
            # Display dataframe
            display_df = df_filtered.copy()
            display_df['SaleDy'] = display_df['SaleDy'].dt.strftime('%Y-%m-%d')
            
            st.dataframe(display_df, use_container_width=True, height=600)
            
            # Download button
            csv = display_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Filtered Data (CSV)",
                data=csv,
                file_name=f"filtered_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    # Tab 4: Export
    with tab4:
        st.subheader("Export Options")
        
        if len(df_filtered) == 0:
            st.warning("No data to export with current filters")
        else:
            st.markdown("### 📊 Available Exports")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Excel Export (Multi-Sheet)")
                st.info("""
                **Includes:**
                - Filtered Data
                - Pivot Table (Store × Coupon)
                - Daily Trend Summary
                - Summary Statistics
                """)
                
                if st.button("🔄 Generate Excel File", type="primary"):
                    with st.spinner("Generating Excel file..."):
                        # Create Excel file
                        output = io.BytesIO()
                        with pd.ExcelWriter(output, engine='openpyxl') as writer:
                            # Sheet 1: Filtered data
                            df_export = df_filtered.copy()
                            df_export['SaleDy'] = df_export['SaleDy'].dt.strftime('%Y-%m-%d')
                            df_export.to_excel(writer, sheet_name='Filtered_Data', index=False)
                            
                            # Sheet 2: Pivot table
                            pivot_df = create_pivot_table(df_filtered)
                            pivot_df.to_excel(writer, sheet_name='Pivot_Store_Coupon', index=False)
                            
                            # Sheet 3: Daily trend
                            daily_summary = df_filtered.groupby(['SaleDy', 'CpnNm'])['Qty'].sum().reset_index()
                            daily_summary['SaleDy'] = daily_summary['SaleDy'].dt.strftime('%Y-%m-%d')
                            daily_summary.to_excel(writer, sheet_name='Daily_Trend', index=False)
                            
                            # Sheet 4: Summary stats
                            summary = pd.DataFrame({
                                'Metric': ['Total Records', 'Total Qty', 'Unique Stores', 'Unique Coupons', 'Date Range'],
                                'Value': [
                                    len(df_filtered),
                                    df_filtered['Qty'].sum(),
                                    df_filtered['StrNm'].nunique(),
                                    df_filtered['CpnNm'].nunique(),
                                    f"{df_filtered['SaleDy'].min().strftime('%Y-%m-%d')} to {df_filtered['SaleDy'].max().strftime('%Y-%m-%d')}"
                                ]
                            })
                            summary.to_excel(writer, sheet_name='Summary', index=False)
                        
                        output.seek(0)
                        
                        st.download_button(
                            label="📥 Download Excel File",
                            data=output,
                            file_name=f"lsi_coupon_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                        
                        st.success("✅ Excel file ready for download!")
            
            with col2:
                st.markdown("#### Individual CSV Exports")
                
                # Filtered data
                csv1 = df_filtered.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📄 Filtered Data (CSV)",
                    data=csv1,
                    file_name=f"filtered_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
                
                # Pivot table
                pivot_df = create_pivot_table(df_filtered)
                csv2 = pivot_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📊 Pivot Table (CSV)",
                    data=csv2,
                    file_name=f"pivot_table_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )

if __name__ == "__main__":
    main()
