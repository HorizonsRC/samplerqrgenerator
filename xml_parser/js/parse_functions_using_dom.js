function extractSampleId(xmlString) {
  return getXmlDoc(xmlString)
    .then(xmlDoc => {
      const sampleId = xmlDoc.documentElement.getAttribute('ID');
      return sampleId; 
    });
}
  
function extractRunName(xmlString) {
	return getXmlDoc(xmlString)
		.then(xmlDoc => {
      const runName = xmlDoc.querySelector('RunName').textContent;
      return runName; 
    });
}

function extractFieldTech(xmlString) {
	return getXmlDoc(xmlString)
		.then(xmlDoc => {
      const fieldTech = xmlDoc.querySelector('FieldTech').textContent;
      return fieldTech; 
    });
}

function extractProject(xmlString) {
	return getXmlDoc(xmlString)
		.then(xmlDoc => {
      const project = xmlDoc.querySelector('Project').textContent;
      return project; 
    });
}

function extractCostCode(xmlString) {
	return getXmlDoc(xmlString)
		.then(xmlDoc => {
      const costCode = xmlDoc.querySelector('CostCode').textContent;
      return costCode; 
    });
}

function extractSiteName(xmlString) {
	return getXmlDoc(xmlString)
		.then(xmlDoc => {
      const siteName = xmlDoc.querySelector('SiteName').textContent;
      return siteName; 
    });
}

// helper function, DO NOT USE
function getXmlDoc(filename) {
  return new Promise((resolve, reject) => {
    fetch(filename)    
      .then(response => response.text())
      .then(xmlText => {
        // Parse the XML text using DOMParser
        const parser = new DOMParser();
        const xmlDoc = parser.parseFromString(xmlText, 'text/xml');
        resolve(xmlDoc);
      })
      .catch(error => {
        console.error('Error reading XML:', error);
        reject(error);
      });
  });
}
