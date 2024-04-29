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
    start_silence = np.zeros(int(sampling_rate * 3), dtype=np.int16)
    end_silence = np.zeros(int(sampling_rate * 4), dtype=np.int16)

    for chapter in chapters:
      if "file" in chapter: continue

      chapter_id = chapter.doc_id
      narration_data = [start_silence]
      fragments = db.get_fragments(book_id, chapter_id)

      for fragment in fragments:
        data, sr = sf.read(fragment["file"], dtype='int16')
        narration_data.append(data)
        narration_data.append(normal_silence)

      narration_data.append(end_silence)

      narration_data = np.concatenate(narration_data)
      file_path = os.path.join(os.path.dirname(__file__), f'{book_id}_{chapter_id}.wav')
      sf.write(file_path, narration_data, sampling_rate, format='WAV')
      db.update_chapter(chapter_id, file=file_path)

  dispatcher.connect(process, signal='attach', weak=False)
