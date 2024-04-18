import time
from pydispatch import dispatcher

# Simulate book orhcestration
script = [
  { 'id': 0, 'voice': 'narrator', 'text': "In a quaint little town nestled between rolling hills and dense forests, lived two friends named Sarah and David. They were inseparable since childhood, sharing laughter, dreams, and the occasional secret. One gloomy evening, the sky painted in shades of gray, they found themselves in Sarah's cozy living room, engrossed in conversation. As the raindrops tapped against the window pane, the room echoed with the warmth of their friendship. The narrator, a silent observer to their tales, watched as Sarah and David exchanged stories of their week, relishing the comforting ambiance of the crackling fireplace."},
  { 'id': 1, 'voice': 'sarah', 'text': 'So, David'},
  { 'id': 2, 'voice': 'narrator', 'text': 'Sarah said, her eyes sparkling with mischief,'},
  { 'id': 3, 'voice': 'sarah', 'text': "have you heard about the old mansion on the outskirts of town? They say it's haunted."},
  { 'id': 4, 'voice': 'narrator', 'text': 'David chuckled,'},
  { 'id': 5, 'voice': 'david', 'text': "Come on, Sarah. Ghost stories? You know I don't believe in that stuff."},
  { 'id': 6, 'voice': 'narrator', 'text': 'As their banter continued, the wind outside grew more insistent, whispering secrets that only the bravest trees dared to share. The narrator could sense a subtle tension building in the room, a prelude to an unexpected twist in their evening. Just as Sarah began to describe the eerie sounds rumored to emanate from the mansion, a sudden, thunderous boom shook the entire house. The lights flickered, casting eerie shadows on the walls. Startled, Sarah and David exchanged wide-eyed glances.'},
  { 'id': 7, 'voice': 'sarah', 'text': 'Was that thunder?'},
  { 'id': 8, 'voice': 'narrator', 'text': 'Sarah asked, her voice barely audible over the howling wind. David nodded, attempting to ease the tension with a reassuring smile.'},
  { 'id': 9, 'voice': 'david', 'text': 'Just a storm, nothing to worry about.'},
  { 'id': 10, 'voice': 'narrator', 'text': 'But before anyone could say another word, a gust of wind burst through the slightly ajar door, slamming it shut with a resounding bang. The room fell into sudden darkness, the only source of light now the occasional lightning that danced across the sky.'},
  { 'id': 11, 'voice': 'david', 'text': 'Maybe we should check outside,'},
  { 'id': 12, 'voice': 'narrator', 'text': 'David suggested, his voice betraying a hint of nervousness. Sarah nodded, and together they cautiously approached the door. With a collective breath, they opened it to reveal a world transformed by the storm. Raindrops lashed against their faces, and the wind howled in protest, carrying with it the whispers of the night. The adventure that had started as a cozy evening by the fireplace had taken an unexpected turn. The thunder, the closing door, and the mysterious mansion on the outskirts of town left an indelible mark on Sarah and David\'s friendship, weaving a tale that would be retold on stormy nights for years to come.'},
]

def orchestrate_book(sender, data):
  print(f'orchestrating book')

  for item in script:
    dispatcher.send(signal='tts', data=item)
    time.sleep(1)

  print(f'book orchestrated')


dispatcher.connect(
  orchestrate_book,
  signal='book_data',
  sender=dispatcher.Any,
)
