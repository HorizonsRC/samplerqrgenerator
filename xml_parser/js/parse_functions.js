function extractSampleId(payload) {
  try {
    // Remove the "json:" prefix from the payload
    const jsonString = payload.replace(/^json:/, '');
    // Parse the JSON string into an object
    const data = JSON.parse(jsonString);
    // Return SampleId if it exists, otherwise return null
    return data.SampleID || null;
  } catch (error) {
    console.error('Error parsing JSON:', error);
    // Handle any parsing errors by returning null
    return null;
  }
}
  
function extractRunName(payload) {
  try {
    // Remove the "json:" prefix from the payload
    const jsonString = payload.replace(/^json:/, '');
    // Parse the JSON string into an object
    const data = JSON.parse(jsonString);
    // Return RunName if it exists, otherwise return null
    return data.RunName || null;
  } catch (error) {
    console.error('Error parsing JSON:', error);
    // Handle any parsing errors by returning null
    return null;
  }
}

function extractSiteName(payload) {
  try {
    // Remove the "json:" prefix from the payload
    const jsonString = payload.replace(/^json:/, '');
    // Parse the JSON string into an object
    const data = JSON.parse(jsonString);
    // Return SiteName if it exists, otherwise return null
    return data.SiteName || null;
  } catch (error) {
    console.error('Error parsing JSON:', error);
    // Handle any parsing errors by returning null
    return null;
  }
}

/**
 * This is used for testing, please ignore
 */
module.exports = {
  extractSampleId,
  extractRunName,
  extractSiteName,
}
