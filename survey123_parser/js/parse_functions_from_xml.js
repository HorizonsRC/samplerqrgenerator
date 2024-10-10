/**
 * Survey123 script for XML parsing from QR code.
 * 
 * Description: Extracts information from xml qr code created by sampler_qr_creator 
 * Author: Nic Mostert, Horizons Regional Council
 * Created: August 15, 2023
 */

/**
 * Extracts the "Sample ID" from an XML string.
 *
 * @param {string} xmlString - The XML string to extract from.
 * @returns {string|"ERROR:NOT FOUND"} The extracted Sample ID or "ERROR:NOT FOUND" if not found.
 */
function extractSampleId(xmlString) {
  const sampleIdRegex = /<Sample\s+ID="([^"]+)">/;
  const sampleIdMatch = xmlString.match(sampleIdRegex);
  const sampleId = sampleIdMatch ? sampleIdMatch[1] : "ERROR:NOT FOUND";
  return sampleId;
}

/**
 * Extracts the "SiteName" from an XML string.
 *
 * @param {string} xmlString - The XML string to extract from.
 * @returns {string|"ERROR:NOT FOUND"} The extracted SiteName or "ERROR:NOT FOUND" if not found.
 */
function extractSiteName(xmlString) {
  const siteNameRegex = /<SiteName>(.*?)<\/SiteName>/;
  const siteNameMatch = xmlString.match(siteNameRegex);
  const siteName = siteNameMatch ? siteNameMatch[1] : "ERROR:NOT FOUND";
  return siteName;
}

/**
 * Extracts the "RunName" from an XML string.
 *
 * @param {string} xmlString - The XML string to extract from.
 * @returns {string|"ERROR:NOT FOUND"} The extracted RunName or "ERROR:NOT FOUND" if not found.
 */
function extractRunName(xmlString) {
  const runNameRegex = /<RunName>(.*?)<\/RunName>/;
  const runNameMatch = xmlString.match(runNameRegex);
  const runName = runNameMatch ? runNameMatch[1] : "NOT FOUND";
  return runName;
}

/**
 * Extracts the Field Technician name from an XML string.
 *
 * @param {string} xmlString - The XML string to extract from.
 * @returns {string|"ERROR:NOT FOUND"} The extracted Field Technician name or "ERROR:NOT FOUND" if not found.
 */
function extractFieldTech(xmlString) {
  const fieldTechRegex = /<FieldTech>(.*?)<\/FieldTech>/;
  const fieldTechMatch = xmlString.match(fieldTechRegex);
  const fieldTech = fieldTechMatch ? fieldTechMatch[1] : "ERROR:NOT FOUND";
  return fieldTech;
}

/**
 * Extracts the Cost Code name from an XML string.
 *
 * @param {string} xmlString - The XML string to extract from.
 * @returns {string|"ERROR:NOT FOUND"} The extracted Cost Code name or "ERROR:NOT FOUND" if not found.
 */
function extractCostCode(xmlString) {
  const costCodeRegex = /<CostCode>(.*?)<\/CostCode>/;
  const costCodeMatch = xmlString.match(costCodeRegex);
  const costCode = costCodeMatch ? costCodeMatch[1] : "ERROR:NOT FOUND";
  return costCode;
}

/**
 * Extracts the Project name from an XML string.
 *
 * @param {string} xmlString - The XML string to extract from.
 * @returns {string|"ERROR:NOT FOUND"} The extracted Project name or "ERROR:NOT FOUND" if not found.
 */
function extractProject(xmlString) {
  const projectRegex = /<Project>(.*?)<\/Project>/;
  const projectMatch = xmlString.match(projectRegex);
  const project = projectMatch ? projectMatch[1] : "ERROR:NOT FOUND";
  return project;
}

/**
 * This is used for testing, please ignore
 */
module.exports = {
  extractSampleId,
  extractRunName,
  extractSiteName,
  extractFieldTech,
  extractCostCode,
  extractProject
}
