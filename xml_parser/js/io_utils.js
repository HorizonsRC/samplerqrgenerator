function testParserFunctions(xmlString) {
 
  getXmlDoc(xmlString)
    .then(domObj => {
      console.log('DOM Object:', domObj)
    })
    .catch(error => {
      console.error("Error:", error)
    });
  
	extractSampleId(xmlString) 
		.then(sampleId => {
  		console.log('SampleId:', sampleId)
		})
		.catch(error => {
			console.error("Error:", error)
		});

  
	extractRunName(xmlString)
		.then(runName => {
  		console.log('RunName:', runName)
		})
		.catch(error => {
			console.error("Error:", error)
		});
  
	extractFieldTech(xmlString)
		.then(fieldTech => {
  		console.log('FieldTech:', fieldTech)
		})
		.catch(error => {
			console.error("Error:", error)
		});
  
	extractProject(xmlString)
		.then(project => {
  		console.log('Project:', project)
		})
		.catch(error => {
			console.error("Error:", error)
		});

	extractCostCode(xmlString)
		.then(costCode => {
  		console.log('CostCode:', costCode)
		})
		.catch(error => {
			console.error("Error:", error)
		});

	extractSiteName(xmlString)
		.then(siteName => {
  		console.log('SiteName:', siteName)
		})
		.catch(error => {
			console.error("Error:", error)
		});
  
}
