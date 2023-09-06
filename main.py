import streamlit as st
from docx import Document
from docx.shared import RGBColor, Inches
import utils.resume_generator as rg
import utils.prompts as pr
import utils.resume_reader as rr
from io import BytesIO
import openai
import re

st.title("Welcome to the Resume Customizer")

primary_title_color = RGBColor(65,105,225)
secondary_title_color = RGBColor(255, 165, 0)

################## Contact Information #################
st.markdown("### Enter Your Personal Information")
enter_name = st.text_input("Enter Your Name")
enter_location = st.text_input("Enter Where You Live")
enter_linkedin = st.text_input("Enter LinkedIn Profile URL")
enter_phone = st.text_input("Enter Phone Number")
enter_email = st.text_input("Enter Email Address")

################### Upload resume as JSON ##############
upload_resume = st.file_uploader("Upload Resume in JSON format",type=["json"])

if upload_resume is not None:
    try:
        resume_json = rr.resume_opener(upload_resume)
        st.success("File uploaded successfully!")
    except:
        st.error("Invalid JSON file. Please upload a valid JSON file.")

################## Convert resume to txt doc############
resume_txt = rr.format_resume_as_str(resume_json)

# todo: fix output from format_resume_as_str
st.write(resume_txt)

################## Key Comptencies #####################
kc = resume_json["skills"]
################### OpenAI Input #######################
st.markdown("### Open AI Credentials")
st.write("You'll need an OpenAI account and API key to use the customizer. This app doesn't save this information. If you don't feel comfortable entering this information, please do not use this application.")
enter_org_id = st.text_input("Enter OpenAI Org Id")
enter_key = st.text_input("Enter OpenAI API Key")
openai.api_key = enter_key
openai.organization = enter_org_id

################## Job Description Inputs ##############
st.markdown("### Job Information")
job_title = st.text_input("Enter the Job Title")
job_title = job_title.replace("/","_")
company_name = st.text_input("Enter Company Name")
paste_job_description = st.text_input("Paste Job Description Here")
################## Submit ##############################
if st.button("Get Custom Resume"):
################## Resume Prompts ######################
    summary = pr.response(pr.summary_prompt(resume_txt, job_title, company_name, paste_job_description))
    if summary is not None:
        st.success("Summary Generated")
        st.write(summary)
    strengths = pr.response(pr.strength_prompt(resume_txt,paste_job_description))
    strengths = re.findall(r"'(.*?)'", strengths)
    strengths = [re.sub(r'\n|�|\dM', ' ', item).strip() for item in strengths]
    if strengths is not None:
        st.success("Key Accomplishments Generated")
        st.write(strengths)
    cover_letter = pr.response(pr.cover_letter_prompt(resume_txt, paste_job_description))
    if cover_letter is not None:
        st.success("Cover Letter Generated")
        st.write(cover_letter)
    skills = pr.response(pr.reword_resume(kc,paste_job_description))
    skills = re.findall(r"'(.*?)'", skills)
    skills = [re.sub(r'\n|�|\dM', ' ', item).strip() for item in skills]
    if skills is not None:
        st.success("Skills Selected")
        st.write(skills)
    kws = pr.response(pr.key_words(resume_txt,paste_job_description))
    #questions = pr.response(pr.sample_interview_questions(paste_job_description))
    #questions_to_list = rg.convert_to_list(questions)
    #if questions is not None:
        #st.success("Questions Generated")
        #st.write(questions)
    #st.write("Generating sample answers...")
    #questions_answers = []
    #for question in questions_to_list:
        #questions_response = pr.response(pr.sample_interview_responses(resume_txt,question))
        #questions_answers.append({question:questions_response})
    #about_myself = pr.response(pr.tell_me_about_yourself(resume_txt,paste_job_description))
    #if questions_answers is not None:
        #st.success("Answers Generated")
    
################## Generate Resume Doc #################
    resume_doc = Document()
    section = resume_doc.sections[0]
    section.top_margin = Inches(0.5)
    section.bottom_margin = Inches(0.5)
    section.left_margin = Inches(0.5)
    section.right_margin = Inches(0.5)
    margin = section.page_width - section.right_margin - section.left_margin
    # Top line
    rg.add_custom_paragraph(resume_doc,margin,enter_name, enter_location, primary_title_color, True, font_size1=16)
    # Add the second line with a horizontal line beneath it
    rg.add_custom_paragraph(resume_doc,margin,enter_linkedin, f"{enter_phone} | {enter_email}", add_line=True,font_size1=10)
    # Add the title section to the document
    rg.add_title_section(resume_doc,f"{job_title} | "+kws,primary_title_color)
    # Add the career summary to the document
    rg.add_career_summary(resume_doc,summary)
    # Add Key Accomplishments
    rg.add_key_accomplishments_sections(resume_doc,strengths,secondary_title_color)

    rg.add_key_competencies_section(resume_doc,skills,secondary_title_color)
    rg.add_experience_header(resume_doc,secondary_title_color)
    # Add Jobs History
    for j in resume_json["experience"]:
        # todo: Add select bullets prompt
        rg.add_career_section(resume_doc,j, paste_job_description,6, primary_title_color)

    rg.add_education_and_training_section(resume_doc,resume_json["education"],secondary_title_color,primary_title_color)

    resume_output = BytesIO()
    resume_doc.save('sample_resume.docx')

################# Cover Letter ########################
    cover_letter_doc = Document()
    cover_letter_section = cover_letter_doc.sections[0]
    cover_letter_section.top_margin = Inches(0.5)
    cover_letter_section.bottom_margin = Inches(0.5)
    cover_letter_section.left_margin = Inches(0.5)
    cover_letter_section.right_margin = Inches(0.5)
    cover_letter_margin = cover_letter_section.page_width - cover_letter_section.right_margin - cover_letter_section.left_margin
    # Top line
    rg.add_custom_paragraph(resume_doc,margin,enter_name, enter_location, primary_title_color, True, font_size1=16)
    # Add the second line with a horizontal line beneath it
    rg.add_custom_paragraph(resume_doc,margin,enter_linkedin, f"{enter_phone} | {enter_email}", add_line=True,font_size1=10)

    cover_letter_output = BytesIO()
    cover_letter_doc.save(resume_output)

################ Interview Questions #################

############### Download Files #######################
    st.download_button(
        label='Download Resume',
        data=resume_output.getvalue(), 
        file_name=f'{enter_name} - {company_name} - {job_title} resume.docx', 
        mime='docx'
        )