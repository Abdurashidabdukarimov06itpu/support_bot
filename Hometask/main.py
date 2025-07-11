import streamlit as st
import google.generativeai as genai
from datetime import datetime


genai.configure(api_key="AIzaSyBdWoXhGB8tFMa1zvBwAd9D7NY2_z64sT0")
model = genai.GenerativeModel('models/gemini-1.5-flash')


company_info = {
    "phone": "+7 (495) 123-45-67",
    "телефон": "+7 (495) 123-45-67",
    "phone number": "+7 (495) 123-45-67",
    "номер телефона": "+7 (495) 123-45-67",
    "contact": "+7 (495) 123-45-67",
    "contacts": "+7 (495) 123-45-67",

    "email": "info@company.com",
    "email address": "info@company.com",
    "электронная почта": "info@company.com",

    "address": "Москва, ул. Примерная, д.1",
    "адрес": "Москва, ул. Примерная, д.1",
    "location": "Москва, ул. Примерная, д.1",

    "working hours": "Пн-Пт, с 9:00 до 18:00",
    "часы работы": "Пн-Пт, с 9:00 до 18:00",
    "время работы": "Пн-Пт, с 9:00 до 18:00",
    "schedule": "Пн-Пт, с 9:00 до 18:00"
}



def check_company_info(question):
    question_lower = question.lower()
    for keyword, answer in company_info.items():
        if keyword in question_lower:
            return answer
    return None


# --- Запрос к ИИ ---
def ask_gemini(question):
    try:
        response = model.generate_content(question)
        return response.text
    except Exception as e:
        return "Ошибка при обращении к AI: " + str(e)

# --- Создание тикета ---
def create_ticket(question):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("support_tickets.txt", "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] Вопрос: {question}\n")
    return "Тикет создан! С вами свяжется служба поддержки."

# --- Интерфейс Streamlit ---
st.title("💬 AI-бот поддержки компании")

question = st.text_input("Введите ваш вопрос:")

if question:
    # Сначала ищем ответ в базе
    company_answer = check_company_info(question)

    if company_answer:
        st.info("Ответ из базы FAQ:")
        st.success(company_answer)
    else:
        ai_response = ask_gemini(question)
        st.info("Ответ ИИ:")
        st.success(ai_response)

        if "не знаю" in ai_response.lower() or "не уверен" in ai_response.lower():
            if st.button("Создать тикет в поддержку"):
                result = create_ticket(question)
                st.warning(result)
