
from datetime import date, datetime, timedelta


def generate_schedule(tasks, available_hours):
    """
    tasks: 從 SQLite get_tasks() 取得的任務
    available_hours: 每週七天的可用時數
    """

    schedule = []
    warnings = []

    today = date.today()

    # 依截止日期排序，同日截止則優先安排重要任務
    sorted_tasks = sorted(
        tasks,
        key=lambda t: (t[2], -t[4])
    )

    # 建立每天剩餘的可用時數
    daily_remaining = {}

    for task in sorted_tasks:
        task_id, name, deadline, hours, priority, completed = task

        end_date = datetime.strptime(
            deadline, "%Y-%m-%d"
        ).date()

        remaining = max(0, hours - completed)
        current_day = today

        while current_day <= end_date and remaining > 0.001:

            if current_day not in daily_remaining:
                daily_remaining[current_day] = (
                    available_hours[current_day.weekday()]
                )

            free_hours = daily_remaining[current_day]

            if free_hours > 0:
                assigned = min(remaining, free_hours)

                schedule.append({
                    "日期": str(current_day),
                    "任務名稱": name,
                    "安排時數": round(assigned, 2),
                    "重要程度": priority
                })

                daily_remaining[current_day] -= assigned
                remaining -= assigned

            current_day += timedelta(days=1)

        if remaining > 0.001:
            warnings.append(
                f"{name}：有 {remaining:.1f} 小時無法在截止日前安排"
            )

    schedule.sort(key=lambda x: (x["日期"], -x["重要程度"]))

    return schedule, warnings
