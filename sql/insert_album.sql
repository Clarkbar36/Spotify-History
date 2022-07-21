INSERT [dbo].[prd.spotifyAlbums]
SELECT [albumID]
      ,[albumName]
      ,[albumReleaseDate]
FROM [dbo].[stg.spotifyAlbums]
WHERE albumID NOT IN (
		SELECT DISTINCT albumID
		FROM [dbo].[prd.spotifyAlbums]
		)
