from pathlib import Path
from openai import OpenAI
import pygame
import pyaudio
import wave


client = OpenAI()


# Initialize the chat messages history
messages = [{"role": "assistant", "content": "How can I help?"}]

# Function to display the chat history
def display_chat_history(messages):
    for message in messages:
        print(f"{message['role'].capitalize()}: {message['content']}")
#########################################################




def grabar(segundos):

	form_1 = pyaudio.paInt16 # 16-bit resolution
	chans = 1 # 1 channel
	samp_rate = 44100 # 44.1kHz sampling rate
	chunk = 4096 # 2^12 samples for buffer
	record_secs = segundos # seconds to record
	dev_index = 2 # device index found by p.get_device_info_by_index(ii)
	wav_output_filename = 'user.wav' # name of .wav file

	audio = pyaudio.PyAudio() # create pyaudio instantiation

# create pyaudio stream
	stream = audio.open(format = form_1,rate = samp_rate,channels = chans,  input = True, \
                    frames_per_buffer=chunk)
	print("recording")
	frames = []

# loop through stream and append audio chunks to frame array
	for ii in range(0,int((samp_rate/chunk)*record_secs)):
    		data = stream.read(chunk)
    		frames.append(data)

	print("finished recording")

# stop the stream, close it, and terminate the pyaudio instantiation
	stream.stop_stream()
	stream.close()
	audio.terminate()

# save the audio frames as .wav file
	wavefile = wave.open(wav_output_filename,'wb')
	wavefile.setnchannels(chans)
	wavefile.setsampwidth(audio.get_sample_size(form_1))
	wavefile.setframerate(samp_rate)
	wavefile.writeframes(b''.join(frames))
	wavefile.close()














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
# Function to create speech to text 

def pasar_a_texto(pregunta):

	audio_file = open( Path(__file__).parent / pregunta, "rb")
	transcript = client.audio.transcriptions.create(
  	model="whisper-1", 
  	file=audio_file, 
  	response_format="text"
	)
	return transcript


# Function to play speech

def reproducir_audio(ruta_archivo):
    pygame.init()
    pygame.mixer.init()

    try:
        # Inicializa el mixer de audio de Pygame
        pygame.mixer.init()

        # Carga el archivo de audio
        pygame.mixer.music.load(ruta_archivo)

        # Reproduce el archivo de audio
        pygame.mixer.music.play()

        # Espera hasta que se complete la reproducción
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    except pygame.error as e:
        print(f"No se pudo reproducir el archivo: {e}")

    finally:
        pygame.mixer.quit()




# Function to get the assistant's response
def get_assistant_response(messages):
    r = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": m["role"], "content": m["content"]} for m in messages],
    )
    response = r.choices[0].message.content
    respuesta_voz(response)	
    reproducir_audio( Path(__file__).parent / "speech.mp3")
    return response




# Main chat loop
while True:
    # Display chat history
    display_chat_history(messages)

    # Get user input
 #   prompt = input("User: ")
    grabar(10)
    pregunta = Path(__file__).parent / "user.wav"
    pregunta = pasar_a_texto(pregunta)
    messages.append({"role": "user", "content": pregunta})

    # Get assistant response
    response = get_assistant_response(messages)
    messages.append({"role": "assistant", "content": response})
