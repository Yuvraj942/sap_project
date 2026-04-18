# Test Cases and Validation

## Test Case Table

| TC_ID | Scenario | Input Condition | Expected Result | Status |
|---|---|---|---|---|
| TC01 | PR Creation | Valid material, quantity, plant | PR number generated | Pass/Fail |
| TC02 | PR to PO Conversion | Approved PR exists | PO created with correct reference | Pass/Fail |
| TC03 | Goods Receipt | PO open quantity available | GR posted, stock updated | Pass/Fail |
| TC04 | Invoice Verification | Valid PO/GR reference | Invoice posted with accounting doc | Pass/Fail |
| TC05 | Payment Run | Due invoice available | Payment doc posted and vendor open item cleared | Pass/Fail |
| TC06 | Cycle Time KPI | Complete process records | All KPI durations non-negative | Pass/Fail |
| TC07 | Vendor Spend KPI | Multiple PO lines for same vendor | Correct aggregated spend in report | Pass/Fail |
| TC08 | Variance KPI | Invoice differs from PO value | Variance % correctly calculated | Pass/Fail |

## Data Quality Checks
1. No null document numbers in fact tables
2. Date sequence integrity maintained
3. Duplicate transaction IDs removed
4. Currency fields standardized

## Validation Summary
- Process flow validated end-to-end
- Evidence captured for each major stage
- KPI values reconciled with source records
- Final PDF and ZIP generated
