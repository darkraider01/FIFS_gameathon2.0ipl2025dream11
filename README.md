# 🏏 IPL Fantasy Squad Prediction System

This project builds an **automated IPL fantasy squad selection system** using a combination of:

- 📊 Statistical modeling  
- 🤖 Neural network predictions  
- 🌐 Web scraping (player historical data)  

It processes player performance data and outputs an **optimal 15-player squad** with Captain (C) and Vice-Captain (VC).

---

## 🚀 Features

- Scrapes IPL player data from Howstat  
- Performs **feature engineering (EDTA)** for batting & bowling  
- Uses:
  - 📈 Statistical model
  - 🧠 Neural Network model (PyTorch weights)
- Combines both models using normalization  
- Selects:
  - ✔️ Best XI (playing squad)
  - ✔️ X-Factor substitutes  
- Assigns:
  - 🏅 Captain (C)
  - 🥈 Vice-Captain (VC)

---

## 📂 Project Structure

```
binary_bandits/
│
├── Dataset/
│   ├── player_data/
│   │   ├── bat/
│   │   └── bowl/
│   ├── modified_player_data/
│   ├── merged_data/
│   └── extras/
│       ├── howstat_id.json
│       └── squaddata.csv
│
├── player_weights/
│   ├── bat/
│   └── bowl/
│
├── binary_bandits_output.csv
└── main_script.py
```

---

## ⚙️ Workflow

### 1. Input
- Excel file: `SquadPlayerNames_IndianT20League_Dup.xlsx`
- Match sheet: `Match_<match_num>`

---

### 2. Data Collection
- Scrapes player data using:
  - Batting stats
  - Bowling stats
  - Summary stats  

---

### 3. Feature Engineering (EDTA)

#### 🏏 Batting
- Runs, Balls Faced, Strike Rate  
- Career averages  
- Rolling averages (last 4 matches)  
- Match-based scoring  

#### 🎯 Bowling
- Wickets, Runs conceded, Economy rate  
- Career + rolling averages  
- Match-based scoring  

---

## 🧠 Models Used

### 📊 Statistical Model
- Combines:
  - Career performance  
  - Recent form  

### 🤖 Neural Network Model
- Uses pre-trained `.pkl` weights  
- Manual forward pass using PyTorch  

---

## 📈 Final Scoring

- Normalize:
  - `Stats_Total_Points`
  - `NN_Total_Points`

```
Final Score = Stats + NN
```

---

## 🏆 Squad Selection Logic

- Select 1 player per role:
  - All-Rounder
  - Bowler
  - Batter
  - WK-Batter  

- Add:
  - Top batters per team  
  - Top bowlers per team  

- Ensure:
  - 11 players → extended to 15  

- Assign:
  - Captain (C)
  - Vice-Captain (VC)

---

## 🔑 Key Functions

- `scrape_howstat_player_data()` → Fetches player stats  
- `batting_EDTA()` → Processes batting features  
- `bowling_EDTA()` → Processes bowling features  
- `predict_points()` → Neural network inference  
- `process_players()` → Batch prediction  

---

## 📦 Requirements

```
pip install pandas numpy torch scikit-learn beautifulsoup4 requests tqdm fuzzywuzzy
```

---

## ▶️ How to Run

```
python main_script.py
```

Make sure:
- Excel file exists  
- Player weights are available  
- Dataset folders are correct  

---

## 📊 Output

### `binary_bandits_output.csv`

| Name | Team | C/VC |
|------|------|------|
| Player1 | TeamA | C |
| Player2 | TeamB | VC |

---

## ⚠️ Notes

- Requires:
  - Player weights (`.pkl`)
  - Player ID mapping (`howstat_id.json`)
- Uses fuzzy matching for player names  
- Handles missing data gracefully  

---

## 💡 Future Improvements

- Replace scraping with live API  
- Train unified neural network  
- Build UI dashboard  
- Add real-time updates  

---

## 👨‍💻 Author

Hybrid ML + statistical approach for IPL fantasy optimization
