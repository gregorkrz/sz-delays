const soap_client = require("./soap_client");
const fs = require('fs');

const train_number = process.argv.slice(2)[0];
const out_file = 'data/raw/trains/' + train_number + '.json';

soap_client.request("Postaje_vlaka_vse", {"vl": train_number, "da": "2021-01-01"}).then( r => {
    fs.writeFileSync(out_file, JSON.stringify(r.Postaje_vlaka_vseResponse.Postaje_vlaka_vseResult.postaje_vlaka.Vlak));
    console.log("Successfully fetched data for train", train_number);
})
