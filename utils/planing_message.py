from apscheduler_di import ContextSchedulerDecorator


def create_delayed_notification(delayed_func, user_id: int, lat: float, lon: float, alarm_time: str,
                                apscheduler: ContextSchedulerDecorator) -> None:
    hour, minute = alarm_time.split(":")
    apscheduler.add_job(delayed_func, trigger="cron",
                        hour=str(hour), minute=str(minute), id=str(user_id),
                        replace_existing=True,
                        kwargs={'user_id': user_id,
                                'lat': lat,
                                'lon': lon})


def remove_delayed_notification(user_id: int, apscheduler: ContextSchedulerDecorator) -> None:
    apscheduler.remove_job(str(user_id))


def remove_all_delayed_notifications(apscheduler: ContextSchedulerDecorator) -> None:
    apscheduler.remove_all_jobs()


