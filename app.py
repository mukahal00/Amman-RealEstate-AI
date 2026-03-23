import streamlit as st
import tensorflow as tf
import numpy as np

st.set_page_config(page_title="حاسبة أسعار العقارات", page_icon="🏠")

# تحميل النموذج الجاهز
@st.cache_resource
def load_model():
    return tf.keras.models.load_model("amman_house_model.keras")

try:
    model = load_model()
except Exception as e:
    st.error(f"حدث خطأ في تحميل النموذج: تأكد من وجود ملف amman_house_model.keras بجانب هذا الملف. التفاصيل: {e}")
    st.stop()

st.title("توقع أسعار البناء في عمّان 🇯🇴🏠")
st.markdown("---")

col1, col2, col3 = st.columns(3)
with col1:
    region = st.selectbox("تصنيف المنطقة", [1.0, 2.0, 3.0])
with col2:
    area = st.number_input("مساحة البناء (م²)", value=150.0)
with col3:
    age = st.number_input("عمر البناء (سنوات)", value=5.0)

if st.button("احسب السعر المتوقع 🔍"):
    prediction = model.predict(np.array([[region, area, age]]))
    st.success(f"السعر التقريبي المتوقع: {prediction[0][0]:,.2f} ألف دينار")