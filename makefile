

all:

install:
	sudo apt-get install python3 python3-all-dev python3-pip build-essential swig git libpulse-dev portaudio19-dev
	python -m pip install --upgrade pip setuptools wheel
	pip3 install --upgrade SpeechRecognition pyaudio pocketsphinx google-api-python-client

clean:
	@find . -type f \( -name '*~' \) -delete
