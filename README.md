# SFT Number Generator System

A comprehensive web-based system for generating unique SFT numbers for applications with persistent memory and Excel backend integration.

## 🚀 Features

- **Unique Number Generation**: Generate numbers in range 3000-9999
- **No Duplicates**: Advanced memory system prevents repetition
- **Excel Backend**: Automatic database updates with full audit trail
- **Bulk Registration**: Register multiple applications at once
- **Number Reservation**: Reserve specific numbers for special applications
- **Real-time Statistics**: Usage analytics and reporting
- **Data Export**: Download Excel reports and CSV files

## 🌐 Live Demo

Visit the live application: [SFT Number Generator](https://your-app.streamlit.app)

## 🏃‍♂️ Quick Start

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/yourusername/sft-number-generator.git
cd sft-number-generator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run streamlit_app.py
```

### Streamlit Cloud Deployment

1. Fork this repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Deploy from your forked repository

## 📁 File Structure

```
sft-number-generator/
├── streamlit_app.py          # Main Streamlit web application
├── sft_number_generator.py   # Core SFT generator class
├── sft_demo.py              # Demo script for testing
├── requirements.txt          # Python dependencies
├── .streamlit/
│   └── config.toml          # Streamlit configuration
├── sft_records.xlsx         # Excel database (auto-generated)
├── sft_memory.json          # Memory persistence (auto-generated)
└── README.md               # This file
```

## 🔧 Configuration

The system uses the following configuration:
- **Number Range**: 3000 - 9999 (7,000 total numbers)
- **Database**: Excel file with automatic updates
- **Memory**: JSON file for persistence across sessions
- **Web Interface**: Streamlit with responsive design

## 📊 Usage

### Single Application Registration
1. Navigate to "Register Application"
2. Enter application name and description
3. Click "Generate SFT Number"
4. Your unique number will be displayed

### Bulk Registration
1. Go to "Bulk Registration"
2. Enter applications in format: `AppName | Description`
3. Click "Bulk Register Applications"
4. View results in the generated table

### Number Reservation
1. Visit "Reserve Number"
2. Enter desired SFT number (3000-9999)
3. Check availability status
4. Reserve if available

## 📈 System Statistics

The dashboard provides:
- Total available numbers
- Numbers currently used
- Remaining capacity
- Usage percentage
- Registration timeline

## 💾 Data Export

Export options include:
- Complete Excel report with summary
- CSV data export
- Real-time download generation

## 🛠️ Technical Details

- **Backend**: Python with pandas for data management
- **Frontend**: Streamlit for web interface
- **Database**: Excel files with openpyxl
- **Memory**: JSON-based persistence
- **Deployment**: Streamlit Cloud ready

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

For support and questions:
- Create an issue in this repository
- Contact: [your-email@example.com]

## 🎯 Roadmap

- [ ] User authentication system
- [ ] API endpoints for external integration
- [ ] Advanced analytics and reporting
- [ ] Number recycling for deleted applications
- [ ] Multi-tenant support
