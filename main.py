import requests
from bs4 import BeautifulSoup
import json
from tqdm import tqdm
import torch
import pandas as pd
import os
import pickle
import glob
from sklearn.preprocessing import MinMaxScaler
from fuzzywuzzy import process
import sys

pd.options.mode.chained_assignment = None 
// ipl teams 2025
players_team_dict = {
"CHE" : ['MS DHONI', 'DEVON CONWAY', 'RAHUL TRIPATHI', 'SHAIK RASHEED', 'VANSH BEDI', 'ANDRE SIDDARTH', 'RACHIN RAVINDRA', 'RAVICHANDRAN ASHWIN', 'VIJAY SHANKAR', 'SAM CURRAN', 'ANSHUL KAMBOJ', 'DEEPAK HOODA', 'JAMIE OVERTON', 'KAMLESH NAGARKOTI', 'RAMAKRISHNA GHOSH', 'RAVINDRA JADEJA', 'SHIVAM DUBE', 'KHALEEL AHMED', 'NOOR AHMAD', 'MUKESH CHOUDHARY', 'GURJAPNEET SINGH', 'NATHAN ELLIS', 'SHREYAS GOPAL', 'MATHEESHA PATHIRANA'],

"DC" : ['KL RAHUL', 'JAKE FRASER-MCGURK', 'KARUN NAIR', 'FAF DU PLESSIS', 'DONOVAN FERREIRA', 'ABISHEK POREL', 'TRISTAN STUBBS', 'AXAR PATEL', 'SAMEER RIZVI', 'ASHUTOSH SHARMA', 'DARSHAN NALKANDE', 'VIPRAJ NIGAM', 'AJAY MANDAL', 'MANVANTH KUMAR', 'TRIPURANA VIJAY', 'MADHAV TIWARI', 'MITCHELL STARC', 'T. NATARAJAN', 'MOHIT SHARMA', 'MUKESH KUMAR', 'DUSHMANTHA CHAMEERA', 'KULDEEP YADAV'],

"GT" : ['SHUBMAN GILL', 'JOS BUTTLER', 'KUMAR KUSHAGRA', 'ANUJ RAWAT', 'SHERFANE RUTHERFORD', 'NISHANT SINDHU', 'MAHIPAL LOMROR', 'WASHINGTON SUNDAR', 'MOHD. ARSHAD KHAN', 'SAI KISHORE', 'JAYANT YADAV', 'KARIM JANAT', 'SAI SUDHARSAN', 'SHAHRUKH KHAN', 'KAGISO RABADA', 'MOHAMMED SIRAJ', 'PRASIDH KRISHNA', 'MANAV SUTHAR', 'GERALD COETZEE', 'GURNOOR SINGH BRAR', 'ISHANT SHARMA', 'KULWANT KHEJROLIYA', 'RAHUL TEWATIA', 'RASHID KHAN'],

"KKR" : ['AJINKYA RAHANE', 'RINKU SINGH', 'QUINTON DE KOCK', 'RAHMANULLAH GURBAZ', 'ANGKRISH RAGHUVANSHI', 'ROVMAN POWELL', 'MANISH PANDEY', 'LUVNITH SISODIA', 'VENKATESH IYER', 'ANUKUL ROY', 'MOEEN ALI', 'RAMANDEEP SINGH', 'ANDRE RUSSELL', 'ANRICH NORTJE', 'VAIBHAV ARORA', 'MAYANK MARKANDE', 'SPENCER JOHNSON', 'HARSHIT RANA', 'SUNIL NARINE', 'VARUN CHAKARAVARTHY', 'CHETAN SAKARIYA'],

"LSG" : ['RISHABH PANT', 'DAVID MILLER', 'AIDEN MARKRAM', 'ARYAN JUYAL', 'HIMMAT SINGH', 'MATTHEW BREETZKE', 'NICHOLAS POORAN', 'MITCHELL MARSH', 'ABDUL SAMAD', 'SHAHBAZ AHAMAD', 'YUVRAJ CHAUDHARY', 'RAJVARDHAN HANGARGEKAR', 'ARSHIN KULKARNI', 'AYUSH BADONI', 'SHARDUL THAKUR', 'AVESH KHAN', 'AKASH DEEP', 'M. SIDDHARTH', 'DIGVESH SINGH', 'AKASH SINGH', 'SHAMAR JOSEPH', 'PRINCE YADAV', 'MAYANK YADAV', 'RAVI BISHNOI'],

"MI" : ['ROHIT SHARMA', 'SURYA KUMAR YADAV', 'ROBIN MINZ', 'RYAN RICKELTON', 'SHRIJITH KRISHNAN', 'BEVON JACOBS', 'N. TILAK VARMA', 'HARDIK PANDYA', 'NAMAN DHIR', 'WILL JACKS', 'MITCHELL SANTNER', 'RAJ ANGAD BAWA', 'VIGNESH PUTHUR', 'CORBIN BOSCH', 'TRENT BOULT', 'KARN SHARMA', 'DEEPAK CHAHAR', 'ASHWANI KUMAR', 'REECE TOPLEY', 'V.SATYANARAYANA PENMETSA', 'ARJUN TENDULKAR', 'MUJEEB-UR-RAHMAN', 'JASPRIT BUMRAH'],

"PBKS" : ['SHREYAS IYER', 'NEHAL WADHERA', 'VISHNU VINOD', 'JOSH INGLIS', 'HARNOOR PANNU', 'PYLA AVINASH', 'PRABHSIMRAN SINGH', 'SHASHANK SINGH', 'MARCUS STOINIS', 'GLENN MAXWELL', 'HARPREET BRAR', 'MARCO JANSEN', 'AZMATULLAH OMARZAI', 'PRIYANSH ARYA', 'AARON HARDIE', 'MUSHEER KHAN', 'SURYANSH SHEDGE', 'ARSHDEEP SINGH', 'YUZVENDRA CHAHAL', 'VYSHAK VIJAYKUMAR', 'YASH THAKUR', 'LOCKIE FERGUSON', 'KULDEEP SEN', 'XAVIER BARTLETT', 'PRAVIN DUBEY'],

"RR" : ['SANJU SAMSON', 'SHUBHAM DUBEY', 'VAIBHAV SURYAVANSHI', 'KUNAL RATHORE', 'SHIMRON HETMYER', 'YASHASVI JAISWAL', 'DHRUV JUREL', 'RIYAN PARAG', 'NITISH RANA', 'YUDHVIR CHARAK', 'JOFRA ARCHER', 'MAHEESH THEEKSHANA', 'WANINDU HASARANGA', 'AKASH MADHWAL', 'KUMAR KARTIKEYA SINGH', 'TUSHAR DESHPANDE', 'FAZALHAQ FAROOQI', 'KWENA MAPHAKA', 'ASHOK SHARMA', 'SANDEEP SHARMA'],

"RCB" : ['RAJAT PATIDAR', 'VIRAT KOHLI', 'PHIL SALT', 'JITESH SHARMA', 'DEVDUTT PADIKKAL', 'SWASTIK CHHIKARA', 'LIAM LIVINGSTONE', 'KRUNAL PANDYA', 'SWAPNIL SINGH', 'TIM DAVID', 'ROMARIO SHEPHERD', 'MANOJ BHANDAGE', 'JACOB BETHELL', 'JOSH HAZLEWOOD', 'RASIKH DAR', 'SUYASH SHARMA', 'BHUVNESHWAR KUMAR', 'NUWAN THUSHARA', 'LUNGISANI NGIDI', 'ABHINANDAN SINGH', 'MOHIT RATHEE', 'YASH DAYAL'],

"SRH" : ['ISHAN KISHAN', 'ATHARVA TAIDE', 'ABHINAV MANOHAR', 'ANIKET VERMA', 'SACHIN BABY', 'HEINRICH KLAASEN', 'TRAVIS HEAD', 'HARSHAL PATEL', 'KAMINDU MENDIS', 'WIAAN MULDER', 'ABHISHEK SHARMA', 'NITISH KUMAR REDDY', 'PAT CUMMINS', 'MOHAMMAD SHAMI', 'RAHUL CHAHAR', 'ADAM ZAMPA', 'SIMARJEET SINGH', 'ZEESHAN ANSARI', 'JAYDEV UNADKAT', 'ESHAN MALINGA']

}




