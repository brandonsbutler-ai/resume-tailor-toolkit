"""Per-job tailorings. Each entry may override the SUMMARY and the SKILLS grid to speak a
specific posting's language. It CANNOT add experience or credentials -- those live only in
candidate.py, so a tailoring can reframe emphasis but can never fabricate.

Add one entry per target role. Keep skill labels short (the resume generator fails loudly on
an overflowing grid cell). The cover-letter text is where you name honest gaps.
"""

TAILORINGS = {
    # --- Example 1: a cloud-security-forward reframing -------------------------------------
    "cloud_security": {
        "job_title": "Cloud Security Engineer",
        "company": "Example Cloud Co.",
        "summary": (
            "Cloud security engineer with 12 years securing production systems, focused on AWS and "
            "GCP: identity and least privilege, infrastructure-as-code guardrails, Kubernetes "
            "security, and detection engineering. Builds the paved road so other teams ship "
            "securely by default, and owns a problem from threat model to shipped fix."
        ),
        "skills": [
            ["Cloud Security (AWS/GCP)", "Identity & Access Mgmt", "Kubernetes Security", "IaC (Terraform)"],
            ["Secure SDLC / CI-CD", "Detection Engineering", "Python / Go", "Zero Trust"],
            ["Threat Modeling", "Security Automation", "SIEM / Log Pipelines", "Incident Response"],
            ["Least Privilege", "Secrets Management", "Code Review", "NIST / SOC 2 / PCI"],
        ],
        # cover-letter body: lead on the match, then name gaps honestly.
        "cover": [
            "Your posting centers on cloud identity and infrastructure-as-code guardrails, which is "
            "the core of what I do. At Northwind Financial I own the paved-road SDK 40+ services "
            "adopt, the CI guardrails that block insecure merges by default, and least-privilege "
            "boundaries across our AWS accounts with automated access reviews and short-lived "
            "credentials.",
            "The detection side is real too: I authored SIEM rules for credential abuse and "
            "exfiltration patterns, tuned for low false positives, so the guardrails have eyes "
            "behind them.",
            "Straight with you on the gaps: my Kubernetes security is production-grade but not "
            "multi-cluster service-mesh depth, and my IaC is Terraform rather than Pulumi. Both are "
            "a short ramp, not a rebuild.",
        ],
    },

    # --- Example 2: an application-security / product-security reframing -------------------
    "product_security": {
        "job_title": "Product Security Engineer",
        "company": "Example Product Co.",
        "summary": (
            "Product security engineer with 12 years owning application security end to end: threat "
            "modeling, secure code review, and CI guardrails that make secure the default. Ships "
            "reference implementations and paved-road tooling teams actually adopt, across "
            "regulated payments and healthcare systems."
        ),
        "skills": [
            ["Application Security", "Threat Modeling", "Secure SDLC / CI-CD", "Code Review"],
            ["SAST / SCA / Secrets", "Python / Go / TypeScript", "Paved-Road Tooling", "IAM"],
            ["Cloud Security (AWS/GCP)", "Detection Engineering", "Incident Response", "Security Automation"],
            ["NIST / SOC 2 / PCI", "Zero Trust", "Mentorship", "Kubernetes Security"],
        ],
        "cover": [
            "Your role is application security owned end to end, which is exactly the program I run "
            "at Northwind Financial: threat modeling, secure code review, a paved-road SDK adopted "
            "by 40+ services, and CI guardrails (SAST, dependency and secret scanning) that block "
            "insecure merges by default.",
            "I care about adoption, not findings volume -- guardrails that developers keep on "
            "because they're fast and low-noise beat a scanner nobody reads.",
            "Honest gap: my background is defensive and platform security, not full-time offensive "
            "research, so deep exploit development would be a ramp.",
        ],
    },
}
