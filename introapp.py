import streamlit as st
from datetime import date
import spacy
from streamlit_tags import st_tags

# Load SpaCy English model
nlp = spacy.load("en_core_web_sm")

# --- APP HEADER ---
st.title("🎓 Student Introduction Format Generator")
st.write("Fill in your details and generate either a **Casual** or a **Professional** introduction!")

# --- Basic Info ---
with st.expander("📝 Basic Info", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        greeting = st.selectbox("Select Greeting", ["Good Morning", "Good Afternoon", "Good Evening"])
        title = st.selectbox("Select Prefix", ["Mr", "Ms", "Mx"])
        name = st.text_input("Full Name")
        age = st.number_input("Age", min_value=5, max_value=100, step=1)
        dob = st.date_input("Date of Birth", value=date(2005, 1, 1), max_value=date(2015, 12, 31))
    with col2:
        department = "Integrated Masters of Physics"
        college_name = "Odisha University of Technology and Research"
        admission_year = st.number_input("Admission Year", min_value=2000, max_value=2100, step=1)
        graduation_year = st.number_input("Graduation Year", min_value=2000, max_value=2100, step=1)
        hometown = st.text_input("Hometown")
        pincode = st.text_input("Hometown Pincode")

def ordinal(n):
    if 10 <= n % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return str(n) + suffix

dob_words = f"{ordinal(dob.day)} {dob.strftime('%B %Y')}"

# --- Education Background ---
with st.expander("🎯 Education Background", expanded=False):
    st.info("⚠️ Please write the full name of your school/college, not abbreviations.")

    def capitalize_proper_nouns(text):
        doc = nlp(text)
        words = []
        for token in doc:
            if token.pos_ in ["PROPN", "NOUN"]:
                words.append(token.text.capitalize())
            else:
                words.append(token.text)
        return " ".join(words)

    affiliation_options = ["CBSE", "ICSE", "CHSE", "HSC"]

    col1, col2 = st.columns(2)
    with col1:
        matric_school = st.text_input("Matriculation School Name")
        matric_school = capitalize_proper_nouns(matric_school)
        matric_school_address = st.text_input("Matriculation School City")
        matric_school_affiliation = st.selectbox("Matriculation School Affiliation", affiliation_options)
        matric_year = st.number_input("Matriculation Year", min_value=2000, max_value=2100, step=1)
        matric_percentage = st.text_input("Matriculation Marks / Percentage").replace("%", "")
    with col2:
        inter_school = st.text_input("Intermediate School/College Name")
        inter_school = capitalize_proper_nouns(inter_school)
        inter_school_address = st.text_input("Intermediate School/College City")
        inter_school_affiliation = st.selectbox("Intermediate School/College Affiliation", affiliation_options)
        inter_year = st.number_input("Intermediate Year", min_value=2000, max_value=2100, step=1)
        inter_percentage = st.text_input("Intermediate Marks / Percentage").replace("%", "")
        jee_year = st.number_input("JEE/OJEE Year", min_value=2000, max_value=2100, step=1)
        jee_rank = st.text_input("JEE/OJEE Percentile").replace("%", "")

# --- Personal Interests (Hobbies) ---
st.header("🎨 Personal Interests")
hobbies_database = [
    "Cricket","Football","Hockey","Volleyball","Basketball","Chess","Swimming","Singing",
    "Dancing","Painting","Photography","Coding","Robotics","Reading","Writing","Gaming",
    "Cycling","Hiking","Cooking","Blogging","Public Speaking"
]

selected_activities = st_tags(
    label='🎨 Enter your hobbies / interests',
    text='Type to get suggestions from database',
    value=[],
    suggestions=hobbies_database,
    maxtags=20,
    key='1'
)

# --- Hobby Formatter ---
def to_gerund(word):
    word = word.lower()
    irregulars = {"run": "running", "swim": "swimming", "sit": "sitting", "begin": "beginning"}
    if word in irregulars:
        return irregulars[word]
    if word.endswith("e") and word not in ["be", "see", "flee"]:
        return word[:-1] + "ing"
    elif word.endswith("ing"):
        return word
    else:
        return word + "ing"

def format_hobby(hobby):
    hobby = hobby.strip()
    if not hobby:
        return ""
    doc = nlp(hobby)
    words = []
    i = 0
    while i < len(doc):
        token = doc[i]
        if token.text.lower() == "to" and i + 1 < len(doc):
            words.append(to_gerund(doc[i + 1].text))
            i += 2
            continue
        elif token.text.lower() == "play" and i + 1 < len(doc):
            words.append("playing")
            words.append(doc[i + 1].text.lower())
            i += 2
            continue
        elif token.pos_ == "VERB":
            words.append(to_gerund(token.text))
        elif token.pos_ == "PROPN":
            words.append(token.text)
        else:
            words.append(token.text.lower())
        i += 1
    if words:
        words[0] = words[0].capitalize()
    return " ".join(words)

def format_hobbies_list(hobbies):
    formatted = [format_hobby(h) for h in hobbies if h.strip()]
    if not formatted:
        return ""
    if len(formatted) == 1:
        return formatted[0]
    return ", ".join(formatted[:-1]) + ", and " + formatted[-1]

if selected_activities:
    formatted_hobbies_list = format_hobbies_list(selected_activities)
    st.markdown(
        f"<div style='background-color: #fef9c3; padding: 10px; border-radius: 8px;'>"
        f"<strong>✅ Formatted Hobbies:</strong> {formatted_hobbies_list}"
        f"</div>",
        unsafe_allow_html=True
    )

# --- Additional Personal Info ---
with st.expander("📝 Additional Info", expanded=False):
    why_college = st.text_area("Why did you choose this college?")
    goals = st.text_area("Your Future Goals")
    fun_fact = st.text_area("A Fun Fact About You")

# --- Validation ---
all_fields_filled = all([
    str(greeting).strip(), str(title).strip(), str(name).strip(), age > 0,
    admission_year > 0, graduation_year > 0, str(hometown).strip(), str(pincode).strip(),
    str(matric_school).strip(), str(matric_school_address).strip(), str(matric_school_affiliation).strip(),
    matric_year > 0, str(matric_percentage).strip(), str(inter_school).strip(), str(inter_school_address).strip(),
    str(inter_school_affiliation).strip(), inter_year > 0, str(inter_percentage).strip(),
    jee_year > 0, str(jee_rank).strip(), str(why_college).strip(), str(goals).strip(),
    str(fun_fact).strip()
]) and len(selected_activities) > 0

# --- Buttons and Output ---
col1, col2 = st.columns(2)
with col1:
    if st.button("Generate Casual Intro"):
        if all_fields_filled:
            hobbies_text = format_hobbies_list(selected_activities)
            casual_intro = f"""
{greeting} everyone 👋  
I'm {name}, {age} years old, currently pursuing {department} at {college_name}.  
I like {hobbies_text} in my free time.  
I chose this college because {why_college}.  
In the future, I want to {goals}.  
A fun fact about me is: {fun_fact}.
"""
            st.markdown(f"<div style='background-color: #e0f7fa; padding: 20px; border-radius: 10px;'>{casual_intro}</div>", unsafe_allow_html=True)
        else:
            st.error("⚠️ Please fill **all the fields** before generating your introduction.")

with col2:
    if st.button("Generate Professional Intro"):
        if all_fields_filled:
            hobbies_text = format_hobbies_list(selected_activities)
            professional_intro = f"""
{greeting} sir/madam,

My name is {title} {name}. I was born on {dob_words}. I am from {hometown}, postal index number {pincode}.  

I have completed my matriculation from {matric_school}, {matric_school_address}, affiliated to {matric_school_affiliation} in {matric_year} with {matric_percentage}%.  

I have completed my intermediate from {inter_school}, {inter_school_address}, affiliated to {inter_school_affiliation} in {inter_year} with {inter_percentage}%.  

I appeared in the JEE/OJEE in {jee_year} and secured a percentile of {jee_rank}%.  

Currently, I am pursuing {department} at {college_name}.  
My hobbies include {hobbies_text}.  

I chose this college because {why_college}.  
In the future, I aim to {goals}.  
Thank you seniors for giving me this opportunity.
"""
            st.markdown(f"<div style='background-color: #fff3e0; padding: 20px; border-radius: 10px;'>{professional_intro}</div>", unsafe_allow_html=True)
        else:
            st.error("⚠️ Please fill **all the fields** before generating your professional introduction.")

# --- Footer ---
st.markdown("<hr><p style='text-align:center'>Developed by Mallick S. | Contact: Soumyakanta2005@outlook.com</p>", unsafe_allow_html=True)
