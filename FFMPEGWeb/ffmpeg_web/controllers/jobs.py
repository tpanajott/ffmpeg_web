from .singleton_meta import SingletonMeta
from ..models import ConvertJob, Preset
from .ffmpeg import FFMPEG_Job


class Jobs(metaclass=SingletonMeta):
    jobs = list()

    def start_new_job(self, source, destination, preset_id, custom_arguments):
        preset = Preset.objects.get(id=preset_id)
        if preset:
            job = ConvertJob(source=source, destination=destination, preset=preset, custom_arguments=custom_arguments)
            job.save()
            ffmpeg_job = FFMPEG_Job(job)
            self.jobs.append(ffmpeg_job)
    
    def check_if_actually_running(self, job_id):
        for job in self.jobs:
            if job.id == job_id:
                return job.is_actually_running()
        return False