const soap_client = require("./soap_client");
const fs = require('fs');

const out_file = 'data/raw/stations.json';
 
soap_client.request("Postaje").then( r => {
    fs.writeFileSync(out_file, JSON.stringify(r.PostajeResponse.PostajeResult.postaje.postaja));
    console.log("Successfully fetched station data");
})
