# This code scrape the Visual Arts Biennale website including bio and opera of each artsits
#%%
import requests
from bs4 import BeautifulSoup
import json
import re
import pandas as pd
import multiprocessing as mp
import os
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
import warnings
# Suppress BeautifulSoup Deprecation Warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
#%%
# Function to scrape one URL and process data
def scrape_artists_data(url):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }
    try:
        # Get the webpage content
        response = requests.get(url,headers=headers,timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        # Find the script tag or the part containing JSON-like data.
        script_tag = soup.find('script', text=re.compile(r'{"took":'))  # Searching for JSON starting with "{"took":"
        if script_tag:
            json_text = script_tag.string
            # Cleaning up the script content (if there is extra JS code around it).
            match = re.search(r'({.*})', json_text, re.DOTALL)  # Extracting the JSON part between curly braces
            if match:
                json_data = json.loads(match.group(1))
                # Person ID and Name
                person_id = json_data['props']['pageProps']['people']['hits']['hits'][0]['_source']['id']
                person_name = json_data['props']['pageProps']['people']['hits']['hits'][0]['_source']['nome_cognome']
                person_info = json_data['props']['pageProps']['people']['hits']['hits'][0]['_source']
                # ------------------- Extract Institutional Roles ------------------- #
                institution_roles = []
                if 'ruolo_istituzionale_sezione' in person_info:
                    for event in person_info['ruolo_istituzionale_sezione']:
                        role = event.get('ruolo', 'N/A')
                        event_year = event.get('anno_manifestazione', 'N/A')  # Extract year from date
                        event_title = event.get('titolo_sezione', 'N/A')
                        event_id = event.get('id_sezione', 'N/A')
                        tipo= event.get('tipo', 'N/A')
                        institution_roles.append({
                            'person_id': person_id,
                            'person_name': person_name,  # Adding person's name
                            'role': role,
                            'event_year': event_year,
                            'event_title': event_title,
                            'event_id': event_id,
                            'event_type': 'section',
                            'tipo': tipo
                        })
                if 'ruolo_istituzionale_evento' in person_info:
                    for event in person_info['ruolo_istituzionale_evento']:
                        role = event.get('ruolo', 'N/A')
                        event_year = event.get('anno_manifestazione', 'N/A')  # Extract year from date
                        event_title = event.get('titolo_evento', 'N/A')
                        event_id = event.get('id_evento', 'N/A')
                        tipo= event.get('tipo', 'N/A')
                        institution_roles.append({
                            'person_id': person_id,
                            'person_name': person_name,  # Adding person's name
                            'role': role,
                            'event_year': event_year,
                            'event_title': event_title,
                            'event_id': event_id,
                            'event_type': 'event',
                            'tipo': tipo
                        })
                if 'ruolo_istituzionale' in person_info:
                    for event in person_info['ruolo_istituzionale']:
                        role = event.get('ruolo', 'N/A')
                        event_year = event.get('anno_manifestazione', 'N/A')
                        event_title = event.get('titolo_manifestazione', 'N/A')
                        event_id = event.get('id_manifestazione', 'N/A')
                        tipo= event.get('tipo', 'N/A')
                        institution_roles.append({
                            'person_id': person_id,
                            'person_name': person_name,  # Adding person's name
                            'role': role,
                            'event_year': event_year,
                            'event_title': event_title,
                            'event_id': event_id,
                            'event_type': 'manifestazione',
                            'tipo': tipo
                        })
                # Convert institution roles to DataFrame if data exists
                df_institution_roles = pd.DataFrame(institution_roles) if institution_roles else pd.DataFrame()
                # ------------------- Extract Roles Under Opera ------------------- #
                opera_roles = []
                if 'opera' in person_info:
                    for work in person_info['opera']:
                        for role in work.get('ruolo', []):
                            opera_roles.append({
                                'person_id': person_id,
                                'person_name': person_name,  # Adding person's name
                                'role_name': role.get('nome', 'N/A'),
                                'opera_category': work.get('categoria_opera', 'N/A'),
                                'opera_id': work.get('id_opera', 'N/A'),
                                'opera_title': work.get('titolo_opera', 'N/A'),
                                'opera_year': work.get('anno_opera', 'N/A')
                            })
                # Convert opera roles to DataFrame if data exists
                df_opera_roles = pd.DataFrame(opera_roles) if opera_roles else pd.DataFrame()
                # ------------------- Combine Birth and Death Information ------------------- #
                birth_death_combined = []
                if ('data_nascita' in person_info or 'data_morte' in person_info) or ('citta_nascita' in person_info or 'nazione_nascita' in person_info or 'nazione_morte' in person_info):
                    birth_death_combined.append({
                        'person_id': person_id,
                        'person_name': person_name,  # Adding person's name
                        'birth_year': person_info.get('data_nascita', 'N/A')[:4] if person_info.get('data_nascita') else 'N/A',
                        'death_year': person_info.get('data_morte', 'N/A')[:4] if person_info.get('data_morte') else 'N/A',
                        'birth_city': person_info.get('citta_nascita', 'N/A'),
                        'birth_country': person_info.get('nazione_nascita', 'N/A'),
                        'death_country': person_info.get('nazione_morte', 'N/A')
                    })
                # Convert combined birth and death info to DataFrame if data exists
                df_birth_death_combined = pd.DataFrame(birth_death_combined) if birth_death_combined else pd.DataFrame()
                return df_institution_roles, df_opera_roles, df_birth_death_combined
            else:
                #print(f"JSON-like content not found in {url}")
                return None, None, None
        else:
            #print(f"Script tag containing JSON data not found in {url}")
            return None, None, None
    except Exception as e:
        #print(f"Error scraping {url}: {e}")
        return None, None, None
#%% Multiprocessing and tqdm setup
if __name__ == '__main__':
    # Load URLs from CSV
    artists = pd.read_csv('artists.csv')
    info = pd.read_csv('scraped_data_biennale_maininfo.csv').dropna(subset=['href'])
    info = info[info['href'].str.contains('persone')]
    artists_urls = list(set(artists['Artist_url']) | set(info['href']))
    # Dynamically determine the number of workers based on available CPU cores
    num_workers = os.cpu_count() or 4  # Fallback to 4 if os.cpu_count() returns None
    print(f"Using {num_workers} workers for scraping.")
    results = []
    # Use ThreadPoolExecutor for multiprocessing with one unified progress bar
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        # Submit all tasks
        futures = [executor.submit(scrape_artists_data, url) for url in artists_urls]
        # Initialize a single progress bar for all URLs
        with tqdm(total=len(futures), desc="Processing URLs", leave=True) as pbar:
            for future in as_completed(futures):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    results.append({"error": str(e)})
                finally:
                    pbar.update(1)  # Update the single progress bar
    print("Scraping completed.")
    # Combine results into final DataFrames
    institution_roles_dfs = [res[0] for res in results if res[0] is not None]
    opera_roles_dfs = [res[1] for res in results if res[1] is not None]
    birth_death_combined_dfs = [res[2] for res in results if res[2] is not None]
    df_institution_roles_final = pd.concat(institution_roles_dfs, ignore_index=True) if institution_roles_dfs else pd.DataFrame()
    df_opera_roles_final = pd.concat(opera_roles_dfs, ignore_index=True) if opera_roles_dfs else pd.DataFrame()
    df_birth_death_combined_final = pd.concat(birth_death_combined_dfs, ignore_index=True) if birth_death_combined_dfs else pd.DataFrame()
    # Save to CSV files
    df_institution_roles_final.to_csv('scrape_arch_biennale_institutions_roles.csv', index=False)
    df_opera_roles_final.to_csv('scrape_arch_biennale_opera_roles.csv', index=False)
    df_birth_death_combined_final.to_csv('scrape_arch_biennale_artists_bio.csv', index=False)
    print("Scraping and processing completed.")
# %%
