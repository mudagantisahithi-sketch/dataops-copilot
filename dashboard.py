import streamlit as st
import json
import time
from pathlib import Path
from datetime import datetime

# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
STATUS_FILE = BASE_DIR / "pipeline_status.json"
INCOMING_DIR = BASE_DIR / "incoming"
DATA_DIR = BASE_DIR / "data"

INCOMING_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="DataOps Copilot",
    page_icon="📊",
    layout="wide"
)

# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>
    .title {
        font-size: 42px;
        font-weight: 700;
        color: #1f77b4;
    }

    .subtitle {
        font-size: 20px;
        color: #666;
        margin-bottom: 25px;
    }

    .stage {
        padding: 15px;
        border-radius: 10px;
        background-color: #f5f7fa;
        margin: 5px 0;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="title">📊 DataOps Copilot</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Real-Time Data Quality Monitoring & Automatic Repair'
    '</div>',
    unsafe_allow_html=True
)

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("⚙️ Monitoring")

auto_refresh = st.sidebar.checkbox(
    "Enable real-time monitoring",
    value=True
)

refresh_seconds = st.sidebar.slider(
    "Refresh interval",
    min_value=1,
    max_value=10,
    value=2
)

st.sidebar.divider()

st.sidebar.info(
    "This dashboard reads the live pipeline status "
    "from pipeline_status.json."
)

# ============================================================
# LOAD STATUS
# ============================================================

def load_status():

    if not STATUS_FILE.exists():

        return {
            "status": "WAITING",
            "stage": "IDLE",
            "message": "Waiting for a new dataset",
            "score": None,
            "input_file": None,
            "rows": None,
            "error": None,
            "updated_at": None
        }

    try:

        with open(
            STATUS_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    except Exception as e:

        return {
            "status": "ERROR",
            "stage": "ERROR",
            "message": "Unable to read pipeline status",
            "score": None,
            "input_file": None,
            "rows": None,
            "error": str(e),
            "updated_at": None
        }


status_data = load_status()

status = status_data.get("status", "WAITING")
stage = status_data.get("stage", "IDLE")
message = status_data.get(
    "message",
    "Waiting for a new dataset"
)

score = status_data.get("score")
input_file = status_data.get("input_file")
rows = status_data.get("rows")
error = status_data.get("error")
updated_at = status_data.get("updated_at")

# ============================================================
# LIVE STATUS
# ============================================================

st.header("🔴 Live Pipeline Status")

status_col, stage_col, time_col = st.columns(3)

with status_col:

    if status == "PASSED":

        st.success("🟢 PASSED")

    elif status == "FAILED":

        st.error("🔴 FAILED")

    elif status == "RUNNING":

        st.warning("🟡 RUNNING")

    elif status == "ERROR":

        st.error("❌ ERROR")

    else:

        st.info("⚪ WAITING")


with stage_col:

    st.metric(
        "Current Stage",
        stage
    )


with time_col:

    if updated_at:

        try:

            dt = datetime.fromisoformat(
                updated_at
            )

            display_time = dt.strftime(
                "%H:%M:%S"
            )

        except:

            display_time = updated_at

    else:

        display_time = "—"

    st.metric(
        "Last Updated",
        display_time
    )

st.info(message)

# ============================================================
# PIPELINE PROGRESS
# ============================================================

st.header("⚡ Real-Time Pipeline")

stages = [
    "FILE_DETECTED",
    "COPYING",
    "QUALITY_CHECK",
    "QUALITY_CHECK_COMPLETE",
    "REPAIRING",
    "FINAL_QUALITY_CHECK",
    "COMPLETED"
]

stage_index = (
    stages.index(stage)
    if stage in stages
    else -1
)

progress_value = 0

if stage_index >= 0:

    progress_value = (
        stage_index + 1
    ) / len(stages)

elif status == "PASSED":

    progress_value = 1.0

st.progress(
    progress_value,
    text=f"Pipeline progress: {progress_value * 100:.0f}%"
)

# ============================================================
# STAGE DISPLAY
# ============================================================

cols = st.columns(len(stages))

for i, stage_name in enumerate(stages):

    with cols[i]:

        if status == "PASSED" and stage_name == "COMPLETED":

            st.success(
                "✅ " + stage_name.replace("_", " ")
            )

        elif i < stage_index:

            st.success(
                "✅ " + stage_name.replace("_", " ")
            )

        elif i == stage_index:

            st.warning(
                "🔄 " + stage_name.replace("_", " ")
            )

        else:

            st.write(
                "⏳ " + stage_name.replace("_", " ")
            )

# ============================================================
# QUALITY SCORE
# ============================================================

st.divider()

st.header("📊 Data Quality")

score_col, rows_col, file_col = st.columns(3)

with score_col:

    if score is not None:

        st.metric(
            "Quality Score",
            f"{float(score):.2f}%"
        )

    else:

        st.metric(
            "Quality Score",
            "—"
        )

with rows_col:

    st.metric(
        "Rows Processed",
        f"{rows:,}" if rows else "—"
    )

with file_col:

    st.metric(
        "Dataset",
        input_file if input_file else "—"
    )

# ============================================================
# FINAL RESULT
# ============================================================

if status == "PASSED":

    st.success(
        "🎉 Data quality validation passed successfully."
    )

    st.write(
        "The dataset completed the DataOps Copilot pipeline "
        "and achieved a 100% quality score."
    )

elif status == "RUNNING":

    st.warning(
        "🔄 DataOps Copilot is currently processing the dataset."
    )

elif status == "FAILED":

    st.error(
        "⚠️ Data quality issues remain after processing."
    )

elif status == "ERROR":

    st.error(
        "❌ Pipeline error detected."
    )

# ============================================================
# ERROR DETAILS
# ============================================================

if error:

    st.divider()

    st.subheader("❌ Error Details")

    st.code(error)

# ============================================================
# DATASET INFORMATION
# ============================================================

st.divider()

st.header("📦 Dataset Information")

if input_file:

    input_path = INCOMING_DIR / input_file

    if input_path.exists():

        size_mb = (
            input_path.stat().st_size /
            (1024 * 1024)
        )

        info1, info2 = st.columns(2)

        with info1:

            st.metric(
                "File Size",
                f"{size_mb:.2f} MB"
            )

        with info2:

            st.metric(
                "File Modified",
                datetime.fromtimestamp(
                    input_path.stat().st_mtime
                ).strftime("%H:%M:%S")
            )

    else:

        st.info(
            "Input file is no longer in the incoming folder."
        )

else:

    st.info(
        "Waiting for a dataset..."
    )

# ============================================================
# AUTO REFRESH
# ============================================================

if auto_refresh:

    time.sleep(refresh_seconds)

    st.rerun()
