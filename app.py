import pandas as pd
import streamlit as st

# Cấu hình trang Streamlit
st.image("logo.jpg")(
    page_title="Máy tính Lãi suất Tiết kiệm", page_icon="💰", layout="centered"
)

st.title("💰 Ứng Dụng Tính Lãi Suất Tiết Kiệm")
st.write(
    "Nhập thông tin khoản tiết kiệm của bạn để tính toán chi tiết tiền lãi định"
    " kỳ, tổng tiền lãi và tổng số tiền nhận được."
)

# Form nhập liệu
with st.form("savings_form"):
  col1, col2 = st.columns(2)

  with col1:
    principal = st.number_input(
        "Số tiền gửi (VNĐ)",
        min_value=100_000,
        value=100_000_000,
        step=1_000_000,
        format="%d",
    )
    term_months = st.number_input(
        "Kỳ hạn gửi (tháng)", min_value=1, value=12, step=1
    )

  with col2:
    annual_rate = st.number_input(
        "Lãi suất (%/năm)", min_value=0.0, value=6.0, step=0.1, format="%.2f"
    )
    interest_method = st.selectbox(
        "Hình thức nhận lãi", ["Cuối kỳ", "Hàng tháng", "Hàng quý"]
    )

  interest_type = st.radio(
      "Chọn phương thức tính lãi",
      ["Lãi đơn", "Lãi kép (Tái đầu tư định kỳ)"],
      horizontal=True,
  )

  submitted = st.form_submit_button("Tính toán")

if submitted:
  P = principal
  r = annual_rate / 100
  n_months = int(term_months)
  t_years = n_months / 12

  # Xử lý tính toán
  if "Lãi đơn" in interest_type:
    # Lãi đơn: I = P * r * t
    total_interest = P * r * t_years
    total_amount = P + total_interest

    if interest_method == "Hàng tháng":
      num_periods = n_months
      periodic_interest = total_interest / num_periods if num_periods > 0 else 0
    elif interest_method == "Hàng quý":
      num_periods = n_months / 3
      periodic_interest = total_interest / num_periods if num_periods > 0 else 0
    else:
      periodic_interest = total_interest

  else:
    # Lãi kép: A = P * (1 + r/n)^(n*t)
    if interest_method == "Hàng tháng":
      r_period = r / 12
      num_periods = n_months
      total_amount = P * ((1 + r_period) ** num_periods)
      total_interest = total_amount - P
      periodic_interest = (
          total_interest / num_periods if num_periods > 0 else 0
      )  # Lãi trung bình hàng tháng
    elif interest_method == "Hàng quý":
      r_period = r / 4
      num_periods = n_months / 3
      total_amount = P * ((1 + r_period) ** num_periods)
      total_interest = total_amount - P
      periodic_interest = total_interest / num_periods if num_periods > 0 else 0
    else:  # Cuối kỳ (gộp lãi cuối kỳ)
      r_period = r
      num_periods = t_years
      total_amount = P * ((1 + r_period) ** num_periods)
      total_interest = total_amount - P
      periodic_interest = total_interest

  # Hiển thị kết quả
  st.markdown("---")
  st.subheader("📊 Kết quả tính toán")

  col_m1, col_m2, col_m3 = st.columns(3)
  with col_m1:
    st.metric(
        label=(
            "Tiền lãi định kỳ"
            if interest_method != "Cuối kỳ"
            else "Tiền lãi cuối kỳ"
        ),
        value=f"{periodic_interest:,.0f} VNĐ",
    )
  with col_m2:
    st.metric(label="Tổng tiền lãi", value=f"{total_interest:,.0f} VNĐ")
  with col_m3:
    st.metric(label="Tổng gốc và lãi", value=f"{total_amount:,.0f} VNĐ")

  # Hiển thị bảng chi tiết nếu nhận lãi định kỳ theo hình thức Lãi đơn
  if "Lãi đơn" in interest_type and interest_method != "Cuối kỳ":
    st.markdown("### 📅 Bảng chi tiết nhận lãi định kỳ")
    schedule_data = []
    if interest_method == "Hàng tháng":
      for i in range(1, n_months + 1):
        schedule_data.append({
            "Kỳ": f"Tháng {i}",
            "Tiền lãi nhận": f"{periodic_interest:,.0f} VNĐ",
            "Số dư gốc": f"{P:,.0f} VNĐ",
        })
    elif interest_method == "Hàng quý":
      num_q = int(n_months / 3)
      for i in range(1, num_q + 1):
        schedule_data.append({
            "Kỳ": f"Quý {i}",
            "Tiền lãi nhận": f"{periodic_interest:,.0f} VNĐ",
            "Số dư gốc": f"{P:,.0f} VNĐ",
        })
    if schedule_data:
      st.table(pd.DataFrame(schedule_data))
