import pypresence
import time
import logging
import sys
import os

logger = logging.getLogger(__name__)

client_id = 1457735765617541262

# Global API client reference (will be set by vrpc.py)
api_client = None

class Presence:
   def __init__(self) -> None:
      try:
         self.client = pypresence.Presence(client_id)
         logger.info(f'Attempting to connect to Discord on {sys.platform}...')
         
         # On Linux, check for IPC socket and set environment variable if needed
         if sys.platform != 'win32':
            uid = os.getuid()
            ipc_paths = [
               f'/run/user/{uid}/discord-ipc-0',  # Standard path
               f'/run/user/{uid}/app/com.discordapp.Discord/discord-ipc-0',  # Flatpak path
               f'/tmp/discord-ipc-0',  # Fallback
            ]
            
            # Set XDG_RUNTIME_DIR if using Flatpak
            for ipc_path in ipc_paths:
               if os.path.exists(ipc_path):
                  logger.info(f'Found Discord IPC socket at: {ipc_path}')
                  # For Flatpak, might need to set environment variable
                  if 'com.discordapp.Discord' in ipc_path:
                     logger.info('Detected Flatpak Discord installation')
                  break
            else:
               logger.warning('Discord IPC socket not found')
               logger.warning('Trying to connect anyway...')
         
         self.client.connect()
         logger.info('✓ Successfully connected to Discord!')
      except Exception as e:
         logger.error(f'✗ Failed to connect to Discord: {e}')
         logger.error('Troubleshooting:')
         logger.error('  1. Make sure Discord desktop app is open and logged in')
         logger.error('  2. On Linux, Discord daemon must be running')
         logger.error('  3. If using Flatpak Discord, ensure it has proper permissions')
         raise

      self._last_updated = time.time() - 15

      self.state = 'Waiting...'
      self.status = {}
      self._prev_status = {}

   def update(self, status: dict) -> None:
      status['buttons'] = [{'label': 'Download from GitHub', 'url': 'https://github.com/PenguinDevs/ValoRPC/releases/latest'}]
      self.status = status
      self.__check_changed()
      
      # Also send to API server if configured
      if api_client and api_client.enabled:
         try:
            # Extract relevant info from status dict
            large_text = status.get('large_text', 'Valorant')
            state = status.get('state', '')
            details = status.get('details', '')
            
            # Determine status: if large_text contains "Valorant" and we have state/details, we're in-game
            if 'Valorant' in large_text and (state or details):
               api_client.set_playing(details=details, state=state)
            elif 'Valorant' in large_text:
               api_client.set_online()
            else:
               api_client.set_offline()
         except Exception as e:
            logger.warning(f'Failed to send update to API: {e}')

   def __check_changed(self) -> None:
      time_now = time.time()
      if (time_now - self._last_updated) >= 15:
         logger.debug(f'Current presence is {self.status}')
         if self.status != self._prev_status:
            try:
               self._prev_status = self.status.copy()
               self.client.update(**self.status)
               self._last_updated = time_now
               logger.info(f'✓ Updated Discord status')
            except Exception as e:
               logger.error(f'✗ Failed to update Discord status: {e}')


if __name__ == '__main__':
   presence = Presence()
   presence.update()