match_num = 76 #sys.argv[1]
sheet_name = f"Match_{match_num}"

excel_path = os.path.join("SquadPlayerNames_IndianT20League_Dup.xlsx")

try:
    input_df = pd.read_excel(excel_path, sheet_name=sheet_name)
except Exception as e:
    print("Error as:", e)
    quit()
    
    
    
input_df["Player Name"] = input_df["Player Name"].apply(
    lambda name: "KL Rahul" if str(name).strip().lower() == "lokesh rahul" else name
)

teams = input_df["Team"].unique().tolist()
teams = [team.strip().upper() for team in teams]

player_names = []

for team in teams:
    player_names.extend(players_team_dict[team])

# player_names = players_team_dict["KKR"] + players_team_dict["RCB"]

def scrape_howstat_player_data(playerID,role_query,playerName):

    if role_query.lower() == 'bat':
        url = f'https://www.howstat.com/Cricket/Statistics/IPL/PlayerProgressBat.asp?PlayerID={playerID}'
         
    elif role_query.lower() == 'bowl':
        url = f'https://www.howstat.com/Cricket/Statistics/IPL/PlayerProgressBowl.asp?PlayerID={playerID}'
    elif role_query.lower() == 'summary':
        url = f'https://www.howstat.com/Cricket/Statistics/IPL/PlayerProgressSummary.asp?PlayerID={playerID}'
        
    # Send a GET request to fetch the HTML content
    response = requests.get(url)

    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the table with the class name "TableLined"
    table = soup.find('table', class_='TableLined')

    # Convert the table to HTML and print it
    if table:
        table_html = str(table)

        
        # Parse HTML using BeautifulSoup
        soup = BeautifulSoup(table_html, "html.parser")

        # Extract table headers
        headers = [th.text.strip() for th in soup.find_all("tr")[2].find_all("td")]

        # Extract table rows
        rows = []
        for tr in soup.find_all("tr")[3:]:
            cols = [td.text.strip() for td in tr.find_all("td")]
            if cols:
                rows.append(cols)

        # Create DataFrame
        df = pd.DataFrame(rows, columns=headers)
        
        if role_query == 'bat':
            df = df[:-1]
        base_dir = os.path.join( "binary_bandits", "Dataset", "player_data", role_query)
        os.makedirs(base_dir, exist_ok=True)
        file_path = os.path.join(base_dir, f"{playerName}.csv")
        df.to_csv(file_path, index=False)
        # print(Fore.GREEN + f"Table found for {playerName} - {role_query}")
    else:
        pass



