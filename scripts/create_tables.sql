SET CLIENT_ENCODING TO UTF8;
SET STANDARD_CONFORMING_STRINGS TO ON;
BEGIN;
CREATE TABLE "school_districts" (gid serial PRIMARY KEY,
    "statefp10" varchar(2),
    "unsdlea10" varchar(5),
    "geoid10" varchar(7),
    "name10" varchar(100),
    "lsad10" varchar(2),
    "lograde10" varchar(2),
    "higrade10" varchar(2),
    "mtfcc10" varchar(5),
    "sdtyp10" varchar(1),
    "funcstat10" varchar(1),
    "aland10" float8,
    "awater10" float8,
    "intptlat10" varchar(11),
    "intptlon10" varchar(12));
    SELECT AddGeometryColumn('','school_districts','the_geom','4269','MULTIPOLYGON',2);
CREATE INDEX "school_districts_the_geom_gist" ON "school_districts" using gist ("the_geom" gist_geometry_ops);
COMMIT;