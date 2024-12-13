# WhatsApp Chat Analyzer

## Overview
This project is a **WhatsApp Chat Analyzer** that provides insightful analytics for WhatsApp chat data. By leveraging Python libraries, I performed data cleaning, exploratory data analysis (EDA), and visualizations to uncover interesting patterns and trends within conversations.

## Key Features
- **Data Cleaning**: Processed raw WhatsApp chat exports to structure the data for analysis.
- **Exploratory Data Analysis (EDA)**:
  - Extracted key metrics such as total messages, word counts, and active participants.
  - Identified the most frequently used words, emojis, and media files shared.
  - Analyzed chat activity trends by time, day, and month.
- **Interactive Visualizations**:
  - Time-series plots for message frequency.
  - Heatmaps for identifying active days and hours.
  - Word clouds for commonly used words.
  
## Tools and Libraries
- **Python**:
  - `pandas` for data manipulation.
  - `matplotlib` and `seaborn` for visualizations.
  - `wordcloud` for generating word clouds.
- **Streamlit**: For deploying the interactive analytics dashboard.

## How to Use
1. Export a WhatsApp chat:
   - Open the chat in WhatsApp.
   - Navigate to **More Options > Export Chat** (without media for faster processing).
  https://whatsapp-chat-analyzerp.streamlit.app/
