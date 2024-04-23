import os
import numpy as np
import soundfile as sf

sampling_rate = 24000

def start(dependencies):
  db = dependencies["db"]
  dispatcher = dependencies["dispatcher"]

  def process(sender, data):
    book_id=data
    chapters=db.get_chapters(book_id)

    normal_silence = np.zeros(int(sampling_rate * 1), dtype=np.int16)
    start_silence = np.zeros(int(sampling_rate * 4), dtype=np.int16)
    chapter_silence = np.zeros(int(sampling_rate * 4), dtype=np.int16)

    print(chapter_silence)

    narration_data = [start_silence]

    for chapter in chapters:
      fragments = db.get_fragments(book_id, chapter.doc_id)

      for fragment in fragments:
        data, sr = sf.read(fragment["file"], dtype='int16')
        narration_data.append(data)
        narration_data.append(normal_silence)

      narration_data.append(chapter_silence)

    narration_data = np.concatenate(narration_data)
    file_path = os.path.join(os.path.dirname(__file__), f'{book_id}.wav')

    sf.write(file_path, narration_data, sampling_rate, format='WAV')

  dispatcher.connect(process, signal='attach', weak=False)
