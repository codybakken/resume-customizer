
import openai

def summary_prompt(resume,job_title,company_name,job_description):
    summary_prompt_txt = f"""Here is my resume:{resume} 
    here is a job description for a {job_title} at {company_name}: {job_description}
    Can you write a a one sentence summary, then follow with a sentence in this format: Seeking a [job title] position at [company name], 
    where I bring my managerial and organisational skills to support your mission of [company mission statement, from their website]."""
    return summary_prompt_txt



def strength_prompt(resume, job_description):
    strength_prompt_txt = f"""here is my resume:
    {resume}

    here is a job description: 
    {job_description}
    
    
    based on my resume and the job description, What 4 technical skills should I highlight based on my resume and the job description? Please select one bullet from my resume that shows that strength.

    return the result as a python list like this:
    ['''<strength>: <text from bullet point>''','''<strength>: <text from bullet point>''']
    """
    return strength_prompt_txt

def cover_letter_prompt(resume,job_description,):
    cover_letter_prompt_txt = f"""Here is my resume: {resume}
    here is the job description: {job_description}
    write a cover letter based on my resume and the job description that tells a story about my career and positions my for the position in 4 short paragraphs and then include sections in this format:
    Please see below two recent key achievements that show how I can support your team [appropriate bullets from my resume]:
    -
    -

    What I have been enjoying the most along my path, has been the pleasure of breaking down a problem and build up from its core: identifying needs, researching, figuring out solutions, documenting, and always integrating novelty into their solutions’ engineering.


    Particularly, I was intrigued by [company] emphasis on [job description requirement]. I believe our ideas align with regard to [x job description value] and I resonate with your value of [x company value]. I would love to learn more about the role’s specifics and discuss further our collaboration. 

    Looking forward to hearing from you!
    Best Regards,
    Cody Bakken
    """
    return cover_letter_prompt_txt

def boss(job_description):
    return f"""Does the job decription mention who this position reports to?
    {job_description}

    if the job description does mention the hiring manager, return the person's title.
    """

def key_words(resume,job_description):
    return f"""
    resume: 
    {resume}

    job description:
    {job_description}
    
    What are the top 3 key words to include in the headline of my resume based on the job description?

    return the results in this format in title case: Competency | Competency | Competency
    """

def sample_interview_questions(job_description):
    prompt_txt = f"""Based on this job description: {job_description} generate 10 sample interview questions
    return the response like this:
    
    ['''question''','''question''','''question''','''question''']
    """
    return prompt_txt

def sample_interview_responses(resume,question):
    prompt_txt = f"""
    my resume:
    resume start
    {resume}
    resume end

    Please write a sample response to his question: 
    {question} 
    """
    return prompt_txt

def tell_me_about_yourself(resume,job_description):
    prompt_txt = f"""
    my resume:
    resume start
    {resume}
    resume end

    job description:
    job description start 
    {job_description} 
    job description end

    based on my resume and the job description write a one paragraph response to the question 'Tell my about yourself'
    """
    return prompt_txt

def reword_resume(kc, job_description):
    kc_text = ''
    for x in kc:
        kc_text += x+'\n'

    return f"""Here is a Job description: {job_description}.
    Here are my key competencies: 
    {kc_text}

    Scan the list of key competencies and choose the best 12 key competencies I should include on my resume based on the job description.

    Return as a python list and each item in title case:
    ['<Key Competencies>','<Key Competencies>']
    """

def add_skills(resume,kc, job_description):
    return f"""Here is a Job description: {job_description}.
    Here are my key competencies: {kc}.
    Here is my resume: {resume}

    Are there other skills I should consider adding to my key competencies and technical competencies lists?
    """

def select_bullets(accomplishments, job_description, bullets):
    # convert list to string
    bullet_text = ''
    for accomplishment in accomplishments:
        bullet_text += accomplishment+'\n'

    return f"""here is the job description:
    {job_description}
    
    here are my accomplishments:
    {bullet_text}
    
    Based on the job description select {bullets} accomplisments from my resume that best show my qualifications for this job.
    Return the response as a python list this: ['''<accomplishment>''','''<accomplishment>''']

    """


def response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k", 
        messages=[
        {"role": "system", "content": "You are an expert resume writer."},
        {"role": "user", "content": prompt}
    ])
    response = response["choices"][0]["message"]["content"]
    return response