/*Here we have cards, with that are missing an image.*/
SELECT *
FROM 'MTG-Cards'
WHERE small_img IS NULL;