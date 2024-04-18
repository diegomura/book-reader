import time
from pydispatch import dispatcher

# Simulate process converted eput to text
story = """
In a quaint little town nestled between rolling hills and dense forests, lived two friends named Sarah and David. They were inseparable since childhood, sharing laughter, dreams, and the occasional secret. One gloomy evening, the sky painted in shades of gray, they found themselves in Sarah's cozy living room, engrossed in conversation.

As the raindrops tapped against the window pane, the room echoed with the warmth of their friendship. The narrator, a silent observer to their tales, watched as Sarah and David exchanged stories of their week, relishing the comforting ambiance of the crackling fireplace.

"So, David," Sarah said, her eyes sparkling with mischief, "have you heard about the old mansion on the outskirts of town? They say it's haunted."

David chuckled, "Come on, Sarah. Ghost stories? You know I don't believe in that stuff."

As their banter continued, the wind outside grew more insistent, whispering secrets that only the bravest trees dared to share. The narrator could sense a subtle tension building in the room, a prelude to an unexpected twist in their evening.

Just as Sarah began to describe the eerie sounds rumored to emanate from the mansion, a sudden, thunderous boom shook the entire house. The lights flickered, casting eerie shadows on the walls.

Startled, Sarah and David exchanged wide-eyed glances. "Was that thunder?" Sarah asked, her voice barely audible over the howling wind.

David nodded, attempting to ease the tension with a reassuring smile. "Just a storm, nothing to worry about."

But before anyone could say another word, a gust of wind burst through the slightly ajar door, slamming it shut with a resounding bang. The room fell into sudden darkness, the only source of light now the occasional lightning that danced across the sky.

As the door closed, Sarah and David exchanged a glance, their expressions now a mix of surprise and concern. The narrator, a silent witness to the unfolding events, could feel the atmosphere thicken with an unspoken uncertainty.

"Maybe we should check outside," David suggested, his voice betraying a hint of nervousness.

Sarah nodded, and together they cautiously approached the door. With a collective breath, they opened it to reveal a world transformed by the storm. Raindrops lashed against their faces, and the wind howled in protest, carrying with it the whispers of the night.

The adventure that had started as a cozy evening by the fireplace had taken an unexpected turn. The thunder, the closing door, and the mysterious mansion on the outskirts of town left an indelible mark on Sarah and David's friendship, weaving a tale that would be retold on stormy nights for years to come.
"""

def process_epub(sender):
  print('processing epub')
  time.sleep(2)
  dispatcher.send(signal='book_data', data=story)


dispatcher.connect(
  process_epub,
  signal='epub_file',
  sender=dispatcher.Any
)