with open(os.path.join("binary_bandits","Dataset","extras","howstat_id.json") , "r") as f:
    player_IDs = json.load(f)


player_IDs = {player: id for player, id in player_IDs.items() if player in player_names}



# for player in tqdm(player_IDs, desc="Updating player data", unit="player"):
#     if player_IDs[player]:
#         try:
#             scrape_howstat_player_data(playerName=player, playerID=player_IDs[player], role_query="bat")
#         except:
#             pass
#         try:
#             scrape_howstat_player_data(playerName=player, playerID=player_IDs[player], role_query="bowl")
#         except:
#             pass
#         try:
#             scrape_howstat_player_data(playerName=player, playerID=player_IDs[player], role_query="summary")
#         except:
#             pass



def batting_EDTA(df,name):
    df = df[~df["How Dismissed"].astype(str).str.strip().isin(["did not bat", "DNB"])]
    df["Name"] = name
    df = df[["Name","Date","Runs","B/F"]]
    df = df[~df["Runs"].astype(str).str.strip().isin(["-","DNB"])]
    df = df[~df["B/F"].astype(str).str.strip().isin(["-","DNB"])]

    
    def convert_fields(value):
        if value[-1] == "*":
            value = value[:len(value)-1]
        
        return int(value)

    df["Runs"] = df["Runs"].astype(str).apply(convert_fields)
    df["B/F"] = df["B/F"].astype(str).apply(convert_fields)
    
    df["Batting S/R"] = (df["Runs"] * 100 / df["B/F"]).round(2)
    
    df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%Y", dayfirst=True)
    df = df.sort_values(by="Date")
    
    df["Career Runs Avg"] = df["Runs"].expanding().apply(lambda x: x[:-1].mean() if len(x) > 1 else 0).round(2)
    df["Career Batting S/R Avg"] = df["Batting S/R"].expanding().apply(lambda x: x[:-1].mean() if len(x) > 1 else 0).round(2)
    df["Career B/F Avg"] = df["B/F"].expanding().apply(lambda x: x[:-1].mean() if len(x) > 1 else 0).round(2)
    
    if len(df) == 0 :
        columns = ['Name', 'Date', 'Runs', 'B/F', 'Batting S/R', 'Career Runs Avg',
       'Career Batting S/R Avg', 'Career B/F Avg', 'Rolling Runs Avg',
       'Rolling B/F Avg', 'Rolling Batting S/R Avg', 'Batting Match Points']
        
        df = pd.DataFrame(columns=columns)  # Initialize empty DataFrame
        df.loc[0] = [0] * len(columns) 
        
        return df
    
    rolling_const = min(4,len(df))

    df["Rolling Runs Avg"] = df["Runs"].shift(1).rolling(window=rolling_const, min_periods=1).mean().round(2).fillna(0) 
    df["Rolling B/F Avg"] = df["B/F"].shift(1).rolling(window=rolling_const, min_periods=1).mean().round(2).fillna(0) 
    df["Rolling Batting S/R Avg"] = df["Batting S/R"].shift(1).rolling(window=rolling_const, min_periods=1).mean().round(2).fillna(0) 

    def calculate_match_points(runs,batting_sr):
        points = runs
        
        if runs>25:points += 4
        if runs>50:points += 8
        if runs>75:points += 12
        if runs>100:points += 16
        
        if batting_sr>170:points +=6
        elif batting_sr>=150.01:points +=4
        elif batting_sr>=130:points +=4
        
        return points

    df["Batting Match Points"] = df.apply(lambda row: calculate_match_points(row["Runs"], row["Batting S/R"]), axis=1)
    
    return df

