-- Skapa en variabel för dynamisk SQL
DECLARE @cols AS NVARCHAR(MAX),
        @query AS NVARCHAR(MAX);

-- Hämta och sortera unika datum från temporär tabell och skapa kolumnlista
SET @cols = STUFF((
    SELECT ',' + QUOTENAME(CONVERT(VARCHAR, OrderDate, 23))
    FROM (
        SELECT DISTINCT OrderDate
        FROM #ZZTempSalesData
        WHERE OrderDate IS NOT NULL
    ) AS DistinctDates
    ORDER BY OrderDate DESC
    FOR XML PATH(''), TYPE
).value('.', 'NVARCHAR(MAX)'), 1, 1, '');

-- Skapa dynamisk SQL för att bygga pivottabellen
SET @query = N'
    SELECT Category, ' + @cols + '
    FROM (
        SELECT Category, 
               CONVERT(VARCHAR, OrderDate, 23) AS OrderDate, 
               ISNULL([Row Count], 0) AS [Row Count]
        FROM #ZZTempSalesData
    ) AS SourceTable
    PIVOT (
        SUM([Row Count])
        FOR OrderDate IN (' + @cols + ')
    ) AS PivotTable
    ORDER BY Category;';

-- Kör den dynamiska SQL
EXEC sp_executesql @query;
