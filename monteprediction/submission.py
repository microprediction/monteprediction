import numpy as np
import requests
import time
from io import StringIO
from monteprediction import MONTE_URL
import json

def send_in_chunks(df, email, num_chunks, name=None, max_retries=3):
    if name is None:
        name = email[:20]
        print(f'Suggest you supply name argument for the leaderboard. Using {name} for now')
    chunks = np.array_split(df, num_chunks)
    for chunk_no, chunk_df in enumerate(chunks):
        for attempt in range(max_retries):
            try:
                # Metadata and URL setup
                metadata = {'email': email, 'name':name, 'chunk': chunk_no, 'num_chunks': num_chunks}

                # Convert DataFrame chunk to CSV string
                csv_string = chunk_df.to_csv(index=False)

                # Stream the CSV string to the server
                with StringIO(csv_string) as f:
                    response = requests.post(MONTE_URL, params=metadata, data=f)

                # Check response
                if response.ok:
                    print(f"Chunk {chunk_no} of {num_chunks} sent successfully.")
                    break  # Break the retry loop if successful
                else:
                    print(f"Failed to send chunk {chunk_no}, attempt {attempt + 1}. Response: {response.content}")

            except Exception as e:
                print(f"An error occurred: {e}")

            # Optional: wait before retrying
            time.sleep(1)  # Wait for 1 second before retrying

        else:
            print(f"Failed to send chunk {chunk_no} after {max_retries} attempts.")
    try: 
        return json.loads(response.content)
    except:
        return {'message':'Failed but try again a little later'}
