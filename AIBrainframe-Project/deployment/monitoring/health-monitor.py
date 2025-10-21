#!/usr/bin/env python3
"""
LBOB AI Health Monitor - Enterprise Grade 24/7 Monitoring
Monitors LBOB API, Ollama, and system health with automated recovery
"""

import requests
import logging
import time
import subprocess
import json
import psutil
from datetime import datetime
from pathlib import Path
import smtplib
from email.mime.text import MimeText
from typing import Dict, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/lbob/health-monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('lbob-health-monitor')

class LBOBHealthMonitor:
    """24/7 Health monitoring for LBOB AI system"""

    def __init__(self):
        self.config = {
            'lbob_api_url': 'http://localhost:8000',
            'ollama_api_url': 'http://localhost:11434',
            'check_interval': 30,  # seconds
            'failure_threshold': 3,  # consecutive failures before action
            'restart_cooldown': 300,  # seconds between restart attempts
        }

        self.failure_counts = {
            'lbob_api': 0,
            'ollama': 0,
            'database': 0
        }

        self.last_restart = {
            'lbob_api': 0,
            'ollama': 0
        }

        self.status_history = []

    def check_lbob_api(self) -> Dict:
        """Check LBOB FastAPI health"""
        try:
            response = requests.get(
                f"{self.config['lbob_api_url']}/health",
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                return {
                    'status': 'healthy',
                    'response_time': response.elapsed.total_seconds(),
                    'details': data
                }
            else:
                return {
                    'status': 'unhealthy',
                    'error': f"HTTP {response.status_code}",
                    'details': response.text
                }

        except requests.exceptions.RequestException as e:
            return {
                'status': 'unhealthy',
                'error': str(e),
                'details': None
            }

    def check_ollama(self) -> Dict:
        """Check Ollama AI service health"""
        try:
            # Check if service is running
            response = requests.get(
                f"{self.config['ollama_api_url']}/api/tags",
                timeout=15
            )

            if response.status_code == 200:
                models = response.json().get('models', [])
                llama_available = any('llama3.1:8b' in model.get('name', '') for model in models)

                return {
                    'status': 'healthy' if llama_available else 'degraded',
                    'response_time': response.elapsed.total_seconds(),
                    'models_count': len(models),
                    'llama_available': llama_available,
                    'details': models
                }
            else:
                return {
                    'status': 'unhealthy',
                    'error': f"HTTP {response.status_code}",
                    'details': response.text
                }

        except requests.exceptions.RequestException as e:
            return {
                'status': 'unhealthy',
                'error': str(e),
                'details': None
            }

    def check_system_resources(self) -> Dict:
        """Check system resource utilization"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')

            return {
                'status': 'healthy',
                'cpu_percent': cpu_percent,
                'memory_percent': memory.percent,
                'disk_percent': disk.percent,
                'memory_available_gb': memory.available / (1024**3),
                'disk_free_gb': disk.free / (1024**3)
            }

        except Exception as e:
            return {
                'status': 'unhealthy',
                'error': str(e)
            }

    def restart_service(self, service_name: str) -> bool:
        """Restart a systemd service with cooldown protection"""
        current_time = time.time()

        # Check cooldown period
        if current_time - self.last_restart[service_name] < self.config['restart_cooldown']:
            logger.warning(f"Restart cooldown active for {service_name}")
            return False

        try:
            logger.info(f"Attempting to restart {service_name}")

            # Stop service
            subprocess.run(['sudo', 'systemctl', 'stop', service_name], check=True)
            time.sleep(5)

            # Start service
            subprocess.run(['sudo', 'systemctl', 'start', service_name], check=True)

            # Update last restart time
            self.last_restart[service_name] = current_time

            logger.info(f"Successfully restarted {service_name}")
            return True

        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to restart {service_name}: {e}")
            return False

    def handle_failure(self, component: str, check_result: Dict):
        """Handle component failure with escalating response"""
        self.failure_counts[component] += 1
        failure_count = self.failure_counts[component]

        logger.warning(f"{component} failure #{failure_count}: {check_result.get('error', 'Unknown error')}")

        # Take action based on failure count
        if failure_count >= self.config['failure_threshold']:
            logger.error(f"{component} has failed {failure_count} times, taking corrective action")

            if component == 'lbob_api':
                self.restart_service('lbob-api')
            elif component == 'ollama':
                self.restart_service('ollama')

            # Reset failure count after action
            self.failure_counts[component] = 0

    def handle_success(self, component: str):
        """Reset failure count on successful check"""
        if self.failure_counts[component] > 0:
            logger.info(f"{component} recovered, resetting failure count")
            self.failure_counts[component] = 0

    def log_status(self, status_report: Dict):
        """Log comprehensive status report"""
        timestamp = datetime.now().isoformat()

        # Add to history
        status_entry = {
            'timestamp': timestamp,
            'status': status_report
        }
        self.status_history.append(status_entry)

        # Keep only last 100 entries
        if len(self.status_history) > 100:
            self.status_history = self.status_history[-100:]

        # Log summary
        lbob_status = status_report['lbob_api']['status']
        ollama_status = status_report['ollama']['status']
        system_status = status_report['system']['status']

        logger.info(f"Health Check - LBOB: {lbob_status}, Ollama: {ollama_status}, System: {system_status}")

        # Write detailed status to file
        status_file = Path('/var/log/lbob/status.json')
        status_file.parent.mkdir(exist_ok=True)

        with open(status_file, 'w') as f:
            json.dump(status_entry, f, indent=2)

    def run_health_check(self) -> Dict:
        """Run complete health check"""
        logger.debug("Running health check cycle")

        # Check all components
        lbob_result = self.check_lbob_api()
        ollama_result = self.check_ollama()
        system_result = self.check_system_resources()

        # Handle results
        components = {
            'lbob_api': lbob_result,
            'ollama': ollama_result,
            'system': system_result
        }

        for component, result in components.items():
            if result['status'] in ['unhealthy', 'degraded']:
                self.handle_failure(component, result)
            else:
                self.handle_success(component)

        # Create status report
        status_report = {
            'lbob_api': lbob_result,
            'ollama': ollama_result,
            'system': system_result,
            'overall_status': self.calculate_overall_status(components)
        }

        # Log status
        self.log_status(status_report)

        return status_report

    def calculate_overall_status(self, components: Dict) -> str:
        """Calculate overall system status"""
        statuses = [comp['status'] for comp in components.values()]

        if all(status == 'healthy' for status in statuses):
            return 'healthy'
        elif any(status == 'unhealthy' for status in statuses):
            return 'unhealthy'
        else:
            return 'degraded'

    def run_monitor(self):
        """Main monitoring loop"""
        logger.info("Starting LBOB AI Health Monitor")
        logger.info(f"Check interval: {self.config['check_interval']} seconds")
        logger.info(f"Failure threshold: {self.config['failure_threshold']} failures")

        while True:
            try:
                self.run_health_check()
                time.sleep(self.config['check_interval'])

            except KeyboardInterrupt:
                logger.info("Health monitor stopped by user")
                break
            except Exception as e:
                logger.error(f"Health monitor error: {e}")
                time.sleep(self.config['check_interval'])

if __name__ == "__main__":
    monitor = LBOBHealthMonitor()
    monitor.run_monitor()