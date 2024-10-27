import requests

def send_article_and_get_dialogue(file_path):
    """
    Sends an article from a text file to the server and retrieves the generated dialogue.
    
    Parameters:
        server_url (str): The public URL of the server (from ngrok).
        file_path (str): The path to the text file containing the article.
    
    Returns:
        dict: Response from the server, either with dialogue or error message.
    """
    # Define endpoint URLs
    submit_article_url = f"https://2f3d-35-198-228-94.ngrok-free.app/submit_article"
    get_dialogue_url = f"https://2f3d-35-198-228-94.ngrok-free.app/get_dialogue"
    
    # Read article text from the provided file path
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            article_text = file.read()
    except FileNotFoundError:
        return {'error': f"File not found: {file_path}"}
    except Exception as e:
        return {'error': f"Error reading file: {e}"}

    # Step 1: Send the article text to the server
    try:
        submit_response = requests.post(submit_article_url, json={'article': article_text})
        submit_response.raise_for_status()  # Raises an error for 4xx or 5xx status codes
    except requests.exceptions.RequestException as e:
        return {'error': f"Failed to submit article: {e}"}
    
    # Check if the article was successfully received
    if submit_response.json().get('message') != 'Article received successfully.':
        return {'error': 'Failed to submit article to the server.'}
    
    # Step 2: Request the generated dialogue from the server
    try:
        get_dialogue_response = requests.get(get_dialogue_url)
        get_dialogue_response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return {'error': f"Failed to retrieve dialogue: {e}"}
    
    # Return the dialogue or any error message from the response
    return get_dialogue_response.json()['dialogue']

# Example usage:
# Replace 'YOUR_NGROK_PUBLIC_URL' with the actual public URL from ngrok output
# file_path = "path/to/your/article.txt"
# response = send_article_and_get_dialogue('YOUR_NGROK_PUBLIC_URL', file_path)
# print(response)