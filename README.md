# Springer Nature – Data Engineer Home Assessment

## 📌 Problem Understanding
The task simulates a **real peer-review workflow**. The goal was to:
1. Build a **preselection dataset** of reviewer invitations for accepted manuscripts in two journals.
2. Use this dataset to answer two analysis questions:
   - **Case A**: Number of completed reviews per revision round (from 2020 onwards).
   - **Case B**: Average time (in days) from reviewer invitation to the first completed review (from 2023 onwards).


## 📂 Approach
### 1. PreSelection (common base)
- Joined the **journal**, **manuscript**, and **reviewer** tables.
- Filtered to:
  - `journal_title` in *["Journal of Economic Structures", "Zoological Letters"]*
  - `site_status = Live`
  - `final_peer_review_decision = Accept`
- Returned **all reviewer columns**, enriched with `journal_title`, `submission_date`, and `final_peer_review_decision`.

### 2. Case A
- Used PreSelection.
- Extracted submission year.
- Counted completed reviews (`COUNTIF(completed)`).
- Grouped by `(submission_year, journal_title, revision_round)`.
- Restricted to `submission_year >= 2020`.

### 3. Case B
- Used PreSelection.
- For each manuscript + revision round:
  - Calculated review duration (`TIMESTAMP_DIFF(stop, start, DAY)`).
  - Picked the **earliest completed review** with `ROW_NUMBER()`.
- Averaged those durations per `(submission_year, journal_title, revision_round)`.
- Restricted to `submission_year >= 2023`.

---

## ✅ Deliverables
- `preselection.sql` → Reviewer invitations dataset.  
- `case_a.sql` → Completed reviews per round, 2020+.  
- `case_b.sql` → Avg days to first review completion, 2023+.  





