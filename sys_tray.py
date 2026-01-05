# System tray compatibility wrapper for Linux
# On Linux, we run in the background without a system tray icon

import logging
import time

logger = logging.getLogger(__name__)


class SystemTrayApp(object):
    """Fallback system tray app for Linux - runs in background"""
    def __init__(self, icon: str, hover_text: str, menu_options: list, window_class_name: str, on_quit=None, default_menu_index=None):
        self.icon = icon
        self.hover_text = hover_text
        self.on_quit = on_quit
        self.menu_options = menu_options
        logger.info(f'Running in background mode (no system tray on Linux)')
    
    def loop(self):
        """Keep the app running"""
        logger.info('ValoRPC running in background')
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info('Application interrupted')
            if self.on_quit:
                self.on_quit(self)
    
    def win_notify(self, title: str, desc: str):
        """Fallback notification using logging"""
        logger.info(f'Notification - {title}: {desc}')
