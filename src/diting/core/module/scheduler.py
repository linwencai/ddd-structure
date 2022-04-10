from inspect import isawaitable
import platform
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sanic import Sanic
from diting.core.common.log import app_logger as logger

app = Sanic.get_app()

async def tick():
    print('Tick! The time is: %s' % datetime.now())

@app.after_server_start
async def initialize_scheduler(app: Sanic, _) -> None:

    try:
        if platform.system() == "Linux":
            import fcntl
            _ = open("/tmp/sanic.lock","w")
            _fd = _.fileno()
            fcntl.lockf(_fd,fcntl.LOCK_EX|fcntl.LOCK_NB)

        scheduler = AsyncIOScheduler({'event_loop': app.loop})
        app.ctx.scheduler = scheduler

        # adding scheduler_tasks
        import diting.core.module.scheduler_task

        scheduler.start()
        logger.info("Scheduler Started!")
    except BlockingIOError:
        pass

@app.after_server_stop
async def shutdown_scheduler(app: Sanic, _) -> None:
    app.ctx.scheduler.shutdown()

from functools import wraps, partial

def scheduler_at(*s_args, **s_kwargs):
    assert "id" in s_kwargs
    s_kwargs['replace_existing'] = True
    def decorator(f):
        app : Sanic = Sanic.get_app()
        scheduler = app.ctx.scheduler
        job = scheduler.add_job(partial(f, app), *s_args, **s_kwargs)
        logger.info(f"add scheduler job: {str(job.id)}")
        @wraps(f)
        async def decorated_function(*args, **kwargs):
            ret = f(*args, **kwargs)

            if isawaitable(ret):
                ret = await ret
            
            return ret
        
        return decorated_function
    return decorator


