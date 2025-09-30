
import streamlit as st
import pandas as pd
import json
from datetime import datetime
import io
import base64
from sft_number_generator import SFTNumberGenerator

# Page configuration
st.set_page_config(
    page_title="SFT Number Generator",
    page_icon="🔢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .success-message {
        padding: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.25rem;
        color: #155724;
    }
    .error-message {
        padding: 0.5rem;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 0.25rem;
        color: #721c24;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'generator' not in st.session_state:
    st.session_state.generator = SFTNumberGenerator()

def get_download_link(df, filename):
    """Generate download link for Excel file"""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)

    excel_data = output.getvalue()
    b64 = base64.b64encode(excel_data).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}">📥 Download Excel File</a>'
    return href

def main():
    # Header
    st.markdown('<h1 class="main-header">🔢 SFT Number Generator System</h1>', unsafe_allow_html=True)
    st.markdown("---")

    # Sidebar
    st.sidebar.title("📋 Navigation")
    page = st.sidebar.selectbox(
        "Select Operation",
        ["🏠 Dashboard", "➕ Register Application", "📊 Bulk Registration", "🎯 Reserve Number", "📈 Statistics", "💾 Export Data"]
    )

    # Dashboard
    if page == "🏠 Dashboard":
        st.header("📊 System Overview")

        # Get current statistics
        stats = st.session_state.generator.get_statistics()

        # Metrics row
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Available", f"{stats['total_available']:,}")

        with col2:
            st.metric("Numbers Used", f"{stats['used_count']:,}")

        with col3:
            st.metric("Remaining", f"{stats['remaining']:,}")

        with col4:
            st.metric("Usage %", f"{stats['usage_percentage']:.2f}%")

        # Progress bar
        progress = stats['used_count'] / stats['total_available']
        st.progress(progress)

        # Recent applications (if Excel file exists)
        try:
            df = pd.read_excel('sft_records.xlsx')
            if not df.empty:
                st.subheader("📋 Recent Applications")
                # Show last 10 registrations
                recent_df = df.tail(10).sort_values('SFT_Number', ascending=False)
                st.dataframe(recent_df, use_container_width=True)
            else:
                st.info("No applications registered yet. Use the 'Register Application' page to get started!")
        except:
            st.info("No applications registered yet. Use the 'Register Application' page to get started!")

    # Register Single Application
    elif page == "➕ Register Application":
        st.header("➕ Register New Application")

        with st.form("register_form"):
            col1, col2 = st.columns(2)

            with col1:
                app_name = st.text_input("Application Name *", placeholder="e.g., WebApp_Authentication")

            with col2:
                description = st.text_area("Description", placeholder="Brief description of the application")

            submitted = st.form_submit_button("🚀 Generate SFT Number", type="primary")

            if submitted:
                if app_name.strip():
                    try:
                        sft_number = st.session_state.generator.register_application(
                            app_name.strip(), 
                            description.strip()
                        )

                        if sft_number:
                            st.success(f"✅ Successfully registered '{app_name}' with SFT Number: **{sft_number}**")

                            # Show the assigned number prominently
                            st.markdown(f"""
                            <div class="success-message">
                                <h3 style="margin:0; text-align:center;">🎯 Your SFT Number: {sft_number}</h3>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.error("❌ Failed to generate SFT number. Please try again.")

                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
                else:
                    st.warning("⚠️ Please enter an application name.")

    # Bulk Registration
    elif page == "📊 Bulk Registration":
        st.header("📊 Bulk Application Registration")

        st.info("💡 Enter multiple applications (one per line) in the format: AppName | Description")

        bulk_input = st.text_area(
            "Applications List",
            placeholder="WebApp_Login | User login system\nMobileApp_Payment | Mobile payment app\nAPI_UserService | User management API",
            height=200
        )

        if st.button("🚀 Bulk Register Applications", type="primary"):
            if bulk_input.strip():
                lines = bulk_input.strip().split('\n')
                applications = []

                for line in lines:
                    if '|' in line:
                        parts = line.split('|', 1)
                        app_name = parts[0].strip()
                        description = parts[1].strip() if len(parts) > 1 else ""
                    else:
                        app_name = line.strip()
                        description = ""

                    if app_name:
                        applications.append({"name": app_name, "description": description})

                if applications:
                    with st.spinner(f"Registering {len(applications)} applications..."):
                        results = st.session_state.generator.bulk_register_applications(applications)

                    # Display results
                    success_count = sum(1 for r in results if r['success'])
                    st.success(f"✅ Successfully registered {success_count}/{len(applications)} applications")

                    # Results table
                    results_df = pd.DataFrame([
                        {
                            "Application": r['application'],
                            "SFT Number": r['sft_number'] if r['sft_number'] else "Failed",
                            "Status": "✅ Success" if r['success'] else "❌ Failed"
                        }
                        for r in results
                    ])

                    st.dataframe(results_df, use_container_width=True)
                else:
                    st.warning("⚠️ No valid applications found in the input.")
            else:
                st.warning("⚠️ Please enter at least one application.")

    # Reserve Specific Number
    elif page == "🎯 Reserve Number":
        st.header("🎯 Reserve Specific SFT Number")

        with st.form("reserve_form"):
            col1, col2 = st.columns(2)

            with col1:
                specific_number = st.number_input(
                    "SFT Number to Reserve",
                    min_value=3000,
                    max_value=9999,
                    value=5000,
                    step=1
                )

            with col2:
                # Check availability
                available = st.session_state.generator.is_number_available(specific_number)
                status_color = "🟢" if available else "🔴"
                status_text = "Available" if available else "Already Used"
                st.markdown(f"**Status:** {status_color} {status_text}")

            app_name = st.text_input("Application Name *", placeholder="e.g., SpecialApp_VIP")
            description = st.text_area("Description", placeholder="Reason for specific number reservation")

            submitted = st.form_submit_button("🔒 Reserve Number", type="primary")

            if submitted:
                if app_name.strip():
                    try:
                        reserved_number = st.session_state.generator.reserve_specific_number(
                            specific_number,
                            app_name.strip(),
                            description.strip()
                        )

                        st.success(f"✅ Successfully reserved SFT Number **{reserved_number}** for '{app_name}'")

                    except ValueError as e:
                        st.error(f"❌ Reservation failed: {str(e)}")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
                else:
                    st.warning("⚠️ Please enter an application name.")

    # Statistics
    elif page == "📈 Statistics":
        st.header("📈 System Statistics & Analytics")

        stats = st.session_state.generator.get_statistics()

        # Detailed metrics
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📊 Usage Metrics")
            st.write(f"**Range:** 3000 - 9999")
            st.write(f"**Total Available:** {stats['total_available']:,}")
            st.write(f"**Numbers Used:** {stats['used_count']:,}")
            st.write(f"**Remaining:** {stats['remaining']:,}")
            st.write(f"**Usage Percentage:** {stats['usage_percentage']:.2f}%")

        with col2:
            st.subheader("🎯 Number Range Analysis")
            if st.session_state.generator.used_numbers:
                used_numbers = list(st.session_state.generator.used_numbers)
                st.write(f"**Lowest Used:** {min(used_numbers)}")
                st.write(f"**Highest Used:** {max(used_numbers)}")
                st.write(f"**Average:** {sum(used_numbers)/len(used_numbers):.0f}")
            else:
                st.write("No numbers used yet.")

        # Usage distribution chart (if we have data)
        try:
            df = pd.read_excel('sft_records.xlsx')
            if not df.empty:
                st.subheader("📅 Registration Timeline")
                df['Date'] = pd.to_datetime(df['Registration_Date']).dt.date
                daily_counts = df.groupby('Date').size().reset_index(name='Applications')
                st.line_chart(daily_counts.set_index('Date'))
        except:
            pass

    # Export Data
    elif page == "💾 Export Data":
        st.header("💾 Export System Data")

        try:
            df = pd.read_excel('sft_records.xlsx')

            if not df.empty:
                st.subheader("📋 Current Data Preview")
                st.dataframe(df, use_container_width=True)

                # Export options
                st.subheader("📥 Download Options")

                col1, col2 = st.columns(2)

                with col1:
                    if st.button("📊 Download Excel Report"):
                        # Create enhanced report
                        stats = st.session_state.generator.get_statistics()

                        # Create summary
                        summary_data = {
                            'Metric': ['Total Available', 'Used Numbers', 'Remaining Numbers', 'Usage Percentage'],
                            'Value': [stats['total_available'], stats['used_count'], 
                                     stats['remaining'], f"{stats['usage_percentage']:.2f}%"]
                        }
                        summary_df = pd.DataFrame(summary_data)

                        # Generate download
                        output = io.BytesIO()
                        with pd.ExcelWriter(output, engine='openpyxl') as writer:
                            df.to_excel(writer, sheet_name='Applications', index=False)
                            summary_df.to_excel(writer, sheet_name='Summary', index=False)

                        st.download_button(
                            label="📥 Download Complete Report",
                            data=output.getvalue(),
                            file_name=f"sft_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )

                with col2:
                    if st.button("📋 Download CSV"):
                        csv = df.to_csv(index=False)
                        st.download_button(
                            label="📥 Download CSV",
                            data=csv,
                            file_name=f"sft_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv"
                        )
            else:
                st.info("📭 No data available to export. Register some applications first!")

        except FileNotFoundError:
            st.info("📭 No data file found. Register some applications first!")
        except Exception as e:
            st.error(f"❌ Error loading data: {str(e)}")

    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666; padding: 1rem;'>
            🔢 SFT Number Generator System | Built with Streamlit | 
            Range: 3000-9999 | Unique Numbers Guaranteed
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
