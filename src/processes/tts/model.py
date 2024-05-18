import os
import torch
from TTS.api import TTS

cwd = os.path.dirname(__file__)

device = "cuda" if torch.cuda.is_available() else "cpu"

def concatenate_to_segments(strings, limit=5):
  result = []
  current_segment = ""

  for s in strings:
    if len(current_segment) + len(s) > limit:
      if current_segment != '': result.append(current_segment)
      current_segment = s
    else:
      current_segment += f' {s}'

  # Append the last segment if it's not empty
  if current_segment:
    result.append(current_segment)

  return result

class TTSModel:
  def __init__(self):
    self.tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
    self.synthesizer = self.tts.synthesizer
    self.config = self.synthesizer.tts_config
    self.sample_rate = self.synthesizer.tts_config.audio["sample_rate"]
    self.max_sentence_length = 240
    self.speakers = {}

  def register_speaker(self, name, path):
    voice_path = os.path.join(cwd, path)
    files = os.listdir(voice_path)
    audio_path = [os.path.join(voice_path, f) for f in files]

    (gpt_cond_latent, speaker_embedding) = self.synthesizer.tts_model.get_conditioning_latents(
      audio_path=audio_path,
      gpt_cond_len=30,
      gpt_cond_chunk_len=4,
      max_ref_length=30,
      sound_norm_refs=False,
    )

    self.speakers[name] = { "gpt_cond_latent": gpt_cond_latent, "speaker_embedding": speaker_embedding}

  def split_into_sentences(self, text):
    sentences = self.synthesizer.split_into_sentences(text)
    return concatenate_to_segments(sentences, limit=self.max_sentence_length)

  def save_wav(self, wav, path):
    self.synthesizer.save_wav(wav=wav, path=path, pipe_out=None)

  def synthesize(self, text, language, speaker):
    if speaker not in self.speakers:
      raise Exception(f"Speaker {speaker} not registered.")

    speaker_data = self.speakers[speaker]
    gpt_cond_latent = speaker_data["gpt_cond_latent"]
    speaker_embedding = speaker_data["speaker_embedding"]

    outputs = self.synthesizer.tts_model.inference(
      text,
      language,
      gpt_cond_latent,
      speaker_embedding,
      temperature=self.config.temperature,
      length_penalty=self.config.length_penalty,
      repetition_penalty=self.config.repetition_penalty,
      top_k=self.config.top_k,
      top_p=self.config.top_p,
      do_sample=True,
    )

    waveform = outputs["wav"].squeeze()

    return list(waveform)

model = TTSModel()
