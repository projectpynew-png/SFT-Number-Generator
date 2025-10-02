import streamlit as st
import pandas as pd
import json
from datetime import datetime
import io
import base64
import random
import os
import re

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
    .sft-number {
        font-size: 1.8rem;
        font-weight: bold;
        color: #2E8B57;
        text-align: center;
        padding: 1rem;
        background-color: #f0f8f0;
        border: 2px solid #2E8B57;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .success-message {
        padding: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.25rem;
        color: #155724;
    }
</style>
""", unsafe_allow_html=True)

class ImprovedSFTNumberGenerator:
    """
    Enhanced SFT Number Generator with persistent storage and formatted SFT numbers
    Format: SFT_XXYZ3000-9999 (where XXYZ is derived from application name)
    """
    def __init__(self):
        self.min_number = 3000
        self.max_number = 9999
        self.data_file = 'sft_persistent_data.json'

        # Load persistent data
        self.load_persistent_data()

    def extract_app_prefix(self, app_name):
        """Extract 4-character prefix from application name"""
        # Clean the application name
        cleaned = re.sub(r'[^a-zA-Z0-9]', '', app_name.upper())

        if len(cleaned) == 0:
            return "XXXX"
        elif len(cleaned) <= 4:
            return cleaned.ljust(4, 'X')
        else:
            # Extract meaningful characters
            # Try to get first 2 and last 2 characters if length > 4
            if len(cleaned) >= 4:
                # Get first 2 chars and last 2 chars
                prefix = cleaned[:2] + cleaned[-2:]
                return prefix[:4]  # Ensure exactly 4 characters
            else:
                return cleaned.ljust(4, 'X')

    def load_persistent_data(self):
        """Load data from persistent storage"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    st.session_state.used_numbers = set(data.get('used_numbers', []))
                    st.session_state.applications = data.get('applications', [])
                    st.session_state.sft_mapping = data.get('sft_mapping', {})
                print(f"✅ Loaded {len(st.session_state.applications)} applications from persistent storage")
            else:
                # Initialize empty data structures
                st.session_state.used_numbers = set()
                st.session_state.applications = []
                st.session_state.sft_mapping = {}
                print("📁 Created new persistent storage")
        except Exception as e:
            print(f"❌ Error loading persistent data: {e}")
            st.session_state.used_numbers = set()
            st.session_state.applications = []
            st.session_state.sft_mapping = {}

    def save_persistent_data(self):
        """Save data to persistent storage"""
        try:
            data = {
                'used_numbers': list(st.session_state.used_numbers),
                'applications': st.session_state.applications,
                'sft_mapping': st.session_state.sft_mapping,
                'last_updated': datetime.now().isoformat()
            }
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
            print("💾 Data saved to persistent storage")
        except Exception as e:
            print(f"❌ Error saving persistent data: {e}")

    def generate_sft_number(self, app_name):
        """Generate formatted SFT number: SFT_XXYZ3000-9999"""
        # Get application prefix
        app_prefix = self.extract_app_prefix(app_name)

        # Find available number
        available_numbers = self.max_number - self.min_number + 1
        if len(st.session_state.used_numbers) >= available_numbers:
            raise ValueError("All SFT numbers in the range have been exhausted!")

        # Generate unique number
        while True:
            number = random.randint(self.min_number, self.max_number)
            if number not in st.session_state.used_numbers:
                st.session_state.used_numbers.add(number)

                # Create formatted SFT number
                sft_number = f"SFT_{app_prefix}{number}"
                return sft_number

    def register_application(self, app_name, description=""):
        """Register a new application and assign an SFT number"""
        try:
            sft_number = self.generate_sft_number(app_name)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            new_record = {
                'SFT_Number': sft_number,
                'Application_Name': app_name,
                'Description': description,
                'Registration_Date': timestamp,
                'Status': 'Active',
                'App_Prefix': self.extract_app_prefix(app_name)
            }

            st.session_state.applications.append(new_record)

            # Update mapping for quick lookup
            st.session_state.sft_mapping[sft_number] = {
                'app_name': app_name,
                'registration_date': timestamp
            }

            # Save to persistent storage
            self.save_persistent_data()

            return sft_number

        except Exception as e:
            st.error(f"Error registering application: {e}")
            return None

    def bulk_register_applications(self, applications_list):
        """Register multiple applications at once"""
        results = []
        for app in applications_list:
            sft_number = self.register_application(
                app.get('name', 'Unknown'),
                app.get('description', '')
            )
            results.append({
                'application': app.get('name', 'Unknown'),
                'sft_number': sft_number,
                'success': sft_number is not None
            })
        return results

    def reserve_specific_number(self, number, app_name, description=""):
        """Reserve a specific number in the SFT format"""
        if not (self.min_number <= number <= self.max_number):
            raise ValueError(f"Number {number} is outside valid range ({self.min_number}-{self.max_number})")

        if number in st.session_state.used_numbers:
            raise ValueError(f"Number {number} is already in use")

        # Generate formatted SFT number
        app_prefix = self.extract_app_prefix(app_name)
        sft_number = f"SFT_{app_prefix}{number}"

        st.session_state.used_numbers.add(number)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        new_record = {
            'SFT_Number': sft_number,
            'Application_Name': app_name,
            'Description': description,
            'Registration_Date': timestamp,
            'Status': 'Reserved',
            'App_Prefix': app_prefix
        }

        st.session_state.applications.append(new_record)
        st.session_state.sft_mapping[sft_number] = {
            'app_name': app_name,
            'registration_date': timestamp
        }

        # Save to persistent storage
        self.save_persistent_data()

        return sft_number

    def get_statistics(self):
        """Get statistics about SFT number usage"""
        total_available = self.max_number - self.min_number + 1
        used_count = len(st.session_state.used_numbers)
        remaining = total_available - used_count

        return {
            'total_available': total_available,
            'used_count': used_count,
            'remaining': remaining,
            'usage_percentage': (used_count / total_available) * 100
        }

    def is_number_available(self, number):
        """Check if a specific number is available"""
        return (self.min_number <= number <= self.max_number) and (number not in st.session_state.used_numbers)

    def search_applications(self, search_term):
        """Search applications by name or SFT number"""
        results = []
        search_term = search_term.upper()

        for app in st.session_state.applications:
            if (search_term in app['Application_Name'].upper() or 
                search_term in app['SFT_Number'].upper() or
                search_term in app.get('Description', '').upper()):
                results.append(app)

        return results

