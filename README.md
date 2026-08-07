# Risk Streamlit 🌞⚡

Risk Streamlit is a **solar maintenance monitoring system** built on a **rule-based logic approach** and hosted with **Streamlit**.  
Its main purpose is to classify the operational state of a solar system into **Normal, Low Risk, High Risk, or Critical**, helping operators quickly identify issues and take preventive action.

---

## 🚀 Features
- **Real-time monitoring**: Pulls live sensor data via **Supabase** integration  
- **Rule-based classification**: Transparent logic for risk levels (Normal, Low, High, Critical)  
- **Interactive dashboards**: Streamlit-powered UI for easy visualization and decision-making  
- **Scalable design**: Ready to expand with more sensors or advanced models  

---

## 🛠️ Tech Stack
- **Python** for backend logic  
- **Streamlit** for interactive dashboards  
- **Supabase** for real-time data ingestion from sensors  

---

## 📂 Project Structure
```
risk_streamlit/
│
├── app.py              # Main Streamlit application
├── Risk_classer.py     # Rule-based risk classification logic
├── .streamlit/         # Streamlit configuration
├── .devcontainer/      # Development container setup
└── requirements.txt    # Python dependencies
```

---

## ▶️ Access the App

You can try the live demo here:  
👉 **[Risk Streamlit App](https://solariskmaintenance.streamlit.app/)**  

---

## 📡 Data Flow
- Sensors → Supabase (real-time ingestion) → Risk Streamlit → Dashboard visualization  

---

## 🌱 Future Improvements
- Add **machine learning models** for predictive risk assessment  
- Expand **sensor integration** for broader solar system monitoring  
- Implement **alert notifications** (email/SMS) for critical states  
- Enhance **visual analytics** with historical trend tracking  

---

## 🤝 Contributing
Contributions are welcome!  
- Fork the repo  
- Create a new branch (`feature/your-feature`)  
- Commit changes  
- Open a Pull Request  

---

## 📜 License
This project is licensed under the MIT License. See `LICENSE` for details.
