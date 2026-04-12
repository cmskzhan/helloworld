---
name: cv-template
description: "Use when: generating CV, resume, tailored CV, CV template, resume format, professional CV layout, CV structure, CV markdown format. Provides a professional CV markdown template with consistent section ordering, formatting conventions, and a complete example."
---

# Professional CV Template

This skill defines the standard markdown format for generating professional CVs. All AI-generated CVs should follow this structure for consistent, beautiful PDF output.

## Template Structure

```markdown
# FULL NAME

**Email** | **Phone** | **Location** | **LinkedIn** | **GitHub**

## Professional Summary

2-3 sentence summary highlighting key expertise, leadership experience and career focus. Tailor to the target role.

## Technical Skills

**Languages:** Python, SQL, Shell Scripting

**AI & Data Science:** LLM prompt engineering, data analysis, machine learning basics

**Cloud & Infrastructure:** AWS (EC2, S3, Lambda, DynamoDB), Docker, Kubernetes, Terraform

**Monitoring & Observability:** Prometheus, Grafana, Datadog, ELK Stack

**Databases:** PostgreSQL, DynamoDB, Redis

**Tools & Practices:** CI/CD, Git, Locust, REST APIs, GraphQL

## Work Experience

**Job Title** | Company Name | Location | Start Date - End Date

- Achievement-oriented bullet point with measurable impact
- Led/designed/built [X] resulting in [Y] improvement
- Reduced/increased [metric] by [X]% through [action]

**Job Title** | Company Name | Location | Start Date - End Date

- Achievement-oriented bullet point
- Technical accomplishment with specific technologies
- Leadership or mentoring achievement

## Education

**Degree Name** | Institution | Location | Start Date - End Date

- Notable achievement, thesis topic, or relevant coursework (optional)

## Certifications

- AWS Certified Solutions Architect - Associate (2023)
- Certified Kubernetes Administrator (CKA) (2022)

## Projects

**Project Name** | Brief description

- Key technical achievement or outcome
- Technologies used: Python, AWS Lambda, DynamoDB

## Publications & Awards (Optional)

- Award Name — Issuing Organization (Year)
- Publication Title — Journal/Conference (Year)
```

## Formatting Conventions

### Contact Header (Line 3)
- Single line with `**Label** | Value` format
- Omit fields that are empty/unknown
- Use ` | ` (space-pipe-space) as separator

### Section Headers
- Use `## ` (H2) for all main sections
- Sections in order: Summary → Experience → Education → Skills → Certifications → Projects → Publications/Awards
- Omit empty sections entirely

### Work Experience Entries
- Header line: `**Job Title** | Company Name | Location | Start Date - End Date`
- Use `- ` for bullet points (not `* `)
- Each bullet: 1-2 lines max, start with action verb
- Focus on achievements, not just responsibilities
- Include metrics where possible (%, $, time saved)

### Education Entries
- Header line: `**Degree Name** | Institution | Location | Start Date - End Date`
- Optional bullet for thesis, honors, or relevant coursework

### Skills Section
- Category in bold, followed by colon and comma-separated list
- One category per line
- Common categories: Languages, Cloud & Infrastructure, Monitoring & Observability, Databases, Tools & Practices, Frameworks, Soft Skills
- Sort items within each category alphabetically

### Certifications
- Bullet list with format: `- Certification Name — Issuing Organization (Year)`

### Projects
- Header line: `**Project Name** | Brief description`
- Bullets for achievements and technologies used

## Anti-Patterns to Avoid

- ❌ Don't use `### ` (H3) headers — the renderer handles job/education headers via the `**Title** | Company` pattern
- ❌ Don't use markdown tables — they don't render well in the PDF
- ❌ Don't use horizontal rules (`---`) — the renderer adds section dividers automatically
- ❌ Don't use inline code blocks (backticks) — use bold for emphasis instead
- ❌ Don't mix bullet styles — always use `- ` consistently
- ❌ Don't include photos, graphics, or images
- ❌ Don't use more than 2-3 sentences in the summary
- ❌ Don't list every single responsibility — focus on top 4-6 achievements per role