# Initialize improved generator
if 'improved_generator' not in st.session_state:
    st.session_state.improved_generator = ImprovedSFTNumberGenerator()

def main():
    # Header
    st.markdown('<h1 class="main-header">🔢 Enhanced SFT Number Generator</h1>', unsafe_allow_html=True)
    st.markdown("### Format: SFT_XXYZ3000-9999 (XXYZ = Application Prefix)")
    st.markdown("---")

    # Sidebar
    st.sidebar.title("📋 Navigation")
    page = st.sidebar.selectbox(
        "Select Operation",
        ["🏠 Dashboard", "➕ Register Application", "📊 Bulk Registration", "🎯 Reserve Number", "🔍 Search Applications", "📈 Statistics", "💾 Export Data"]
    )

    # Get generator instance
    generator = st.session_state.improved_generator

    # Dashboard
    if page == "🏠 Dashboard":
        st.header("📊 System Overview")

        # Get current statistics
        stats = generator.get_statistics()

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

        # Recent applications
        if st.session_state.applications:
            st.subheader("📋 Recent Applications")
            df = pd.DataFrame(st.session_state.applications)
            # Show last 10 registrations
            recent_df = df.tail(10).sort_values('Registration_Date', ascending=False)
            st.dataframe(recent_df, use_container_width=True)

            # Show SFT format examples
            st.subheader("🎯 SFT Number Format Examples")
            examples = recent_df.head(5)
            for _, row in examples.iterrows():
                st.write(f"**{row['Application_Name']}** → `{row['SFT_Number']}`")
        else:
            st.info("No applications registered yet. Use the 'Register Application' page to get started!")

    # Register Single Application
    elif page == "➕ Register Application":
        st.header("➕ Register New Application")

        with st.form("register_form"):
            col1, col2 = st.columns(2)

            with col1:
                app_name = st.text_input("Application Name *", placeholder="e.g., WebApp_Authentication")
                # Show preview of SFT format
                if app_name:
                    preview_prefix = generator.extract_app_prefix(app_name)
                    st.info(f"SFT Format Preview: SFT_{preview_prefix}XXXX")

            with col2:
                description = st.text_area("Description", placeholder="Brief description of the application")

            submitted = st.form_submit_button("🚀 Generate SFT Number", type="primary")

            if submitted:
                if app_name.strip():
                    try:
                        sft_number = generator.register_application(
                            app_name.strip(), 
                            description.strip()
                        )

                        if sft_number:
                            st.success(f"✅ Successfully registered '{app_name}' with SFT Number: **{sft_number}**")

                            # Show the assigned number prominently
                            st.markdown(f"""
                            <div class="sft-number">
                                🎯 Your SFT Number: {sft_number}
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
                        results = generator.bulk_register_applications(applications)

                    # Display results
                    success_count = sum(1 for r in results if r['success'])
                    st.success(f"✅ Successfully registered {success_count}/{len(applications)} applications")

                    # Results table with SFT numbers
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
                    "Number to Reserve (3000-9999)",
                    min_value=3000,
                    max_value=9999,
                    value=5000,
                    step=1
                )

                app_name = st.text_input("Application Name *", placeholder="e.g., SpecialApp_VIP")
                # Show preview
                if app_name:
                    preview_prefix = generator.extract_app_prefix(app_name)
                    preview_sft = f"SFT_{preview_prefix}{specific_number}"
                    st.info(f"SFT Number Preview: {preview_sft}")

            with col2:
                # Check availability
                available = generator.is_number_available(specific_number)
                status_color = "🟢" if available else "🔴"
                status_text = "Available" if available else "Already Used"
                st.markdown(f"**Status:** {status_color} {status_text}")

                description = st.text_area("Description", placeholder="Reason for specific number reservation")

            submitted = st.form_submit_button("🔒 Reserve Number", type="primary")

            if submitted:
                if app_name.strip():
                    try:
                        reserved_sft = generator.reserve_specific_number(
                            specific_number,
                            app_name.strip(),
                            description.strip()
                        )

                        st.success(f"✅ Successfully reserved SFT Number **{reserved_sft}** for '{app_name}'")

                        st.markdown(f"""
                        <div class="sft-number">
                            🎯 Reserved SFT Number: {reserved_sft}
                        </div>
                        """, unsafe_allow_html=True)

                    except ValueError as e:
                        st.error(f"❌ Reservation failed: {str(e)}")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
                else:
                    st.warning("⚠️ Please enter an application name.")

    # Search Applications
    elif page == "🔍 Search Applications":
        st.header("🔍 Search Applications")

        search_term = st.text_input("Search by Application Name, SFT Number, or Description", 
                                  placeholder="e.g., WebApp or SFT_WEBA or authentication")

        if search_term:
            results = generator.search_applications(search_term)

            if results:
                st.success(f"Found {len(results)} matching applications:")
                df = pd.DataFrame(results)
                st.dataframe(df, use_container_width=True)

                # Show breakdown by prefix
                if len(results) > 1:
                    prefixes = [app.get('App_Prefix', 'N/A') for app in results]
                    prefix_counts = pd.Series(prefixes).value_counts()

                    st.subheader("📊 Applications by Prefix")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.bar_chart(prefix_counts)
                    with col2:
                        for prefix, count in prefix_counts.items():
                            st.metric(f"Prefix: {prefix}", count)
            else:
                st.info("No applications found matching your search term.")

    # Statistics
    elif page == "📈 Statistics":
        st.header("📈 System Statistics & Analytics")

        stats = generator.get_statistics()

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
            if st.session_state.used_numbers:
                used_numbers = list(st.session_state.used_numbers)
                st.write(f"**Lowest Used:** {min(used_numbers)}")
                st.write(f"**Highest Used:** {max(used_numbers)}")
                st.write(f"**Average:** {sum(used_numbers)/len(used_numbers):.0f}")
            else:
                st.write("No numbers used yet.")

        # Application prefix analysis
        if st.session_state.applications:
            st.subheader("🏷️ Application Prefix Analysis")
            df = pd.DataFrame(st.session_state.applications)

            # Prefix distribution
            prefix_counts = df['App_Prefix'].value_counts()
            col1, col2 = st.columns(2)

            with col1:
                st.bar_chart(prefix_counts)

            with col2:
                st.write("**Top Prefixes:**")
                for prefix, count in prefix_counts.head(10).items():
                    st.write(f"**{prefix}:** {count} applications")

            # Registration timeline
            st.subheader("📅 Registration Timeline")
            df['Date'] = pd.to_datetime(df['Registration_Date']).dt.date
            daily_counts = df.groupby('Date').size().reset_index(name='Applications')
            st.line_chart(daily_counts.set_index('Date'))

    # Export Data
    elif page == "💾 Export Data":
        st.header("💾 Export System Data")

        # Get stats for export
        stats = generator.get_statistics()

        if st.session_state.applications:
            df = pd.DataFrame(st.session_state.applications)

            st.subheader("📋 Current Data Preview")
            st.dataframe(df, use_container_width=True)

            # Export options
            st.subheader("📥 Download Options")

            col1, col2 = st.columns(2)

            with col1:
                # Excel export
                excel_data = io.BytesIO()
                with pd.ExcelWriter(excel_data, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False, sheet_name='Applications')

                    # Add summary sheet with stats
                    summary_data = {
                        'Metric': ['Total Available', 'Used Numbers', 'Remaining Numbers', 'Usage Percentage'],
                        'Value': [stats['total_available'], stats['used_count'], 
                                 stats['remaining'], f"{stats['usage_percentage']:.2f}%"]
                    }
                    summary_df = pd.DataFrame(summary_data)
                    summary_df.to_excel(writer, index=False, sheet_name='Summary')

                    # Prefix analysis sheet
                    if len(df) > 0:
                        prefix_analysis = df['App_Prefix'].value_counts().reset_index()
                        prefix_analysis.columns = ['Prefix', 'Count']
                        prefix_analysis.to_excel(writer, index=False, sheet_name='Prefix_Analysis')

                st.download_button(
                    label="📊 Download Complete Excel Report",
                    data=excel_data.getvalue(),
                    file_name=f"sft_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

            with col2:
                # CSV export
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📋 Download CSV Data",
                    data=csv,
                    file_name=f"sft_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        else:
            st.info("📭 No data available to export. Register some applications first!")

    # Footer
    st.markdown("---")
    st.markdown(
        f"""
        <div style='text-align: center; color: #666; padding: 1rem;'>
            🔢 Enhanced SFT Number Generator | Format: SFT_XXYZ3000-9999 | 
            Persistent Storage: {len(st.session_state.applications)} applications stored
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
