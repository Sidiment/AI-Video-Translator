# Chinese Video Translator

This software translates Chinese videos to English, including voice conversion and lip-sync matching.

## Features

- Chinese speech recognition
- Chinese to English translation
- English text-to-speech synthesis
- Video processing with audio replacement

## Installation

1. Clone this repository
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Place your Chinese video file in the project directory
2. Update the input and output video paths in `video_translator.py`
3. Run the script:
```bash
python video_translator.py
```

## Requirements

- Python 3.8 or higher
- CUDA-capable GPU (recommended for faster processing)
- Sufficient disk space for video processing

## Notes

- The first run will download necessary models, which may take some time
- Processing time depends on video length and your hardware
- The quality of translation and voice synthesis may vary based on the input video quality 