INSERT [dbo].[prd.spotifyStream]
SELECT [playedAt]
      ,[albumID]
      ,[trackID]
      ,[hashID]
FROM [dbo].[stg.spotifyStream]
WHERE hashID NOT IN (
		SELECT DISTINCT hashID
		FROM [dbo].[prd.spotifyStream]
		)