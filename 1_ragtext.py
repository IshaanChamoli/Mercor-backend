import json

def format_experience(experiences):
    if not experiences:
        return "No professional experience listed"
    
    exp_list = []
    for exp in experiences:
        exp_list.append(f"{exp['roleName']} at {exp['company']}")
    return "EXPERIENCE: " + "; ".join(exp_list)

def format_education(education):
    if not education.get('degrees'):
        return "No education listed"
    
    edu_list = []
    for deg in education['degrees']:
        if not deg.get('degree'):
            continue
            
        details = []
        if deg.get('subject'):
            details.append(f"in {deg['subject']}")
        if deg.get('originalSchool'):
            details.append(f"from {deg['originalSchool']}")
        if deg.get('startDate') and deg.get('endDate'):
            details.append(f"({deg['startDate']}-{deg['endDate']})")
        if deg.get('gpa'):
            details.append(f"GPA {deg['gpa']}")
            
        edu_str = f"{deg['degree']} {' '.join(details)}"
        edu_list.append(edu_str.strip())
    
    return "EDUCATION: " + "; ".join(edu_list)

def format_skills(skills):
    if not skills:
        return "SKILLS: None listed"
    return "SKILLS: " + ", ".join(skills)

def format_preferences(availability, salary):
    prefs = []
    if availability:
        prefs.append(f"Available for {' and '.join(availability)}")
    if salary and salary.get('full-time'):
        prefs.append(f"Expected salary: {salary['full-time']}")
    return "PREFERENCES: " + "; ".join(prefs)

def create_candidate_summary(candidate):
    sections = [
        f"LOCATION: {candidate['location']}",
        format_experience(candidate['work_experiences']),
        format_education(candidate['education']),
        format_skills(candidate['skills']),
        format_preferences(candidate['work_availability'], candidate['annual_salary_expectation'])
    ]
    return " | ".join(sections)

def transform_candidates(input_file, output_file):
    with open(input_file, 'r') as f:
        candidates = json.load(f)
    
    structured_summaries = []
    for candidate in candidates:
        structured_summaries.append({
            "name": candidate.get('name', ''),
            "email": candidate.get('email', ''),
            "rag_text": create_candidate_summary(candidate)
        })
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(structured_summaries, f, ensure_ascii=False, indent=2)

# Run the transformation
transform_candidates('form-submissions.json', 'candidate_summaries.json') 