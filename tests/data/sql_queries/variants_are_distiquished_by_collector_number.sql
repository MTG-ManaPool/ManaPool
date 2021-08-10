/* This test show cases that each card is distinguished by it's collection number and set. */
SELECT multiverse_ids, name, `set`, collector_number, foil, nonfoil
FROM 'MTG-Cards'
WHERE `set`="afr"  AND (collector_number=200 OR collector_number=402)
ORDER BY "collector_number"
/*
Here we have two cards, with the same name, in the same set.
Our inventory tracks two different entries for these, as each of them have a unique artwork.
Additionally, our inventory tracks stock counts for both foil, and nonfoil for each artwork, 
as we could possibly own either of those variants for either artwork version of the card.
*/