import requests


def create_dialog_llama(server_url, article_text):
    """
    Sends an article text to the server and retrieves the generated dialogue.

    Parameters:
        server_url (str): The public URL of the server (from ngrok).
        article_text (str): The text of the article to submit.

    Returns:
        dict: Response from the server, either with dialogue or error message.
    """
    # Define endpoint URLs
    submit_article_url = f"{server_url}/submit_article"
    get_dialogue_url = f"{server_url}/get_dialogue"

    # Step 1: Send the article text to the server
    try:
        submit_response = requests.post(submit_article_url, json={'article': article_text})
        submit_response.raise_for_status()  # Raises an error for 4xx or 5xx status codes
    except requests.exceptions.RequestException as e:
        return {'error': f"Failed to submit article: {e}"}

    # Check if the article was successfully received
    if submit_response.json().get('message') != 'Article received successfully.':
        return {'error': 'Failed to submit article to the server.'}

    try:
        get_dialogue_response = requests.get(get_dialogue_url)
        get_dialogue_response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return {'error': f"Failed to retrieve dialogue: {e}"}

    return get_dialogue_response.json()
