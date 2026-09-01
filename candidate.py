"""Single source of truth. Everything on a generated resume traces back to this file.

Replace the SAMPLE data below (a fictional candidate, "Alex Morgan") with your own real
history. The one rule that makes this toolkit worth using: if a fact is not in this file, it
does not go on the resume -- tailorings (tailorings.py) may reframe the SUMMARY and SKILLS,
never add experience or credentials.

NEVER_CLAIM is the teeth: list credentials/claims you do NOT hold, and verify.py will fail the
build if any of them appear on a generated PDF.
"""

HEADER = {
    "name": "Alex Morgan",
    "contact": "Austin, TX  |  alex.morgan@example.com  |  United States (remote)",
    # cover-letter contact block (city on its own line)
    "city": "Austin, TX",
    "email": "alex.morgan@example.com",
}

SUMMARY = (
    "Security engineer with 12 years building and defending production systems: application and "
    "cloud security, identity and access management, and detection engineering across regulated "
    "industries. Ships tooling that makes secure the default -- guardrails, automated checks, and "
    "reference implementations other teams can adopt. Comfortable owning a problem from threat "
    "model to shipped fix."
)

# 4 rows x 4 columns. Keep each label short; generate_resume.py fails loudly if one overflows.
SKILLS = [
    ["Application Security", "Cloud Security (AWS/GCP)", "Identity & Access Mgmt", "Detection Engineering"],
    ["Threat Modeling", "Secure SDLC / CI-CD", "Python / Go / TypeScript", "IaC (Terraform)"],
    ["Kubernetes Security", "SIEM / Log Pipelines", "Incident Response", "Security Automation"],
    ["NIST / SOC 2 / PCI", "Zero Trust / Segmentation", "Code Review", "Mentorship"],
]

# (company_location, dates, title_or_None, blocks)
# block = ("para", text) | ("sub", heading) | ("bul", text) | ("used", text)
EXPERIENCE = [
    ("Northwind Financial -- Austin, TX", "2021 - Present", "Senior Security Engineer", [
        ("bul", "Led the application-security program for a payments platform: threat modeling, secure code review, and a paved-road SDK adopted by 40+ services"),
        ("bul", "Built CI guardrails (SAST, dependency and secret scanning) that block insecure merges by default, cutting critical findings reaching production by a large margin"),
        ("bul", "Designed IAM and least-privilege boundaries across AWS accounts; automated access reviews and short-lived credentials"),
        ("bul", "Stood up detection engineering on a SIEM: authored rules for credential abuse and data-exfiltration patterns with tested, low-false-positive alerts"),
        ("used", "Used: Python, Terraform, AWS, GitHub Actions, Semgrep, a SIEM, Kubernetes"),
    ]),
    ("Cedar Health Systems -- Remote", "2017 - 2021", "Security Engineer", [
        ("bul", "Hardened a HIPAA-regulated data platform: network segmentation, encryption in transit and at rest, and audit logging mapped to control requirements"),
        ("bul", "Wrote remediation automation for Windows and Linux fleets and a verification pass that re-checked each fix"),
        ("bul", "Ran incident response for suspected data-access events; produced the timeline and the post-incident control changes"),
        ("used", "Used: Go, Ansible, GCP, Elastic, PowerShell"),
    ]),
    ("Basecamp Retail -- Dallas, TX", "2013 - 2017", "Systems / Security Administrator", [
        ("bul", "Managed identity, endpoint, and PCI-scoped systems for a mid-size retailer; ran the annual PCI DSS assessment support"),
        ("bul", "Automated patching and configuration baselines; reduced manual toil and drift across the fleet"),
    ]),
]

CERTS = "CompTIA Security+ | AWS Certified Security - Specialty"
EDU = "B.S. Computer Science -- State University (2013)"

# --- the honesty gate's blocklist ---------------------------------------------------------
# Credentials / claims this candidate does NOT hold. verify.py fails if any appear on a PDF.
# (For the sample candidate, these are examples. Set them to YOUR real non-credentials.)
NEVER_CLAIM = ["CISSP", "CISM", "OSCP", "CCSP", "GIAC", "PhD", "20 years", "25 years"]
