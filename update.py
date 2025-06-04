import aiohttp
import asyncio
from bs4 import BeautifulSoup
import json
import pandas as pd
import os
from tqdm.asyncio import tqdm as async_tqdm

# Keep your existing players_team_dict here

async def scrape_howstat_player_data_async(session, playerID, role_query, playerName):
    """Asynchronous version of the player data scraping function"""
    if role_query.lower() == 'bat':
        url = f'https://www.howstat.com/Cricket/Statistics/IPL/PlayerProgressBat.asp?PlayerID={playerID}'
    elif role_query.lower() == 'bowl':
        url = f'https://www.howstat.com/Cricket/Statistics/IPL/PlayerProgressBowl.asp?PlayerID={playerID}'
    elif role_query.lower() == 'summary':
        url = f'https://www.howstat.com/Cricket/Statistics/IPL/PlayerProgressSummary.asp?PlayerID={playerID}'
    
    try:
        # Send a GET request to fetch the HTML content asynchronously
        async with session.get(url) as response:
            content = await response.text()
            
            # Parse the HTML with BeautifulSoup
            soup = BeautifulSoup(content, 'html.parser')
            
            # Find the table with the class name "TableLined"
            table = soup.find('table', class_='TableLined')
            
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
                    df = df[:-1]  # Remove the last row for batting stats
                    
                # Save to csv
                base_dir = os.path.join("binary_bandits", "Dataset", "player_data", role_query)
                os.makedirs(base_dir, exist_ok=True)
                file_path = os.path.join(base_dir, f"{playerName}.csv")
                df.to_csv(file_path, index=False)
                return f"Data saved for {playerName} - {role_query}"
            else:
                return None
    except Exception as e:
        return f"Error for {playerName} - {role_query}: {str(e)}"

async def process_player(session, player, player_id):
    """Process a single player for all three role queries"""
    tasks = []
    for role in ["bat", "bowl", "summary"]:
        tasks.append(scrape_howstat_player_data_async(session, player_id, role, player))
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return results

async def main():
    # Get player names from the two teams
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


    player_names = players_team_dict["RCB"] + players_team_dict["PBKS"]

    
    # Load player IDs from file
    with open(os.path.join("binary_bandits", "Dataset", "extras", "howstat_id.json"), "r") as f:
        player_IDs = json.load(f)
    
    # Filter IDs for players in our list
    player_IDs = {player: id for player, id in player_IDs.items() if player in player_names}
    
    print(f"Processing {len(player_IDs)} players")
    
    # Create async HTTP session
    async with aiohttp.ClientSession() as session:
        tasks = []
        for player, player_id in player_IDs.items():
            if player_id:
                tasks.append(process_player(session, player, player_id))
        
        # Show progress bar while awaiting results
        results = await async_tqdm.gather(*tasks, desc="Scraping player data")

if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
