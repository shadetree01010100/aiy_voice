from nio import Block, Signal
from nio.properties import VersionProperty
from nio.util.threading import spawn
import aiy.audio
import aiy.voicehat
import aiy.assistant.auth_helpers
from aiy.assistant.library import Assistant
from google.assistant.library.event import EventType


class OKGoogle(Block):

    version = VersionProperty('0.1.0')

    def __init__(self):
        super().__init__()
        self._thread = None
        self._kill = False
        self.credentials = aiy.assistant.auth_helpers.get_assistant_credentials()

    def start(self):
        super().start()
        self._thread = spawn(self.gobabygo)

    def stop(self):
        super().stop()
        self._kill = True
        self._thread.join()
        self.logger.debug('secondary thread stopped')

    def gobabygo(self):
        self.logger.debug('secondary thread started')
        with Assistant(self.credentials) as assistant:
            for event in assistant.start():
                if not self._kill:
                    self.process_event(assistant, event)
                else:
                    break

    def process_event(self, assistant, event):
        self.logger.debug(event.type)
        if event.type == EventType.ON_MUTED_CHANGED:
            self.logger.debug(event.args['is_muted'])
        if event.type == EventType.ON_RECOGNIZING_SPEECH_FINISHED and event.args:
            self.notifiy_signals(Signal({'speech': event.args['text']}))
