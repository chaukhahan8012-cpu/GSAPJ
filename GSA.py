import streamlit as st
import pandas as pd
import plotly.express as px

# Cấu hình trang
st.set_page_config(page_title="Momentum Engine", page_icon="🚀")

st.title("🚀 Post-Tet Momentum Engine")
st.markdown("### Đừng để 'nợ' Tết làm phiền bạn. Hãy dọn dẹp một cách khoa học!")

# Sidebar để nhập liệu
with st.sidebar:
    st.header("➕ Thêm Task Mới")
    with st.form("task_form"):
        name = st.text_input("Tên công việc:")
        impact = st.slider("Tầm quan trọng (Impact)", 1, 10, 5)
        urgency = st.slider("Độ khẩn cấp (Urgency)", 1, 10, 5)
        submitted = st.form_submit_button("Thêm vào danh sách")

# Khởi tạo danh sách task trong session state
if 'tasks' not in st.session_state:
    st.session_state.tasks = []

if submitted and name:
    st.session_state.tasks.append({"Task": name, "Impact": impact, "Urgency": urgency})

if st.session_state.tasks:
    df = pd.DataFrame(st.session_state.tasks)
    
    # Phân loại Eisenhower
    def classify(row):
        if row['Impact'] >= 7 and row['Urgency'] >= 7: return "P1: Làm Ngay"
        if row['Impact'] >= 7 and row['Urgency'] < 7: return "P2: Lên Lịch"
        if row['Impact'] < 7 and row['Urgency'] >= 7: return "P3: Ủy Thác"
        return "P4: Xóa Bỏ"
    
    df['Quadrant'] = df.apply(classify, axis=1)
    df['Priority'] = (df['Impact'] * 0.6) + (df['Urgency'] * 0.4)

    # Hiển thị biểu đồ
    fig = px.scatter(df, x="Urgency", y="Impact", color="Quadrant",
                     size="Priority", text="Task", hover_name="Task",
                     title="Ma trận Ưu tiên Eisenhower",
                     range_x=[0, 11], range_y=[0, 11])
    
    # Vẽ đường chia 4 ô
    fig.add_vline(x=7, line_dash="dash", line_color="gray")
    fig.add_hline(y=7, line_dash="dash", line_color="gray")
    
    st.plotly_chart(fig, use_container_width=True)

    # Danh sách chi tiết
    st.write("### 📋 Action Plan của bạn:")
    st.dataframe(df.sort_values(by="Priority", ascending=False)[['Task', 'Quadrant', 'Priority']])
else:
    st.info("Nhập task bên trái để bắt đầu sắp xếp nhé!")