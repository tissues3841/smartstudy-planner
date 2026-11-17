
import streamlit as st
import pandas as pd
from datetime import date

from database import (
    init_db,
    add_task,
    get_tasks,
    delete_task
)
from scheduler import generate_schedule

st.set_page_config(
    page_title="SmartStudy Planner",
    page_icon="📚",
    layout="wide"
)

init_db()

st.title("📚 SmartStudy Planner")
st.subheader("大學生智慧課業排程系統")

st.header("➕ 新增任務")

with st.form("task_form"):
    task_name = st.text_input("任務名稱")

    deadline = st.date_input(
        "截止日期",
        min_value=date.today()
    )

    hours = st.number_input(
        "預估所需時間（小時）",
        min_value=0.5,
        value=2.0,
        step=0.5
    )

    priority = st.slider(
        "重要程度",
        min_value=1,
        max_value=5,
        value=3
    )

    submitted = st.form_submit_button("新增任務")

if submitted:
    if task_name.strip():
        add_task(
            task_name.strip(),
            deadline,
            hours,
            priority
        )
        st.success("任務已成功儲存！")
    else:
        st.warning("請輸入任務名稱！")

st.header("📋 目前任務清單")

tasks = get_tasks()

if tasks:
    df = pd.DataFrame(
        tasks,
        columns=[
            "ID",
            "任務名稱",
            "截止日期",
            "預估工時",
            "重要程度",
            "已完成工時"
        ]
    )

    st.dataframe(df, use_container_width=True)

    st.subheader("🗑️ 刪除任務")

    options = {
        f"{task[0]} - {task[1]}": task[0]
        for task in tasks
    }

    selected = st.selectbox(
        "選擇要刪除的任務",
        options=list(options.keys())
    )

    if st.button("刪除選取任務"):
        delete_task(options[selected])
        st.rerun()

else:
    st.info("目前還沒有任務，請先新增一筆。")

    
st.divider()

st.header("📅 智慧讀書排程")

st.subheader("設定每天可用的讀書時間")

weekdays = [
    "星期一", "星期二", "星期三",
    "星期四", "星期五", "星期六", "星期日"
]

available_hours = []

cols = st.columns(7)

for i, day in enumerate(weekdays):
    with cols[i]:
        h = st.number_input(
            day,
            min_value=0.0,
            max_value=24.0,
            value=2.0,
            step=0.5,
            key=f"hours_{i}"
        )
        available_hours.append(h)

if st.button("🚀 自動產生讀書計畫"):

    tasks = get_tasks()

    if not tasks:
        st.warning("請先新增至少一項任務！")

    else:
        schedule, warnings = generate_schedule(
            tasks,
            available_hours
        )

        st.subheader("你的讀書計畫")

        if schedule:
            df_schedule = pd.DataFrame(schedule)
            st.dataframe(
                df_schedule,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("目前沒有可安排的任務時數。")

        if warnings:
            st.error("⚠️ 部分任務無法如期安排")

            for warning in warnings:
                st.write(warning)
        else:
            st.success("所有剩餘任務工時皆已安排完成！")
