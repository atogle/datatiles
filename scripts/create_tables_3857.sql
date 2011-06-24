SET CLIENT_ENCODING TO UTF8;
SET STANDARD_CONFORMING_STRINGS TO ON;
BEGIN;
CREATE TABLE "states_3857" (gid serial PRIMARY KEY,
"region10" varchar(2),
"division10" varchar(2),
"statefp10" varchar(2),
"statens10" varchar(8),
"geoid10" varchar(2),
"stusps10" varchar(2),
"name10" varchar(100),
"lsad10" varchar(2),
"mtfcc10" varchar(5),
"funcstat10" varchar(1),
"aland10" float8,
"awater10" float8,
"intptlat10" varchar(11),
"intptlon10" varchar(12));
SELECT AddGeometryColumn('','states_3857','the_geom','3857','MULTIPOLYGON',2);
CREATE INDEX "states_3857_the_geom_gist" ON "states_3857" using gist ("the_geom" gist_geometry_ops);

CREATE TABLE "counties_3857" (gid serial PRIMARY KEY,
"statefp10" varchar(2),
"countyfp10" varchar(3),
"countyns10" varchar(8),
"geoid10" varchar(5),
"name10" varchar(100),
"namelsad10" varchar(100),
"lsad10" varchar(2),
"classfp10" varchar(2),
"mtfcc10" varchar(5),
"csafp10" varchar(3),
"cbsafp10" varchar(5),
"metdivfp10" varchar(5),
"funcstat10" varchar(1),
"aland10" float8,
"awater10" float8,
"intptlat10" varchar(11),
"intptlon10" varchar(12));
SELECT AddGeometryColumn('','counties_3857','the_geom','3857','MULTIPOLYGON',2);
CREATE INDEX "counties_3857_the_geom_gist" ON "counties_3857" using gist ("the_geom" gist_geometry_ops);

CREATE TABLE "school_districts_3857" (gid serial PRIMARY KEY,
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
SELECT AddGeometryColumn('','school_districts_3857','the_geom','3857','MULTIPOLYGON',2);
CREATE INDEX "school_districts_3857_the_geom_gist" ON "school_districts_3857" using gist ("the_geom" gist_geometry_ops);

COMMIT;