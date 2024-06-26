# Simple Lidarr, Radarr, Readarr, Sonarr and Whisparr script created by Matt (MattDGTL) Pomales to clean out stalled downloads.
# Couldn't find a python script to do this job so I figured why not give it a try.

import os
import asyncio
import logging
import requests
from requests.exceptions import RequestException
import json

# Set up logging
logging.basicConfig(
    format='%(asctime)s [%(levelname)s]: %(message)s', 
    level=logging.INFO, 
    handlers=[logging.StreamHandler()]
)

# Lidarr, Radarr, Readarr, Sonarr and Whisparr Script Enabler

LIDARR_RUN_SCRIPT = (os.environ['LIDARR_RUN_SCRIPT'])
RADARR_RUN_SCRIPT = (os.environ['RADARR_RUN_SCRIPT'])
READARR_RUN_SCRIPT = (os.environ['READARR_RUN_SCRIPT'])
SONARR_RUN_SCRIPT = (os.environ['SONARR_RUN_SCRIPT'])
WHISPARR_RUN_SCRIPT = (os.environ['WHISPARR_RUN_SCRIPT'])

# Lidarr, Radarr, Readarr, Sonarr and Whisparr API endpoints
LIDARR_API_URL = (os.environ['LIDARR_URL']) + "/api/v3"
RADARR_API_URL = (os.environ['RADARR_URL']) + "/api/v3"
READARR_API_URL = (os.environ['READARR_URL']) + "/api/v3"
SONARR_API_URL = (os.environ['SONARR_URL']) + "/api/v3"
WHISPARR_API_URL = (os.environ['WHISPARR_URL']) + "/api/v3"

# Lidarr, Radarr, Readarr, Sonarr and Whisparr API keys
LIDARR_API_KEY = (os.environ['LIDARR_API_KEY'])
RADARR_API_KEY = (os.environ['RADARR_API_KEY'])
READARR_API_KEY = (os.environ['READARR_API_KEY'])
SONARR_API_KEY = (os.environ['SONARR_API_KEY'])
WHISPARR_API_KEY = (os.environ['WHISPARR_API_KEY'])

# Timeout for API requests in seconds
API_TIMEOUT = int(os.environ['API_TIMEOUT']) # 10 minutes

# Function to make API requests with error handling
async def make_api_request(url, api_key, params=None):
    try:
        headers = {'X-Api-Key': api_key}
        response = await asyncio.get_event_loop().run_in_executor(None, lambda: requests.get(url, params=params, headers=headers))
        response.raise_for_status()
        return response.json()
    except RequestException as e:
        logging.error(f'Error making API request to {url}: {e}')
        return None
    except ValueError as e:
        logging.error(f'Error parsing JSON response from {url}: {e}')
        return None

# Function to make API delete with error handling
async def make_api_delete(url, api_key, params=None):
    try:
        headers = {'X-Api-Key': api_key}
        response = await asyncio.get_event_loop().run_in_executor(None, lambda: requests.delete(url, params=params, headers=headers))
        response.raise_for_status()
        return response.json()
    except RequestException as e:
        logging.error(f'Error making API request to {url}: {e}')
        return None
    except ValueError as e:
        logging.error(f'Error parsing JSON response from {url}: {e}')
        return None

# Function to remove stalled Lidarr downloads
async def remove_stalled_lidarr_downloads():
    logging.info('Checking lidarr queue...')
    lidarr_url = f'{LIDARR_API_URL}/queue'
    lidarr_queue = await make_api_request(lidarr_url, LIDARR_API_KEY, {'page': '1', 'pageSize': await count_records(LIDARR_API_URL,LIDARR_API_KEY)})
    if lidarr_queue is not None and 'records' in lidarr_queue:
        logging.info('Processing Lidarr queue...')
        for item in lidarr_queue['records']:
            if 'title' in item and 'status' in item and 'trackedDownloadStatus' in item:
                logging.info(f'Checking the status of {item["title"]}')
                if item['status'] == 'warning' and item['errorMessage'] == 'The download is stalled with no connections':
                    logging.info(f'Removing stalled Lidarr download: {item["title"]}')
                    await make_api_delete(f'{LIDARR_API_URL}/queue/{item["id"]}', LIDARR_API_KEY, {'removeFromClient': 'true', 'blocklist': 'true'})
            else:
                logging.warning('Skipping item in Lidarr queue due to missing or invalid keys')
    else:
        logging.warning('Lidarr queue is None or missing "records" key')

# Function to remove stalled Radarr downloads
async def remove_stalled_radarr_downloads():
    logging.info('Checking radarr queue...')
    radarr_url = f'{RADARR_API_URL}/queue'
    radarr_queue = await make_api_request(radarr_url, RADARR_API_KEY, {'page': '1', 'pageSize': await count_records(RADARR_API_URL,RADARR_API_KEY)})
    if radarr_queue is not None and 'records' in radarr_queue:
        logging.info('Processing Radarr queue...')
        for item in radarr_queue['records']:
            if 'title' in item and 'status' in item and 'trackedDownloadStatus' in item:
                logging.info(f'Checking the status of {item["title"]}')
                if item['status'] == 'warning' and item['errorMessage'] == 'The download is stalled with no connections':
                    logging.info(f'Removing stalled Radarr download: {item["title"]}')
                    await make_api_delete(f'{RADARR_API_URL}/queue/{item["id"]}', RADARR_API_KEY, {'removeFromClient': 'true', 'blocklist': 'true'})
            else:
                logging.warning('Skipping item in Radarr queue due to missing or invalid keys')
    else:
        logging.warning('Radarr queue is None or missing "records" key')

