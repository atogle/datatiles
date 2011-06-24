SET CLIENT_ENCODING TO UTF8;
SET STANDARD_CONFORMING_STRINGS TO ON;
BEGIN;
INSERT INTO "states_3857" ("region10","division10","statefp10","statens10","geoid10","stusps10","name10","lsad10","mtfcc10","funcstat10","aland10","awater10","intptlat10","intptlon10","the_geom")
SELECT "region10","division10","statefp10","statens10","geoid10","stusps10","name10","lsad10","mtfcc10","funcstat10","aland10","awater10","intptlat10","intptlon10",ST_Transform("the_geom", 3857) FROM states;

INSERT INTO "counties_3857" ("statefp10","countyfp10","countyns10","geoid10","name10","namelsad10","lsad10","classfp10","mtfcc10","csafp10","cbsafp10","metdivfp10","funcstat10","aland10","awater10","intptlat10","intptlon10","the_geom")
SELECT "statefp10","countyfp10","countyns10","geoid10","name10","namelsad10","lsad10","classfp10","mtfcc10","csafp10","cbsafp10","metdivfp10","funcstat10","aland10","awater10","intptlat10","intptlon10",ST_Transform("the_geom", 3857) FROM counties;

INSERT INTO "school_districts_3857" ("statefp10","unsdlea10","geoid10","name10","lsad10","lograde10","higrade10","mtfcc10","sdtyp10","funcstat10","aland10","awater10","intptlat10","intptlon10","the_geom")
SELECT "statefp10","unsdlea10","geoid10","name10","lsad10","lograde10","higrade10","mtfcc10","sdtyp10","funcstat10","aland10","awater10","intptlat10","intptlon10",ST_Transform("the_geom", 3857) FROM school_districts;

COMMIT;