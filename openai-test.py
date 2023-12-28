import os
from openai import OpenAI, api_key
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()

resume_text = ""
with open("recognized.txt", "r", encoding="utf-8") as file:
    for line in file:
        resume_text += line

job_requirement = """{"Position":"Manufacturing Engineer", "Tasks & Responsibilities":["Responsible for collecting and reviewing production data from production cells to ensure implemented process improvements are sustained.", "Identify and support production quality processes and procedures to increase production throughput and eliminate impact to the customer.", "Participate, lead and facilitate kaizen events to improve internal LEAN manufacturing (ABS) processes to increase production's efficiency and quality.", "Train production operators on lean principles and manufacturing processes to increase production's efficiency and quality.",  "Lean Cell Design.", "Work with Cross-Functional teams in the planning and designing of new products to ensure their manufacturability.", "Research and review industry trends and technological advancements for products and processes."], "Minimum Education":"Bachelor of Engineering", "Skills and Experience Required":["Bachelor's Degree in Mechanical, Electrical or Industrial Engineering or Engineering Technology Degree required", "1 to 5 years experience in manufacturing", "Experience and Foundational Knowledge of Lean Principles, Lean Cell Design, and demonstrated ability in continuous improvement", "Knowledge of engineering concepts and principles - Design for Manufacturability, Failure Mode and Effects Analysis,  Design/Process Control Methods", "Proficient Computer and Analytical Skills"]}"""

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": """
            Disregarding previous information. You are the human resources manager, and you are given the resume (text) and job requirements (JSON). 
            You need to view the resume, and output the infomation in following json format: 
            {"Applicant":"(Applicant's Name)", "Email":"(Applicant's email)", "Phone":"(phone number)", "links":[{"(link1)":"(url1)"}, {"(link2)":"(url2)"}, ...], "Position": "(mostly described job position)", "Major": "(Highest degree major) ", "Skill Match Score": (1-10), "Experience Score": (1 -10), "Interview Questions": [(Question 1), (Question 2), ...]}. 
            First, for "Applicant", "Email", "Phone", "links", "Position", "Major", extract the applicant's name, email, phone number and related websites (possibly multiple) from the resume, and if there is any lack of value of any key, store "None" in the value. 
            Second, for "Match skill Score", "Experience Score", check whether the applicant meets the given job requirements based on the resume. For "Skill Match Score" and "Experience Score", check whether the applicant meets the skills, experience requirements, you scores these aspect of the applicant (1-10).
            Last, for "Interview Questions", generate some questions that can be asked during the interview based on the information in the resume.
        """}, 

        {"role": "user", "content": f"""
            Job Requirement:
            {job_requirement}
            Resume text:
            {resume_text}
        """}
    ],
    temperature=1,
    max_tokens=2000,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
)

# print(response)
# print("====================")

# print(response.choices[0])
print("====================")

print(response.choices[0].message.content)
# print("====================")

# print(type(response.choices[0].message.content))
# print("====================")

# {"Position": "Manufacturing Engineer", "Same position": "Yes", "Skill matching score": 8, "Experience score": 7, "Interview questions": ["Can you provide examples of process improvements you have implemented in your previous roles?", "Tell me about your experience with lean principles and continuous improvement.", "Have you worked on any projects involving Design for Manufacturability?", "How proficient are you in using AutoCAD?"]}
# {"Position": "Manufacturing Engineer", "Same position": "No", "Skill matching score": 5, "Experience score": 3, "Interview questions": ["Can you explain your experience with Lean Principles and Lean Cell Design?", "Have you worked on implementing process improvements in a manufacturing setting?", "Can you provide an example of a time when you trained production operators on lean principles and manufacturing processes?", "How familiar are you with engineering concepts such as Design for Manufacturability and Failure Mode and Effects Analysis?"]}