fp = os.path.join("binary_bandits","Dataset","player_data","bat")

output_fp = os.path.join("binary_bandits","Dataset","modified_player_data","bat")
os.makedirs(output_fp, exist_ok=True)

print("Processing")
for file in tqdm(os.listdir(fp), desc="Processing files", unit="file"):
    try:
        df = batting_EDTA(df = pd.read_csv(os.path.join(fp, file)),name=file.replace(".csv", ""))
    except:
        pass
    df.to_csv(os.path.join(output_fp, file), index=False)
    
    
def bowling_EDTA(df,name):
    
        df = df[~df["Batsman Dismissed"].astype(str).str.strip().isin(["did not bowl", "DNB"])]
        df["Name"] = name
        
        df = df[["Name","Date","Overs","Wickets"]]
        df = df[~df["Wickets"].astype(str).str.strip().isin(["-", "DNB"])].dropna(subset=["Wickets"])
        df = df[~df["Overs"].astype(str).str.strip().isin(["-", "DNB"])].dropna(subset=["Overs"])

        
        if len(df) == 0 :
            columns = ['Name', 'Date', 'Wickets', 'Runs Conceded', 'Bowling E/R',
        'Career Wickets Avg', 'Career Runs Conceded Avg',
        'Career Bowling E/R Avg', 'Rolling Wickets Avg',
        'Rolling Runs Conceded Avg', 'Rolling Bowling E/R Avg', 'Bowling Match Points']
            
            df = pd.DataFrame(columns=columns)  # Initialize empty DataFrame
            df.loc[0] = [0] * len(columns) 
            
            return df
        
        df[["Wickets", "Runs Conceded"]] = df["Wickets"].str.split("/", expand=True)
        
        df["Wickets"] = df["Wickets"].astype(int)
        df["Runs Conceded"] = df["Runs Conceded"].astype(int)

        
        df["Bowling E/R"] = (df["Runs Conceded"]/df["Overs"]).round(2)
        df = df.drop(columns=["Overs"])

        df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%Y", dayfirst=True)
        df = df.sort_values(by="Date")
        
        
        df["Career Wickets Avg"] = df["Wickets"].expanding().apply(lambda x: x[:-1].mean() if len(x) > 1 else 0).round(2)
        df["Career Runs Conceded Avg"] = df["Runs Conceded"].expanding().apply(lambda x: x[:-1].mean() if len(x) > 1 else 0).round(2)
        df["Career Bowling E/R Avg"] = df["Bowling E/R"].expanding().apply(lambda x: x[:-1].mean() if len(x) > 1 else 0).round(2)
        
        
        
        rolling_const = min(4,len(df))

        df["Rolling Wickets Avg"] = df["Wickets"].shift(1).rolling(window=rolling_const, min_periods=1).mean().round(2).fillna(0) 
        df["Rolling Runs Conceded Avg"] = df["Runs Conceded"].shift(1).rolling(window=rolling_const, min_periods=1).mean().round(2).fillna(0) 
        df["Rolling Bowling E/R Avg"] = df["Bowling E/R"].shift(1).rolling(window=rolling_const, min_periods=1).mean().round(2).fillna(0) 


        def calculate_match_points(wickets,bowling_er):
            points = wickets*25

            if bowling_er<5:points +=6
            elif bowling_er<6:points +=4
            elif bowling_er<7:points +=2
            
            return points

        df["Bowling Match Points"] = df.apply(lambda row: calculate_match_points(row["Wickets"], row["Bowling E/R"]), axis=1)
        
        
        return df


        



fp = os.path.join("binary_bandits","Dataset","player_data","bowl")
output_fp = os.path.join("binary_bandits","Dataset","modified_player_data","bowl")
os.makedirs(output_fp, exist_ok=True)


for file in tqdm(os.listdir(fp), desc="Processing files", unit="file"):
    try:
        df = bowling_EDTA(pd.read_csv(os.path.join(fp, file)),name=file.replace(".csv", ""))
    except:
        pass
    df.to_csv(os.path.join(output_fp, file), index=False)
    


folder_path = os.path.join("binary_bandits","Dataset","modified_player_data","bowl")  # Change this to your folder path
all_files = glob.glob(os.path.join(folder_path, "*.csv"))  # Get all CSV files

df_list = [pd.read_csv(file) for file in all_files]  # Read all CSVs
final_df = pd.concat(df_list, ignore_index=True)  # Concatenate vertically

