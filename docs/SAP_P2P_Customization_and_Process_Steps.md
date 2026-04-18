# SAP P2P Customization and Process Steps

## 1. Objective
To design and validate an end-to-end Procure-to-Pay process in SAP and prepare analytics checkpoints for Data Analytics Engineer reporting.

## 2. Customization Blueprint (High-Level)

### 2.1 Enterprise Structure and Assignment
1. Define company and company code
2. Define plant and storage location
3. Define purchasing organization and purchasing group
4. Assign purchasing organization to company code and plant
5. Configure valuation area and account determination basics

### 2.2 Master Data Preparation
1. Create vendor master (general, company code, purchasing data)
2. Create material master (basic, purchasing, accounting views)
3. Define material group and purchasing info records
4. Maintain source list

### 2.3 Procurement Configuration Highlights
1. Document types for PR and PO
2. Release strategy for approval simulation
3. Pricing procedure and condition records
4. Tolerance limits for invoice verification
5. Automatic account determination (OBYC checkpoints)

## 3. End-to-End Execution Steps

### Step 1: Create Purchase Requisition (PR)
- Transaction: ME51N
- Inputs: Material, quantity, plant, delivery date
- Output: PR number generated
- Analytics log fields:
  - pr_no
  - pr_date
  - requested_qty
  - requester

### Step 2: Convert PR to Purchase Order (PO)
- Transaction: ME21N
- Reference PR and assign vendor
- Validate price and delivery terms
- Save PO number
- Analytics log fields:
  - po_no
  - po_date
  - vendor_id
  - net_order_value

### Step 3: Post Goods Receipt (GR)
- Transaction: MIGO
- Reference PO and post received quantity
- Verify movement type and storage location
- Analytics log fields:
  - gr_doc_no
  - gr_date
  - received_qty
  - accepted_qty

### Step 4: Perform Invoice Verification
- Transaction: MIRO
- Reference PO/GR
- Post invoice and verify tax/amount
- Analytics log fields:
  - invoice_doc_no
  - invoice_date
  - invoice_amount
  - variance_amount

### Step 5: Execute Vendor Payment
- Transaction: F110 (or simulation flow)
- Select due invoices and run payment proposal
- Post payment run
- Analytics log fields:
  - payment_doc_no
  - payment_date
  - paid_amount
  - payment_method

## 4. FI Integration Posting Logic (Conceptual)
1. GR Posting:
- Dr Inventory/Consumption
- Cr GR/IR Clearing

2. Invoice Posting:
- Dr GR/IR Clearing
- Cr Vendor Liability

3. Payment Posting:
- Dr Vendor Liability
- Cr Bank/Cash

## 5. KPI Model Mapping
1. PR to PO Conversion Time = po_date - pr_date
2. PO to GR Lead Time = gr_date - po_date
3. GR to Invoice Lag = invoice_date - gr_date
4. Invoice to Payment Lag = payment_date - invoice_date
5. Vendor On-Time Rate = on_time_receipts / total_receipts
6. Spend by Vendor = sum(net_order_value)
7. Price Variance % = variance_amount / invoice_amount * 100

## 6. Validation Checks
1. PR created and linked to PO
2. PO quantity equals or exceeds approved PR quantity
3. GR quantity reconciliation with PO
4. Invoice reference available for GR/PO
5. Payment posted against invoice
6. No negative cycle time across process checkpoints

## 7. Deliverables from This Document
- Customization roadmap
- Execution evidence sequence
- KPI extraction points
- Process narration for project evaluation
