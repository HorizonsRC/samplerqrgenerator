function testParserFunctions(filename) {
  const fs = require('fs');
  fs.readFile(filename, 'utf8', (err, data) => {
    if (err) {
      console.error('Error reading CSV file:', err);
      return;
    }
    runName = extractFunctions.extractRunName(data)
    console.log('RunName:', runName)

    sampleId = extractFunctions.extractSampleId(data) 
    console.log('SampleID:', sampleId)
    
    siteName = extractFunctions.extractSiteName(data)
    console.log('SiteName:', siteName)
  });
  
}

const extractFunctions = require('./parse_functions')
console.log(extractFunctions)
testParserFunctions('../test_payload.txt') 
