from nio.block.base import Block
from nio.properties import VersionProperty, StringProperty
import aiy.audio

class AiyVoice(Block):

    version = VersionProperty('0.1.0')
    text = StringProperty(title='Text to Speak', default='')
    def process_signals(self, signals):
        output_signals = []
        for signal in signals:
            aiy.audio.say(self.text(signal))
        self.notify_signals(output_signals)
