import threading
import subprocess
import random
import shlex
import os
import datetime
import time
from ..models import ConvertJob, Preset


class FFMPEG_Job:
    _thread: threading.Thread = None
    _ffmpeg_proc = None
    _job_model = None

    @property
    def source(self):
        return self._job_model.source
    
    @property
    def destination(self):
        return self._job_model.destination
    
    @property
    def preset(self):
        return self._job_model.preset
    
    @property
    def custom_arguments(self):
        return self._job_model.custom_arguments
    
    @property
    def percentage(self):
        return self._job_model.percentage
    
    @percentage.setter
    def percentage(self, current_percentage):
        self._job_model.percentage = current_percentage
        self._job_model.save()
    
    @property
    def status(self):
        return self._job_model.status
    
    @status.setter
    def status(self, new_status):
        self._job_model.status = new_status
        self._job_model.save()
    
    @property
    def error_text(self):
        return self._job_model.error_text
    
    @error_text.setter
    def error_text(self, new_error_text):
        self._job_model.error_text = new_error_text
        self._job_model.save()
    
    @property
    def id(self):
        return self._job_model.id
    
    @property
    def time_left(self):
        return self._job_model.time_left

    @time_left.setter
    def time_left(self, current_time_left):
        self._job_model.time_left = current_time_left
        self._job_model.save()
    
    @property
    def speed(self):
        return self._job_model.speed
    
    @speed.setter
    def speed(self, current_speed):
        self._job_model.speed = current_speed
        self._job_model.save()
        
    @property
    def log(self):
        with open(self._job_model.log_location(), 'r') as log:
            return log.read()
    
    @property
    def source_file_name(self):
        return os.path.basename(self.source)
    
    @property
    def destination_file_name(self):
        return os.path.basename(self.destination)

    def __init__(self, job_model):
        super().__init__()
        self._job_model = job_model
        self._start_thread()
    
    def _start_thread(self):
        if self._thread == None or not self._thread.is_alive():
            self._thread = threading.Thread(target=self._run_ffmpeg)
            self._thread.setDaemon(True)
            self._thread.start()

    def _run_ffmpeg(self):
        if os.path.isfile(self.source):
            self.status = "running"
            preset_arguments = self.preset.arguments
            command = shlex.split(F"ffmpeg -i '{self.source}'  {preset_arguments} {self.custom_arguments} '{self.destination}'")
            if os.path.isfile(self.destination) and "-y" not in command:
                self.status = "failed"
                self._append_to_log("Destination file exists")
                return None
            self._ffmpeg_proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

            # Run the ffmpeg command and read the status
            while True:
                status_line = self._ffmpeg_proc.stderr.readline()
                if status_line == '' and self._ffmpeg_proc.poll() != None:
                    break
                elif status_line.strip().startswith("Duration: "):
                    str_timestamp = status_line.strip().split()[1][:-1]
                    dt_obj = datetime.datetime.strptime(str_timestamp, '%H:%M:%S.%f') - datetime.datetime(1900,1,1)
                    self.length_seconds = dt_obj.total_seconds()
                elif "time=" in status_line and "speed=" in status_line:
                    str_timestamp = status_line.strip().split('time=')[1].split()[0]
                    if str_timestamp:
                        try:
                            dt_obj = datetime.datetime.strptime(str_timestamp, '%H:%M:%S.%f') - datetime.datetime(1900,1,1)
                            percentage_done = round((dt_obj.total_seconds() / self.length_seconds)*100, 2)
                            self.percentage = percentage_done

                            # Calculate an estimet "time left"
                            str_speed = float(status_line.strip().split('speed=')[1][:-1].strip())
                            seconds_left = (self.length_seconds - dt_obj.total_seconds()) / str_speed
                            self.time_left = time.strftime("%H:%M:%S", time.gmtime(seconds_left))
                            self.speed = str_speed
                        except Exception as e:
                            print(e)
                            print(str_timestamp)
                            print(status_line)
                            print("----------------------")
                self._append_to_log(status_line)
            
            stdout, stderr = self._ffmpeg_proc.communicate()
            if self._ffmpeg_proc.returncode == 0:
                self.status = "complete"
                self.percentage = 100
                self.time_left = "00:00:00"
                self.speed = "0"
            else:
                self.status = "failed"
                print(stderr)
        else:
            self.status = "failed"
            self._append_to_log(F"Source file '{self.source}' does not exist!")
        
    def is_actually_running(self):
        """Check if the process is actually running"""
        if self.status == "running" and self._thread:
            if self._thread.is_alive():
                return True
        return False
    
    def rerun(self):
        if self.status != "running":
            if "-y" not in self.custom_arguments:
                self.custom_arguments += "-y"
            self.percentage = 0
            self._start_thread()

    def cancel(self):
        if self._thread:
            if self._thread.is_alive():
                if self._ffmpeg_proc:
                    self._ffmpeg_proc.terminate()
                self.status = "canceled"
                os.remove(self._job_model.destination)
    
    def _append_to_log(self, new_line):
        with open(self._job_model.log_location(), 'a') as log:
            log.write(new_line)