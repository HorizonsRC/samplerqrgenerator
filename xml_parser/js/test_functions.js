function testParserFunctions(filename) {
  const fs = require('fs');
  fs.readFile(filename, 'utf8', (err, data) => {
    if (err) {
      console.error('Error reading CSV file:', err);
      return;
    }

    sampleId = extractFunctions.extractSampleId(data) 
    console.log('SampleId:', sampleId)
    
    runName = extractFunctions.extractRunName(data)
    console.log('RunName:', runName)
    
    fieldTech = extractFunctions.extractFieldTech(data)
    console.log('FieldTech:', fieldTech)
    
    project = extractFunctions.extractProject(data)
    console.log('Project:', project)

    costCode = extractFunctions.extractCostCode(data)
    console.log('CostCode:', costCode)

    siteName = extractFunctions.extractSiteName(data)
    console.log('SiteName:', siteName)
  });
  
}

const extractFunctions = require('./parse_functions')
console.log(extractFunctions)
testParserFunctions('../xml/20233622.xml') 
