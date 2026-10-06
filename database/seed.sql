-- ====================================================================
-- SMART EXPENSE CATEGORY PREDICTION & FINANCIAL ANALYTICS
-- Seed Initial Data for Oracle Database
-- ====================================================================

-- 1. Insert Categories
INSERT INTO CATEGORIES (NAME, DESCRIPTION, COLOR_HEX, ICON_NAME) 
VALUES ('Food', 'Dining out, groceries, food delivery, and cafeteria', '#10B981', 'Utensils');

INSERT INTO CATEGORIES (NAME, DESCRIPTION, COLOR_HEX, ICON_NAME) 
VALUES ('Transportation', 'Cabs, fuel, metro cards, public transit, and parking', '#3B82F6', 'Car');

INSERT INTO CATEGORIES (NAME, DESCRIPTION, COLOR_HEX, ICON_NAME) 
VALUES ('Shopping', 'Clothing, electronics, household items, and retail', '#EC4899', 'ShoppingBag');

INSERT INTO CATEGORIES (NAME, DESCRIPTION, COLOR_HEX, ICON_NAME) 
VALUES ('Entertainment', 'Streaming platforms, movies, games, concerts, outings', '#8B5CF6', 'Film');

INSERT INTO CATEGORIES (NAME, DESCRIPTION, COLOR_HEX, ICON_NAME) 
VALUES ('Utilities', 'Electricity, water, gas cylinder, internet, mobile bills', '#F59E0B', 'Zap');

INSERT INTO CATEGORIES (NAME, DESCRIPTION, COLOR_HEX, ICON_NAME) 
VALUES ('Healthcare', 'Doctor visits, pharmacy, medicines, diagnostics', '#EF4444', 'HeartPulse');

INSERT INTO CATEGORIES (NAME, DESCRIPTION, COLOR_HEX, ICON_NAME) 
VALUES ('Education', 'Tuition, textbooks, online courses, exam fees', '#06B6D4', 'GraduationCap');

INSERT INTO CATEGORIES (NAME, DESCRIPTION, COLOR_HEX, ICON_NAME) 
VALUES ('Other', 'Miscellaneous personal and household expenses', '#6B7280', 'MoreHorizontal');

-- 2. Insert Default Demo User (demo@smartexpense.com / demo123)
-- Password hash: SHA256 of demo123
INSERT INTO USERS (EMAIL, PASSWORD_HASH, FULL_NAME)
VALUES ('demo@smartexpense.com', '62251143a219355966930cb9b7d99407f51262121a5baaa34da3588e8920180c', 'Demo User');

-- 3. Insert Initial Monthly Salary for Demo User (₹50,000)
INSERT INTO INCOME (USER_ID, MONTHLY_INCOME)
VALUES (1, 50000.00);

-- 4. Insert Seed Expenses for Demo User
INSERT INTO EXPENSES (USER_ID, DESCRIPTION, AMOUNT, CATEGORY, PREDICTED_CATEGORY, MERCHANT, PAYMENT_METHOD, EXPENSE_DATE)
VALUES (1, 'Swiggy dinner', 350.00, 'Food', 'Food', 'Swiggy', 'UPI', TO_DATE('2026-10-06', 'YYYY-MM-DD'));

INSERT INTO EXPENSES (USER_ID, DESCRIPTION, AMOUNT, CATEGORY, PREDICTED_CATEGORY, MERCHANT, PAYMENT_METHOD, EXPENSE_DATE)
VALUES (1, 'Uber ride to college', 220.00, 'Transportation', 'Transportation', 'Uber', 'UPI', TO_DATE('2026-10-05', 'YYYY-MM-DD'));

INSERT INTO EXPENSES (USER_ID, DESCRIPTION, AMOUNT, CATEGORY, PREDICTED_CATEGORY, MERCHANT, PAYMENT_METHOD, EXPENSE_DATE)
VALUES (1, 'Amazon wireless headphones', 1500.00, 'Shopping', 'Shopping', 'Amazon', 'Credit Card', TO_DATE('2026-10-04', 'YYYY-MM-DD'));

INSERT INTO EXPENSES (USER_ID, DESCRIPTION, AMOUNT, CATEGORY, PREDICTED_CATEGORY, MERCHANT, PAYMENT_METHOD, EXPENSE_DATE)
VALUES (1, 'Bescom electricity monthly bill', 1850.00, 'Utilities', 'Utilities', 'Bescom', 'Net Banking', TO_DATE('2026-10-02', 'YYYY-MM-DD'));

INSERT INTO EXPENSES (USER_ID, DESCRIPTION, AMOUNT, CATEGORY, PREDICTED_CATEGORY, MERCHANT, PAYMENT_METHOD, EXPENSE_DATE)
VALUES (1, 'Netflix monthly subscription', 649.00, 'Entertainment', 'Entertainment', 'Netflix', 'Credit Card', TO_DATE('2026-10-01', 'YYYY-MM-DD'));

INSERT INTO EXPENSES (USER_ID, DESCRIPTION, AMOUNT, CATEGORY, PREDICTED_CATEGORY, MERCHANT, PAYMENT_METHOD, EXPENSE_DATE)
VALUES (1, 'Apollo Pharmacy medicines', 850.00, 'Healthcare', 'Healthcare', 'Apollo Pharmacy', 'UPI', TO_DATE('2026-09-28', 'YYYY-MM-DD'));

INSERT INTO EXPENSES (USER_ID, DESCRIPTION, AMOUNT, CATEGORY, PREDICTED_CATEGORY, MERCHANT, PAYMENT_METHOD, EXPENSE_DATE)
VALUES (1, 'Coursera ML Specialization installment', 3200.00, 'Education', 'Education', 'Coursera', 'Credit Card', TO_DATE('2026-09-25', 'YYYY-MM-DD'));

INSERT INTO EXPENSES (USER_ID, DESCRIPTION, AMOUNT, CATEGORY, PREDICTED_CATEGORY, MERCHANT, PAYMENT_METHOD, EXPENSE_DATE)
VALUES (1, 'Zomato lunch biryani with colleagues', 480.00, 'Food', 'Food', 'Zomato', 'UPI', TO_DATE('2026-09-24', 'YYYY-MM-DD'));

COMMIT;
