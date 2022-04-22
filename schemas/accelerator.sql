-- This schema adds the tables necessary for Accelerator accounting as a
-- separate record as part of the wider Cloud Accounting system.

DROP TABLE IF EXISTS AcceleratorRecords;
CREATE TABLE AcceleratorRecords (
  UpdateTime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  MeasurementMonth INT NOT NULL,
  MeasurementYear INT NOT NULL,

  AssociatedRecordType VARCHAR(255) NOT NULL,
  AssociatedRecord VARCHAR(255) NOT NULL,

  GlobalUserName VARCHAR(255),      
  FQAN VARCHAR(255) NOT NULL,       
  SiteName VARCHAR(255) NOT NULL,   
  Count DECIMAL(10,3) NOT NULL,
  Cores INT,
  ActiveDuration INT,
  AvailableDuration INT,
  BenchmarkType VARCHAR(255),       
  Benchmark DECIMAL(10,3),                
  Type VARCHAR(255) NOT NULL,       
  Model VARCHAR(255),               
  PublisherDNID INT NOT NULL,

  PRIMARY KEY (MeasurementMonth, MeasurementYear, 
               AssociatedRecordType, AssociatedRecord, 
               SiteName)

  -- [?] INDEX

);

DROP PROCEDURE IF EXISTS ReplaceAcceleratorRecord;
DELIMITER //
CREATE PROCEDURE ReplaceAcceleratorRecord(
  measurementMonth INT,
  measurementYear INT,
  associatedRecordType VARCHAR(255),
  associatedRecord VARCHAR(255),
  globalUserName VARCHAR(255),
  fqan VARCHAR(255),
  siteName VARCHAR(255),
  count DECIMAL(10,3),
  cores INT,
  activeDuration INT,
  availableDuration INT,
  benchmarkType VARCHAR(255),
  benchmark DECIMAL,
  type VARCHAR(255),
  model VARCHAR(255),
  publisherDN VARCHAR(255)
)
BEGIN
REPLACE INTO AcceleratorRecords(
  MeasurementMonth,
  MeasurementYear,
  AssociatedRecordType,
  AssociatedRecord,
  GlobalUserName,
  FQAN,
  SiteName,
  Count,
  Cores,
  ActiveDuration,
  AvailableDuration,
  BenchmarkType,
  Benchmark,
  Type,
  Model,
  PublisherDNID
)
VALUES(
  measurementMonth,
  measurementYear,
  associatedRecordType,
  associatedRecord,
  globalUserName,
  fqan,
  siteName,
  count,
  cores,
  activeDuration,
  availableDuration,
  benchmarkType,
  benchmark,
  type,
  model,
  DNLookup(publisherDN)
);
END //
DELIMITER ;

