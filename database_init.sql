-- データベースの選択
USE pos_db;

-- 商品テーブル
CREATE TABLE IF NOT EXISTS product (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    barcode VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 取引テーブル
CREATE TABLE IF NOT EXISTS transaction (
    TRD_ID INT AUTO_INCREMENT PRIMARY KEY,
    DATETIME TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    EMP_CD CHAR(10) DEFAULT '9999999999' NOT NULL,
    STORE_CD CHAR(5) DEFAULT '30' NOT NULL,
    POS_NO CHAR(3) DEFAULT '90' NOT NULL,
    TOTAL_AMT INT NOT NULL,
    TTL_AMT_EX_TAX INT NOT NULL,
    payment_method VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 取引詳細テーブル
CREATE TABLE IF NOT EXISTS transaction_detail (
    TRD_ID INT NOT NULL,
    DTL_ID INT AUTO_INCREMENT PRIMARY KEY,
    PRD_ID INT NOT NULL,
    PRD_CODE CHAR(13) NOT NULL,
    PRD_NAME VARCHAR(50) NOT NULL,
    PRD_PRICE INT NOT NULL,
    TAX_CD CHAR(2) DEFAULT '10' NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (TRD_ID) REFERENCES transaction(TRD_ID),
    FOREIGN KEY (PRD_ID) REFERENCES product(id)
);

-- 商品データの挿入（単品）
INSERT INTO product (name, price, barcode) VALUES 
('ハイマッキー（黒）', 150.00, '4901681502516'),
('ハイマッキー（青）', 150.00, '4901681502523'),
('ハイマッキー（ライトブルー）', 150.00, '4901681502530'),
('ハイマッキー（緑）', 150.00, '4901681502547'),
('ハイマッキー（ライトグリーン）', 150.00, '4901681502554'),
('ハイマッキー（黄）', 150.00, '4901681502561'),
('ハイマッキー（ピンク）', 150.00, '4901681502578'),
('ハイマッキー（紫）', 150.00, '4901681502585'),
('ハイマッキー（赤）', 150.00, '4901681502592'),
('ハイマッキー（オレンジ）', 150.00, '4901681502608'),
('ハイマッキー（ライトブラウン）', 150.00, '4901681502615'),
('ハイマッキー（茶）', 150.00, '4901681502622');

-- 商品データの挿入（セット商品）
INSERT INTO product (name, price, barcode) VALUES 
('ハイマッキー 8色セット', 1200.00, '4901681502639'),
('ハイマッキー 12色セット', 1800.00, '4901681502646');

-- トランザクションのテストデータ
-- 1. 単品購入（ハイマッキー黒1本）
INSERT INTO transaction (TOTAL_AMT, TTL_AMT_EX_TAX, payment_method) VALUES 
(165, 150, 'CASH');

-- 2. 複数商品購入（ハイマッキー黒、青、赤の3本）
INSERT INTO transaction (TOTAL_AMT, TTL_AMT_EX_TAX, payment_method) VALUES 
(495, 450, 'CREDIT');

-- 3. セット商品購入（12色セット1つと単品2本）
INSERT INTO transaction (TOTAL_AMT, TTL_AMT_EX_TAX, payment_method) VALUES 
(2310, 2100, 'CASH');

-- トランザクション詳細のテストデータ
-- 1. 単品購入の詳細
INSERT INTO transaction_detail (TRD_ID, PRD_ID, PRD_CODE, PRD_NAME, PRD_PRICE) VALUES 
(1, 1, '4901681502516', 'ハイマッキー（黒）', 150);

-- 2. 複数商品購入の詳細
INSERT INTO transaction_detail (TRD_ID, PRD_ID, PRD_CODE, PRD_NAME, PRD_PRICE) VALUES 
(2, 1, '4901681502516', 'ハイマッキー（黒）', 150),
(2, 2, '4901681502523', 'ハイマッキー（青）', 150),
(2, 9, '4901681502592', 'ハイマッキー（赤）', 150);

-- 3. セット商品購入の詳細
INSERT INTO transaction_detail (TRD_ID, PRD_ID, PRD_CODE, PRD_NAME, PRD_PRICE) VALUES 
(3, 14, '4901681502646', 'ハイマッキー 12色セット', 1800),
(3, 1, '4901681502516', 'ハイマッキー（黒）', 150),
(3, 2, '4901681502523', 'ハイマッキー（青）', 150); 