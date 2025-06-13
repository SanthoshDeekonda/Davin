# 🚀 Davin - Data Visualization Interface

Davin is a user-friendly desktop application built using **Python** and **PyQt5**, designed to simplify data visualization and reporting for CSV and Excel files. Whether you're a student, educator, or data enthusiast, Davin enables you to quickly upload, visualize, and document data without writing a single line of code.

---

## 📊 Features

✅ **Multi-format Support**  
• Load data from CSV, Excel (.xlsx) files.  

✅ **Interactive Visualizations**  
• Create and interact with a wide range of Plotly charts:
  - Bar Chart (Vertical & Horizontal)  
  - Line Plot  
  - Pie Chart  
  - Scatter Plot  
  - Histogram  
  - Area Chart  
  - Box Plot  

✅ **Zoom & Pan**  
• Charts are embedded using `QWebEngineView` and support zooming/panning through a custom `QGraphicsView`.

✅ **Image Export**  
• Save charts as high-quality PNG files.

✅ **Report Editor**  
• Compose rich text reports with chart previews.  
• Format text (bold, italic, underline, fonts, sizes).  
• Export the entire report (with charts) as a **PDF**.

✅ **Multi-window Architecture**  
• Cleanly separated workflow:  
  1. **Data Upload Window**  
  2. **Visualization Window**  
  3. **Report Editor Window**

✅ **Threaded Architecture**  
• Heavy operations (e.g., chart generation) run in background threads to keep the UI smooth.

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **PyQt5**
- **Pandas**
- **Plotly**
- **QWebEngineView**
- **OpenPyXL**
- **Kaleido** (for saving charts as images)

---

## 💻 Installation

1. **Clone this repository:**
   ```bash
   git clone https://github.com/SanthoshDeekonda/Davin
   cd davin
