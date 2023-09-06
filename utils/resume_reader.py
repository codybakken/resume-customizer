import json

def resume_opener(json_file):
    data = json.load(json_file)
    return data

def format_resume_as_str(experience_data):
    result = ""
    for company in experience_data['experience']:
        result += f"{company['company_name']}\n{company['location']}\n{company['years']}\n"
        
        if 'summary' in company:
            result += f"{company['summary']}\n"
        
        for role in company['roles']:
            result += f"\n{role['title']}\n{role['dates']}\n - " + '\n - '.join(role['accomplishments']) + "\n"
        
        result += "\n"
    
    return result



