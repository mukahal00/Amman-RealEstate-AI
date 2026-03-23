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

# إنشاء قاموس يربط اسم المنطقة بالرقم الخاص بها
locations_map = {
    # 1. High-End
    "عبدون (Abdoun)": 1.0, 
    "دابوق (Dabouq)": 1.0, 
    "دير غبار (Deir Ghbar)": 1.0, 
    "أم أذينة (Um Uthaina)": 1.0, 
    "الصويفية (Sweifieh)": 1.0,
    
    # 2. Mid-Range
    "خلدا (Khalda)": 2.0, 
    "تلاع العلي (Tlaa Al Ali)": 2.0, 
    "الشميساني (Shmeisani)": 2.0, 
    "الجبيهة (Jubeiha)": 2.0, 
    "الرابية (Rabieh)": 2.0,
    
    # 3. Affordable
    "طبربور (Tabarbour)": 3.0, 
    "ماركا (Marka)": 3.0, 
    "الهاشمي (Al-Hashimi)": 3.0, 
    "أبو نصير (Abu Nuseir)": 3.0, 
    "النزهة (Al-Nuzha)": 3.0
}

# ترتيب الحقول في الشاشة
col1, col2, col3 = st.columns(3)

with col1:
    selected_area_name = st.selectbox("اختر المنطقة", list(locations_map.keys()))
    region_number = locations_map[selected_area_name]
    
with col2:
    # حولنا القيم إلى أرقام صحيحة (Integer) بإزالة الفواصل
    area = st.number_input("مساحة البناء (م²)", value=150, min_value=50, step=1)
    
with col3:
    # حولنا القيم إلى أرقام صحيحة (Integer) بإزالة الفواصل
    age = st.number_input("عمر البناء (سنوات)", value=5, min_value=0, step=1)

if st.button("احسب السعر المتوقع 🔍"):
    # نقوم بتحويل المدخلات إلى Float فقط داخل النموذج ليتمكن من حسابها بدقة
    input_data = np.array([[region_number, float(area), float(age)]])
    prediction = model.predict(input_data)
    
    # عرض السعر النهائي كـ Float مع منزلتين عشريتين
    st.success(f"السعر التقريبي المتوقع في {selected_area_name.split(' ')[0]}: {prediction[0][0]:,.2f} ألف دينار")
