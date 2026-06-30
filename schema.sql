-- ============================================================
-- schema.sql
-- FinRelief AI — SQLite Database Schema
-- AI Powered Debt Relief and Financial Recovery Platform
-- ============================================================
-- Run this file to create all tables from scratch.
-- Tables are created in dependency order:
--   1. USER           (no dependencies)
--   2. FINANCIAL_DATA (depends on USER)
--   3. AI_ANALYSIS    (depends on FINANCIAL_DATA)
-- ============================================================

-- Drop tables in reverse dependency order before recreating
DROP TABLE IF EXISTS AI_ANALYSIS;
DROP TABLE IF EXISTS FINANCIAL_DATA;
DROP TABLE IF EXISTS USER;

-- ============================================================
-- TABLE 1: USER
-- Stores login credentials for every registered user.
-- This is the root table — all other tables trace back to it.
-- ============================================================

CREATE TABLE USER (
    user_id   INTEGER      PRIMARY KEY AUTOINCREMENT,
    username  VARCHAR(100) NOT NULL UNIQUE,
    password  VARCHAR(255) NOT NULL
);

-- ============================================================
-- TABLE 2: FINANCIAL_DATA
-- Stores each financial submission made by a user.
-- One user can have many financial records (One-to-Many).
-- Linked to USER via user_id Foreign Key.
-- ============================================================

CREATE TABLE FINANCIAL_DATA (
    finance_id      INTEGER      PRIMARY KEY AUTOINCREMENT,
    user_id         INTEGER      NOT NULL,
    income          DECIMAL(15,2) NOT NULL,
    debt            DECIMAL(15,2) NOT NULL,
    expenses        DECIMAL(15,2) NOT NULL,
    financial_score DECIMAL(5,2)  DEFAULT 0.00,

    CONSTRAINT fk_financial_user
        FOREIGN KEY (user_id)
        REFERENCES USER (user_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- ============================================================
-- TABLE 3: AI_ANALYSIS
-- Stores the AI-generated analysis results for each submission.
-- One financial record can have many analysis results (One-to-Many).
-- Linked to FINANCIAL_DATA via finance_id Foreign Key.
-- ============================================================

CREATE TABLE AI_ANALYSIS (
    analysis_id INTEGER      PRIMARY KEY AUTOINCREMENT,
    finance_id  INTEGER      NOT NULL,
    health      VARCHAR(50)  NOT NULL,
    settlement  VARCHAR(100) NOT NULL,
    suggestion  TEXT         NOT NULL,

    CONSTRAINT fk_analysis_financial
        FOREIGN KEY (finance_id)
        REFERENCES FINANCIAL_DATA (finance_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- ============================================================
-- SAMPLE DATA — for testing and demonstration
-- ============================================================

-- Insert sample users (passwords should be hashed in production)
INSERT INTO USER (username, password) VALUES
    ('john_doe',   '$2b$12$samplehashvalue001'),
    ('jane_smith', '$2b$12$samplehashvalue002');

-- Insert sample financial records
INSERT INTO FINANCIAL_DATA (user_id, income, debt, expenses, financial_score) VALUES
    (1, 5000.00, 15000.00, 2500.00, 41.67),
    (1, 5200.00, 14000.00, 2400.00, 48.15),
    (2, 3500.00, 20000.00, 3000.00,  0.00);

-- Insert sample AI analysis results
INSERT INTO AI_ANALYSIS (finance_id, health, settlement, suggestion) VALUES
    (1, 'At Risk',  'Medium Probability', 'Allocate surplus income to highest-interest debt and review monthly subscriptions for cuts.'),
    (2, 'At Risk',  'Medium Probability', 'Income improved slightly — consider a debt consolidation loan to reduce interest burden.'),
    (3, 'Critical', 'Low Probability',    'Expenses exceed income. Seek non-profit credit counseling and prioritize essential bills only.');

-- ============================================================
-- USEFUL QUERIES
-- ============================================================

-- Query 1: Get all financial submissions for a specific user
SELECT
    u.username,
    fd.finance_id,
    fd.income,
    fd.debt,
    fd.expenses,
    fd.financial_score
FROM USER u
JOIN FINANCIAL_DATA fd ON u.user_id = fd.user_id
WHERE u.username = 'john_doe';

-- Query 2: Get the full analysis report for a specific user
SELECT
    u.username,
    fd.income,
    fd.debt,
    fd.expenses,
    fd.financial_score,
    ai.health,
    ai.settlement,
    ai.suggestion
FROM USER u
JOIN FINANCIAL_DATA fd ON u.user_id    = fd.user_id
JOIN AI_ANALYSIS    ai ON fd.finance_id = ai.finance_id
WHERE u.username = 'john_doe';

-- Query 3: Get all Critical health cases across all users
SELECT
    u.username,
    fd.income,
    fd.debt,
    fd.financial_score,
    ai.health,
    ai.settlement,
    ai.suggestion
FROM AI_ANALYSIS    ai
JOIN FINANCIAL_DATA fd ON ai.finance_id = fd.finance_id
JOIN USER           u  ON fd.user_id    = u.user_id
WHERE ai.health = 'Critical';
