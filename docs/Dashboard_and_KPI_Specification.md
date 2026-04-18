# Dashboard and KPI Specification

## Candidate Details
- Name: Yuvraj Singh
- Roll Number: 23051883
- Batch/Program: 2023-27 BTech CSE | SAP Course Program: 2026 SAP Data Analytics Engineer

## 1. Dashboard Objective
To provide procurement and finance stakeholders a single view of P2P cycle health, vendor performance, and liability movement.

## 2. Target Users
- Procurement Manager
- Purchase Executive
- Finance Controller
- Leadership/Operations Head

## 3. KPI Cards (Top Section)
1. Total Purchase Value (Current Period)
2. Open PO Value
3. Average PR-to-PO Days
4. Average PO-to-GR Days
5. Average Invoice-to-Payment Days
6. Vendor On-Time Delivery Rate

## 4. Visuals (Middle and Bottom)
1. Monthly Spend Trend (Line chart)
2. Vendor-wise Spend (Bar chart)
3. Cycle Time Breakdown by Stage (Stacked bar)
4. Invoice Variance Distribution (Histogram)
5. Plant-wise Procurement Performance (Map/Table)
6. Open Liabilities Aging (Matrix)

## 5. Filters/Slicers
- Date range
- Company code
- Plant
- Vendor
- Material group
- Purchasing group

## 6. Data Model Entities
- dim_vendor
- dim_material
- dim_organization
- dim_date
- fact_p2p_transactions
- fact_invoice_payment

## 7. Business Rules
1. Any cycle time < 0 is data quality error
2. Open PO means PO created but no complete GR
3. Open liability means invoice posted and payment pending
4. Variance threshold alert at +/- 5%

## 8. Recommended Dashboard Layout
- Row 1: KPI cards (6)
- Row 2: Spend trend + vendor ranking
- Row 3: cycle times + variance analysis
- Row 4: open liability aging table with conditional formatting

