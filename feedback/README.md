# Feedback

This folder stores doctor review output and clinic feedback before it becomes approved RAG content.

Flow:

```text
01_incoming_doctor_reviews
        ↓
02_triaged_questions
        ↓
03_approved_clinic_qa
        ↓
data content lanes
```

## File Naming

All feedback files must start with a date:

```text
YYYY_MM_DD_topic_short_description[_status_or_version].md
```

Example:

```text
2026_06_27_doctor_chat_review_initial.md
```
