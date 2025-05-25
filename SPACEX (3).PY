{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 10,
   "id": "cbbc7055-e20a-439f-99d9-070ec45bffcd",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "2025-05-25 08:12:21.897 No runtime found, using MemoryCacheStorageManager\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Welcome to the application!\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "DeltaGenerator()"
      ]
     },
     "execution_count": 10,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "import streamlit as st\n",
    "import pandas as pd\n",
    "import requests\n",
    "\n",
    "# index.py\n",
    "\n",
    "def main():\n",
    "    print(\"Welcome to the application!\")\n",
    "    # Your main application logic goes here\n",
    "\n",
    "if __name__ == \"__main__\":\n",
    "    main()\n",
    "\n",
    "\n",
    "st.set_page_config(page_title=\"SpaceX Launch Analysis & Prediction\", layout=\"wide\")\n",
    "\n",
    "st.title(\"🚀 SpaceX Launch Analysis & Prediction Platform\")\n",
    "\n",
    "# Load launch data\n",
    "@st.cache_data\n",
    "def load_launch_data():\n",
    "    url = \"https://api.spacexdata.com/v4/launches\"\n",
    "    response = requests.get(url)\n",
    "    data = response.json()\n",
    "    df = pd.json_normalize(data)\n",
    "    return df\n",
    "\n",
    "# Simulated weather function (replace with real API as needed)\n",
    "def get_weather_condition(date):\n",
    "    # Just an example. In real use, fetch historical weather for the date & location.\n",
    "    import random\n",
    "    return random.choice(['Clear', 'Cloudy', 'Rainy', 'Stormy', 'Windy'])\n",
    "\n",
    "# Load data\n",
    "df = load_launch_data()\n",
    "\n",
    "# Show column names to verify\n",
    "st.write(\"Available columns:\", df.columns.tolist())\n",
    "\n",
    "# Add weather condition column\n",
    "if 'weather_condition' not in df.columns:\n",
    "    df['weather_condition'] = df['date_utc'].apply(get_weather_condition)\n",
    "\n",
    "# Extract year from date\n",
    "df['year'] = pd.to_datetime(df['date_utc']).dt.year\n",
    "\n",
    "# Sidebar filters\n",
    "years = st.sidebar.multiselect(\"Select Launch Years\", sorted(df['year'].unique()), default=sorted(df['year'].unique()))\n",
    "\n",
    "filtered_df = df[df['year'].isin(years)]\n",
    "\n",
    "st.subheader(f\"Filtered Launches ({len(filtered_df)} records)\")\n",
    "\n",
    "# Columns to display – check existence to avoid KeyError\n",
    "columns_to_display = ['name', 'rocket', 'success', 'date_utc', 'weather_condition']\n",
    "available_columns = [col for col in columns_to_display if col in filtered_df.columns]\n",
    "\n",
    "# Show filtered table\n",
    "st.dataframe(filtered_df[available_columns].head(20))\n",
    "\n",
    "# Optional: Add a map if location data is available\n",
    "if 'launchpad.latitude' in filtered_df.columns and 'launchpad.longitude' in filtered_df.columns:\n",
    "    st.subheader(\"Launch Locations Map\")\n",
    "    map_df = filtered_df[['launchpad.latitude', 'launchpad.longitude']].dropna()\n",
    "    map_df.columns = ['lat', 'lon']\n",
    "    st.map(map_df)\n",
    "\n",
    "# Optional: Show charts\n",
    "st.subheader(\"Launches by Year\")\n",
    "launch_count = filtered_df.groupby('year').size()\n",
    "st.bar_chart(launch_count)\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "8a16202f-0f7f-48d2-8047-ccb0d087b153",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
