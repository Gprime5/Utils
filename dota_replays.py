import requests
import bz2
import logging

__all__ = ["get_replay"]

def _get_cluster(match_id):
    """
    
    Private function to retrieve server cluster the match is stored in.
    
    """
    
    url = "https://api.opendota.com/api/replays"
    parameters = {"match_id": match_id}
    retries = 3
    
    while retries:
        response = requests.get(url, parameters)
        if response.headers.get("Content-Encoding"):
            response = response.json()[0]
            
            return response["cluster"], response["replay_salt"]
            
        logging.info(f"Replay not found, trying again.")
        retries -= 1
    
    return None, None

def get_replay(match_id, download=True):
    """ 
    
    Returns True if replay is available.
    
    If download is True, will download and decompress replay file.
    
    File can be called in command line
    
        >python dota_replays.py match_id [-nd] [--nodownload]
    
    """
    
    logging.info("Retrieving data")
    
    cluster, salt = _get_cluster(match_id)
    if cluster is None:
        return False
        
    url = f"http://replay{cluster}.valve.net/570/{match_id}_{salt}.dem.bz2"

    response = requests.get(url, stream=True)

    if response.status_code == 200:
        logging.info(f"Replay found {match_id}")
        
        if download:
            logging.info(f"Downloading {match_id}")
            
            data = bytearray()
            
            for chunk in response.iter_content(1024*1024):
                data += chunk
                
                _total = response.headers['Content-Length']
                _percent = f"{100*len(data)/int(_total):>6.2f}"
                _progress = f"{len(data):>{len(_total)}}"
                
                logging.info(f"{_percent}% {_progress}/{_total}")
            
            logging.info("Saving file")
            
            with open(f"{match_id}.dem", "wb") as file:
                file.write(bz2.decompress(data))
                
            logging.info(f"Complete")
        return True
    return False
    
if __name__ == "__main__":
    import argparse
    
    logging.basicConfig(
        style="{",
        level=logging.INFO,
        format="[{levelname}] {asctime} {message}",
        datefmt='%H:%M:%S'
    )

    parser = argparse.ArgumentParser()
    parser.add_argument("match_id", type=int)
    parser.add_argument("-nd", "--nodownload", action="store_true")
    args = parser.parse_args()
    
    if not get_replay(args.match_id, not args.nodownload):
        logging.info("Replay unavailable")