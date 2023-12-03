from pathlib import Path
from openai import OpenAI
client = OpenAI()


# Initialize the chat messages history
messages = [{"role": "assistant", "content": "How can I help?"}]

# Function to display the chat history
def display_chat_history(messages):
    for message in messages:
        print(f"{message['role'].capitalize()}: {message['content']}")

# Function to create text to speech
def respuesta_voz(mensaje):
        speech_file_path = Path(__file__).parent / "speech.mp3"
        response = client.audio.speech.create(
                model="tts-1",
                voice="alloy",
                input=mensaje
        )

        response.stream_to_file(speech_file_path)
        return  response


# Function to get the assistant's response
def get_assistant_response(messages):
    r = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": m["role"], "content": m["content"]} for m in messages],
    )
    response = r.choices[0].message.content
    respuesta_voz(response)	
    return response




# Main chat loop
while True:
    # Display chat history
    display_chat_history(messages)

    # Get user input
    prompt = input("User: ")
    messages.append({"role": "user", "content": prompt})

    # Get assistant response
    response = get_assistant_response(messages)
    messages.append({"role": "assistant", "content": response})