# Save the merged DataFrame
os.makedirs(os.path.join("binary_bandits","Dataset","merged_data"), exist_ok=True)

final_df.to_csv(os.path.join("binary_bandits","Dataset","merged_data","all_bowling_merged.csv"), index=False)

folder_path = os.path.join("binary_bandits","Dataset","modified_player_data","bat") # Change this to your folder path
all_files = glob.glob(os.path.join(folder_path, "*.csv"))  # Get all CSV files

df_list = [pd.read_csv(file) for file in all_files]  # Read all CSVs
final_df = pd.concat(df_list, ignore_index=True)  # Concatenate vertically

# Save the merged DataFrame
final_df.to_csv(os.path.join("binary_bandits","Dataset","merged_data","all_batting_merged.csv"), index=False)
    
    
    
def predict_points(df, weights, feature_type="bowling"):
    try:
        # Select appropriate feature columns based on type
        if feature_type == "bowling":
            feature_cols = ['Career Wickets Avg', 'Career Runs Conceded Avg', 'Career Bowling E/R Avg', 
                           'Rolling Wickets Avg', 'Rolling Runs Conceded Avg', 'Rolling Bowling E/R Avg']
        else:  # batting
            feature_cols = ['Career Runs Avg', 'Career B/F Avg', 'Career Batting S/R Avg', 
                           'Rolling Runs Avg', 'Rolling B/F Avg', 'Rolling Batting S/R Avg']
        
        # Process input data
        df_clean = df.dropna()
        input_features = df_clean[feature_cols].mean().values
        input_tensor = torch.tensor(input_features, dtype=torch.float32)
        
        # Extract and sort layer weights
        weight_keys = sorted([k for k in weights.keys() if '.weight' in k], 
                            key=lambda x: int(x.split('.')[1]))
        
        # Build layers from weights and biases
        layers = []
        for weight_key in weight_keys:
            layer_prefix = weight_key.rsplit('.', 1)[0]
            bias_key = f"{layer_prefix}.bias"
            
            w = torch.tensor(weights[weight_key], dtype=torch.float32)
            b = torch.tensor(weights[bias_key], dtype=torch.float32)
            layers.append((w, b))
        
        # Forward pass
        output = input_tensor
        for i, (w, b) in enumerate(layers):
            output = torch.matmul(output, w.T) + b
            if i < len(layers) - 1:
                output = torch.relu(output)
        
        # Fix for NumPy scalar conversion warning
        output_value = output.detach().numpy()
        return float(output_value.item())  # Extract scalar value properly
    
    except Exception as e:
        print(f"Points prediction failed: {e}")
        return 0

def process_players(player_names):

    results = []  # Store results as list of dicts firs
    weights_dir = os.path.join("binary_bandits","player_weights")
    

    
    for i, player in enumerate(player_names):
        try:
                
            # Process batting points
            batting_filepath = os.path.join("binary_bandits","Dataset","modified_player_data","bat")
            batting_df = pd.read_csv(os.path.join(batting_filepath, f"{player}.csv"))
            batting_df['Date'] = pd.to_datetime(batting_df['Date'], errors='coerce')
            
            batting_weights_path = os.path.join(weights_dir, "bat", f"{player}_weights.pkl")
            with open(batting_weights_path, 'rb') as f:
                batting_weights = pickle.load(f)
            
            batting_pts = predict_points(batting_df, batting_weights, feature_type="batting")
            if len(batting_df)<4:
                batting_pts *= len(batting_df)/4
                
            if len(batting_df[batting_df['Date'].dt.year == 2025]) <3:
                batting_pts *= len(batting_df[batting_df['Date'].dt.year == 2025]) /3

            
            # Process bowling points
            bowling_filepath = os.path.join("binary_bandits","Dataset","modified_player_data","bowl")
            bowling_df = pd.read_csv(os.path.join(bowling_filepath, f"{player}.csv"))
            bowling_df['Date'] = pd.to_datetime(bowling_df['Date'], errors='coerce')

            
            bowling_weights_path = os.path.join(weights_dir, "bowl", f"{player}_weights.pkl")
            with open(bowling_weights_path, 'rb') as f:
                bowling_weights = pickle.load(f)
            
            bowling_pts = predict_points(bowling_df, bowling_weights, feature_type="bowling")
            if len(bowling_df) < 4:
                bowling_pts *= len(bowling_df) / 4
            
            
            if len(bowling_df[bowling_df['Date'].dt.year == 2025]) <3:
                bowling_pts *= len(bowling_df[bowling_df['Date'].dt.year == 2025]) /3
            # Add to results list
            results.append({
                "Name": player,
                "Batting Points": batting_pts,
                "Bowling Points": bowling_pts
            })
        
        except Exception as e:
            # print(len(bowling_df[bowling_df['Date'].dt.year == 2025]))
            # print("error")
            pass
    
    # Create DataFrame from results list at the end (avoids concat warnings)
    return pd.DataFrame(results)


