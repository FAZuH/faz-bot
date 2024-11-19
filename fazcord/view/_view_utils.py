from datetime import timedelta


class ViewUtils:

    @staticmethod
    def format_timedelta(timedelta: timedelta) -> str:
        total_seconds = int(timedelta.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        formatted_time = f"{hours}h {minutes}m" if hours > 0 else f"{minutes}m"
        return formatted_time
