CREATE TABLE #ZZTempSalesData (
    Category NVARCHAR(255),
    OrderDate DATE,
    [Row Count] INT
);


-- Fyll temporär tabell med data för de senaste 30 dagarna
INSERT INTO #ZZTempSalesData (Category, OrderDate, [Row Count])
SELECT
    'Web EU orders, RV excluded.' AS Category,
    CAST([Original Sales order date] AS DATE) AS OrderDate,
    COUNT(DISTINCT [SO Reference]) AS [Row Count]
FROM
    [sage].[PROD].[ZZDATASALESORDER_TABLE_V2]
WHERE
    [Sales type] = 'Sales instruments'
    AND [Sales site] = 101
    AND LEFT([SO Reference], 2) <> 'RV'
    AND [Original Sales order date] >= DATEADD(DAY, -30, CAST(GETDATE() AS DATE))
    AND [Original Sales order date] < CAST(GETDATE() AS DATE)
GROUP BY CAST([Original Sales order date] AS DATE)

UNION ALL

SELECT
    'Web EU sold instruments, RV excluded.' AS Category,
    CAST([Original Sales order date] AS DATE) AS OrderDate,
    COUNT(*) AS [Row Count]
FROM
    [sage].[PROD].[ZZDATASALESORDER_TABLE_V2]
WHERE
    [Sales type] = 'Sales instruments'
    AND [Sales site] = 101
    AND LEFT([SO Reference], 2) <> 'RV'
    AND [Original Sales order date] >= DATEADD(DAY, -30, CAST(GETDATE() AS DATE))
    AND [Original Sales order date] < CAST(GETDATE() AS DATE)
GROUP BY CAST([Original Sales order date] AS DATE)

UNION ALL

SELECT
    'EU Reverb orders' AS Category,
    CAST([Original Sales order date] AS DATE) AS OrderDate,
    COUNT(DISTINCT [SO Reference]) AS [Row Count]
FROM
    [sage].[PROD].[ZZDATASALESORDER_TABLE_V2]
WHERE
    [Sales type] = 'Sales instruments'
    AND [Sales site] = 101
    AND LEFT([SO Reference], 2) = 'RV'
    AND [Original Sales order date] >= DATEADD(DAY, -30, CAST(GETDATE() AS DATE))
    AND [Original Sales order date] < CAST(GETDATE() AS DATE)
GROUP BY CAST([Original Sales order date] AS DATE)

UNION ALL

SELECT
    'EU Reverb sold instruments' AS Category,
    CAST([Original Sales order date] AS DATE) AS OrderDate,
    COUNT(*) AS [Row Count]
FROM
    [sage].[PROD].[ZZDATASALESORDER_TABLE_V2]
WHERE
    [Sales type] = 'Sales instruments'
    AND [Sales site] = 101
    AND LEFT([SO Reference], 2) = 'RV'
    AND [Original Sales order date] >= DATEADD(DAY, -30, CAST(GETDATE() AS DATE))
    AND [Original Sales order date] < CAST(GETDATE() AS DATE)
GROUP BY CAST([Original Sales order date] AS DATE)

UNION ALL

SELECT
    'Web US orders, RV excluded.' AS Category,
    CAST([Original Sales order date] AS DATE) AS OrderDate,
    COUNT(DISTINCT [SO Reference]) AS [Row Count]
FROM
    [sage].[PROD].[ZZDATASALESORDER_TABLE_V2]
WHERE
    [Sales type] = 'Sales instruments'
    AND [Sales site] = 211
    AND LEFT([SO Reference], 2) <> 'RV'
    AND [Original Sales order date] >= DATEADD(DAY, -30, CAST(GETDATE() AS DATE))
    AND [Original Sales order date] < CAST(GETDATE() AS DATE)
GROUP BY CAST([Original Sales order date] AS DATE)

UNION ALL

SELECT
    'Web US sold instruments, RV excluded.' AS Category,
    CAST([Original Sales order date] AS DATE) AS OrderDate,
    COUNT(*) AS [Row Count]
FROM
    [sage].[PROD].[ZZDATASALESORDER_TABLE_V2]
