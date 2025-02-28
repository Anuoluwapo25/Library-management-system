from django.core.management.base import BaseCommand
import requests
import time
import os
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Pings the application to keep it alive'

    def handle(self, *args, **options):
        app_url = os.environ.get('APP_URL')
        
        if not app_url:
            self.stderr.write("Error: APP_URL environment variable is not set")
            return
            
        self.stdout.write(f"Starting ping service for {app_url}")
        
        while True:
            try:
                response = requests.get(app_url)
                self.stdout.write(f"Pinged {app_url}, status: {response.status_code}")
                logger.info(f"Pinged {app_url}, status: {response.status_code}")
            except Exception as e:
                error_msg = f"Failed to ping {app_url}: {str(e)}"
                self.stderr.write(error_msg)
                logger.error(error_msg)
            
            # Wait for 10 minutes before the next ping
            time.sleep(600)