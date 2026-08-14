MATCH path =
(s:Supplier)-[:SUPPLIES]->
(m:Manufacturer)-[:PRODUCES]->
(p:Product)-[:BELONGS_TO]->
(i:Industry)
RETURN path;