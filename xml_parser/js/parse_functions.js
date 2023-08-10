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
 * @returns {string|null} The extracted Sample ID or null if not found.
 */
function extractSampleId(xmlString) {
  const sampleIdRegex = /<Sample\s+ID="([^"]+)">/;
  const sampleIdMatch = xmlString.match(sampleIdRegex);
  const sampleId = sampleIdMatch ? sampleIdMatch[1] : null;
  return sampleId;
}

/**
 * Extracts the "SiteName" from an XML string.
 *
 * @param {string} xmlString - The XML string to extract from.
 * @returns {string|null} The extracted SiteName or null if not found.
 */
function extractSiteName(xmlString) {
  const siteNameRegex = /<SiteName>(.*?)<\/SiteName>/;
  const siteNameMatch = xmlString.match(siteNameRegex);
  const siteName = siteNameMatch ? siteNameMatch[1] : null;
  return siteName;
}

/**
 * Extracts the "RunName" from an XML string.
 *
 * @param {string} xmlString - The XML string to extract from.
 * @returns {string|null} The extracted RunName or null if not found.
 */
function extractRunName(xmlString) {
  const runNameRegex = /<RunName>(.*?)<\/RunName>/;
  const runNameMatch = xmlString.match(runNameRegex);
  const runName = runNameMatch ? runNameMatch[1] : null;
  return runName;
}

/**
 * Extracts the Field Technician name from an XML string.
 *
 * @param {string} xmlString - The XML string to extract from.
 * @returns {string|null} The extracted Field Technician name or null if not found.
 */
function extractFieldTech(xmlString) {
  const fieldTechRegex = /<FieldTech>(.*?)<\/FieldTech>/;
  const fieldTechMatch = xmlString.match(fieldTechRegex);
  const fieldTech = fieldTechMatch ? fieldTechMatch[1] : null;
  return fieldTech;
}

/**
 * Extracts the Cost Code name from an XML string.
 *
 * @param {string} xmlString - The XML string to extract from.
 * @returns {string|null} The extracted Cost Code name or null if not found.
 */
function extractCostCode(xmlString) {
  const costCodeRegex = /<CostCode>(.*?)<\/CostCode>/;
  const costCodeMatch = xmlString.match(costCodeRegex);
  const costCode = costCodeMatch ? costCodeMatch[1] : null;
  return costCode;
}

/**
 * Extracts the Project name from an XML string.
 *
 * @param {string} xmlString - The XML string to extract from.
 * @returns {string|null} The extracted Project name or null if not found.
 */
function extractProject(xmlString) {
  const projectRegex = /<Project>(.*?)<\/Project>/;
  const projectMatch = xmlString.match(projectRegex);
  const project = projectMatch ? projectMatch[1] : null;
  return project;
}