NN_model_df = process_players(player_names=player_names)
NN_model_df.fillna(0,inplace=True)

squads_df = pd.read_csv(os.path.join("binary_bandits","Dataset","extras","squaddata.csv"))

squads_df['Name'] = squads_df['Name'].str.strip().str.title()
NN_model_df['Name'] = NN_model_df['Name'].str.strip().str.title()
NN_model_df = NN_model_df.drop(columns=['Team', 'Role','Predicted Role'], errors='ignore')
NN_model_df = NN_model_df.merge(squads_df[['Name', 'Team', 'Role','Predicted Role']], on='Name', how='left')



NN_model_df.loc[NN_model_df["Predicted Role"].isin(["Batter", "WK-Batter"]), "Bowling Points"] = 0
NN_model_df.loc[NN_model_df["Predicted Role"].isin(["Bowler"]), "Batting Points"] = 0

NN_model_df["NN_Total_Points"] = NN_model_df['Batting Points'] + NN_model_df['Bowling Points'] 
# NN_model_df.loc[NN_model_df["Predicted Role"] == "All-Rounder", "NN_Total_Points"] *= 0.8


NN_model_df = NN_model_df.sort_values(by="NN_Total_Points", ascending=False).reset_index(drop=True)

# print("\n"," "*15,"-"*30,"NN Model","-"*30,"\n")
# print(NN_model_df)

# Read separate datasets for batting and bowling
batting_df = pd.read_csv(os.path.join("binary_bandits","Dataset","merged_data","all_batting_merged.csv"))
bowling_df = pd.read_csv(os.path.join("binary_bandits","Dataset","merged_data","all_bowling_merged.csv"))





def predict_batting_points(career_runs, career_batting_sr, rolling_runs, rolling_sr, match_num,this_year_matches=4,career_factor=0.4,rolling_factor=1):
    runs = ((career_factor*career_runs)+(rolling_factor*rolling_runs))/2
    batting_sr = ((career_factor*career_batting_sr)+(rolling_factor*rolling_sr))/2
    points = runs
        
    if runs>25:points += 4
    if runs>50:points += 8
    if runs>75:points += 12
    if runs>100:points += 16
    
    if batting_sr>170:points +=6
    elif batting_sr>=150.01:points +=4
    elif batting_sr>=130:points +=2
    
    if match_num<4:
        points *= match_num/4
        
    if this_year_matches<3:
        points *=0.5
    
    return points

def predict_bowling_points(career_wickets, career_er, rolling_wickets, rolling_er,match_num,this_year_matches=4,career_factor=0.4, rolling_factor=1):
    wickets = ((career_factor*career_wickets)+(rolling_factor*rolling_wickets))/2
    batting_sr = ((career_factor*career_er)+(rolling_factor*rolling_er))/2
    points = wickets*25

    if batting_sr>5:points +=6
    elif batting_sr>6:points +=4
    elif batting_sr>7:points +=2
    
    if match_num<4:
        points *= match_num/4
        
    if this_year_matches<3:
        points *=0.5
    
    return points

# Filter datasets
filtered_batting_df = batting_df[batting_df["Name"].isin(player_names)]
filtered_bowling_df = bowling_df[bowling_df["Name"].isin(player_names)]

# Function to extract player features
def get_batting_features(player, data_df):
    player_df = data_df[data_df["Name"] == player].copy()
    player_df['Date'] = pd.to_datetime(player_df['Date'], errors='coerce')
    rolling_const = min(4, len(player_df))
    
    if player_df.empty:
        return {'Career Runs Avg': 0, 'Career Batting S/R Avg': 0, 
                'Rolling Runs Avg': 0, 'Rolling Batting S/R Avg': 0}
    
    return {
        'Career Runs Avg': player_df["Runs"].mean(),
        'Career Batting S/R Avg': player_df["Batting S/R"].mean(),
        'Rolling Runs Avg': player_df["Runs"].tail(rolling_const).mean() if rolling_const > 0 
            else 0.5*(player_df["Runs"].mean()),
        'Rolling Batting S/R Avg': player_df["Batting S/R"].tail(rolling_const).mean() if rolling_const > 0 
            else 0.5*(player_df["Batting S/R"].mean()),
            'No. of Matches' : len(player_df),
            'No of Matches this year' : len(player_df[player_df['Date'].dt.year == 2025])
    }

