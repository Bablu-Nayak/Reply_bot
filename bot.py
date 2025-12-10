import pyautogui
import pyperclip
import time
from groq import Groq

# Name of the person your bot should reply to
sender = "Mom"

# Your Groq API key (keep this secret!)
GROQ_API_KEY = "<api_key>"   
client = Groq(api_key=GROQ_API_KEY)

def is_last_message_from_sender(chat_log, sender_name=sender):
    # Take the full chat text and focus on the last part
    messages = chat_log.strip().split("/2025] ")[-1]
    # Check if sender's name appears in that last part
    if sender_name in messages:
        return True 
    return False

# Click on Chrome / WhatsApp Web to bring it to front
pyautogui.click(1341, 1053)
time.sleep(1)

# Run forever, check every few seconds
while True:
    time.sleep(5)

    # Select the chat area by dragging the mouse
    pyautogui.moveTo(669, 264)
    pyautogui.dragTo(1186, 1031, duration=2.0, button='left')

    # Copy the selected chat text
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(2)
    pyautogui.click(1871, 969)

    # Get copied text from clipboard
    chat_history = pyperclip.paste()
    print(chat_history)  # For debugging

    # Only reply if last message seems to be from the chosen sender
    if is_last_message_from_sender(chat_history):
        print("DEBUG: last from sender, replying...")

        # Ask Groq AI to generate a reply
        completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a person named Bablu who speaks only english. You are from India and you are a coder. You analyze chat history. Output should be the next chat response (text message only)"
                },
                {
                    "role": "system",
                    "content": f"Do not start like this [21:02, 12/10/2025]{sender}"
                },
                {
                    "role": "user",
                    "content": chat_history,
                }
            ],
            model="llama-3.3-70b-versatile",
        )

        # Get the text reply from the AI
        response = completion.choices[0].message.content
        # Copy AI reply to clipboard
        pyperclip.copy(response)

        # Click on message input box
        pyautogui.click(870, 1032)
        time.sleep(1)

        # Paste and send reply
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(1)
        pyautogui.press('enter')

    else:
        # Do nothing if last message is not from Mom
        print("DEBUG: last not from sender, skipping")
