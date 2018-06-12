DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_addCollection`(
    IN p_name VARCHAR(45),
    IN p_arn VARCHAR(70)
)
BEGIN
    if ( select exists (select 1 from collections where CollectionName = p_name) ) THEN
     
        select 'Collection Already Exists !!';
     
    ELSE
     
        insert into collections
        (
            CollectionName,
            CollectionARN
        )
        values
        (
            p_name,
            p_arn
        );
     
    END IF;
END$$
DELIMITER ;