def get_bowling_features(player, data_df):
    player_df = data_df[data_df["Name"] == player].copy()
    player_df['Date'] = pd.to_datetime(player_df['Date'], errors='coerce')
    rolling_const = min(4, len(player_df))
    
    if player_df.empty:
        return {'Career Wickets Avg': 0, 'Career Bowling E/R Avg': 0, 
                'Rolling Wickets Avg': 0, 'Rolling Bowling E/R Avg': 0}
    
    return {
        'Career Wickets Avg': player_df["Wickets"].mean(),
        'Career Bowling E/R Avg': player_df["Bowling E/R"].mean(),
        'Rolling Wickets Avg': player_df["Wickets"].tail(rolling_const).mean() if rolling_const > 0 
            else 0.5*(player_df["Wickets"].mean()),
        'Rolling Bowling E/R Avg': player_df["Bowling E/R"].tail(rolling_const).mean() if rolling_const > 0 
            else 0.5*(player_df["Bowling E/R"].mean()),
        'No. of Matches' : len(player_df),
        'No of Matches this year' : len(player_df[player_df['Date'].dt.year == 2025])
        # 'No. of Matches this year' : len(player_df)
    }

# Get features for all players
batting_features = {}
bowling_features = {}

for player in player_names:
    batting_features[player] = get_batting_features(player, filtered_batting_df)
    bowling_features[player] = get_bowling_features(player, filtered_bowling_df)

# Convert to dataframes
batting_stats_df = pd.DataFrame.from_dict(batting_features, orient="index").reset_index().rename(columns={"index": "Name"})
bowling_stats_df = pd.DataFrame.from_dict(bowling_features, orient="index").reset_index().rename(columns={"index": "Name"})

# Calculate predicted points
# Calculate predicted points
batting_stats_df["Batting Points"] = batting_stats_df.apply(
    lambda row: predict_batting_points(
        row["Career Runs Avg"], 
        row["Career Batting S/R Avg"],
        row["Rolling Runs Avg"],
        row["Rolling Batting S/R Avg"],
        row['No. of Matches'],
        row['No of Matches this year'],
        career_factor=0.4, rolling_factor=1,
        
    ), axis=1
)

bowling_stats_df["Bowling Points"] = bowling_stats_df.apply(
    lambda row: predict_bowling_points(
        row["Career Wickets Avg"], 
        row["Career Bowling E/R Avg"],
        row["Rolling Wickets Avg"],
        row["Rolling Bowling E/R Avg"],
        row['No. of Matches'],
        row['No of Matches this year'],
        career_factor=0.4, rolling_factor=1
    ), axis=1
)



# Merge dataframes and calculate total points
stats_df = pd.merge(
    batting_stats_df[["Name", "Batting Points"]], 
    bowling_stats_df[["Name", "Bowling Points"]], 
    on="Name", how="outer"
)

stats_df.fillna(0, inplace=True)
stats_df["Total Points"] = stats_df["Bowling Points"] + stats_df["Batting Points"]


# Final dataframe with required columns
stats_model_df = stats_df[["Name", "Batting Points", "Bowling Points","Total Points"]]

squads_df = pd.read_csv(os.path.join("binary_bandits","Dataset","extras","squaddata.csv"))


squads_df['Name'] = squads_df['Name'].str.strip().str.title()
stats_model_df['Name'] = stats_model_df['Name'].str.strip().str.title()
stats_model_df = stats_model_df.drop(columns=['Team', 'Role','Predicted Role'], errors='ignore')
stats_model_df = stats_model_df.merge(squads_df[['Name', 'Team', 'Role','Predicted Role']], on='Name', how='left')




stats_model_df.loc[stats_model_df["Predicted Role"].isin(["Batter", "WK-Batter"]), "Bowling Points"] = 0
stats_model_df.loc[stats_model_df["Predicted Role"].isin(["Bowler"]), "Batting Points"] = 0

# Step 1: Select 1 player from each role based on "Total Points"
stats_model_df = stats_model_df.sort_values(by="Total Points", ascending=False).reset_index(drop=True)
stats_model_df = stats_model_df.rename(columns={"Total Points": "Stats_Total_Points"})
stats_model_df.loc[stats_model_df["Predicted Role"] == "All-Rounder", "Stats_Total_Points"] *= 0.8

# print("\n"," "*15,"-"*30,"Stats Model","-"*30,"\n")
# print(stats_model_df)


final_df = pd.merge(stats_model_df, NN_model_df, on="Name", how="inner", suffixes=('', '_drop'))

# Drop columns with '_drop' suffix
final_df = final_df[[col for col in final_df.columns if not col.endswith('_drop')]]

scaler = MinMaxScaler()

# Normalize the two columns
final_df[["Stats_Total_Points", "NN_Total_Points"]] = scaler.fit_transform(
    final_df[["Stats_Total_Points", "NN_Total_Points"]]
)

final_df["Total Points"] = final_df["Stats_Total_Points"] + final_df["NN_Total_Points"]
final_df = final_df[~final_df["Name"].isin(["Vipraj Nigam"])]

