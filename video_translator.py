import os
import torch
import whisper
import numpy as np
from moviepy.editor import VideoFileClip, AudioFileClip
from transformers import MarianMTModel, MarianTokenizer
from TTS.api import TTS
import cv2

class VideoTranslator:
    def __init__(self):
        # Initialize models
        self.whisper_model = whisper.load_model("base")
        self.translator_model = MarianMTModel.from_pretrained("Helsinki-NLP/opus-mt-zh-en")
        self.translator_tokenizer = MarianTokenizer.from_pretrained("Helsinki-NLP/opus-mt-zh-en")
        self.tts = TTS(model_name="tts_models/en/vctk/vits", progress_bar=True)
        
    def extract_audio(self, video_path):
        """Extract audio from video file."""
        video = VideoFileClip(video_path)
        audio = video.audio
        audio.write_audiofile("temp_audio.wav")
        return "temp_audio.wav"
    
    def transcribe_audio(self, audio_path):
        """Transcribe Chinese audio to text."""
        result = self.whisper_model.transcribe(audio_path)
        return result["text"]
    
    def translate_text(self, chinese_text):
        """Translate Chinese text to English."""
        inputs = self.translator_tokenizer(chinese_text, return_tensors="pt", padding=True)
        translated = self.translator_model.generate(**inputs)
        english_text = self.translator_tokenizer.decode(translated[0], skip_special_tokens=True)
        return english_text
    
    def generate_speech(self, english_text, output_path):
        """Generate English speech from text."""
        self.tts.tts_to_file(text=english_text, file_path=output_path, speaker="p335")
    
    def process_video(self, input_video_path, output_video_path):
        """Process the video: translate audio and generate new video."""
        # Extract audio
        audio_path = self.extract_audio(input_video_path)
        
        # Transcribe Chinese audio
        chinese_text = self.transcribe_audio(audio_path)
        print(f"Transcribed Chinese text: {chinese_text}")
        
        # Translate to English
        english_text = self.translate_text(chinese_text)
        print(f"Translated English text: {english_text}")
        
        # Generate English speech
        english_audio_path = "english_audio.wav"
        self.generate_speech(english_text, english_audio_path)
        
        # Combine video with new audio
        video = VideoFileClip(input_video_path)
        audio = AudioFileClip(english_audio_path)
        final_video = video.set_audio(audio)
        final_video.write_videofile(output_video_path)
        
        # Cleanup temporary files
        os.remove(audio_path)
        os.remove(english_audio_path)

if __name__ == "__main__":
    translator = VideoTranslator()
    input_video = "input.mp4"  # Replace with your input video path
    output_video = "output.mp4"  # Replace with your desired output path
    translator.process_video(input_video, output_video) 