## Example: Complete CV

```markdown
# Kai Zhang

**Email** | kaizhang@hotmail.com | **Phone** | +44-07460959753 | **Location** | Woking, Surrey, UK | **LinkedIn** | linkedin.com/in/kai-zhang-93488414

## Professional Summary

Principal Site Reliability Engineer with 20+ years of experience designing and operating mission-critical systems in financial services and technology. Expert in AWS cloud infrastructure, Kubernetes orchestration, and building observability platforms that minimize MTTD/MTTR. Proven track record of leading global teams, automating complex workflows, and delivering high-availability solutions for trading platforms serving millions of users.

## Technical Skills

**Languages:** Python, Bash, SQL, Shell Scripting

**Cloud & Infrastructure:** AWS (EC2, S3, Lambda, DynamoDB), Docker, Kubernetes, Terraform, Puppet

**Monitoring & Observability:** Prometheus, Grafana, Datadog, ELK Stack, SLO/SLI Frameworks

**Databases:** PostgreSQL, DynamoDB, Redis

**Tools & Practices:** CI/CD, Git, Locust, REST APIs, GraphQL, Perforce, FIX Protocol

**Operating Systems:** Linux, Unix, Solaris, Windows Server

## Work Experience

**Principal Site Reliability Engineer** | Vanguard, International Systems and Technologies | UK | Jan 2021 - Present

- Designed and implemented availability and latency detection tools, reducing MTTD by 40% for AWS-hosted applications
- Developed a custom LLM prompt engineering framework for incident response automation, improving MTTR times by 30%
- Developed comprehensive monitoring dashboards using Grafana and Prometheus, improving operational visibility across 50+ services
- Led European branch of a global SRE team of 5 engineers supporting 24/7 operations across UK, US, and Australia
- Established SLO/SLI frameworks for mission-critical products, enabling data-driven reliability targets
- Built Python automation scripts for data reconciliation across DynamoDB and GraphQL backends
- Led multi-region disaster recovery test projects, ensuring business continuity across UK, US, and Australia
- Supervised performance testing against REST APIs and GraphQL using Locust, identifying critical bottlenecks
- Chaired developer experience forums, improving self-service portal adoption by 60%

**Senior System Specialist** | NASDAQ International, Market Technology | UK | Feb 2016 - Jan 2021

- Designed and deployed on-prem multi-master Kubernetes cluster for market surveillance platform
- Developed Puppet modules and Hiera configurations for automated server build and configuration management
- Built PostgreSQL database cluster conforming to NASDAQ infosec standards
- Acted as deputy Technical Operations Manager, achieving SOC2 compliance for integrated production systems
- Supported hybrid Linux/Windows Docker container platform for buyside surveillance software

**Technical Service Delivery Engineer** | Fidessa PLC, Hosted Exchange and Ticker Plant Division | UK | Oct 2013 - Feb 2016

- Implemented Ticker Plant systems across European Unix/Linux platforms with automated weekend release processes
- Led end-to-end network testing, connectivity verification, and ACL/NAT troubleshooting
- Coordinated network and hardware changes with regional data centers for exchange DR tests
- Technical lead for client change requests and project delivery

## Education

**MPhil Computer Science** | University Institution | UK | Sep 2000 - Jun 2004


## Certifications

- AWS Certified Solutions Architect - Associate

## Projects

**Availability Detection Platform** | Real-time monitoring system for Vanguard application health

- Built Python-based detection tools integrating with AWS CloudWatch and custom metrics
- Reduced incident response time through automated alerting and dashboard creation

**Multi-Region DR Framework** | Automated disaster recovery testing across AWS regions

- Orchestrated failover tests across UK, US, and Australia availability zones
- Documented runbooks and automated validation checks
```

## Usage Notes

When generating a tailored CV:
1. Follow the section order defined above
2. Use the `**Title** | Company | Location | Dates` pattern for all experience and education entries
3. Keep bullets achievement-oriented with measurable outcomes
4. Tailor the Professional Summary to match the target job description
5. Prioritize skills and experiences that match the JD keywords
6. Omit sections that have no content (don't include empty sections)