WHERE
    [Sales type] = 'Sales instruments'
    AND [Sales site] = 211
    AND LEFT([SO Reference], 2) <> 'RV'
    AND [Original Sales order date] >= DATEADD(DAY, -30, CAST(GETDATE() AS DATE))
    AND [Original Sales order date] < CAST(GETDATE() AS DATE)
GROUP BY CAST([Original Sales order date] AS DATE)

UNION ALL

SELECT
    'US Reverb orders' AS Category,
    CAST([Original Sales order date] AS DATE) AS OrderDate,
    COUNT(DISTINCT [SO Reference]) AS [Row Count]
FROM
    [sage].[PROD].[ZZDATASALESORDER_TABLE_V2]
WHERE
    [Sales type] = 'Sales instruments'
    AND [Sales site] = 211
    AND LEFT([SO Reference], 2) = 'RV'
    AND [Original Sales order date] >= DATEADD(DAY, -30, CAST(GETDATE() AS DATE))
    AND [Original Sales order date] < CAST(GETDATE() AS DATE)
GROUP BY CAST([Original Sales order date] AS DATE)

UNION ALL

SELECT
    'US Reverb sold instruments' AS Category,
    CAST([Original Sales order date] AS DATE) AS OrderDate,
    COUNT(*) AS [Row Count]
FROM
    [sage].[PROD].[ZZDATASALESORDER_TABLE_V2]
WHERE
    [Sales type] = 'Sales instruments'
    AND [Sales site] = 211
    AND LEFT([SO Reference], 2) = 'RV'
    AND [Original Sales order date] >= DATEADD(DAY, -30, CAST(GETDATE() AS DATE))
    AND [Original Sales order date] < CAST(GETDATE() AS DATE)
GROUP BY CAST([Original Sales order date] AS DATE)

UNION ALL

SELECT
    'US B2B orders' AS Category,
    CAST([Original Sales order date] AS DATE) AS OrderDate,
    COUNT(DISTINCT [SO Reference]) AS [Row Count]
FROM
    [sage].[PROD].[ZZDATASALESORDER_TABLE_V2]
WHERE
    [Sales type] = 'Sales instruments'
    AND [Sales site] IN (212, 213, 214)
    AND [Original Sales order date] >= DATEADD(DAY, -30, CAST(GETDATE() AS DATE))
    AND [Original Sales order date] < CAST(GETDATE() AS DATE)
GROUP BY CAST([Original Sales order date] AS DATE)

UNION ALL

SELECT
    'US B2B sold instruments' AS Category,
    CAST([Original Sales order date] AS DATE) AS OrderDate,
    COUNT(*) AS [Row Count]
FROM
    [sage].[PROD].[ZZDATASALESORDER_TABLE_V2]
WHERE
    [Sales type] = 'Sales instruments'
    AND [Sales site] IN (212, 213, 214)
    AND [Original Sales order date] >= DATEADD(DAY, -30, CAST(GETDATE() AS DATE))
    AND [Original Sales order date] < CAST(GETDATE() AS DATE)
GROUP BY CAST([Original Sales order date] AS DATE)

UNION ALL

SELECT
    'EU B2B orders' AS Category,
    CAST([Original Sales order date] AS DATE) AS OrderDate,
    COUNT(DISTINCT [SO Reference]) AS [Row Count]
FROM
    [sage].[PROD].[ZZDATASALESORDER_TABLE_V2]
WHERE
    [Sales type] = 'Sales instruments'
    AND [Sales site] IN (102, 103, 104)
    AND [Original Sales order date] >= DATEADD(DAY, -30, CAST(GETDATE() AS DATE))
    AND [Original Sales order date] < CAST(GETDATE() AS DATE)
GROUP BY CAST([Original Sales order date] AS DATE)

UNION ALL

SELECT
    'EU B2B sold instruments' AS Category,
    CAST([Original Sales order date] AS DATE) AS OrderDate,
    COUNT(*) AS [Row Count]
FROM
    [sage].[PROD].[ZZDATASALESORDER_TABLE_V2]
WHERE
    [Sales type] = 'Sales instruments'
    AND [Sales site] IN (102, 103, 104)
    AND [Original Sales order date] >= DATEADD(DAY, -30, CAST(GETDATE() AS DATE))
    AND [Original Sales order date] < CAST(GETDATE() AS DATE)
GROUP BY CAST([Original Sales order date] AS DATE);