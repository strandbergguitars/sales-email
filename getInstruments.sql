SELECT
    'Web EU orders' AS Category,
    COUNT(DISTINCT [SO Reference]) AS [Row Count]
FROM
    [sage].[PROD].[ZZDATASALESORDER_TABLE_V2]
WHERE
    [Sales type] = 'Sales instruments'
    AND [Sales site] = 101
    AND CAST([Original Sales order date] AS DATE) = CAST(DATEADD(day, -1, GETDATE()) AS DATE)

UNION ALL

SELECT
    'Web EU sold instruments' AS Category,
    COUNT(*) AS [Row Count]
FROM
    [sage].[PROD].[ZZDATASALESORDER_TABLE_V2]
WHERE
    [Sales type] = 'Sales instruments'
    AND [Sales site] = 101
    AND CAST([Original Sales order date] AS DATE) = CAST(DATEADD(day, -1, GETDATE()) AS DATE)

UNION ALL

SELECT
    'EU Reverb orders' AS Category,
    COUNT(DISTINCT [SO Reference]) AS [Row Count]
FROM
    [sage].[PROD].[ZZDATASALESORDER_TABLE_V2]
WHERE
    [Sales type] = 'Sales instruments'
    AND [Sales site] = 101
    AND LEFT([SO Reference], 2) = 'RV'
    AND CAST([Original Sales order date] AS DATE) = CAST(DATEADD(day, -1, GETDATE()) AS DATE)

UNION ALL

SELECT
    'EU Reverb sold instruments' AS Category,
    COUNT(*) AS [Row Count]
FROM
    [sage].[PROD].[ZZDATASALESORDER_TABLE_V2]
WHERE
    [Sales type] = 'Sales instruments'
    AND [Sales site] = 101
    AND LEFT([SO Reference], 2) = 'RV'
    AND CAST([Original Sales order date] AS DATE) = CAST(DATEADD(day, -1, GETDATE()) AS DATE)

UNION ALL

SELECT
    'Web US orders' AS Category,
    COUNT(DISTINCT [SO Reference]) AS [Row Count]
FROM
    [sage].[PROD].[ZZDATASALESORDER_TABLE_V2]
WHERE
    [Sales type] = 'Sales instruments'
    AND [Sales site] = 211
    AND LEFT([SO Reference], 2) <> 'RV'
    AND CAST([Original Sales order date] AS DATE) = CAST(DATEADD(day, -1, GETDATE()) AS DATE)

UNION ALL

SELECT
    'Web US sold instruments' AS Category,
    COUNT(*) AS [Row Count]
FROM
    [sage].[PROD].[ZZDATASALESORDER_TABLE_V2]
WHERE
    [Sales type] = 'Sales instruments'
    AND [Sales site] = 211
    AND LEFT([SO Reference], 2) <> 'RV'
    AND CAST([Original Sales order date] AS DATE) = CAST(DATEADD(day, -1, GETDATE()) AS DATE)

UNION ALL

SELECT
    'US Reverb orders' AS Category,
    COUNT(DISTINCT [SO Reference]) AS [Row Count]
FROM
    [sage].[PROD].[ZZDATASALESORDER_TABLE_V2]
WHERE
    [Sales type] = 'Sales instruments'
    AND [Sales site] = 211
    AND LEFT([SO Reference], 2) = 'RV'
    AND CAST([Original Sales order date] AS DATE) = CAST(DATEADD(day, -1, GETDATE()) AS DATE)

UNION ALL

SELECT
    'US Reverb sold instruments' AS Category,
    COUNT(*) AS [Row Count]
FROM
    [sage].[PROD].[ZZDATASALESORDER_TABLE_V2]
WHERE
    [Sales type] = 'Sales instruments'
    AND [Sales site] = 211
    AND LEFT([SO Reference], 2) = 'RV'
    AND CAST([Original Sales order date] AS DATE) = CAST(DATEADD(day, -1, GETDATE()) AS DATE)

UNION ALL

SELECT
    'US B2B orders' AS Category,
    COUNT(DISTINCT [SO Reference]) AS [Row Count]
FROM
    [sage].[PROD].[ZZDATASALESORDER_TABLE_V2]
WHERE
    [Sales type] = 'Sales instruments'
    AND [Sales site] IN (212, 213, 214)
    AND CAST([Original Sales order date] AS DATE) = CAST(DATEADD(day, -1, GETDATE()) AS DATE)

UNION ALL

SELECT
    'US B2B sold instruments' AS Category,
    COUNT(*) AS [Row Count]
FROM
    [sage].[PROD].[ZZDATASALESORDER_TABLE_V2]
WHERE
    [Sales type] = 'Sales instruments'
    AND [Sales site] IN (212, 213, 214)
    AND CAST([Original Sales order date] AS DATE) = CAST(DATEADD(day, -1, GETDATE()) AS DATE)

UNION ALL

SELECT
    'EU B2B orders' AS Category,
    COUNT(DISTINCT [SO Reference]) AS [Row Count]
FROM
    [sage].[PROD].[ZZDATASALESORDER_TABLE_V2]
WHERE
    [Sales type] = 'Sales instruments'
    AND [Sales site] IN (102, 103, 104)
    AND CAST([Original Sales order date] AS DATE) = CAST(DATEADD(day, -1, GETDATE()) AS DATE)

UNION ALL

SELECT
    'EU B2B sold instruments' AS Category,
    COUNT(*) AS [Row Count]
FROM
    [sage].[PROD].[ZZDATASALESORDER_TABLE_V2]
WHERE
    [Sales type] = 'Sales instruments'
    AND [Sales site] IN (102, 103, 104)
    AND CAST([Original Sales order date] AS DATE) = CAST(DATEADD(day, -1, GETDATE()) AS DATE);