# Function to remove stalled Readarr downloads
async def remove_stalled_readarr_downloads():
    logging.info('Checking readarr queue...')
    readarr_url = f'{READARR_API_URL}/queue'
    readarr_queue = await make_api_request(readarr_url, READARR_API_KEY, {'page': '1', 'pageSize': await count_records(READARR_API_URL,READARR_API_KEY)})
    if readarr_queue is not None and 'records' in readarr_queue:
        logging.info('Processing Readarr queue...')
        for item in readarr_queue['records']:
            if 'title' in item and 'status' in item and 'trackedDownloadStatus' in item:
                logging.info(f'Checking the status of {item["title"]}')
                if item['status'] == 'warning' and item['errorMessage'] == 'The download is stalled with no connections':
                    logging.info(f'Removing stalled Readarr download: {item["title"]}')
                    await make_api_delete(f'{READARR_API_URL}/queue/{item["id"]}', READARR_API_KEY, {'removeFromClient': 'true', 'blocklist': 'true'})
            else:
                logging.warning('Skipping item in Readarr queue due to missing or invalid keys')
    else:
        logging.warning('Readarr queue is None or missing "records" key')

# Function to remove stalled Sonarr downloads
async def remove_stalled_sonarr_downloads():
    logging.info('Checking Sonarr queue...')
    sonarr_url = f'{SONARR_API_URL}/queue'
    sonarr_queue = await make_api_request(sonarr_url, SONARR_API_KEY, {'page': '1', 'pageSize': await count_records(SONARR_API_URL,SONARR_API_KEY)})
    if sonarr_queue is not None and 'records' in sonarr_queue:
        logging.info('Processing Sonarr queue...')
        for item in sonarr_queue['records']:
            if 'title' in item and 'status' in item and 'trackedDownloadStatus' in item:
                logging.info(f'Checking the status of {item["title"]}')
                if item['status'] == 'warning' and item['errorMessage'] == 'The download is stalled with no connections':
                    logging.info(f'Removing stalled Sonarr download: {item["title"]}')
                    await make_api_delete(f'{SONARR_API_URL}/queue/{item["id"]}', SONARR_API_KEY, {'removeFromClient': 'true', 'blocklist': 'true'})
            else:
                logging.warning('Skipping item in Sonarr queue due to missing or invalid keys')
    else:
        logging.warning('Sonarr queue is None or missing "records" key')

# Function to remove stalled Whisparr downloads
async def remove_stalled_whisparr_downloads():
    logging.info('Checking whisparr queue...')
    whisparr_url = f'{WHISPARR_API_URL}/queue'
    whisparr_queue = await make_api_request(whisparr_url, WHISPARR_API_KEY, {'page': '1', 'pageSize': await count_records(WHISPARR_API_URL,WHISPARR_API_KEY)})
    if whisparr_queue is not None and 'records' in whisparr_queue:
        logging.info('Processing Whisparr queue...')
        for item in whisparr_queue['records']:
            if 'title' in item and 'status' in item and 'trackedDownloadStatus' in item:
                logging.info(f'Checking the status of {item["title"]}')
                if item['status'] == 'warning' and item['errorMessage'] == 'The download is stalled with no connections':
                    logging.info(f'Removing stalled Whisparr download: {item["title"]}')
                    await make_api_delete(f'{WHISPARR_API_URL}/queue/{item["id"]}', WHISPARR_API_KEY, {'removeFromClient': 'true', 'blocklist': 'true'})
            else:
                logging.warning('Skipping item in Whisparr queue due to missing or invalid keys')
    else:
        logging.warning('Whisparr queue is None or missing "records" key')

# Make a request to view and count items in queue and return the number.
async def count_records(API_URL, API_Key):
    the_url = f'{API_URL}/queue'
    the_queue = await make_api_request(the_url, API_Key)
    if the_queue is not None and 'records' in the_queue:
        return the_queue['totalRecords']

# Main function
async def main():
    while True:
        logging.info('Running media-tools script')
        #
        if LIDARR_RUN_SCRIPT.casefold() == 'True':
            await remove_stalled_lidarr_downloads()
        else:
            logging.info('Lidarr queue script not active')
        if RADARR_RUN_SCRIPT.casefold() == 'True':
            await remove_stalled_radarr_downloads()
        #else:
            logging.info('Radarr queue script not active')
        if READARR_RUN_SCRIPT.casefold() == 'True':
            await remove_stalled_readarr_downloads()
        else:
            logging.info('Readarr queue script not active')
        if SONARR_RUN_SCRIPT.casefold() == 'True':
            await remove_stalled_sonarr_downloads()
        else:
            logging.info('Sonarr queue script not active')
        if WHISPARR_RUN_SCRIPT.casefold() == 'True':
            await remove_stalled_whisparr_downloads()
        else:
            logging.info('Whisparr queue script not active')
        logging.info(f'Finished running media-tools script. Sleeping for {API_TIMEOUT} seconds.')
        await asyncio.sleep(API_TIMEOUT)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
