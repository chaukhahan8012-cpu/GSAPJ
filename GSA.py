import streamlit as st
import pandas as pd
import plotly.express as px

# Cấu hình trang
st.set_page_config(page_title="Momentum Engine", page_icon="🚀")

st.title("🚀 Chiến Thần Dọn Nợ - Chuẩn Eisenhower")
st.markdown("### Quản lý thời gian khoa học, đánh bay sự trì hoãn!")

# Sidebar để nhập liệu
with st.sidebar:
    st.header("➕ Thêm Task Mới")
    with st.form("task_form"):
        name = st.text_input("Tên công việc:")
        impact = st.slider("Mức độ Quan trọng (1-10):", 1, 10, 5)
        urgency = st.slider("Mức độ Khẩn cấp (1-10):", 1, 10, 5)
        submitted = st.form_submit_button("Thêm vào danh sách")

# Khởi tạo danh sách task trong session state
if 'tasks' not in st.session_state:
    st.session_state.tasks = []

if submitted and name:
    st.session_state.tasks.append({"Task": name, "Impact": impact, "Urgency": urgency})

if st.session_state.tasks:
    df = pd.DataFrame(st.session_state.tasks)
    
    # Phân loại Eisenhower CHUẨN KHOA HỌC (Lấy mốc 5.5 làm ranh giới giữa Khẩn cấp/Quan trọng)
    def classify(row):
        if row['Impact'] >= 6 and row['Urgency'] >= 6: 
            return "Q1 (Đỏ): Quan trọng & Khẩn cấp (Làm ngay)"
        elif row['Impact'] >= 6 and row['Urgency'] < 6: 
            return "Q2 (Xanh dương): Quan trọng, Không khẩn cấp (Lên lịch)"
        elif row['Impact'] < 6 and row['Urgency'] >= 6: 
            return "Q3 (Xanh lá): Khẩn cấp, Không quan trọng (Ủy quyền)"
        else: 
            return "Q4 (Vàng): Không quan trọng & Không khẩn cấp (Loại bỏ)"
    
    df['Quadrant'] = df.apply(classify, axis=1)

    # Quy định màu sắc chuẩn xác theo lý thuyết ma trận
    color_map = {
        "Q1 (Đỏ): Quan trọng & Khẩn cấp (Làm ngay)": "red",
        "Q2 (Xanh dương): Quan trọng, Không khẩn cấp (Lên lịch)": "blue",
        "Q3 (Xanh lá): Khẩn cấp, Không quan trọng (Ủy quyền)": "green",
        "Q4 (Vàng): Không quan trọng & Không khẩn cấp (Loại bỏ)": "yellow"
    }

    # Hiển thị biểu đồ bong bóng
    fig = px.scatter(df, x="Urgency", y="Impact", color="Quadrant",
                     text="Task", hover_name="Task", size_max=20,
                     color_discrete_map=color_map,
                     title="Bản đồ Phân bổ Công việc",
                     range_x=[0, 11], range_y=[0, 11])
    
    # Vẽ đường chia 4 ô chuẩn xác
    fig.add_vline(x=5.5, line_dash="dash", line_color="gray")
    fig.add_hline(y=5.5, line_dash="dash", line_color="gray")
    
    # Cập nhật giao diện biểu đồ để bong bóng to đều dễ nhìn
    fig.update_traces(marker=dict(size=15, opacity=0.8), textposition='top center')
    
    st.plotly_chart(fig, use_container_width=True)

    # Danh sách chi tiết tự động ưu tiên từ Q1 đến Q4
    st.write("### 📋 Kế hoạch hành động chi tiết:")
    # Sắp xếp ưu tiên: Impact cao nhất và Urgency cao nhất lên đầu
    st.dataframe(df.sort_values(by=["Impact", "Urgency"], ascending=[False, False])[['Task', 'Quadrant', 'Impact', 'Urgency']])
else:
    st.info("Nhập task bên trái để AI tự động phân loại vào 4 ô Eisenhower nhé!")