# Step 1: Select 1 player from each role based on "Total Points"
final_df.sort_values(by="Total Points", ascending=False)



# Step 2: List of names from df
input_df_names = input_df["Player Name"].tolist()

# Step 3–5: Match and add matched_player_name and IsPlaying columns
matched_names = []
is_playing_statuses = []

for name in final_df["Name"]:
    # Get the best match and score
    matched_name, score = process.extractOne(name, input_df_names)
    
    # Save the matched name
    matched_names.append(matched_name)
    
    # Lookup IsPlaying value for that matched name
    is_playing = input_df.loc[input_df["Player Name"] == matched_name, "IsPlaying"].values
    is_playing_statuses.append(is_playing[0] if len(is_playing) > 0 else None)

# Add to final_df
final_df["matched_player_name"] = matched_names
final_df["IsPlaying"] = is_playing_statuses
final_df = final_df[final_df['IsPlaying'].isin(['PLAYING', 'X_FACTOR_SUBSTITUTE'])].reset_index(drop=True)



playing_df = final_df[final_df['IsPlaying'] == 'PLAYING']
xfactor_df = final_df[final_df['IsPlaying'] == 'X_FACTOR_SUBSTITUTE']

# Sort and group to take top 2 X_FACTOR_SUBSTITUTE players per team
top_xfactors = (
    xfactor_df.sort_values('Total Points', ascending=False)
              .groupby('Team')
              .head(2)
)

# Combine both
final_df = pd.concat([playing_df, top_xfactors], ignore_index=True).reset_index(drop=True)

roles = ["All-Rounder", "Bowler", "Batter", "WK-Batter"]
selected_players = []
selected_names = set()

for role in roles:
    for _, row in final_df[final_df["Role"] == role].iterrows():
        if row["Name"] not in selected_names:
            selected_players.append(row)
            selected_names.add(row["Name"])
            break

df = pd.DataFrame(selected_players)

# Step 2: Top 3 players from each of the first 2 teams based on "Batting Points"
final_df = final_df.sort_values(by="Batting Points", ascending=False)
teams = final_df["Team"].unique()[:2]

for team in teams:
    count = 0
    for _, row in final_df[final_df["Team"] == team].iterrows():
        if row["Name"] not in selected_names:
            df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
            selected_names.add(row["Name"])
        count += 1
        if count == 3:
            break
        
        
# Step 3: Top 2 players from each of the same 2 teams based on "Bowling Points"
final_df = final_df.sort_values(by="Bowling Points", ascending=False)

for team in teams:
    count = 0
    for _, row in final_df[final_df["Team"] == team].iterrows():
        if row["Name"] not in selected_names:
            df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
            selected_names.add(row["Name"])
        count += 1
        if count == 2:
            break


# Step 4: Add 1 final best player by "Total Points" not already selected
final_df = final_df.sort_values(by="Total Points", ascending=False)
df = df.sort_values(by="Total Points", ascending=False).reset_index(drop=True)

while len(df)<11:
    for _, row in final_df.iterrows():
        if row["Name"] not in selected_names:
            df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
            selected_names.add(row["Name"])
            break
        

df = df.sort_values(by="Total Points", ascending=False).reset_index(drop=True)

while len(df) > 11:
    for i in reversed(range(len(df))):
        role = df.loc[i, "Role"]
        role_count = (df["Role"] == role).sum()

        if role_count > 1:
            df = df.drop(index=i).reset_index(drop=True)
            break  


df["C/VC"] = "NA"

i = 0
for idx, row in df.iterrows():
    if row["Predicted Role"] in ["Batter", "WK-Batter", "All-Rounder"] and df.at[idx, "C/VC"] == "NA":
        if i==0:
            i +=1
        else:
            df.at[idx, "C/VC"] = "C"
            break
        
i = 0
for idx, row in df.iterrows():
    if row["Predicted Role"] in ["Batter", "WK-Batter", "All-Rounder"] and df.at[idx, "C/VC"] == "NA":
        if i==0:
            i +=1
        else:
            df.at[idx, "C/VC"] = "VC"
            break
    
df = df.sort_values(by="Total Points", ascending=False).reset_index(drop=True)

final_df = final_df.sort_values(by="Total Points", ascending=False)
df = df.sort_values(by="Total Points", ascending=False).reset_index(drop=True)

while len(df)<15:
    for _, row in final_df.iterrows():
        if row["Name"] not in selected_names:
            df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
            selected_names.add(row["Name"])
            break
        
df["C/VC"] = df["C/VC"].fillna("NA")
        
print("✅ Final Selected Squad:")
df = df[["Name","Team","C/VC"]]
df.to_csv("binary_bandits_output.csv", index=False)
print(df)
# print(final_df)
