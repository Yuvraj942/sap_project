-- Base table for analytical processing (adapt datatypes to your SAP HANA schema)
CREATE COLUMN TABLE p2p_transactions (
    transaction_id NVARCHAR(20),
    company_code NVARCHAR(10),
    plant NVARCHAR(10),
    vendor_id NVARCHAR(20),
    material_id NVARCHAR(30),
    pr_no NVARCHAR(20),
    pr_date DATE,
    po_no NVARCHAR(20),
    po_date DATE,
    gr_doc_no NVARCHAR(20),
    gr_date DATE,
    invoice_doc_no NVARCHAR(20),
    invoice_date DATE,
    payment_doc_no NVARCHAR(20),
    payment_date DATE,
    currency NVARCHAR(5),
    po_value DECIMAL(15,2),
    invoice_amount DECIMAL(15,2),
    variance_amount DECIMAL(15,2),
    received_qty DECIMAL(15,3),
    on_time_flag INTEGER
);

-- Stage-level cycle time view
CREATE OR REPLACE VIEW vw_p2p_cycle_time AS
SELECT
    transaction_id,
    company_code,
    plant,
    vendor_id,
    material_id,
    DAYS_BETWEEN(pr_date, po_date) AS pr_to_po_days,
    DAYS_BETWEEN(po_date, gr_date) AS po_to_gr_days,
    DAYS_BETWEEN(gr_date, invoice_date) AS gr_to_invoice_days,
    DAYS_BETWEEN(invoice_date, payment_date) AS invoice_to_payment_days,
    po_value,
    invoice_amount,
    variance_amount,
    on_time_flag
FROM p2p_transactions;

-- Vendor-level KPI summary
CREATE OR REPLACE VIEW vw_vendor_kpi_summary AS
SELECT
    vendor_id,
    COUNT(*) AS total_transactions,
    SUM(po_value) AS total_po_value,
    SUM(invoice_amount) AS total_invoice_amount,
    AVG(DAYS_BETWEEN(pr_date, po_date)) AS avg_pr_to_po_days,
    AVG(DAYS_BETWEEN(po_date, gr_date)) AS avg_po_to_gr_days,
    AVG(DAYS_BETWEEN(gr_date, invoice_date)) AS avg_gr_to_invoice_days,
    AVG(DAYS_BETWEEN(invoice_date, payment_date)) AS avg_invoice_to_payment_days,
    SUM(on_time_flag) * 100.0 / NULLIF(COUNT(*), 0) AS on_time_rate_pct,
    SUM(variance_amount) AS total_variance
FROM p2p_transactions
GROUP BY vendor_id;

-- Monthly procurement and liability summary
CREATE OR REPLACE VIEW vw_monthly_procurement_summary AS
SELECT
    TO_VARCHAR(po_date, 'YYYY-MM') AS month_key,
    SUM(po_value) AS monthly_po_value,
    SUM(invoice_amount) AS monthly_invoice_value,
    SUM(CASE WHEN payment_date IS NULL THEN invoice_amount ELSE 0 END) AS open_liability,
    AVG(DAYS_BETWEEN(pr_date, po_date)) AS avg_pr_to_po_days,
    AVG(DAYS_BETWEEN(po_date, gr_date)) AS avg_po_to_gr_days
FROM p2p_transactions
GROUP BY TO_VARCHAR(po_date, 'YYYY-MM');
