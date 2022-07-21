INSERT [dbo].[prd.spotifyArtist]
SELECT [artistID]
      ,[artistName]
      ,[trackID]
      ,[artistPopularity]
      ,[followers]
      ,[genre0]
      ,[genre1]
      ,[genre2]
      ,[genre3]
      ,[genre4]
      ,[uniqArtID]
FROM [dbo].[stg.spotifyArtist]
WHERE uniqArtID NOT IN (
		SELECT DISTINCT uniqArtID
		FROM [dbo].[prd.spotifyArtist]
		)