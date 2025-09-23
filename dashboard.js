/*
 * Simple dashboard logic for VRF cloud connectivity.
 * This script stores connection records in memory and updates the table accordingly.
 * It also supports importing data from an Excel file using the SheetJS library.
 */

// In-memory array to hold connection records
const connections = [];

// Handle tab switching
function initTabs() {
  const tabs = document.querySelectorAll('.tab');
  tabs.forEach((tab) => {
    tab.addEventListener('click', () => {
      tabs.forEach((t) => t.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach((c) => c.classList.remove('active'));
      tab.classList.add('active');
      const targetId = tab.getAttribute('data-target');
      document.getElementById(targetId).classList.add('active');
    });
  });
}

document.addEventListener('DOMContentLoaded', initTabs);

// Helper to add a connection and refresh table
function addConnection(provider, vrfId, connId, region, zone, vlan, primary, secondary) {
  connections.push({ provider, vrfId, connId, region, zone, vlan, primary, secondary });
  updateTable();
}

function updateTable() {
  const tbody = document.querySelector('#connectionsTable tbody');
  tbody.innerHTML = '';
  connections.forEach((rec) => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${rec.provider}</td>
      <td>${rec.vrfId}</td>
      <td>${rec.connId}</td>
      <td>${rec.region}</td>
      <td>${rec.zone}</td>
      <td>${rec.vlan}</td>
      <td>${rec.primary}</td>
      <td>${rec.secondary}</td>
    `;
    tbody.appendChild(tr);
  });
}

// Add AWS connection
function addAwsConnection() {
  const vrfId = document.getElementById('awsVrfId').value.trim();
  const connId = document.getElementById('awsConnId').value.trim();
  const vifType = document.getElementById('awsVifType').value;
  const vifId = document.getElementById('awsVifId').value.trim();
  const region = document.getElementById('awsRegion').value.trim();
  const zone = document.getElementById('awsAz').value.trim();
  const vlan = document.getElementById('awsVlan').value.trim();
  const localAsn = document.getElementById('awsLocalAsn').value.trim();
  const peerIp = document.getElementById('awsPeerIp').value.trim();
  const localIp = document.getElementById('awsLocalIp').value.trim();
  const primary = document.getElementById('awsPrimaryRouter').value.trim();
  const secondary = document.getElementById('awsSecondaryRouter').value.trim();

  if (!vrfId || !connId || !vifId) {
    alert('Please fill in required fields (VRF ID, Connection ID, VIF ID).');
    return;
  }
  const combinedId = `${connId}/${vifId}`;
  addConnection(`AWS (${vifType})`, vrfId, combinedId, region, zone, vlan, primary, secondary);
  document.querySelectorAll('#awsForm input').forEach((inp) => (inp.value = ''));
}

// Add Azure connection
function addAzureConnection() {
  const vrfId = document.getElementById('azVrfId').value.trim();
  const circuitId = document.getElementById('azCircuitId').value.trim();
  const peeringType = document.getElementById('azPeeringType').value;
  const region = document.getElementById('azRegion').value.trim();
  const zone = document.getElementById('azAz').value.trim();
  const vlan = document.getElementById('azVlan').value.trim();
  const primarySubnet = document.getElementById('azPrimarySubnet').value.trim();
  const secondarySubnet = document.getElementById('azSecondarySubnet').value.trim();
  const localAsn = document.getElementById('azLocalAsn').value.trim();
  const primary = document.getElementById('azPrimaryRouter').value.trim();
  const secondary = document.getElementById('azSecondaryRouter').value.trim();

  if (!vrfId || !circuitId) {
    alert('Please fill in required fields (VRF ID, Circuit ID).');
    return;
  }
  const combinedId = `${circuitId}/${peeringType}`;
  addConnection(`Azure (${peeringType})`, vrfId, combinedId, region, zone, vlan, primary, secondary);
  document.querySelectorAll('#azureForm input').forEach((inp) => (inp.value = ''));
}

// Add GCP connection
function addGcpConnection() {
  const vrfId = document.getElementById('gcpVrfId').value.trim();
  const interconnectId = document.getElementById('gcpInterconnectId').value.trim();
  const region = document.getElementById('gcpRegion').value.trim();
  const zone = document.getElementById('gcpZone').value.trim();
  const attachmentName = document.getElementById('gcpAttachmentName').value.trim();
  const vlan = document.getElementById('gcpVlan').value.trim();
  const vpc = document.getElementById('gcpVpc').value.trim();
  const localAsn = document.getElementById('gcpLocalAsn').value.trim();
  const peerIp = document.getElementById('gcpPeerIp').value.trim();
  const localIp = document.getElementById('gcpLocalIp').value.trim();
  const primary = document.getElementById('gcpPrimaryRouter').value.trim();
  const secondary = document.getElementById('gcpSecondaryRouter').value.trim();

  if (!vrfId || !interconnectId || !attachmentName) {
    alert('Please fill in required fields (VRF ID, Interconnect ID, Attachment Name).');
    return;
  }
  const combinedId = `${interconnectId}/${attachmentName}`;
  addConnection('GCP', vrfId, combinedId, region, zone, vlan, primary, secondary);
  document.querySelectorAll('#gcpForm input').forEach((inp) => (inp.value = ''));
}

// Import Excel file
function importExcel() {
  const fileInput = document.getElementById('excelFile');
  const file = fileInput.files[0];
  if (!file) {
    alert('Please select an Excel or CSV file.');
    return;
  }
  const reader = new FileReader();
  reader.onload = (e) => {
    const data = new Uint8Array(e.target.result);
    const workbook = XLSX.read(data, { type: 'array' });
    const sheetName = workbook.SheetNames[0];
    const sheet = workbook.Sheets[sheetName];
    const json = XLSX.utils.sheet_to_json(sheet, { header: 1 });
    const headers = json[0].map((h) => h.toString().trim().toLowerCase());
    for (let i = 1; i < json.length; i++) {
      const row = json[i];
      if (!row || row.length === 0) continue;
      const record = {};
      for (let j = 0; j < headers.length; j++) {
        record[headers[j]] = row[j];
      }
      const provider = record.provider || '';
      const vrfId = record['vrf id'] || record.vrf || '';
      const connId = record['connection id'] || record.connid || record['circuit id'] || '';
      const region = record.region || '';
      const zone = record['availability zone'] || record.zone || '';
      const vlan = record.vlan || record['vlan id'] || '';
      const primary = record['primary router'] || record.primary || '';
      const secondary = record['secondary router'] || record.secondary || '';
      if (provider && vrfId && connId) {
        addConnection(provider, vrfId, connId, region, zone, vlan, primary, secondary);
      }
    }
    alert('Import complete. Records added to the table.');
  };
  reader.readAsArrayBuffer(file);
}
