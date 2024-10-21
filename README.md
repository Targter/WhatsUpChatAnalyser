# WhatsApp Chat Analyzer

This is a **Streamlit-based application** that allows you to analyze WhatsApp chat data. Users can upload WhatsApp chat files (in `.txt`, `.csv`, or `.xlsx` format) and generate insights such as the most active users, media statistics, and activity timelines.

## Features
- **User Activity Insights:** Analyze total messages, media messages, and URLs shared by users.
- **Timeline Analysis:** Visualize chat activity over time (monthly, daily, and weekly).
- **Word Cloud:** Generate a word cloud based on the most frequent words in the chat.
- **Emoji Analysis:** See how frequently different emojis are used in the chat.
- **Heatmap:** A heatmap showing the weekly activity of users.
- **Most Active Users:** Identify the most active users in group chats.

## Demo
You can see the app in action [here]((https://abwork-chatanalyser.streamlit.app/))

## Installation

To run this application locally, follow these steps:

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/whatsapp-chat-analyzer.git
cd whatsapp-chat-analyzer
pip install -r requirements.txt
streamlit run app.py
## 2. Install the Dependencies
Ensure you have Python installed (preferably 3.8+). Then, install the required dependencies using:

bash
Copy code
pip install -r requirements.txt
## 3. Run the Application
You can run the Streamlit app using the following command:

bash
Copy code
streamlit run app.py
This will open the app in your browser on http://localhost:8501.

### Usage
Upload the WhatsApp chat file (txt, csv, or xlsx) from the sidebar.
Select the user for which you want to see the analysis.
Explore the insights, including message statistics, media messages, word clouds, and emoji usage.
