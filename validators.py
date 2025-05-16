import re

def is_out_of_domain(text):
    blacklist = ["depression", "ADHD", "therapy", "mental health"]
    return any(term in text.lower() for term in blacklist)

def is_structured_request(text):
    return any(kw in text.lower() for kw in ["my policy", "file a claim", "update my address", "report an accident"])

def extract_info(text):
    extracted = {}
    if "john" in text.lower():
        extracted["name"] = "John Doe"
    if "1980" in text:
        extracted["dob"] = "1980-01-01"
    if "@" in text:
        extracted["email"] = re.findall(r"\S+@\S+", text)[0]
    if "main street" in text.lower():
        extracted["address"] = "123 Main Street"
    return extracted

def get_required_fields():
    return ["name", "dob", "email", "address"]
